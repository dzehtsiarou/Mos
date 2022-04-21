import pytest
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope='session')
def web_browser():
    """browser fixture"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    browser.set_window_size(1920, 1080)
    browser.implicitly_wait(2)

    yield browser
    browser.quit()
