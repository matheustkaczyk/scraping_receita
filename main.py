from functools import partial
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver as webdriver_seleniumwire
from dotenv import load_dotenv
from datetime import datetime
import os
import time
import datetime
import json

from index import (
  login_index,
  main_index,
  consulting_index,
  data_index
)

load_dotenv()

CPF  = os.environ.get('CPF')
PASSWORD = os.environ.get('PASSWORD')
CNPJ = os.environ.get('CNPJ_OWN')
URL='https://receita.pr.gov.br/login'

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

# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
driver = webdriver_seleniumwire.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

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
consulting_select = driver.find_element(By.XPATH, consulting_index['consulting_select'])
consulting_filter_select = driver.find_element(By.XPATH, consulting_index['consulting_filter_select'])
consulting_submit = driver.find_element(By.XPATH, consulting_index['consulting_submit'])

consulting_select.click()
consulting_select_opt = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/article/div[2]/div[1]/div[1]/div/select/option[2]')

time.sleep(.5)

consulting_select_opt.click()

consulting_filter_select = Select(driver.find_element(By.XPATH, consulting_index['consulting_filter_select']))
consulting_filter_select.select_by_visible_text('Destinatário')

time.sleep(.5)

consulting_target_cnpj_input = driver.find_element(By.XPATH, consulting_index['consulting_target_cnpj_input'])
consulting_target_cnpj_input.send_keys(CNPJ_target)

time.sleep(.5)

consulting_submit.click()

time.sleep(.5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#Captura dos dados
partial_data = []
# list_table_elements = driver.find_elements(By.XPATH, data_index['data_table'])

# line_number = 1
# page_number = 3 # Página 3 é a primeira página com dados
# page_list_xpath = f'//*[@id="app"]/div[1]/div/div/div[2]/table/tfoot/tr/td/div/nav/ul/li[{page_number}]'

# for element in list_table_elements:
#   element_text = element.text + ' '
#   split_element = element_text.split(' ')
#   splitted_date = split_element[1].split('/')
#   formatted_date = [int(splitted_date[2]), int(splitted_date[1]), int(splitted_date[0])]
#   element_date = datetime.date(year=formatted_date[0], month=formatted_date[1], day=formatted_date[2])
#   before_folder = os.listdir(os.getcwd())

#   if(element_date <= date_target_parsed):
#     xml_btn_path = f'//*[@id="app"]/div[1]/div/div/div[2]/table/tbody/tr[{line_number}]/td[10]/button'
    
#     xml_btn = driver.find_element(By.XPATH, xml_btn_path)
#     xml_btn.click()

#     time.sleep(2.5)

#     after_folder = os.listdir(os.getcwd())
#     diff = set(after_folder) - set(before_folder)

#     with open('nfae.xml', 'rb') as xml_file:
#       xml_data = xmltodict.parse(xml_file.read())
#       total_value = xml_data['nfeProc']['NFe']['infNFe']['total']['ICMSTot']['vNF']

#     if(len(diff) == 1):
#       file_name = diff.pop()
#       os.remove(file_name)
#     else:
#       print('More than one file or no file downloaded')

#     line_number += 1

#     final_data.append({
#       'date': split_element[1],
#       'code': split_element[2],
#       'value': total_value
#     })
  
# print(final_data)

for requests in driver.requests:
  if (requests.url == 'https://nfae.fazenda.pr.gov.br/nfae/api/nfae?acao=LISTAR'):
    partial_data.append(requests.response.body)

time.sleep(2)

parsing = json.loads(partial_data[0])
final_json = json.dumps(parsing)


json_data = json.loads(final_json)

for item in json_data['lista']:
  parsed_json = json.loads(item['json'])
  data = datetime.datetime.fromtimestamp(item['dtProcessamento']).strftime('%d/%m/%Y'),
  parsed_year = str(datetime.datetime.fromtimestamp(item['dtProcessamento'])).split(' ')[0].split('-')[0]

  if int(parsed_year) == int(YEAR_target):
    final_data.append({
      "data": data,
      "total_value": parsed_json['total']['ICMSTotal']['vNF']
    })

driver.quit()

time.sleep(30)
