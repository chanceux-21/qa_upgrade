import json
import pytest
import os
from pages.auth_page import AuthPage

# Загрузка тестовых данных
with open(os.path.join(os.path.dirname(__file__), "../data/test_cargo.json")) as f:
    test_data = json.load(f)


@pytest.mark.parametrize("data", test_data, ids=[item["query"] for item in test_data])
def test_cargo_search_parametrized(browser, data):
    # Авторизация
    auth_page = AuthPage(browser)
    main_page = auth_page.login(
        os.getenv("ATI_USER"),
        os.getenv("ATI_PASSWORD")
    )

    # Поиск груза
    main_page.search_cargo(data["query"])
    results = main_page.get_search_results(limit=5)

    # Проверки
    for result in results:
        assert any(kw in result.lower() for kw in data["expected_keywords"]), (
            f"Результат '{result}' не содержит ожидаемых ключевых слов"
        )

    weights = main_page.get_cargo_weights()
    assert all(w >= data["min_weight"] for w in weights), (
        f"Найден груз с весом меньше {data['min_weight']} тонн"
    )   