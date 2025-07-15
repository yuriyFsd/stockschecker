from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os

# Set up Chrome options for headless mode
options = Options()
options.headless = True
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Optional: for Windows
options.add_argument("--window-size=1600,1500")  # Optional: set screenshot resolution

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def getGoogleFinScreen(ticker: str, output_folder: str) -> str:
    url = f"https://www.google.com/finance/quote/{ticker}:NASDAQ"
    driver.get(url)
    xpath = "//div[contains(@class, 'YMlKec fxKbKc')]"  # tag text to find correct part of the page
    element = driver.find_element(By.XPATH, xpath)
    # Save screenshot to a specific folder
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
    screenshot_path = os.path.join(output_folder, f"finGoogle_{ticker}.png")
    element.screenshot(screenshot_path)
    # element.screenshot(f"finGoogle_{ticker}.png")
    return output_folder

def getYahooFinScreen(ticker: str, output_folder: str) -> str:
    url = f"https://finance.yahoo.com/quote/{ticker}/analysis/"
    driver.get(url)
    xpath = "//article[contains(@class, 'gridLayout')]"# tag text to find correct part of the page
    element = driver.find_element(By.XPATH, xpath)
    # Save screenshot to a specific folder    
    driver.implicitly_wait(3)#pause for second to allow page to load
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
    screenshot_path = os.path.join(output_folder, f"finYahoo_{ticker}.png")
    element.screenshot(screenshot_path)
    # element.screenshot(f"finYahoo_{ticker}.png") 
    print(f"Screenshot saved to {screenshot_path}")
    return screenshot_path

def getScreenshots(tickers: list, output_folder: str):
    print(f"Processing {len(tickers)} tickers...")
    for ticker in tickers:
        try:
            print(f"Processing ticker: {ticker}")
            getYahooFinScreen(ticker, output_folder)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
    driver.quit()

def quitDriver():
    driver.quit()
# getYahooFinScreen('PLTR', './../screens')
# getScreenshots(['PLTR', 'AAPL', 'MSFT', 'BYRN'], 'results')

#exit(0)

# # Target URL
# url = "https://finance.yahoo.com/quote/PLTR/analysis/"
# driver.get(url)

# # Locate the element (e.g., by ID, class, tag, etc.)
# #element = driver.find_element(By.t, "article")
# element = driver.find_element(By.XPATH, "//article[contains(@class, 'gridLayout')]")

# # <article class="gridLayout yf-lqb5cj">

# # Save screenshot
# element.screenshot("element_screenshot.png")
# #screenshot_path = "screenshot.png"
# #driver.save_screenshot(screenshot_path)
# print(f"Screenshot saved to element_screenshot.png")

# # Clean up
# driver.quit()
