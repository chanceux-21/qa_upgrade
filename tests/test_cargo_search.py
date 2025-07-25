# Импорт необходимых модулей
import pytest
# Импорт page objects
from pages.auth_page import AuthPage
from pages.main_page import MainPage
from pages.api_client import ATISUAPIClient
from db_utils import execute_sql_query  # Кастомный модуль для работы с БД


# Используем фикстуру browser (определена в conftest.py)
@pytest.mark.usefixtures("browser")
def test_search_and_verify_cargo(browser):
    # ШАГ 1: Авторизация через UI
    auth_page = AuthPage(browser)  # Создаем экземпляр страницы авторизации
    main_page = auth_page.login("valid_user@ati.su", "secure_password")  # Выполняем вход

    # ШАГ 2: Поиск груза через UI
    main_page.search_cargo("зерно из Краснодара")  # Выполняем поиск

    # Получаем текст ссылки на первый груз
    cargo_link_text = main_page.find_element(MainPage.FIRST_CARGO_LINK).text

    # ШАГ 3: Получение данных через API
    api_client = ATISUAPIClient(access_token="test_token")  # Создаем API клиент
    cargo_id = cargo_link_text.split("#")[-1]  # Извлекаем ID груза из текста ссылки
    api_data = api_client.get_cargo_details(cargo_id)  # Получаем данные по API

    # ШАГ 4: Проверка данных в БД
    db_query = f"SELECT * FROM cargos WHERE id = '{cargo_id}';"  # SQL запрос
    db_result = execute_sql_query("ati_db", db_query)  # Выполняем запрос к БД

    # ПРОВЕРКИ:
    # Сравниваем вес из API и БД
    assert api_data["weight"] == db_result["weight"], "Несоответствие веса в API и БД"

    # Проверяем наличие ключевого слова в описании
    assert "зерно" in api_data["description"], "Груз не содержит ключевое слово"
