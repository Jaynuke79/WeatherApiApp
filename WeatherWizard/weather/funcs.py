from typing import Final
from rich.console import Console

# Initialize the Rich console for pretty CLI output
console: Final[Console] = Console()

# Constants for the API and default coordinates (New York City)
BASE_URL: Final[str] = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL: Final[str] = "https://geocoding-api.open-meteo.com/v1/search"
LATITUDE: Final[float] = 40.7128
LONGITUDE: Final[float] = -74.0060
