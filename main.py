from cmd import PROMPT
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

from index import (
  login_index,
  main_index,
  consulting_index
)

load_dotenv()

CPF  = os.environ.get('CPF')
PASSWORD = os.environ.get('PASSWORD')
CNPJ = os.environ.get('CNPJ_OWN')
URL='https://receita.pr.gov.br/login'

CNPJ_target = input('CNPJ: ')

driver = webdriver.Chrome(ChromeDriverManager().install())
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

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(30)