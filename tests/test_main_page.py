from multiprocessing import Pool
import allure
import pytest
from base import BasePage
from locators import MainPageLocators


class Test:
    """"""
    main_page_url = 'https://www.mos.ru/'

    @allure.story("Проверяем Title главной страницы")
    def test_go_to_main_page(self, web_browser):
        with allure.step(f'Переходим на : {self.main_page_url}'):
            main_page = BasePage(web_browser, self.main_page_url)
            main_page.get_page()
            with allure.step(f'Проверяем Title главной страницы == Официальный сайт Мэра Москвы'):
                assert main_page.get_title() == 'Официальный сайт Мэра Москвы', \
                    f'{main_page.get_title()} != Официальный сайт Мэра Москвы'

    @allure.story("Собираем все ссылки")
    def test_collect_link(self, web_browser):
        with allure.step(f'Переходим на : {self.main_page_url}'):
            main_page = BasePage(web_browser, self.main_page_url)
            main_page.get_page()
        with allure.step(f'С помощью метода get_all_url() получаем атрибут по тегу "href"'):
            main_page.get_all_url()

    @allure.story("1) Проверить наличие шапки.")
    def test_header(self, web_browser):
        with allure.step(f'Переходим на : {self.main_page_url}'):
            main_page = BasePage(web_browser, self.main_page_url)
            main_page.get_page()
        with allure.step(f'Проверяем наличие шапки по ID {MainPageLocators.header}'):
            assert main_page.is_element_present(MainPageLocators.header)

    @allure.story("2) Проверить наличие подвала.")
    def test_footer(self, web_browser):
        with allure.step(f'Переходим на : {self.main_page_url}'):
            main_page = BasePage(web_browser, self.main_page_url)
            main_page.get_page()
        with allure.step(f'Проверяем наличие подвала по ID {MainPageLocators.footer}'):
            assert main_page.is_element_present(MainPageLocators.footer)

    @allure.story("3) Вытащить все ссылки со страницы и проверить их на 200 (280 шт.)")
    @pytest.mark.xfail(reason='https://www.mos.ru/pgu/ru/drafts/: 404 Страница не найдена ')
    def test_all_link(self):
        with allure.step(f'С помощью ini_reader получаем урлы'):
            items = BasePage.ini_reader()
        with allure.step(f'Используя модуль multiprocessing проходим по всем урлам и получаем статускоды'):
            with Pool(32) as p:
                p.map(BasePage.get_status_code, set(items))  # set что бы не проверять дубли

    @allure.story("4) Открыть каждую ссылку и проверить адресную строку браузера, что открывается нужная ссылка")
    def test_lines(self, web_browser):
        with allure.step(f'С помощью ini_reader получаем урлы'):
            items = BasePage.ini_reader()
        with allure.step(f'Циклом передаем каждый урл для проверки, предварительно убрав дубли (set)'):
            for item in set(items):  # set что бы не проверять дубли
                main_page = BasePage(web_browser, f'{item}')
                main_page.get_page()

        with allure.step(f'[:5] потому что одна ссылка http вместо https,а or использую потому что идут редиректы.'):
            assert item[5:] in main_page.get_current_url() \
                   or main_page.get_current_url().startswith('https://login.mos.ru/sps/login/methods/') \
                   or main_page.get_current_url().startswith('https://www.mos.ru/mobile/?referrer=appmetrica') \
                   or main_page.get_current_url().startswith('https://www.mos.ru/map/?collection') \
                   or main_page.get_current_url().startswith('https://www.mos.ru/otvet-socialnaya-podderjka/')


if __name__ == "__main__":
    pytest.main()
