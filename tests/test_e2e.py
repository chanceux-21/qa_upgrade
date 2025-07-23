import os
import pytest
from pages.auth_page import AuthPage
from pages.main_page import MainPage
from pages.api_client import ATIAPIClient


@pytest.mark.e2e
def test_cargo_search_and_verify(browser):
    # Инициализация API клиента
    api_client = ATIAPIClient()

    # Шаг 1: UI - Авторизация
    login_page = AuthPage(browser)
    main_page = login_page.login(
        os.getenv("ATI_USER"),
        os.getenv("ATI_PASSWORD")
    )

    # Шаг 2: UI - Поиск груза
    cargo_query = "зерно из Краснодара"
    main_page.search_cargo(cargo_query)
    cargo_id = main_page.get_first_cargo_id()

    # Шаг 3: API - Проверка данных
    cargo_data = api_client.get_cargo_details(cargo_id)

    # Проверки
    assert cargo_data["status"] == "active", "Статус груза не активен"
    assert "зерно" in cargo_data["description"].lower(), "Описание не содержит ключевое слово"
    assert cargo_data["weight"] > 0, "Вес груза должен быть положительным"

    # Шаг 4: UI - Открытие детальной страницы
    details_page = main_page.open_cargo_details(cargo_id)
    assert details_page.is_loaded(), "Страница деталей груза не загрузилась"
    assert cargo_data["title"] in details_page.get_title(), "Заголовок не соответствует данным API"