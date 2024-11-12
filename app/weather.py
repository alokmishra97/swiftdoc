from .scraper import TemperatureScraper

class WeatherService:
    def __init__(self, scraper: TemperatureScraper):
        self.scraper = scraper

    def get_temperature(self):
        try:
            # Get the current temperature from the scraper
            temp = self.scraper.fetch_temperature()
            return round(temp)  # Round the temperature to the nearest integer
        except Exception as e:
            raise ValueError(f"Error retrieving temperature: {e}")
