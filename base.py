import time
import allure
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators import MainPageLocators


class BasePage:
    """BasePage методы"""

    def __init__(self, driver, url):
        self.driver = driver
        self.base_url = url

    def get_page(self):
        """открытие страницы"""
        self.driver.get(self.base_url)

    def get_title(self):
        """получение заголовка страницы"""
        with allure.step(f'Возвращаем Title страницы {self.driver.title}'):
            return self.driver.title

    def get_all_url(self):
        """получение всех ссылок"""
        with allure.step(f'Клик на  элемент'):
            self.scroll_down()
            time.sleep(0.5)
            self.scroll_up()
            time.sleep(0.5)
            elems = self.find_elements(MainPageLocators.link)
            i = 0
            with open("link.csv", "w") as file:
                for elem in elems:
                    # убрал из выборки ссылок редиректы на магазины приложений,можно отдельным тестом
                    if not elem.get_attribute('class').startswith('MobileApp_sectionItem__3bYVx'):
                        file.write(elem.get_attribute('href') + '; ')
                        i += 1
                print(i)

    def find_element(self, locator, time=5):
        """поиск элемента на странице"""
        with allure.step(f'Ищем элемент  {locator}'):
            return WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(locator),
                                                          message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=5):
        """поиск элементов на странице"""
        with allure.step(f'Ищем элементы  {locator}.'):
            return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                          message=f"Can't find elements by locator {locator}")

    def send_keys(self, locator, key=None, ):
        """отправка текста в поля ввода"""
        with allure.step(f'Ищем элемент  {locator} и используя send_keys отправляем {key}.'):
            element = self.find_element(locator)
            if element:
                element.send_keys(key)

            else:
                msg = 'Element with locator {0} not found'
                raise AttributeError(msg.format(locator))

    def click_on_elem(self, locator):
        """нажатие на элемент"""
        with allure.step(f'Ищем элемент  {locator} и кликаем его.'):
            return self.find_element(locator).click(), f"Can't find element by locator {locator}"

    def is_element_present(self, locator, timeout=4):
        """проверка присутствия элемента"""
        with allure.step(f'Ищем элемент  {locator}'):
            try:
                WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            except NoSuchElementException:
                return False
            return True

    def scroll_down(self, offset=0):
        """ скролл вниз """

        if offset:
            self.driver.execute_script('window.scrollTo(0, {0});'.format(offset))
        else:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    def scroll_up(self, offset=0):
        """ скролл вверх """

        if offset:
            self.driver.execute_script('window.scrollTo(0, -{0});'.format(offset))
        else:
            self.driver.execute_script('window.scrollTo(0, -document.body.scrollHeight);')

    def get_current_url(self):
        """ возвращает текущий урл """
        return self.driver.current_url

    @staticmethod
    def get_status_code(url):
        """получение статус кодов"""
        statuscode_url = requests.get(url).status_code
        assert statuscode_url == 200, f'{url} status_code: {statuscode_url}'
        print(f'\n {url} {statuscode_url}')

    @staticmethod
    def ini_reader():
        """читалка файла с ссылками"""
        with open('link.csv', 'r') as file:
            links = file.read()
            items = links[:-1].split('; ')
            return items
