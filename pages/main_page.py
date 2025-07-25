# Импорт модулей
from selenium.webdriver.common.by import By
from .base_page import BasePage


class MainPage(BasePage):
    # Локаторы элементов главной страницы
    SEARCH_INPUT = (By.ID, "cargoSearchInput")  # Поле поиска грузов
    SEARCH_BUTTON = (By.ID, "searchCargoBtn")  # Кнопка поиска
    RESULTS_TABLE = (By.CLASS_NAME, "cargo-results")  # Таблица результатов
    FIRST_CARGO_LINK = (By.XPATH, "//div[@class='cargo-item'][1]//a")  # Ссылка на первый груз

    # Метод поиска грузов
    def search_cargo(self, cargo_query: str):
        self.find_element(self.SEARCH_INPUT).send_keys(cargo_query)  # Вводим запрос
        self.click_element(self.SEARCH_BUTTON)  # Кликаем поиск

        # Ожидаем появления таблицы результатов
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.RESULTS_TABLE)
        )

    # Метод открытия первого груза в результатах
    def open_first_cargo(self):
        self.click_element(self.FIRST_CARGO_LINK)  # Кликаем по ссылке первого груза
        return "CargoDetailsPage"  # Возвращаем идентификатор следующей страницы
