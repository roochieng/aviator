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
auto_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="tab ng-star-inserted" and contains(text(), "Auto")]')))
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
    button_xpath = '//button[@class="btn btn-success bet ng-star-inserted"]'
    bet_button = driver.find_element(By.XPATH, button_xpath)
    bet_button.click()


check_list = [99, 99, 99, 99, 99, 0]
time_list = [0, 0]
text_file = f"history {today_date}.txt"
dict_list = []

nums_of_checks = 0
status = True


while status:
    payouts = driver.find_element(By.XPATH, '//div[@class="result-history disabled-on-game-focused my-2"]')
    payouts = payouts.text.split("\n")
    cleaned_payouts = [item.replace('x', '') for item in payouts]

    if cleaned_payouts[0] != check_list[0] and time_list[0] != datetime.today().strftime('%Y-%m-%d %H:%M:%S'):
        check_list.insert(0, cleaned_payouts[0])
        time_list.insert(0, datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        if float(check_list[0]) < 1.1 and float(check_list[1]) < 1.1 and float(check_list[2]) < 1.1:
            # Update Bet Amount and place bet
            get_bet_amount()
            print(f"Current Balance: {get_balance()}")
            place_bet()
            print(f"Bet Placed on Pattern 1, stake: {stake(get_balance())}")
            new_data = {}
            new_data["odd"] = check_list[0]
            new_data["datetime"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            new_data["round"] = nums_of_checks
            new_data["odd_bet_placed"] = "Next with Pattern 1"
            dict_list.append(new_data)
            with open(text_file, 'a') as file:
                file.write(f'{new_data}\n')
            print(f"Round: {nums_of_checks}, odd: {check_list[0]}")

        elif float(check_list[0]) < 1.2 and float(check_list[1]) > 2.0 and float(check_list[2]) < 1.2 and float(check_list[3]) < 1.5 and float(check_list[4]) < 1.5 and float(check_list[5]) < 1.5 and float(check_list[6]) < 1.5:
            get_bet_amount()
            print(f"Current Balance: {get_balance()}")
            place_bet()
            print(f"Bet Placed on pattern 2, stake: {stake(get_balance())}")
            new_data = {}
            new_data["odd"] = check_list[0]
            new_data["datetime"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            new_data["round"] = nums_of_checks
            new_data["odd_bet_placed"] = "Next with Pattern 2"
            dict_list.append(new_data)
            with open(text_file, 'a') as file:
                file.write(f'{new_data}\n')
            print(f"Round: {nums_of_checks}, odd: {check_list[0]}")
        elif float(check_list[0]) > 10.0 and float(check_list[1]) < 1.2 and float(check_list[2]) < 1.5 and float(check_list[3]) < 1.5:
            get_bet_amount()
            print(f"Current Balance: {get_balance()}")
            place_bet()
            print(f"Bet Placed on pattern 3, stake: {stake(get_balance())}")
            new_data = {}
            new_data["odd"] = check_list[0]
            new_data["datetime"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            new_data["round"] = nums_of_checks
            new_data["odd_bet_placed"] = "Next with Pattern 3"
            dict_list.append(new_data)
            with open(text_file, 'a') as file:
                file.write(f'{new_data}\n')
            print(f"Round: {nums_of_checks}, odd: {check_list[0]}")
    else:
        new_data = {}
        new_data["odd"] = check_list[0]
        new_data["datetime"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        new_data["round"] = nums_of_checks
        new_data["odd_bet_placed"] = "No Bet Placed"
        dict_list.append(new_data)
        print(f"Round: {nums_of_checks}, odd: {check_list[0]}")
        with open(text_file, 'a') as file:
            file.write(f'{new_data}\n')
        if len(check_list) > 20:
            check_list.pop()
        if len(time_list) > 20:
            time_list.pop()
        nums_of_checks += 1
    if nums_of_checks > 3000:
        status = False


df = pd.DataFrame(dict_list)
df.to_csv(f"Aviator odds history {today_date}.csv", index=False)


# Close the browser window
driver.quit()
