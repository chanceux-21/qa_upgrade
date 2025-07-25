# Импорт модулей для работы с ожиданиями в Selenium
from selenium .webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
# Конструктор класса, инициализирует драйвер и базовые параметры
    def __init__(self, driver, base_url="https://ati.su"):
        self.driver = driver # Экземпляр веб-драйвера
        self.base_url = base_url # Базовый URL сайта
        self.timeout =  10 # Таймаут по умолчанию для ожиданий

# Метод для открытия страницы по относительному пути
    def open(self, path):
        self.driver.get(f"{self.base_url}{path}") # Формирование полного URL

 # Поиск элемента с ожиданием его появления в DOM
    def find_element(self, locator, timeout=None):
        timeout = timeout or self.timeout #Используем переданный таймаут или значение по умолчанию
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator),  # Ожидание появления элемента
            message=f"Element {locator} not found"  # Сообщение об ошибке
            )

  # Клик по элементу
    def click_element(self, locator):
        element =self.find_element(locator) # Сначала находим элемент
        element.click() # Выполняем клик
