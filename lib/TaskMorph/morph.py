import undetected_chromedriver as uc
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import pyautogui

from time import sleep

from PIL import Image
import io

import os
import json

from typing import Union, Literal, List, Optional, Tuple, Any
from pathlib import Path

class TaskMorph:
    
    by_mapping = {
        "id" : By.ID,
        "name" : By.NAME,
        "xpath" : By.XPATH,
        "tag_name" : By.TAG_NAME,
        "link_text" : By.LINK_TEXT,
        "class_name" : By.CLASS_NAME,
        "css_selector" : By.CSS_SELECTOR,
        "partial_link_text" : By.PARTIAL_LINK_TEXT,
    }
    
    def get_options(self) -> uc.ChromeOptions:
        return uc.ChromeOptions()
    
    def initialize_driver(self, driverexe_path: Union[Path, str], options: uc.ChromeOptions, browser_logs: bool = False, performance_logs: bool = False) -> WebDriver:
        driverexe_path = str(driverexe_path)
        
        if os.path.isfile(driverexe_path):
            
            if performance_logs is True:
                options.set_capability(
                    "goog:loggingPrefs", {"performance": "ALL"}
                )
            
            if browser_logs is True:
                options.set_capability(
                    "goog:loggingPrefs", {"browser": "ALL"}
                )

            return uc.Chrome(options, driver_executable_path = driverexe_path)

        raise FileNotFoundError(f'File not found in: {driverexe_path}')
    
    def find_element(self, driver: WebDriver, by: Literal['id', 'name', 'xpath', 'link_text', 'partial_link_text', 'tag_name', 'class_name', 'css_selector'], param: str, timeout: int = 10) -> WebElement:
        if by not in self.by_mapping:
            raise ValueError(f"Invalid locator type: {by}")
        
        by_type = self.by_mapping[by]
        
        element = WebDriverWait(driver, timeout).until(
            expected_conditions.presence_of_element_located(
                (by_type, param)
            )
        )
        
        return element
    
    def find_elements(self, driver: WebDriver, by: Literal['id', 'name', 'xpath', 'link_text', 'partial_link_text', 'tag_name', 'class_name', 'css_selector'], param: str, timeout: int = 10) -> List[WebElement]:
        if by not in self.by_mapping:
            raise ValueError(f"Invalid locator type: {by}")
        
        by_type = self.by_mapping[by]
        
        element = WebDriverWait(driver, timeout).until(
            expected_conditions.presence_of_all_elements_located(
                (by_type, param)
            )
        )
        
        return element
    
    def find_element_or_none(self, driver: WebDriver, by: Literal['id', 'name', 'xpath', 'link_text', 'partial_link_text', 'tag_name', 'class_name', 'css_selector'], param: str, timeout: int = 10) -> Optional[WebElement]:
        try:
            element = self.find_element(driver, by, param, timeout)
            return element
            
        except(TimeoutException, NoSuchElementException):
            return None
        
    def change_iframe(self, driver: WebDriver, by: Optional[Literal['id', 'name', 'xpath', 'link_text', 'partial_link_text', 'tag_name', 'class_name', 'css_selector']] = None, param: Optional[str] = None) -> None:
        if by is None or param is None:
            driver.switch_to.default_content()
            return
        
        frame_element: WebElement = self.search_by_element_or_null(driver, by, param) # type: ignore
        driver.switch_to.frame(frame_element)
        
    def get_all_headers(self, driver: WebDriver) -> Optional[List[dict]]:
        list_headers = []
        
        logs = driver.get_log('performance')

        for entry in logs:
            try:
                log = json.loads(entry['message'])['message']
                
            except (KeyError, json.JSONDecodeError):
                continue

            if log.get('method') == 'Network.requestWillBeSentExtraInfo':
                params = log.get('params', {})
                headers = params.get('headers', {})
                list_headers.append(headers)

        return list_headers
    
    def locate_image_or_none(self, image_paths: Union[str, List[str], Path, List[Path]], max_search_duration: int, region: Optional[Tuple[int, int, int, int]] = None, confidence: float = 0.7, grayscale: bool = False) -> Optional[pyautogui.Point]:
        if isinstance(image_paths, (str, Path)):
            image_paths = [Path(image_paths).as_posix()]
            
        elif isinstance(image_paths, list):
            image_paths = [Path(p).as_posix() if isinstance(p, (str, Path)) else p for p in image_paths]
    
        elapsed_time  = 0
        while elapsed_time <= max_search_duration:
            try:
                for image_path in image_paths:
                    
                    located_image = pyautogui.locateCenterOnScreen(
                        image      = image_path,
                        region     =    region,
                        grayscale  = grayscale,
                        confidence = confidence
                    ) # type: ignore
                    
                    if located_image:
                        return located_image
                    
            except pyautogui.ImageNotFoundException:
                pass
            
            finally:
                wait_time_image += 1
                sleep(1)
        
        return None
    
    def scroll_page(self, driver: WebDriver, direction: Literal['up', 'down'] = 'down', amount: int = 300) -> None:
        if direction == 'down':
            driver.execute_script(f"window.scrollBy(0, {amount});")
        elif direction == 'up':
            driver.execute_script(f"window.scrollBy(0, -{amount});")
    
    def execute_script(self, driver: WebDriver, script: str, *args) -> Any:
        return driver.execute_script(script, *args)

    def execute_async_script(self, driver: WebDriver, script: str, *args) -> Any:
        return driver.execute_async_script(script, *args)

    def get_performance_logs(self, driver: WebDriver) -> List[dict]:
        logs = driver.get_log('performance')
        return logs

    def get_console_logs(self, driver: WebDriver) -> List[dict]:
        logs = driver.get_log('browser')
        return logs
    
    def get_local_storage(self, driver: WebDriver) -> dict:
        return driver.execute_script("return window.localStorage;")

    def set_local_storage(self, driver: WebDriver, key: str, value: str) -> None:
        driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
    
    def navigate_and_interact(self, image: Union[str, Path, pyautogui.Point], action: Literal['click', 'close', 'double_click'] = 'click', search_time: int = 10) -> bool:
        if isinstance(image, (str, Path)):
            location = self.locate_image_or_none(image, search_time)
            
        elif isinstance(image, (pyautogui.Point, tuple)):
            location = image
            
        if location:
            if action == 'click':
                pyautogui.click(location)
            elif action == 'close':
                pyautogui.press('esc')
            elif action == 'double_click':
                pyautogui.doubleClick(location)
            return True
        
        return False

    def accept_alert(self, driver: WebDriver) -> None | bool:
        try:
            WebDriverWait(driver, 10).until(expected_conditions.alert_is_present()).accept()
        except TimeoutException:
            return False

    def dismiss_alert(self, driver: WebDriver) -> None | bool:
        try:
            WebDriverWait(driver, 10).until(expected_conditions.alert_is_present()).dismiss()
        except TimeoutException:
            return False
    
    def center_mouse_and_click(self, click_mouse: Optional[bool] = True) -> None:
        screen_width, screen_height = pyautogui.size()
        
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        pyautogui.moveTo(center_x, center_y)
        
        if click_mouse:
            pyautogui.click()
            
    def capture_screenshot(self, driver: WebDriver, filename: str, download_path: Optional[str] = None, region: Optional[Tuple[int, int, int, int]] = None) -> None:
        screenshot = driver.get_screenshot_as_png()
        
        if region:
            screenshot_image = Image.open(io.BytesIO(screenshot))
            screenshot_image = screenshot_image.crop(region)
        else:
            screenshot_image = Image.open(io.BytesIO(screenshot))
        
        if download_path:
            if not filename.lower().endswith('.png'):
                filename += '.png'
            download_path = os.path.join(download_path, filename)
        else:
            if not filename.lower().endswith('.png'):
                filename += '.png'
            download_path = filename

        screenshot_image.save(download_path, format='PNG')