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
from plyer import notification


load_dotenv()

# windows notification system

def show_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_icon=None,
        timeout=10,  # seconds
    )



today_date = datetime.today().strftime('%Y-%m-%d')
url = os.environ.get('SPESA_URL')

# Setup Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode for faster performance
chrome_service = ChromeService(executable_path='/home/me/Dependancies/chromedriver-linux64/chromedriver')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


# Open the URL in the browser
driver.get(url)

# Get logins
wait = WebDriverWait(driver, 20)
username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="text"][placeholder="Mobile"]')))
password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]')))
submit_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="submit"]')))

# username = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, "user")))

# password_field = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, "password")))

# button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//button[@class='button--primary login-form__button']"))
# )



# Enter login credentials
username_input.send_keys(os.environ.get('_USERNAME'))
password_input.send_keys(os.environ.get('PASSWORD'))

# Submit the form
submit_button.click()


# Casino button avaitor button
aviator_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.aviator"))
)

# Click the Aviator link
aviator_link.click()

time.sleep(30)


# Get list of last payouts
payouts_data = driver.find_element(By.XPATH, '//div[@class="result-history disabled-on-game-focused my-2"]')
payouts_data = payouts_data.text.split("\n")
prep_data = [item.replace('x', '') for item in payouts_data]


# bet by clicking bet button
def place_bet():
    button_xpath = '//button[@class="btn btn-success bet ng-star-inserted"]'
    bet_button = driver.find_element(By.XPATH, button_xpath)
    bet_button.click()


# Get account balance
def get_balance() -> float:
    """Method to get sportpesa account balance

    Returns:
        float: account balance in float type
    """
    balance = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'amount.font-weight-bold')))
    #.text.replace(' KES', '')
    balance = balance.text
    return (float(balance))


# Get amount to bet
def stake(balance) -> int:
    if int(balance // 2) > 2500:
        bet_amount = 2500
    else:
        bet_amount = balance // 2
    return (bet_amount)


# Get bet amount
def update_bet_amount():
    bet_amount = driver.find_element(By.XPATH, '//div[@class="input"]/input[@class="font-weight-bold"]')
    if bet_amount.is_displayed() and bet_amount.is_enabled():
        bet_amount.send_keys(Keys.CONTROL + "a")
        bet_amount.send_keys(Keys.BACKSPACE)
        new_text = stake(get_balance())
        bet_amount.send_keys(new_text)

# Odds update
def second_odd_bet():
    odd_element = driver.find_element(By.XPATH, '//div[@class="cashout-spinner-wrapper"]//input[@class="font-weight-bold"]')
    odd_element.send_keys(Keys.CONTROL + "a")
    odd_element.send_keys(Keys.BACKSPACE)
    new_text = "1.20"
    odd_element.send_keys(new_text)


def first_odd_bet():
    odd_element = driver.find_element(By.XPATH, '//div[@class="cashout-spinner-wrapper"]//input[@class="font-weight-bold"]')
    odd_element.send_keys(Keys.CONTROL + "a")
    odd_element.send_keys(Keys.BACKSPACE)
    new_text = "1.10"
    odd_element.send_keys(new_text)


check_list = prep_data[::]
text_file = f"sportpesa_logs/Sportpesa Aviator history {today_date}.txt"
previous_cleaned_payouts = ['s', 'a', 'c']
dict_list = []

payouts = driver.find_element(By.XPATH, '//div[@class="result-history disabled-on-game-focused my-2"]')
payouts = payouts.text.split("\n")
cleaned_payouts = [item.replace('x', '') for item in payouts]

wait_check = True

while wait_check:
    payouts = driver.find_element(By.XPATH, '//div[@class="result-history disabled-on-game-focused my-2"]')
    payouts = payouts.text.split("\n")
    cleaned_payouts = [item.replace('x', '') for item in payouts]
    if cleaned_payouts[0:4] != check_list[0:4]:
        # Locate and click Auto button
        auto_button = WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="tab ng-star-inserted" and contains(text(), "Auto")]')))
        ActionChains(driver).move_to_element(auto_button).perform()
        auto_button.click()

        time.sleep(0.5)

        # Click auto-cashout to on
        auto_cash_out_switcher = driver.find_element(By.XPATH, '//app-ui-switcher[@class="ng-untouched ng-pristine ng-valid"]/div[@class="input-switch off"]')
        auto_cash_out_switcher.click()

        wait_check = False

directory = 'csv'
if not os.path.exists(directory):
    os.makedirs(directory)


wins = 0
nums_of_checks = 0
status = True


while status:
    payouts = driver.find_element(By.XPATH, '//div[@class="result-history disabled-on-game-focused my-2"]')
    payouts = payouts.text.split("\n")
    cleaned_payouts = [item.replace('x', '') for item in payouts]

    if cleaned_payouts[0:4] != check_list[0:4]:
        previous_cleaned_payouts = cleaned_payouts
        check_list.insert(0, cleaned_payouts[0])
        if float(check_list[0]) > 1.10 and float(check_list[1]) == 1.00 and float(check_list[2]) == 1.00:# and float(check_list[4]) == 1.00:
            show_notification("Youre pattern is found, bet imediately:", f"Your pattern of: {check_list[0]} and {check_list[1]} and {check_list[2]}")
            # Update Bet Amount and place bet
            print(f"Round: {nums_of_checks}, odd: {check_list[0]}")
            second_odd_bet()
            update_bet_amount()
            place_bet()
            print(f"Current Balance: {get_balance()}")
            print(f"Bet Placed on Pattern 1, stake: {stake(get_balance())}")
            wins += 1
            new_data = {}
            new_data["odd"] = check_list[0]
            new_data["datetime"] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            new_data["round"] = nums_of_checks
            new_data["odd_bet_placed"] = "Next with Pattern 1"
            dict_list.append(new_data)
            with open(text_file, 'a') as file:
                file.write(f'{new_data}\n')


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
        nums_of_checks += 1
    if wins > 2:
        status = False
    if nums_of_checks > 30000:
        status = False


df = pd.DataFrame(dict_list)
df.to_csv(f"csv/SportPesa Aviator odds history {today_date}.csv", index=False)

time.sleep(10)
# Close the browser window
driver.quit()