# Selenium & PyAutoGUI
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException
)

import pyautogui
from pyautogui import Point
from time import sleep

# Pillow
from PIL import Image


# Standand Packages
import os
import io
import json
from typing import (
    Union,
    Literal,
    Optional,
    List,
    Tuple,
    Dict,
    Any
)


class TaskMorph:
    
    by_mapping: Dict[str, str] = {
        "id" : By.ID,
        "name" : By.NAME,
        "xpath" : By.XPATH,
        "tag_name" : By.TAG_NAME,
        "link_text" : By.LINK_TEXT,
        "class_name" : By.CLASS_NAME,
        "css_selector" : By.CSS_SELECTOR,
        "partial_link_text" : By.PARTIAL_LINK_TEXT,
    }
    
    @staticmethod
    def initialize_driver(
        driver_path: Optional[str] = None,
        options: Optional[uc.ChromeOptions] = None,
    ) -> WebDriver:
        """
        Inicializa o driver.

        Args:
            driver_path (Optional[str], optional): Caminho para o executavel do driver. Defaults to None.
            options (Optional[uc.ChromeOptions], optional): Opções para modifical o navegador. Defaults to None.

        Returns:
            WebDriver: Retorna o WebDriver configurado (ou não).
        """
        if not driver_path:
            driver_path = ChromeDriverManager().install()
            
        if not options:
            options = uc.ChromeOptions()
        
        return uc.Chrome(
            options = options,
            driver_executable_path = driver_path
        )
        
    @staticmethod
    def find_element(
        driver: WebDriver,
        by: Literal[
            'id', 
            'name', 
            'xpath', 
            'tag_name', 
            'link_text', 
            'class_name',
            'css_selector',
            'partial_link_text', 
        ],
        value: str,
        timeout: int = 10
    ) -> WebElement:
        """
        Procura o Elemento do valor especificado.

        Args:
            driver (WebDriver):
            by (Literal[ &#39;id&#39;, &#39;name&#39;, &#39;xpath&#39;, &#39;tag_name&#39;, &#39;link_text&#39;, &#39;class_name&#39;, &#39;css_selector&#39;, &#39;partial_link_text&#39;, ]): 
            value (str):
            timeout (int, optional): Tempo de espera. Defaults to 10.

        Raises:
            ValueError: Levantará a Exception quando a chave by não for encontrada no dicionário.

        Returns:
            WebElement: Retorna o Elemento encontrado.
        """
        if by not in TaskMorph.by_mapping:
            raise ValueError(f"Invalid locator type: {by}")
        
        by_type = TaskMorph.by_mapping[by]
        
        element = WebDriverWait(driver, timeout).until(
            expected_conditions.presence_of_element_located(
                (by_type, value)
            )
        )
        
        return element
    
    @staticmethod
    def find_elements(
        driver: WebDriver,
        by: Literal[
            'id', 
            'name', 
            'xpath', 
            'tag_name', 
            'link_text', 
            'class_name',
            'css_selector',
            'partial_link_text', 
        ],
        value: str,
        timeout: int = 10
    ) -> List[WebElement]:
        """
        Procura os Elementos que contém o valor especificado.

        Args:
            driver (WebDriver):
            by (Literal[ &#39;id&#39;, &#39;name&#39;, &#39;xpath&#39;, &#39;tag_name&#39;, &#39;link_text&#39;, &#39;class_name&#39;, &#39;css_selector&#39;, &#39;partial_link_text&#39;, ]): 
            value (str):
            timeout (int, optional): Tempo de espera. Defaults to 10.

        Raises:
            ValueError: Levantará a Exception quando a chave by não for encontrada no dicionário.

        Returns:
            List[WebElement]: Retorna uma lista de Elementos.
        """
        if by not in TaskMorph.by_mapping:
            raise ValueError(f"Invalid locator type: {by}")
        
        by_type = TaskMorph.by_mapping[by]
        
        element = WebDriverWait(driver, timeout).until(
            expected_conditions.presence_of_all_elements_located(
                (by_type, value)
            )
        )
        
        return element
    
    @staticmethod
    def find_element_or_none(
        driver: WebDriver,
        by: Literal[
            'id', 
            'name', 
            'xpath', 
            'tag_name', 
            'link_text', 
            'class_name',
            'css_selector',
            'partial_link_text', 
        ],
        value: str,
        timeout: int = 10 
    ) -> Optional[WebElement]:
        """
        Procura o Elemento do valor especificado. Se não achado, retornará nulo e não levantará uma Exception.

        Args:
            driver (WebDriver):
            by (Literal[ &#39;id&#39;, &#39;name&#39;, &#39;xpath&#39;, &#39;tag_name&#39;, &#39;link_text&#39;, &#39;class_name&#39;, &#39;css_selector&#39;, &#39;partial_link_text&#39;, ]): 
            value (str):
            timeout (int, optional): Tempo de espera. Defaults to 10.

        Raises:
            ValueError: Levantará a Exception quando a chave by não for encontrada no dicionário.

        Returns:
            WebElement: Caso encontrado, retornará o Elemento. Se não encontrado, retornará None
        """
        try:
            element = TaskMorph.find_element(driver, by, value, timeout)
            return element
        
        except (TimeoutException, NoSuchElementException):
            return None
    
    @staticmethod
    def change_iframe(
        driver: WebDriver,
        
        by: Optional[
            Literal[
                'id', 
                'name', 
                'xpath', 
                'tag_name', 
                'link_text', 
                'class_name',
                'css_selector',
                'partial_link_text', 
            ]
        ] = None,
        
        value: Optional[str] = None,
        timeout: int = 10
    ):
        """
        Troca para um IFrame de acordo com o valor especificado. 
        Caso os parametros by e value não sejam declarados, ele voltará para o IFrame padrão.

        Args:
            driver (WebDriver): 
            by (Literal[ &#39;id&#39;, &#39;name&#39;, &#39;xpath&#39;, &#39;tag_name&#39;, &#39;link_text&#39;, &#39;class_name&#39;, &#39;css_selector&#39;, &#39;partial_link_text&#39;, ], optional): 
            value (str, optional): 
            timeout (int, optional): Tempo de espera. Defaults to 10.
        
        Raises:
            ValueError: Levantará a Exception quando a chave by não for encontrada no dicionário.
        """
        if by is None or value is None:
            driver.switch_to.default_content()
            return
        
        frame_element: WebElement = TaskMorph.find_element(driver, by, value, timeout)
        driver.switch_to.frame(frame_element)
        
    @staticmethod
    def get_all_headers(driver: WebDriver) -> Optional[List[dict]]:
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
    
    @staticmethod
    def get_performance_logs(driver: WebDriver) -> List[dict]:
        logs = driver.get_log('performance')
        return logs

    @staticmethod
    def get_console_logs(driver: WebDriver) -> List[dict]:
        logs = driver.get_log('browser')
        return logs
    
    @staticmethod
    def execute_script(driver: WebDriver, script: str, *args) -> Any:
        return driver.execute_script(script, *args)

    @staticmethod
    def execute_async_script(driver: WebDriver, script: str, *args) -> Any:
        return driver.execute_async_script(script, *args)
    
    @staticmethod
    def scroll_page(
        driver: WebDriver, 
        direction: Literal['up', 'down'] = 'down', 
        amount: int = 300  
    ):
        """
        Scrolla a página.

        Args:
            driver (WebDriver):
            direction (Literal[&#39;up&#39;, &#39;down&#39;], optional): Lado que deseja scrollar. Defaults to 'down'.
            amount (int, optional): Quantidade que deseja scrollar. Defaults to 300.
        """
        if direction == 'down':
            driver.execute_script(f"window.scrollBy(0, {amount});")
        elif direction == 'up':
            driver.execute_script(f"window.scrollBy(0, -{amount});")

    @staticmethod         
    def get_local_storage(driver: WebDriver) -> dict:
        return driver.execute_script("return window.localStorage;")

    @staticmethod
    def set_local_storage(driver: WebDriver, key: str, value: str) -> None:
        driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
    
    @staticmethod
    def accept_alert(driver: WebDriver) -> bool:
        """
        Aceita o alert.

        Args:
            driver (WebDriver):

        Returns:
            bool: Retorna True caso encontre o alert. Retorna False caso não encontre o alert.
        """
        try:
            WebDriverWait(driver, 10).until(expected_conditions.alert_is_present()).accept()
            return True
        except TimeoutException:
            return False

    @staticmethod
    def dismiss_alert(driver: WebDriver) -> bool:
        """
        Recusa o alert.

        Args:
            driver (WebDriver):

        Returns:
            bool: Retorna True caso encontre o alert. Retorna False caso não encontre o alert.
        """
        try:
            WebDriverWait(driver, 10).until(expected_conditions.alert_is_present()).dismiss()
            return True
        except TimeoutException:
            return False
    
    @staticmethod
    def capture_screenshot(
        driver: WebDriver, 
        filename: str, 
        download_path: Optional[str] = None, 
        region: Optional[Tuple[int, int, int, int]] = None
    ):
        """
        Captura um screenshot do navegador.

        Args:
            driver (WebDriver):
            filename (str): O nome do arquivo que será salvo o screenshot
            download_path (Optional[str], optional): O caminho até a pasta que será salvo o screenshot. Defaults to None.
            region (Optional[Tuple[int, int, int, int]], optional): Região do screenshot. Defaults to None.
        """
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
        
    @staticmethod
    def locate_image(
        image_path: str, 
        max_search_duration: int, 
        region: Optional[Tuple[int, int, int, int]] = None, 
        confidence: float = 0.7, 
        grayscale: bool = False,
        raise_exeception: bool = False
    ) -> Optional[Point]:
        """
        Localiza a imagem especificada na tela, retornando as coordenadas do centro da imagem localizada.

        Args:
            image_path (str): O caminho da imagem.
            
            max_search_duration (int): O tempo máximo em segundos para procurar a imagem na tela.
            
            region (Optional[Tuple[int, int, int, int]], optional): Um tupla de quatro inteiros que define a região da tela 
                (x, y, largura, altura) onde a busca deve ocorrer. Se None, a busca será feita em toda a tela.
                
            confidence (float, optional): O nível de confiança necessário para considerar que a imagem foi localizada. O valor deve estar entre 0 e 1. 
                Defaults to 0.7.
                
            grayscale (bool, optional): Se True, a busca será feita em escala de cinza. 
                Defaults to False.
            
            raise_exeception (bool, optional): Se True, uma exceção será levantada quando a imagem não for encontrada. 
                Defaults to False.

        Raises:
            e: Raises: Levantado se raise_exeception for True e a imagem não for encontrada.

        Returns:
            Optional[Point]: Um objeto Point representando as coordenadas (x, y) do 
            centro da imagem localizada. Retorna None se a imagem não for encontrada 
            dentro do tempo máximo.
            
        """

        elapsed_time  = 0
        while elapsed_time <= max_search_duration:
            try:
                located_image = pyautogui.locateCenterOnScreen(
                    image      = image_path,
                    region     =    region,
                    grayscale  = grayscale,
                    confidence = confidence
                ) # type: ignore
                
                if located_image:
                    return located_image
                    
            except pyautogui.ImageNotFoundException as e:
                if raise_exeception:
                    raise e
            
            finally:
                elapsed_time += 1
                sleep(1)
        
        return None
    
    @staticmethod
    def navigate_and_interact(
        image: Union[str, pyautogui.Point], 
        action: Literal['click', 'close', 'double_click'] = 'click', 
        search_time: int = 10
    ) -> bool:
        """
        Navega e interage com um elemento da tela, com base em uma imagem ou coordenadas.

        Args:
            image (Union[str, pyautogui.Point]): O caminho para a imagem a ser localizada ou um objeto Point (ou tupla) representando coordenadas específicas na tela.
            action (Literal[&#39;click&#39;, &#39;close&#39;, &#39;double_click&#39;], optional): A ação a ser realizada após a localização da imagem ou coordenada. Pode ser 'click', 'close' (pressiona 'esc') ou 'double_click'. Defaults to 'click'.
            search_time (int, optional): O tempo máximo (em segundos) para procurar a imagem na tela, caso um caminho de imagem seja fornecido. Defaults to 10.

        Returns:
            bool: Retorna True se a imagem foi localizada e a ação foi realizada com sucesso. Retorna False se a imagem não foi encontrada dentro do tempo especificado ou se a ação não foi realizada.
        """
        if isinstance(image, str):
            location = TaskMorph.locate_image(image, search_time)
            
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
        
    def center_mouse_and_click(self, click_mouse: Optional[bool] = True) -> None:
        screen_width, screen_height = pyautogui.size()
        
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        pyautogui.moveTo(center_x, center_y)
        
        if click_mouse:
            pyautogui.click()