# Импорт модулей для работы с локаторами
from selenium.webdriver.common.by import By
# Импорт базового класса страницы
from .base_page import BasePage


class AuthPage(BasePage):
    # Локаторы элементов страницы авторизации
    USERNAME_INPUT = (By.ID, "username")  # Поле ввода логина
    PASSWORD_INPUT = (By.ID, "password")  # Поле ввода пароля
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")  # Кнопка входа
    PROFILE_BUTTON = (By.CLASS_NAME, "header-profile")  # Кнопка профиля (видна после входа)

    # Метод выполнения авторизации
    def login(self, username: str, password: str):
        self.open("/login")  # Открываем страницу авторизации
        # Вводим логин и пароль
        self.find_element(self.USERNAME_INPUT).send_keys(username)
        self.find_element(self.PASSWORD_INPUT).send_keys(password)
        self.click_element(self.LOGIN_BUTTON)  # Кликаем по кнопке входа

        # Ожидаем появления элемента профиля (подтверждение успешного входа)
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.PROFILE_BUTTON)
        )
        return MainPage(self.driver)  # Возвращаем экземпляр главной страницы