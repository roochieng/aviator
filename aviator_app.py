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

check_list = [0]
# text_file = f"history {today_date}.txt"
dict_list = []

nums_of_checks = 0
status = True

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

# Locate and click Auto button
auto_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="tab ng-star-inserted" and contains(text(), "Auto")]')))
ActionChains(driver).move_to_element(auto_button).perform()
auto_button.click()


# Update Bet Amount
def update_bet_amount():
    input_element = driver.find_element(By.XPATH, '//div[@class="input"]/input[@class="font-weight-bold"]')
    if input_element.is_displayed() and input_element.is_enabled():
        # Clear existing text by backspacing
        input_element.send_keys(Keys.CONTROL + "a")
        input_element.send_keys(Keys.BACKSPACE)
        new_text = stake(get_balance())
        input_element.send_keys(new_text)

update_bet_amount()
# Update odds


"""
#toggle Auto-cashout on
auto_cash_out_xpath = '//button[@class="tab ng-star-inserted"]'
auto_cash_out = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, auto_cash_out_xpath)))
auto_cash_out3 = driver.find_element(By.XPATH, '//app-ui-switcher[@class="ng-untouched ng-pristine ng-valid"]/div[@class="input-switch off"]')
auto_cash_out3.click()"""

time.sleep(10)
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

# bet by clicking bet button
def place_bet():
    button_xpath = '//button[@class="btn btn-success bet holiday-theme ng-star-inserted"]'
    bet_button = driver.find_element(By.XPATH, button_xpath)
    bet_button.click()


"""
while status:
    payouts = driver.find_element(By.XPATH, '//div[@class="result-history disabled-on-game-focused my-2"]')
    payouts = payouts.text.split("\n")
    cleaned_payouts = [item.replace('x', '') for item in payouts]
    if cleaned_payouts[0] != check_list[0]:
        check_list.insert(0, cleaned_payouts[0])
        new_data = {}
        new_data["odd"] = check_list[0]
        new_data["datetime"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        dict_list.append(new_data)

        print(f"Round: {nums_of_checks}, odd: {check_list[0]}")
        with open(text_file, 'a') as file:
            file.write(f'{check_list[0]}\n')
        nums_of_checks += 1
    if nums_of_checks > 3000:
        status = False


# # Write the updated dataframe to an Excel file
# with pd.ExcelWriter('your_file.xlsx') as writer:
#     df = pd.DataFrame({'odd': [dict_list['odd']], 'datetime': [dict_list['datetime']]})
#     df.to_excel(writer, sheet_name='Sheet1', index=False)
df = pd.DataFrame(dict_list)
df.to_csv(f"Aviator odds history {today_date}.csv", index=False)
"""

# Close the browser window
driver.quit()
