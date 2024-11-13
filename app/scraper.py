from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


class TemperatureScraper:
    def __init__(self, url: str):
        self.url = url

    def fetch_temperature(self):
        # Setup WebDriver for Selenium 
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode (no UI)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Navigate to the page
        driver.get(self.url)

        # Switch to iframe as the temperature element is inside an iframe
        try:
            # Find iframe element
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(iframe)
            print("Switched to iframe.")
        except Exception as e:
            print("No iframe found or switching to iframe failed.")

        try:
            # Wait up to 20 seconds for the temperature element to be visible
            print("Waiting for temperature element...")
            temperature_element = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.ID, "ajaxtemp"))
            )
            print("Temperature element found!")

            # Extract and clean the temperature value
            temperature = float(temperature_element.text.strip().replace('°C', '').replace(',', '.'))

        except Exception as e:
            driver.quit()
            raise Exception(f"Error retrieving temperature: {e}")

        driver.quit()  # Close the browser
        return temperature

