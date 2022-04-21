# Mos
How To Run Tests:
  pip install -r requirements.txt
  py.test --alluredir=%allure_result_folder% ./tests
  allure serve %allure_result_folder%
Из костылей: 404 на одной из ссылок, тест как mark.xfail отмечен и в ассерт добавлены ссылки на которые просходил редирект, фикстура логина из-за впн особо ситуацию не изменила - каждый раз смс-подтвержение просило все равно.
