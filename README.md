# Aviator APP
## Automated Aviator Odds Collection Bet Placement and Prediction
This is a Python script for collecting Aviator odds.
## Overview
This project aims to automate the collection of betting odds from various sports betting websites and prepare data for future predictive modeling. The scripts are designed to scrape odds from specific websites (sportpesa.com, betika.co.ke, 1xbet.co.ke) using Python, Selenium, and multiprocessing for parallel processing. The collected data is saved into Pandas DataFrames for further analysis and training predictive models.

## Features
- Automated collection of betting odds from multiple websites.
- Parallel processing for enhanced efficiency.
- Data saved into Pandas DataFrames for future use.
- Flexibility to accommodate website layout changes.

## Setup
1. Clone the repository:
```
git clone https://github.com/roochieng/aviator.git
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Ensure you have the necessary drivers (e.g., ChromeDriver) installed and configured.

## Usage
1. Navigate to the directory of the specific script you want to run (e.g., sportpesa_script, betika_script, 1xbet_script).
2. Run the script:
```
python script_name.py
```
3. The script will launch the browser, scrape the odds, and save the data into a Pandas DataFrame.

# Development Report
1. ### Successes:
  - Successfully developed Python scripts for automated odds collection.
  - Implemented parallel processing to enhance efficiency.
  - Data saved into Pandas DataFrame for future use.
2. ### Challenges:
  - Overcoming website layout changes affecting web scraping.
  - Ensuring script robustness and stability.
  - Handling authentication and security measures on betting websites.
3. ### Areas for Improvement:
  - Refining error handling and logging mechanisms.
  - Enhancing scalability for additional betting websites.
  - Improving data preprocessing for better model training.

4. ### Lessons Learned:
  - Importance of flexibility in web scraping scripts.
  - Collaboration and communication are crucial for a multi-team member project.
  - Continuous monitoring and adaptation to website changes are essential.
5. ## Next Steps
  - Utilize collected data to train predictive models for betting odds.
  - Implement machine learning algorithms for odds prediction.
  - Expand data collection to include more betting websites and sports.
  - Regular updates and maintenance to accommodate website changes.

## Contributions
Contributions are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue or submit a pull request.



### Notice

- **This is not to promote gambling**
- **I am trying to improve my data science knowledge.**
- **Nobody should use this as an investment advice or guide.**
