from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert

options = Options()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get("https://jumin.mois.go.kr/")

wait = WebDriverWait(driver, 10) 

admm_age_element = wait.until(EC.element_to_be_clickable((By.ID, 'admmAge')))
admm_age_element.click()

driver.switch_to.frame(driver.find_element(By.ID, 'totalFrame'))

wait.until(EC.presence_of_element_located((By.NAME, 'searchYearStart')))

select_elements = {
    'searchYearStart': '2023',
    'searchYearEnd': '2023',
    'searchMonthStart': '12',
    'searchMonthEnd': '12'
}
for name, value in select_elements.items():
    select_element = wait.until(EC.presence_of_element_located((By.NAME, name)))
    select = Select(select_element)
    select.select_by_value(value)

select = wait.until(EC.presence_of_element_located((By.NAME, 'sltArgTypes')))
select = Select(select)
select.select_by_value('5')

select = wait.until(EC.presence_of_element_located((By.NAME, 'sltArgTypeB')))
select = Select(select)
select.select_by_value('100')

search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn_search')))
search_button.click()

download_button = wait.until(EC.element_to_be_clickable((By.NAME, 'xlsxDown')))
download_button.click()

wait.until(EC.alert_is_present())
alert = Alert(driver)
alert.accept()
