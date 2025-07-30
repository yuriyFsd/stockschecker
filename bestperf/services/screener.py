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

def initDriver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def quitDriver(driver):
    driver.quit()

def getGoogleFinChartScreen(driver, ticker: str, StEx: str, output_folder: str) -> str:
    # options.add_argument("--window-size=1300,1250")  # Increase width to allow cropping
    elementOfFinancials = proceedGoogleFin(driver, ticker, StEx)
    if not elementOfFinancials:
        return None
    left_offset = 100
    right_offset = 100
    height = (getPixelYPositionOfElement(elementOfFinancials)) or 1000

    driver.set_window_size(1300, height)

    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
    screenshot_path = os.path.join(output_folder, f"finChartGoogle_{ticker}.png")
    driver.save_screenshot(screenshot_path)
    img = Image.open(screenshot_path)
    cropped_img = img.crop((left_offset, 0, img.width-right_offset, img.height))
    cropped_img.save(screenshot_path)
    # element.screenshot(f"finGoogle_{ticker}.png")
    return screenshot_path

def getGoogleFinScreen(driver, ticker: str, StEx: str, output_folder: str) -> str:
    elementOfFinancials = proceedGoogleFin(driver, ticker, StEx)
    if not elementOfFinancials:
        return None
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
    return screenshot_path

def proceedGoogleFin(driver, ticker: str, StEx: str):
    url = f"https://www.google.com/finance/quote/{ticker}:{StEx}?window=5D"
    driver.get(url)
    elementOfFinancials = findElementByTagAndText(driver, 'div', 'Financials')
    if not elementOfFinancials:
        return None
    return elementOfFinancials

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
        print(f"For '{driver.current_url}' element with tag '{tag}' and text '{text}' not found.")
        return None
        # raise Exception

def getPixelYPositionOfElement(element) -> int:
    location = element.location
    y = location['y']
    size = element.size
    # x = location['x']
    # width = size['width']
    # height = size['height']
    return y

# Example usage
# driver = initDriver()
# getGoogleFinChartScreen(driver, 'KINS', 'NASDAQ', './../screens')
# getGoogleFinScreen(driver, 'KINS', 'NASDAQ', './../screens')
# quitDriver()

def getYahooFinScreen(driver, ticker: str, output_folder: str) -> str:
    driver.set_window_size(1600, 1500)
    url = f"https://finance.yahoo.com/quote/{ticker}/analysis/"
    driver.get(url)
    time.sleep(5) 
    xpath = "//article[contains(@class, 'gridLayout')]"# tag text to find correct part of the page
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
    screenshot_path = os.path.join(output_folder, f"finYahoo_{ticker}.png")
    try:
        element = driver.find_element(By.XPATH, xpath)
        element.screenshot(screenshot_path)
    except Exception as e:
        driver.save_screenshot(screenshot_path)
        
    # driver.implicitly_wait(3)#pause for second to allow page to load
    
    print(f"Screenshot saved to {screenshot_path}")
    return screenshot_path

def getScreenshots(tickers: list, output_folder: str):#not used
    print(f"Processing {len(tickers)} tickers...")
    for ticker in tickers:
        try:
            print(f"Processing ticker: {ticker}")
            getYahooFinScreen(ticker, output_folder)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
