from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os

from index import indexes

load_dotenv()

CPF  = os.environ.get('CPF')
PASSWORD = os.environ.get('PASSWORD')

URL='https://receita.pr.gov.br/login'

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(URL)