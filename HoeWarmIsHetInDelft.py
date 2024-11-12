from app.weather import WeatherService
from app.scraper import TemperatureScraper

def main():
    # URL of the weather site
    url = 'http://www.weerindelft.nl/'

    # Instantiate scraper and weather service
    scraper = TemperatureScraper(url)
    weather_service = WeatherService(scraper)

    try:
        temperature = weather_service.get_temperature()
        print(f"{temperature} degrees Celcius")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
