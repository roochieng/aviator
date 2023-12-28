from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
from pandas import read_csv



load_dotenv()

url = os.environ.get('URL')

# Set the path to your ChromeDriver executable
chrome_driver_path = "E:/Development/chromedriver-win64/chromedriver.exe"

# Create Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")

# You can add additional options if needed, e.g., headless mode
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

# Enter your login credentials
username_field.send_keys(os.environ.get('PASSWORD'))
password_field.send_keys(os.environ.get('USERNAME'))

# Submit the login form
login_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.session__form__button')))
login_button.click()
# JavaScript click on the login button
# driver.execute_script("arguments[0].click();", login_button)

# Wait for the dynamic content to load using WebDriverWait
wait = WebDriverWait(driver, timeout=20)
time.sleep(20)
# Print the page source
# print(driver.page_source) 
## Use XPath to navigate through intervening elements
wait = WebDriverWait(driver, 20)
iframe = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="betika-fasta-container"]/iframe')))

check_list = [0]
odds_dict = {}
text_file = "history.txt"

nums_of_checks = 0
status = True

while status:
    # Switch to the iframe
    driver.switch_to.frame(iframe)
    payouts = driver.find_element(By.XPATH, '//div[@class="result-history disabled-on-game-focused my-2"]')
    payouts = payouts.text.split("\n")
    cleaned_payouts = [item.replace('x', '') for item in payouts]
    if cleaned_payouts[0] != check_list[0]:
        check_list.insert(0, cleaned_payouts[0])
        odds_dict["odd"] = cleaned_payouts[0]
        odds_dict["datetime"] = datetime.now()
        nums_of_checks += 1
    if nums_of_checks == 1000:
        status = False
    print(nums_of_checks)

print(odds_dict)

# Append the items to the existing text file
with open(text_file, 'a') as file:
    for item in check_list:
        file.write(f'{item}\n')


today_date = datetime.today().strftime('%Y-%m-%d')
df = pd.DataFrame({'odd': [odds_dict['odd']], 'datetime': [odds_dict['datetime']]})
df.to_csv(f"Aviator odds history {today_date}.csv", index=False)

print(check_list)
print(odds_dict)
# Close the browser window
driver.quit()
