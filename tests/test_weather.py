import unittest
from unittest.mock import MagicMock
from app.weather import WeatherService
from app.scraper import TemperatureScraper


class TestWeatherService(unittest.TestCase):
    def test_get_temperature_success(self):
        # Mock the scraper to return a fixed temperature
        mock_scraper = MagicMock(TemperatureScraper)
        mock_scraper.fetch_temperature.return_value = 18.3

        weather_service = WeatherService(mock_scraper)
        temperature = weather_service.get_temperature()

        # Check if the temperature is rounded correctly
        self.assertEqual(temperature, 18)

    def test_get_temperature_failure(self):
        # Mock the scraper to raise an exception
        mock_scraper = MagicMock(TemperatureScraper)
        mock_scraper.fetch_temperature.side_effect = Exception("Failed to fetch temperature")

        weather_service = WeatherService(mock_scraper)

        # Ensure that an exception is raised
        with self.assertRaises(ValueError) as context:
            weather_service.get_temperature()

        self.assertTrue("Error retrieving temperature" in str(context.exception))
