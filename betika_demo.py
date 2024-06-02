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
# import openpyxl
# from openpyxl.workbook import Workbook
import copy


today_date = datetime.today().strftime('%Y-%m-%d')
url = 'https://www.betika.com/en-ke/aviator'


# Set the path to your ChromeDriver executable
chrome_driver_path = "/home/me/Dependancies/chromedriver-linux64/chromedriver"

# Create Chrome options
chrome_options = Options()

# Open chrome in background mode
# chrome_options.add_argument("--headless")

# Create a Chrome webdriver with options
service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the URL in the browser
driver.get(url)
# Find the button by its class name
demo_button = driver.find_element(By.CLASS_NAME, 'button.account__payments__submit.button.button__secondary')

# Click the button
demo_button.click()


wait = WebDriverWait(driver, timeout=20)
time.sleep(20)
wait = WebDriverWait(driver, 20)
iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'aviator-iframe')))
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
def stake(total_balance) -> int:
    spread = 5
    return (int(total_balance // spread))

#Close Extra Bet window
extra_betwindow_element = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'sec-hand-btn.close.ng-star-inserted')))
extra_betwindow_element.click()

# Locate and click Auto button
auto_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="tab ng-star-inserted" and contains(text(), "Auto")]')))
ActionChains(driver).move_to_element(auto_button).perform()
auto_button.click()


balance = float(driver.find_element(By.XPATH, '//div[@class="balance px-2 d-flex justify-content-end align-items-center"]').text.replace(' KES', ''))
print(balance)

# Click the auto cashout switch on
auto_cash_out_switcher = driver.find_element(By.XPATH, '//app-ui-switcher[@class="ng-untouched ng-pristine ng-valid"]/div[@class="input-switch off"]')
auto_cash_out_switcher.click()


# Odd update
odd_element = driver.find_element(By.XPATH, '//div[@class="cashout-spinner-wrapper"]//input[@class="font-weight-bold"]')
odd_element.send_keys(Keys.CONTROL + "a")
odd_element.send_keys(Keys.BACKSPACE)
new_text = "2.0"
odd_element.send_keys(new_text)


# Get bet amount
def get_bet_amount():
    bet_amount = driver.find_element(By.XPATH, '//div[@class="input"]/input[@class="font-weight-bold"]')
    if bet_amount.is_displayed() and bet_amount.is_enabled():
        # Clear existing text by backspacing
        bet_amount.send_keys(Keys.CONTROL + "a")
        bet_amount.send_keys(Keys.BACKSPACE)
        new_text = stake(balance)
        bet_amount.send_keys(new_text)


# bet by clicking bet button
def place_bet():
    button_xpath = '//button[@class="btn btn-success bet ng-star-inserted"]'
    bet_button = driver.find_element(By.XPATH, button_xpath)
    bet_button.click()

payouts_data = driver.find_element(By.XPATH, '//div[@class="result-history disabled-on-game-focused my-2"]')
payouts_data = payouts_data.text.split("\n")
prep_data = [item.replace('x', '') for item in payouts_data]


check_list = prep_data[::]
text_file = f"Aviator history Demo Odds {today_date}.txt"
dict_list = []

nums_of_checks = 0
status = True


while status:
    payouts = driver.find_element(By.XPATH, '//div[@class="result-history disabled-on-game-focused my-2"]')
    payouts = payouts.text.split("\n")
    cleaned_payouts = [item.replace('x', '') for item in payouts]

    if cleaned_payouts[0:4] != check_list[0:4]:
        check_list.insert(0, cleaned_payouts[0])
        if float(check_list[0]) < 1.1 and float(check_list[1]) < 1.1 and float(check_list[2]) < 1.1:
            # Update Bet Amount
            get_bet_amount()
            print(f"Current Balance: {get_balance()}")
            place_bet()
            print(f"Bet Placed with stake: {stake(get_balance())}")
            # new_data = {}
            # new_data["odd"] = check_list[0]
            # new_data["datetime"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            # new_data["round"] = nums_of_checks
            # new_data["odd_bet_placed"] = "Next"
            # dict_list.append(new_data)
            # with open(text_file, 'a') as file:
            #     file.write(f'{new_data}\n')
            # print(f"Round: {nums_of_checks}, odd: {check_list[0]}")

        elif float(check_list[0]) < 1.2 and float(check_list[1]) < 1.2 and float(check_list[2]) < 1.2 and float(check_list[3]) < 1.2:
            get_bet_amount()
            print(f"Current Balance{get_balance()}")
            place_bet()
            print(f"Bet Placed with stake: {stake(get_balance())}")
            # new_data = {}
            # new_data["odd"] = check_list[0]
            # new_data["datetime"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            # new_data["round"] = nums_of_checks
            # new_data["odd_bet_placed"] = "Next"
            # dict_list.append(new_data)
            # with open(text_file, 'a') as file:
            #     file.write(f'{new_data}\n')
            # print(f"Round: {nums_of_checks}, odd: {check_list[0]}")

        elif float(check_list[0]) < 1.2 and float(check_list[1]) > 2.0 and float(check_list[2]) > 2.0 and float(check_list[3]) < 1.3:
            get_bet_amount()
            print(f"Current Balance{get_balance()}")
            place_bet()
            print(f"Bet Placed with stake: {stake(get_balance())}")
            # new_data = {}
            # new_data["odd"] = check_list[0]
            # new_data["datetime"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            # new_data["round"] = nums_of_checks
            # new_data["odd_bet_placed"] = "Next"
            # dict_list.append(new_data)
            # with open(text_file, 'a') as file:
            #     file.write(f'{new_data}\n')
            # print(f"Round: {nums_of_checks}, odd: {check_list[0]}")
        new_data = {}
        new_data["odd"] = check_list[0]
        new_data["datetime"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        new_data["round"] = nums_of_checks
        new_data["odd_bet_placed"] = "Not Placed"
        dict_list.append(new_data)
        print(f"Round: {nums_of_checks}, odd: {check_list[0]}")
        with open(text_file, 'a') as file:
            file.write(f'{new_data}\n')
        nums_of_checks += 1
    previous_cleaned_payouts = cleaned_payouts[::]
    if nums_of_checks > 1500:
        status = False
df = pd.DataFrame(dict_list)
df.to_csv(f"Aviator Demo odds history {today_date}.csv", index=False)


time.sleep(10)


driver.quit()