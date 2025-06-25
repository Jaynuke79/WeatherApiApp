import unittest
from unittest.mock import patch
from WeatherWizard.app import app


class TestWeatherAPI(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    # --- /api/weather Tests ---

    @patch("WeatherWizard.app.weather_manager.fetch")
    @patch("WeatherWizard.app.weather_manager.geocode_city")
    def test_get_weather_success(self, mock_geocode, mock_fetch):
        mock_geocode.return_value = (40.0, -74.0)
        mock_fetch.return_value = type("Weather", (), {
            "temperature": 22.0,
            "windspeed": 5.5,
            "description": "Clear sky"
        })()
        response = self.client.get("/api/weather?city=Berlin")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["temperature"], 22.0)
        self.assertEqual(data["windspeed"], 5.5)
        self.assertEqual(data["description"], "Clear sky")
        self.assertEqual(data["city"], "Berlin")

    def test_get_weather_missing_city_param(self):
        response = self.client.get("/api/weather")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "City is required")

    @patch("WeatherWizard.app.weather_manager.geocode_city", side_effect=ValueError("City not found"))
    def test_get_weather_city_not_found(self, mock_geocode):
        response = self.client.get("/api/weather?city=InvalidCity")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())

    @patch("WeatherWizard.app.weather_manager.geocode_city", side_effect=Exception("Unexpected API failure"))
    def test_get_weather_server_error(self, mock_geocode):
        response = self.client.get("/api/weather?city=Denver")
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.get_json())

    # --- /api/city/autocomplete Tests ---

    @patch("requests.get")
    def test_autocomplete_success(self, mock_requests_get):
        mock_requests_get.return_value.raise_for_status = lambda: None
        mock_requests_get.return_value.json.return_value = {
            "results": [
                {"name": "Berlin", "country": "Germany"},
                {"name": "Berkeley", "country": "USA"}
            ]
        }
        response = self.client.get("/api/city/autocomplete?q=ber")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, ["Berlin, Germany", "Berkeley, USA"])

    def test_autocomplete_too_short_query(self):
        response = self.client.get("/api/city/autocomplete?q=a")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    @patch("requests.get", side_effect=Exception("Autocomplete API crashed"))
    def test_autocomplete_server_error(self, mock_get):
        response = self.client.get("/api/city/autocomplete?q=denver")
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), [])

    # --- Error Handler Routes ---

    def test_404_handler_returns_json(self):
        response = self.client.get("/nonexistent-route", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json())
        self.assertEqual(response.get_json()["error"], "Not found")


    def test_500_handler_returns_json(self):
        with patch("requests.get", side_effect=Exception("Boom")):
            response = self.client.get("/api/city/autocomplete?q=denver")
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.get_json(), [])


if __name__ == "__main__":
    unittest.main()
