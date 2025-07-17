from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time

# Set up Chrome options for headless mode
options = Options()
options.headless = True
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Optional: for Windows
# Remove window-size from global options, set per function

# Initialize the WebDriver
def initDriver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def quitDriver():
    driver.quit()

def getGoogleFinChartScreen(driver, ticker: str, StEx: str, output_folder: str) -> str:
    # options.add_argument("--window-size=1300,1250")  # Increase width to allow cropping
    url = f"https://www.google.com/finance/quote/{ticker}:{StEx}?window=5D"
    driver.get(url)
    elementOfFinancials = findElementByTagAndText(driver, 'div', 'Financials')
    left_offset = 100
    right_offset = 100
    height = (getPixelYPositionOfElement(elementOfFinancials)) or 1000
    #options.add_argument(f"--window-size=1300,{height}")  # Set window size for the screenshot
    # xpath = "//div[@role='heading' and @aria-level='1' and contains(text(), 'Palantir Technologies Inc')]"
    # To update the window size after the driver is created, use:
    driver.set_window_size(1300, height)
    # element = driver.find_element(By.XPATH, xpath)

    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
    screenshot_path = os.path.join(output_folder, f"finChartGoogle_{ticker}.png")
    driver.save_screenshot(screenshot_path)
    img = Image.open(screenshot_path)
    cropped_img = img.crop((left_offset, 0, img.width-right_offset, img.height))
    cropped_img.save(screenshot_path)
    # element.screenshot(f"finGoogle_{ticker}.png")
    return output_folder

def getGoogleFinScreen(driver, ticker: str, StEx: str, output_folder: str) -> str:
    # options.add_argument("--window-size=1300,2700")  # Increase width to allow cropping
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f"https://www.google.com/finance/quote/{ticker}:{StEx}?window=5D"
    driver.get(url)
    elementOfFinancials = findElementByTagAndText(driver, 'div', 'Financials')
    left_offset = 100
    right_offset = 100
    top_offset = getPixelYPositionOfElement(elementOfFinancials) or 1000
    driver.set_window_size(1300, 2700)
    mouseClickOnBalanceSheetTag(driver)
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
    screenshot_path = os.path.join(output_folder, f"finGoogle_{ticker}.png")
    driver.save_screenshot(screenshot_path)
    img = Image.open(screenshot_path)
    cropped_img = img.crop((left_offset, top_offset, img.width-right_offset, img.height))
    cropped_img.save(screenshot_path)
    return output_folder

def mouseClickOnBalanceSheetTag(driver):
    print("Clicking on Balance Sheet tag...")
    xpath = "//span[contains(text(), 'Balance Sheet')]"
    
    element = driver.find_element(By.XPATH, xpath)
    parentDivOfElement = element.find_element(By.XPATH, '..')
    parentDivOfElement.click()
    pause = 5  # seconds
    time.sleep(pause)  # Wait for the page to load

def findElementByTagAndText(driver, tag: str, text: str):
    # Make both sides lowercase for case-insensitive matching
    xpath = (
        f"//{tag}[contains(translate(text(), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), "
        f"'{text.lower()}')]"
    )
    elements = driver.find_elements(By.XPATH, xpath)
    if elements:
        print(f"Found {len(elements)} elements with tag '{tag}' and text '{text}'.")
        return elements[0]
    else:
        raise Exception(f"Element with tag '{tag}' and text '{text}' not found.")

def getPixelYPositionOfElement(element) -> int:
    location = element.location
    size = element.size
    x = location['x']
    y = location['y']
    width = size['width']
    height = size['height']
    print(f"Element position: x={x}, y={y}, width={width}, height={height}")
    return y

driver = initDriver()
getGoogleFinChartScreen(driver, 'GE', 'NYSE', './../screens')
getGoogleFinScreen(driver, 'GE', 'NYSE', './../screens')
quitDriver()

def getYahooFinScreen(ticker: str, output_folder: str) -> str:
    options.add_argument("--window-size=1600,1500")  # Optional: set screenshot resolution
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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
