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
from plyer import notification


load_dotenv()

# windows notification system

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon=None,  # e.g. 'C:\\icon_32x32.ico'
        timeout=10,  # seconds
    )



today_date = datetime.today().strftime('%Y-%m-%d')
url = os.environ.get('ONE_X_BET')

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

# Find and interact with the login form elements

# Assuming 'driver' is your WebDriver instance
wait = WebDriverWait(driver, 40)
login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'loginDropTop')))
login_button.click()
username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="tel"][placeholder=" 712 123456"]')))
password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))

username_field.send_keys(os.environ.get('X_USERNAME'))
password_field.send_keys(os.environ.get('PASSWORD'))

# Click login button
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'auth-button--block'))
)
login_button.click()

time.sleep(10)
# Reload Page
driver.refresh()
time.sleep(30)

wait = WebDriverWait(driver, 20)
iframe = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="slots-app_place"]/iframe')))
# Switch to the iframe
driver.switch_to.frame(iframe)

# Get account balance
def get_balance() -> float:
    """Method to get Aviator account balance

    Returns:
        float: account balance in float type
    """
    balance = driver.find_element(By.XPATH, '//div[@class="amount font-weight-bold"]').text
    return (float(balance))
print(get_balance())

# Get amount to bet
def stake(balance) -> int:
    amount = 2
    return (int(balance // amount))
print(stake(get_balance()))

# Locate and click Auto button
auto_button = WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="tab ng-star-inserted" and contains(text(), "Auto")]')))
ActionChains(driver).move_to_element(auto_button).perform()
auto_button.click()

time.sleep(5)
# Click auto-cashout to on
auto_cash_out_switcher = driver.find_element(By.XPATH, '//app-ui-switcher[@class="ng-untouched ng-pristine ng-valid"]/div[@class="input-switch off"]')
auto_cash_out_switcher.click()


# Odd update
odd_element = driver.find_element(By.XPATH, '//div[@class="cashout-spinner-wrapper"]//input[@class="font-weight-bold"]')
odd_element.send_keys(Keys.CONTROL + "a")
odd_element.send_keys(Keys.BACKSPACE)
new_text = "1.1"
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
get_bet_amount()

# bet by clicking bet button
def place_bet():
    button_xpath = '//button[@class="btn btn-success bet ng-star-inserted"]'
    bet_button = driver.find_element(By.XPATH, button_xpath)
    bet_button.click()

payouts_data = driver.find_element(By.XPATH, '//div[@class="result-history disabled-on-game-focused my-2"]')
payouts_data = payouts_data.text.split("\n")
prep_data = [item.replace('x', '') for item in payouts_data]

print(prep_data)

check_list = prep_data[::]
text_file = f"history {today_date}.txt"
previous_cleaned_payouts = ['s', 'a', 'c']
dict_list = []

nums_of_checks = 0
status = True



# Close the browser window
driver.quit()
