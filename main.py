from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
import time
import datetime

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
DATE_target = input('Data (dd/mm/aa): ')

options = Options()
options.add_experimental_option("prefs", {
  "download.default_directory": os.getcwd(),
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

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

#Análise dos dados

list_table_elements = driver.find_elements(By.XPATH, data_index['data_table'])
date_target_split = DATE_target.split('/')
date_target_parsed = datetime.date(int(date_target_split[2]), int(date_target_split[1]), int(date_target_split[0]))

line_number = 1
w_handles = driver.current_window_handle
for element in list_table_elements:
  element_text = element.text + ' '
  split_element = element_text.split(' ')
  splitted_date = split_element[1].split('/')
  element_date = datetime.date(year=int(splitted_date[2]), month=int(splitted_date[1]), day=int(splitted_date[0]))

  if(element_date <= date_target_parsed):
    xml_btn_path = f'//*[@id="app"]/div[1]/div/div/div[2]/table/tbody/tr[{line_number}]/td[10]/button'
    
    xml_btn = driver.find_element(By.XPATH, xml_btn_path)
    xml_btn.click()

    time.sleep(1)

    line_number += 1
  
print(final_data)

time.sleep(30)
