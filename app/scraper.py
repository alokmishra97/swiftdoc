import requests
from bs4 import BeautifulSoup


class TemperatureScraper:
    def __init__(self, url: str):
        self.url = url

    def fetch_temperature(self):
        # Send GET request to retrieve the page content
        response = requests.get(self.url)

        # Ensure the request was successful
        if response.status_code != 200:
            raise Exception("Failed to retrieve data from the website.")

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the element containing the temperature.
        temperature_element = soup.find('span', {'class': 'temp'})

        if not temperature_element:
            raise Exception("Could not find the temperature element on the page.")

        # Extract and clean the temperature value
        temperature = float(temperature_element.text.strip().replace('°C', '').replace(',', '.'))
        return temperature
