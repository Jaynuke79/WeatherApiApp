import unittest
from WeatherWizard.weather.weather import Weather
from hypothesis import given
from hypothesis.strategies import floats, text


class TestWeather(unittest.TestCase):

    @given(floats(allow_nan=False), floats(allow_nan=False), text())
    def test_weather_properties(self, temp, wind, desc):
        weather = Weather(temp, wind, desc)
        self.assertEqual(weather.temperature, temp)
        self.assertEqual(weather.windspeed, wind)
        self.assertEqual(weather.description, desc)
    
    @given(floats(allow_nan=False), floats(allow_nan=False), text())
    def test_weather_properties(self, temp, wind, desc):
        weather = Weather(temp, wind, desc)
        self.assertEqual(weather.temperature, temp)
        self.assertEqual(weather.windspeed, wind)
        self.assertEqual(weather.description, desc)
        self.assertIsInstance(str(weather), str)  # exercise __str__ or representation



if __name__ == "__main__":
    unittest.main()
