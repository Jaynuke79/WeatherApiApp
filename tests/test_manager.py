import unittest
from unittest.mock import patch
from WeatherWizard.weather.manager import WeatherManager


class TestWeatherManager(unittest.TestCase):

    def setUp(self):
        self.manager = WeatherManager()

    def test_get_weather_description_boundary(self):
        self.assertEqual(self.manager._get_weather_description(-1), "Unknown")
        self.assertEqual(self.manager._get_weather_description(10000), "Unknown")

    @patch("WeatherWizard.weather.manager.requests.get")
    def test_geocode_city_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            "results": [{"latitude": 10.0, "longitude": 20.0}]
        }
        mock_get.return_value.raise_for_status = lambda: None
        lat, lon = self.manager.geocode_city("London")
        self.assertEqual((lat, lon), (10.0, 20.0))

    @patch("WeatherWizard.weather.manager.requests.get")
    def test_geocode_city_no_results(self, mock_get):
        mock_get.return_value.json.return_value = {"results": []}
        mock_get.return_value.raise_for_status = lambda: None
        with self.assertRaises(ValueError):
            self.manager.geocode_city("Atlantis")

    @patch("WeatherWizard.weather.manager.requests.get")
    def test_fetch_weather_and_description(self, mock_get):
        mock_get.return_value.json.return_value = {
            "current_weather": {
                "temperature": 13.4,
                "windspeed": 3.2,
                "weathercode": 65  # should map to Heavy rain
            }
        }
        mock_get.return_value.raise_for_status = lambda: None
        weather = self.manager.fetch()
        self.assertEqual(weather.temperature, 13.4)
        self.assertEqual(weather.windspeed, 3.2)
        self.assertEqual(weather.description, "Heavy rain")

    def test_get_weather_description_all_known_codes(self):
        known_codes = [
            0, 1, 2, 3, 45, 48, 51, 53, 55, 56, 57,
            61, 63, 65, 66, 67, 71, 73, 75, 77,
            80, 81, 82, 85, 86, 95, 96, 99
        ]
        for code in known_codes:
            desc = self.manager._get_weather_description(code)
            self.assertIsInstance(desc, str)
            self.assertNotEqual(desc, "Unknown")

    def test_get_weather_description_unknown_code(self):
        self.assertEqual(self.manager._get_weather_description(999), "Unknown")


if __name__ == "__main__":
    unittest.main()
