"""Weather CLI App using OOP, JSON, and API with Singleton Pattern."""


class Weather:
    """Encapsulates weather details such as temperature, windspeed,
    and a textual description."""

    def __init__(self, temperature: float,
                 windspeed: float,
                 description: str) -> None:
        # All attributes are private and accessed through properties
        self._temperature: float = temperature
        self._windspeed: float = windspeed
        self._description: str = description

    @property
    def temperature(self) -> float:
        # Getter for temperature
        return self._temperature

    @property
    def windspeed(self) -> float:
        # Getter for windspeed
        return self._windspeed

    @property
    def description(self) -> str:
        # Getter for weather description
        return self._description
