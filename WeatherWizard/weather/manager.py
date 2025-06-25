import requests
from typing import Optional, Tuple
from weather.weather import Weather
from weather.funcs import LATITUDE, LONGITUDE, BASE_URL, GEOCODE_URL


class WeatherManager:
    """
    Singleton class to handle weather data fetching from the API.
    Ensures only one instance manages all weather retrievals.
    """

    _instance: Optional['WeatherManager'] = None

    def __new__(cls) -> 'WeatherManager':
        # Implementing singleton pattern to ensure only one instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def geocode_city(self, city_name: str) -> Tuple[float, float]:
        """
        Given a city name, return a tuple of (latitude, longitude)
        using Open-Meteo's geocoding API.
        """
        params: dict[str, str | int] = {
            "name": city_name,
            "count": 1,
            "format": "json"
        }
        response = requests.get(GEOCODE_URL, params=params)
        response.raise_for_status()
        results = response.json().get("results")

        if not results:
            raise ValueError(f"No coordinates found for city: {city_name}")

        lat: float = results[0].get("latitude", LATITUDE)
        lon: float = results[0].get("longitude", LONGITUDE)
        return lat, lon

    def fetch(self, lat: float = LATITUDE, lon: float = LONGITUDE) -> Weather:
        # Prepare query parameters for the API call
        params: dict[str, float | bool] = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }
        # Send the GET request to the weather API
        response = requests.get(BASE_URL, params=params)
        # Raise an exception for bad HTTP status codes
        response.raise_for_status()
        # Extract current weather data safely
        weather_data: dict[str, float] = response.json().get(
            "current_weather", {})

        # Get weather code to determine description
        weather_code = weather_data.get("weathercode", 0)
        description = self._get_weather_description(int(weather_code))

        # Return a Weather object with extracted or default values
        return Weather(
            temperature=weather_data.get("temperature", 0.0),
            windspeed=weather_data.get("windspeed", 0.0),
            description=description
        )

    def _get_weather_description(self, code: int) -> str:
        """
        Translate weather code to human-readable description.
        Based on WMO Weather interpretation codes (WW)
        https://open-meteo.com/en/docs
        """
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }

        return weather_codes.get(code, "Unknown")
