from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from pandas import read_csv
import openpyxl
from openpyxl.workbook import Workbook



load_dotenv()

today_date = datetime.today().strftime('%Y-%m-%d')
url = os.environ.get('URL')

# Set the path to your ChromeDriver executable
chrome_driver_path = "E:/Development/chromedriver-win64/chromedriver.exe"

# Create Chrome options
chrome_options = Options()

# Open chrome in background mode
# chrome_options.add_argument("--headless")

# Create a Chrome webdriver with options
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL in the browser
driver.get(url)

# Locate the login button and click it (assuming there's a separate login page)
login_button = driver.find_element(By.LINK_TEXT, "Login")
login_button.click()

# Wait for the login page to load using WebDriverWait
wait = WebDriverWait(driver, 20)
username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][placeholder="e.g. 0712 234567"]')))
password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))

# login credentials
username_field.send_keys(os.environ.get('USERNAME'))
password_field.send_keys(os.environ.get('PASSWORD'))

# Submit the login form
login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.session__form__button')))
login_button.click()

# Wait for the dynamic content to load using WebDriverWait
wait = WebDriverWait(driver, timeout=20)
time.sleep(20)
wait = WebDriverWait(driver, 20)
iframe = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="betika-fasta-container"]/iframe')))
# Switch to the iframe
driver.switch_to.frame(iframe)


# Locate and click Auto button
auto_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="tab ng-star-inserted" and contains(text(), "Auto")]')))
ActionChains(driver).move_to_element(auto_button).perform()
auto_button.click()

# Get account balance
def get_balance() -> float:
    """Method to get Aviator account balance

    Returns:
        float: account balance in float type
    """
    balance = driver.find_element(By.XPATH, '//div[@class="balance px-2 d-flex justify-content-end align-items-center"]').text.replace(' KES', '')
    return (float(balance))

# Get amount to bet
def stake(balance) -> int:
    amount = 5
    return (int(balance // amount))


auto_cash_out_xpath = '//button[@class="tab ng-star-inserted"]'
auto_cash_out = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, auto_cash_out_xpath)))
driver.execute_script("arguments[0].scrollIntoView();", auto_cash_out)

# Now you can interact with other elements after the click
auto_cash_out_switcher = driver.find_element(By.XPATH, '//app-ui-switcher[@class="ng-untouched ng-pristine ng-valid"]/div[@class="input-switch off"]')
auto_cash_out_switcher.click()


# Odd update
odd_element = driver.find_element(By.XPATH, '//div[@class="cashout-spinner-wrapper"]//input[@class="font-weight-bold"]')
odd_element.send_keys(Keys.CONTROL + "a")
odd_element.send_keys(Keys.BACKSPACE)
new_text = "1.49"
odd_element.send_keys(new_text)


# Get bet amount

def get_bet_amount():
    bet_amount = driver.find_element(By.XPATH, '//div[@class="input"]/input[@class="font-weight-bold"]')
    if bet_amount.is_displayed() and bet_amount.is_enabled():
        # Clear existing text by backspacing
        bet_amount.send_keys(Keys.CONTROL + "a")
        bet_amount.send_keys(Keys.BACKSPACE)
        new_text = stake(get_balance())
        bet_amount.send_keys(new_text)

# bet by clicking bet button
def place_bet():
    button_xpath = '//button[contains(@class, "bet")]'
    bet_button = driver.find_element(By.XPATH, button_xpath)
    bet_button.click()

get_bet_amount()
place_bet()

# Close the browser window
driver.quit()