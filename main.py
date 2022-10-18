from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as webdriver_seleniumwire
from dotenv import load_dotenv
from datetime import datetime
from pandas import DataFrame
import os
import time
import json

from index import (
    login_index,
    main_index,
    consulting_index,
)

load_dotenv()

CPF = os.environ.get('CPF')
PASSWORD = os.environ.get('PASSWORD')
CNPJ = os.environ.get('CNPJ_OWN')
URL = 'https://receita.pr.gov.br/login'

final_data = []

CNPJ_target = input('CNPJ: ')
YEAR_target = input('Ano desejado: ')

options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": os.getcwd(),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver_seleniumwire.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=options)

driver.maximize_window()
driver.get(URL)

# Login
login_input = driver.find_element(By.XPATH, login_index['login_xpath'])
login_password = driver.find_element(By.XPATH, login_index['password_xpath'])
login_submit = driver.find_element(By.XPATH, login_index['submit_login'])

login_input.send_keys(CPF)
login_password.send_keys(PASSWORD)
login_submit.click()

time.sleep(2)

# Logado, tela principal
main_wrapper = driver.find_element(By.XPATH, main_index['nf_wrapper'])
main_wrapper.click()

time.sleep(.5)

main_consulting = driver.find_element(By.XPATH, main_index['nf_consulting'])
main_consulting.click()

time.sleep(1)

# Tela de consulta
consulting_select = driver.find_element(
    By.XPATH, consulting_index['consulting_select'])
consulting_filter_select = driver.find_element(
    By.XPATH, consulting_index['consulting_filter_select'])
consulting_submit = driver.find_element(
    By.XPATH, consulting_index['consulting_submit'])

consulting_select.click()
consulting_select_opt = driver.find_element(
    By.XPATH,
    '//*[@id="app"]/div[1]/article/div[2]/div[1]/div[1]/div/select/option[2]'
    )

time.sleep(.5)

consulting_select_opt.click()

consulting_filter_select = Select(driver.find_element(
    By.XPATH, consulting_index['consulting_filter_select']))
consulting_filter_select.select_by_visible_text('Destinatário')

time.sleep(.5)

consulting_target_cnpj_input = driver.find_element(
    By.XPATH, consulting_index['consulting_target_cnpj_input'])
consulting_target_cnpj_input.send_keys(CNPJ_target)

time.sleep(.5)

consulting_submit.click()

time.sleep(.5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Captura dos dados
partial_data = []

for requests in driver.requests:
    if (requests.url == 'https://nfae.fazenda.pr.gov.br/nfae/api/nfae?acao=LISTAR'):
        partial_data.append(requests.response.body)

time.sleep(2)

parsing = json.loads(partial_data[0])
final_json = json.dumps(parsing)

json_data = json.loads(final_json)


for item in json_data['lista']:
    parsed_json = json.loads(item['json'])
    data = datetime.fromtimestamp(
        item['dtProcessamento']).strftime('%d/%m/%Y'),
    parsed_year = str(datetime.fromtimestamp(
        item['dtProcessamento'])).split(' ')[0].split('-')[0]

    if (int(parsed_year) == int(YEAR_target)) and item['indSituacao'] != '0':
        final_data.append({
            "data": data[0],
            "total_value": float(parsed_json['total']['ICMSTotal']['vNF'].replace(',', '.')),
        })

driver.quit()

# Resultado
df = DataFrame(final_data)
df.to_excel('dados.xlsx', index=False)

print('Finalizado com sucesso!')
