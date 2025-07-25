import pytest
import allure
from selenium import webdriver


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser")
        if driver:
            screenshot = driver.get_screenshot_as_base64()
            html = f'<div><img src="data:image/png;base64,{screenshot}" alt="screenshot"></div>'
            allure.attach(html, name="screenshot", attachment_type=allure.attachment_type.HTML)


@pytest.fixture(scope="function")
def browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

# Добавить обработку разных браузеров
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser: chrome/firefox")


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser")
    if browser_name == "firefox":
        driver = webdriver.Firefox()
    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Добавить headless режим
        driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(5)
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs["browser"]
        screenshot = driver.get_screenshot_as_base64()
        html = f'<div><img src="data:image/png;base64,{screenshot}" alt="screenshot"></div>'
        report.extra = [pytest_html.extras.html(html)]
