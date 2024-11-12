import unittest
from unittest.mock import patch, MagicMock
from app.scraper import TemperatureScraper


class TestTemperatureScraper(unittest.TestCase):
    @patch('app.scraper.requests.get')
    def test_fetch_temperature_success(self, mock_get):
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'<html><span class="temp">18.3°C</span></html>'
        mock_get.return_value = mock_response

        scraper = TemperatureScraper('http://www.weerindelft.nl/')
        temperature = scraper.fetch_temperature()

        # Check if the temperature is correctly parsed
        self.assertEqual(temperature, 18.3)

    @patch('app.scraper.requests.get')
    def test_fetch_temperature_failure(self, mock_get):
        # Mock a failed HTTP request
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        scraper = TemperatureScraper('http://www.weerindelft.nl/')

        # Ensure that an exception is raised when HTTP request fails
        with self.assertRaises(Exception) as context:
            scraper.fetch_temperature()

        self.assertTrue('Failed to retrieve data from the website' in str(context.exception))

    @patch('app.scraper.requests.get')
    def test_parse_temperature_missing_element(self, mock_get):
        # Mock a valid HTTP response, but without the temperature element
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'<html><span>No Temperature Data</span></html>'
        mock_get.return_value = mock_response

        scraper = TemperatureScraper('http://www.weerindelft.nl/')

        # Ensure an exception is raised if the temperature element is missing
        with self.assertRaises(Exception) as context:
            scraper.fetch_temperature()

        self.assertTrue('Could not find the temperature element on the page' in str(context.exception))
