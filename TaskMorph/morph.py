# Selenium & PyAutoGUI
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)

from PIL import Image

from typing import (
    Union,
    Literal,
    Optional,
    List,
    Tuple,
    Any
)

try:
    import pyautogui
except ImportError:
    import collections
    pyautogui = None

import os
import io
import json
from time import sleep

from TaskMorph.models import ByMapping
from TaskMorph.errors import DriverNotInitializedError


class TaskMorph:
    # Facilita a procura por um By
    by_mapping = ByMapping(
        id = By.ID,
        name = By.NAME,
        xpath = By.XPATH,
        tag_name = By.TAG_NAME,
        link_text = By.LINK_TEXT,
        class_name = By.CLASS_NAME,
        css_selector = By.CSS_SELECTOR,
        partial_link_text = By.PARTIAL_LINK_TEXT 
    )
    
    # Somente um driver pode ser inicializado
    __driver: Optional[WebDriver] = None
    __Point = collections.namedtuple("Point", "x y")
    
    @classmethod
    def start_driver(
        cls,
        options: Optional[uc.ChromeOptions] = None,
        driver_path: Optional[str] = None,
    ) -> WebDriver:
        """
        Inicializa o driver.

        Args:
            driver_path (Optional[str], optional): Caminho para o executavel do driver. Defaults to None.
            options (Optional[uc.ChromeOptions], optional): Opções para modifical o navegador. Defaults to None.

        Returns:
            WebDriver: Retorna o WebDriver configurado (ou não).
        """ 
        if not cls.__driver:
            cls.__driver = uc.Chrome(
                options = options if options else None,
                driver_executable_path = driver_path if driver_path else None
            )
            
        return cls.__driver
    
    @classmethod
    def close_driver(cls) -> None:
        if cls.__driver:
            cls.__driver.quit()
            cls.__driver = None
    
    @classmethod
    def find_element(
        cls,
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
            by (Literal[ &#39;id&#39;, &#39;name&#39;, &#39;xpath&#39;, &#39;tag_name&#39;, &#39;link_text&#39;, &#39;class_name&#39;, &#39;css_selector&#39;, &#39;partial_link_text&#39;, ]): 
            value (str):
            timeout (int, optional): Tempo de espera. Defaults to 10.

        Raises:
            ValueError: Levantará a Exception quando a chave by não for encontrada no dicionário.
            DriverNotInitializedError: Lenvantará a Exception quando o driver não tiver sido inicializado.
            
        Returns:
            WebElement: Retorna o Elemento encontrado.
        """
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        if by not in cls.by_mapping:
            raise ValueError(f"Invalid locator type: {by}")
        
        by_type = cls.by_mapping[by]
        
        element = WebDriverWait(cls.__driver, timeout).until(
            expected_conditions.presence_of_element_located(
                (by_type, value)
            )
        )
        
        return element
    
    @classmethod
    def find_elements(
        cls,
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
            by (Literal[ &#39;id&#39;, &#39;name&#39;, &#39;xpath&#39;, &#39;tag_name&#39;, &#39;link_text&#39;, &#39;class_name&#39;, &#39;css_selector&#39;, &#39;partial_link_text&#39;, ]): 
            value (str):
            timeout (int, optional): Tempo de espera. Defaults to 10.

        Raises:
            ValueError: Levantará a Exception quando a chave by não for encontrada no dicionário.
            DriverNotInitializedError: Lenvantará a Exception quando o driver não tiver sido inicializado.

        Returns:
            List[WebElement]: Retorna uma lista de Elementos.
        """
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        if by not in cls.by_mapping:
            raise ValueError(f"Invalid locator type: {by}")
        
        by_type = cls.by_mapping[by]
        
        element = WebDriverWait(cls.__driver, timeout).until(
            expected_conditions.presence_of_all_elements_located(
                (by_type, value)
            )
        )
        
        return element
    
    @classmethod
    def find_element_clickable( 
        cls,
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
        timeout: int = 10,
        max_retries: int = 5
    ):
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        retries = 0
        while retries < max_retries:
            try:
                element = cls.find_element(by, value)
                element = WebDriverWait(cls.__driver, timeout).until(
                    expected_conditions.element_to_be_clickable(element)
                )
                return element
            
            except (TimeoutException, StaleElementReferenceException):
                retries += 1
        
        raise TimeoutException(f"Elemento '{value}' não ficou clicável após {max_retries} tentativas.")
    
    @classmethod
    def find_element_or_none(
        cls,
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
            by (Literal[ &#39;id&#39;, &#39;name&#39;, &#39;xpath&#39;, &#39;tag_name&#39;, &#39;link_text&#39;, &#39;class_name&#39;, &#39;css_selector&#39;, &#39;partial_link_text&#39;, ]): 
            value (str):
            timeout (int, optional): Tempo de espera. Defaults to 10.

        Raises:
            ValueError: Levantará a Exception quando a chave by não for encontrada no dicionário.
            DriverNotInitializedError: Lenvantará a Exception quando o driver não tiver sido inicializado.
            
        Returns:
            WebElement: Caso encontrado, retornará o Elemento. Se não encontrado, retornará None
        """
        try:
            element = cls.find_element(by, value, timeout)
            return element
        
        except (TimeoutException, NoSuchElementException):
            return None
        
    @classmethod
    def change_iframe(
        cls,
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
            by (Literal[ &#39;id&#39;, &#39;name&#39;, &#39;xpath&#39;, &#39;tag_name&#39;, &#39;link_text&#39;, &#39;class_name&#39;, &#39;css_selector&#39;, &#39;partial_link_text&#39;, ], optional): 
            value (str, optional): 
            timeout (int, optional): Tempo de espera. Defaults to 10.
        
        Raises:
            ValueError: Levantará a Exception quando a chave by não for encontrada no dicionário.
        """
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        if by is None or value is None:
            cls.__driver.switch_to.default_content()
            return
        
        frame_element: WebElement = cls.find_element(by, value, timeout)
        cls.__driver.switch_to.frame(frame_element)
        
    @classmethod
    def get_all_headers(cls) -> Optional[List[dict]]:
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        list_headers = []
        
        logs = cls.__driver.get_log('performance')

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
    
    @classmethod
    def get_performance_logs(cls) -> List[dict]:
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        logs = cls.__driver.get_log('performance')
        return logs

    @classmethod
    def get_console_logs(cls) -> List[dict]:
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        logs = cls.__driver.get_log('browser')
        return logs
    
    @classmethod
    def execute_script(cls, script: str, *args) -> Any:
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        return cls.__driver.execute_script(script, *args)

    @classmethod
    def execute_async_script(cls, script: str, *args) -> Any:
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        return cls.__driver.execute_async_script(script, *args)
    
    @classmethod
    def scroll_page(
        cls, 
        direction: Literal['up', 'down'] = 'down', 
        amount: int = 300  
    ):
        """
        Scrolla a página.

        Args:
            direction (Literal[&#39;up&#39;, &#39;down&#39;], optional): Lado que deseja scrollar. Defaults to 'down'.
            amount (int, optional): Quantidade que deseja scrollar. Defaults to 300.
        """
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        if direction == 'down':
            cls.__driver.execute_script(f"window.scrollBy(0, {amount});")
        elif direction == 'up':
            cls.__driver.execute_script(f"window.scrollBy(0, -{amount});")

    @classmethod         
    def get_local_storage(cls) -> dict:
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        return cls.__driver.execute_script("return window.localStorage;")

    @classmethod
    def set_local_storage(cls, key: str, value: str) -> None:
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        cls.__driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
    
    @classmethod
    def accept_alert(cls) -> bool:
        """
        Aceita o alert.

        Returns:
            bool: Retorna True caso encontre o alert. Retorna False caso não encontre o alert.
        """
        try:
            if not cls.__driver:
                raise DriverNotInitializedError()
        
            WebDriverWait(cls.__driver, 10).until(expected_conditions.alert_is_present()).accept()
            return True
        
        except TimeoutException:
            return False

    @classmethod
    def dismiss_alert(cls) -> bool:
        """
        Recusa o alert.

        Returns:
            bool: Retorna True caso encontre o alert. Retorna False caso não encontre o alert.
        """
        try:
            if not cls.__driver:
                raise DriverNotInitializedError()
        
            WebDriverWait(cls.__driver, 10).until(expected_conditions.alert_is_present()).dismiss()
            return True
        
        except TimeoutException:
            return False
    
    @classmethod
    def capture_screenshot(
        cls,
        filename: str, 
        download_path: Optional[str] = None, 
        region: Optional[Tuple[int, int, int, int]] = None
    ):
        """
        Captura um screenshot do navegador.

        Args:
            filename (str): O nome do arquivo que será salvo o screenshot
            download_path (Optional[str], optional): O caminho até a pasta que será salvo o screenshot. Defaults to None.
            region (Optional[Tuple[int, int, int, int]], optional): Região do screenshot. Defaults to None.
        """
        if not cls.__driver:
            raise DriverNotInitializedError()
        
        screenshot = cls.__driver.get_screenshot_as_png()
        
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
    ):
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
        if pyautogui:
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
        else:
            raise ModuleNotFoundError('Para utilizar esse metódo é necessário installar o `pyautogui`e `opencv-python`')
            
    @staticmethod
    def navigate_and_interact(
        image: Union[str, __Point],
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
        if pyautogui:
            if isinstance(image, str):
                location = TaskMorph.locate_image(image, search_time)
                
            elif isinstance(image, (__Point, tuple)):
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
        else:
            raise ModuleNotFoundError('Para utilizar esse metódo é necessário installar o `pyautogui`e `opencv-python`')
        
    def center_mouse_and_click(self, click_mouse: Optional[bool] = True) -> None:
        if pyautogui:
            screen_width, screen_height = pyautogui.size()
            
            center_x = screen_width // 2
            center_y = screen_height // 2
            
            pyautogui.moveTo(center_x, center_y)
            
            if click_mouse:
                pyautogui.click()
        else:
            raise ModuleNotFoundError('Para utilizar esse metódo é necessário installar o `pyautogui`e `opencv-python`')