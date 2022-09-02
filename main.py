from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

from index import (
  login_index,
  main_index
)

load_dotenv()

CPF  = os.environ.get('CPF')
PASSWORD = os.environ.get('PASSWORD')
URL='https://receita.pr.gov.br/login'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(URL)

# Login
login_input = driver.find_element_by_xpath(login_index['login_xpath'])
login_password = driver.find_element_by_xpath(login_index['password_xpath'])
login_submit = driver.find_element_by_xpath(login_index['submit_login'])

login_input.send_keys(CPF)
login_password.send_keys(PASSWORD)
login_submit.click()

time.sleep(2)

# Logado, tela principal
main_wrapper = driver.find_element_by_xpath(main_index['nf_wrapper'])
main_wrapper.click()

main_consulting = driver.find_element_by_xpath(main_index['nf_consulting'])
main_consulting.click()

time.sleep(30)