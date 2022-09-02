from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

load_dotenv()

URL='https://receita.pr.gov.br/login'

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(URL)