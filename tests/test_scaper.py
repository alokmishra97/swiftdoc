import unittest
from unittest.mock import patch, MagicMock
from app.scraper import TemperatureScraper


class TestTemperatureScraper(unittest.TestCase):

    @patch('selenium.webdriver.Chrome')  # Mock the Chrome WebDriver
    def test_fetch_temperature_success(self, MockWebDriver):
        # Create a mock driver instance
        mock_driver = MagicMock()
        MockWebDriver.return_value = mock_driver

        
        mock_driver.get.return_value = None 
        mock_driver.find_element.return_value = MagicMock()  # Mock the element

        
        mock_wait = MagicMock()
        mock_wait.until.return_value = MagicMock(text="20.5°C")  
        mock_driver.switch_to.frame.return_value = None  

        # Create an instance of the scraper
        scraper = TemperatureScraper(url="http://www.weerindelft.nl/")

        # Call the fetch_temperature method
        temperature = scraper.fetch_temperature()

        # Assert the temperature is correctly parsed
        self.assertEqual(temperature, 20.5) 
        mock_driver.quit.assert_called_once()  

    @patch('selenium.webdriver.Chrome')  
    def test_fetch_temperature_with_iframe(self, MockWebDriver):
        
        mock_driver = MagicMock()
        MockWebDriver.return_value = mock_driver

       
        mock_driver.get.return_value = None  # Don't actually navigate to a URL
        mock_driver.find_element.return_value = MagicMock()  # Mock the element

        
        iframe_mock = MagicMock()
        mock_driver.find_element.return_value = iframe_mock  # Return iframe mock

        
        mock_wait = MagicMock()
        mock_wait.until.return_value = MagicMock(text="22.0°C")  # Simulate the text of the temperature element
        mock_driver.switch_to.frame.return_value = None  # Mock the iframe switching

        
        scraper = TemperatureScraper(url="http://www.weerindelft.nl/")

        
        temperature = scraper.fetch_temperature()

       
        self.assertEqual(temperature, 22.0)  
        mock_driver.switch_to.frame.assert_called_once()  
        mock_driver.quit.assert_called_once()  

    @patch('selenium.webdriver.Chrome')  
    def test_fetch_temperature_failure(self, MockWebDriver):
        # Create a mock driver instance
        mock_driver = MagicMock()
        MockWebDriver.return_value = mock_driver

        # Simulate failure: WebDriver can't find the temperature element
        mock_driver.get.return_value = None  
        mock_driver.find_element.side_effect = Exception(
            "Element not found")  # Force an exception when finding elements

        
        scraper = TemperatureScraper(url="http://www.weerindelft.nl/")

        # Test that an exception is raised when the element can't be found
        with self.assertRaises(Exception) as context:
            scraper.fetch_temperature()

        self.assertTrue(
            "Error retrieving temperature" in str(context.exception))  # Check if the correct error message was raised
        mock_driver.quit.assert_called_once()  # Ensure the browser is closed even on failure

