import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from app.scraper import TemperatureScraper


class TestTemperatureScraper(unittest.TestCase):

    @patch('swiftdoc.app.scraper.webdriver.Chrome')  # Mock the Chrome WebDriver
    @patch('swiftdoc.app.scraper.WebDriverWait')  # Mock WebDriverWait
    @patch('swiftdoc.app.scraper.Service')  # Mock the Service class
    def test_fetch_temperature(self, MockService, MockWebDriverWait, MockChrome):
        # Arrange
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.text = "15.5°C"  # Simulate the temperature text

        # Set up what the mocked WebDriver should return
        MockChrome.return_value = mock_driver
        mock_driver.find_element.return_value = mock_element
        MockWebDriverWait.return_value.until.return_value = mock_element  # Simulate WebDriverWait

        mock_driver.switch_to.frame = MagicMock()

        MockService.return_value = MagicMock()

        # URL to be tested
        url = "http://example.com"
        scraper = TemperatureScraper(url)

        # Act
        temperature = scraper.fetch_temperature()

        # Assert
        mock_driver.quit.assert_called_once()  # Ensure driver.quit() is called
        mock_driver.find_element.assert_called_with(By.TAG_NAME, "iframe")
        self.assertEqual(temperature, 15.5)  # Check if the temperature extracted is correct

    @patch('swiftdoc.app.scraper.webdriver.Chrome')  # Mock the Chrome WebDriver
    @patch('swiftdoc.app.scraper.WebDriverWait')  # Mock WebDriverWait
    def test_fetch_temperature_no_iframe(self, MockWebDriverWait, MockChrome):
        # Arrange
        mock_driver = MagicMock()
        mock_element = MagicMock()
        mock_element.text = "20°C"  # Simulate the temperature text

        MockChrome.return_value = mock_driver
        mock_driver.find_element.return_value = mock_element
        MockWebDriverWait.return_value.until.return_value = mock_element  # Simulate WebDriverWait

        mock_driver.switch_to.frame = MagicMock()
        mock_driver.find_element.side_effect = Exception("No iframe found")  # Simulate no iframe found error

        url = "http://example.com"
        scraper = TemperatureScraper(url)

        # Act & Assert
        with self.assertLogs(level='INFO') as log:
            temperature = scraper.fetch_temperature()
            self.assertEqual(temperature, 20)  # Temperature should be extracted correctly without iframe
            self.assertNotIn("No iframe found or switching to iframe failed.", log.output[0])

    @patch('swiftdoc.app.scraper.webdriver.Chrome')  # Mock the Chrome WebDriver
    @patch('swiftdoc.app.scraper.WebDriverWait')  # Mock WebDriverWait
    def test_fetch_temperature_element_not_found(self, MockWebDriverWait, MockChrome):
        # Arrange
        mock_driver = MagicMock()
        mock_driver.find_element.return_value = None  # Simulate no element found

        MockChrome.return_value = mock_driver
        MockWebDriverWait.return_value.until.side_effect = Exception("Timeout waiting for element")

        url = "http://example.com"
        scraper = TemperatureScraper(url)

        # Act & Assert
        with self.assertRaises(Exception) as context:
            scraper.fetch_temperature()

        self.assertTrue('Error retrieving temperature' in str(context.exception))  # Ensure the exception is raised



