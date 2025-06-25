import os
import logging
from flask import (Flask, render_template, request, jsonify, Response,
                   make_response)
from typing import Any, Dict, List
from weather.manager import WeatherManager

# Create Flask app
app: Flask = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Initialize weather manager
weather_manager: WeatherManager = WeatherManager()


@app.errorhandler(404)
def not_found(e):  # type: ignore
    if request.accept_mimetypes.accept_json and \
       not request.accept_mimetypes.accept_html:
        return jsonify(error="Not found"), 404
    return render_template("index.html"), 404  # pragma: no cover


@app.errorhandler(500)
def internal_error(e):  # type: ignore
    if request.accept_mimetypes.accept_json and \
       not request.accept_mimetypes.accept_html:  # pragma: no cover
        return jsonify(error="Internal server error"), 500  # pragma: no cover
    return render_template("index.html"), 500  # pragma: no cover


@app.route('/')
def index() -> str:
    """Render the main page of the application."""
    return render_template('index.html')  # pragma: no cover


@app.route('/api/weather', methods=['GET'])
def get_weather() -> Response:
    """API endpoint to get weather data for a city."""
    try:
        # Get city from query parameters
        city: str = request.args.get('city', '')
        if not city:
            return make_response(jsonify({'error': 'City is required'}), 400)

        # Get coordinates for the city
        lat, lon = weather_manager.geocode_city(city)

        # Fetch weather data
        weather = weather_manager.fetch(lat, lon)  # type: Any

        # Return weather data as JSON
        return make_response(jsonify({
            'temperature': weather.temperature,
            'windspeed': weather.windspeed,
            'description': weather.description,
            'city': city,
            'coordinates': {'lat': lat, 'lon': lon}
        }), 200)
    except ValueError as e:
        logging.error(f"Value error: {str(e)}")
        return make_response(jsonify({'error': str(e)}), 404)
    except Exception as e:
        logging.error(f"Error fetching weather: {str(e)}")
        return make_response(
            jsonify({'error': 'Weather data fetch failed'}),
            500)


@app.route('/api/city/autocomplete', methods=['GET'])
def autocomplete_city() -> Response:
    """API endpoint for city name autocomplete."""
    try:
        # Get query from request parameters
        query: str = request.args.get('q', '')
        if not query or len(query) < 2:
            return make_response(jsonify([]), 200)

        # Use the geocoding API to get city suggestions
        import requests
        from weather.funcs import GEOCODE_URL

        params: Dict[str, Any] = {
            "name": query,
            "count": 5,  # Limit to 5 suggestions
            "format": "json"
        }

        response = requests.get(GEOCODE_URL, params=params)
        response.raise_for_status()

        results: List[Dict[str, Any]] = response.json().get("results", [])

        # Format the results for autocomplete
        suggestions: List[str] = []
        for result in results:
            city_name: str = result.get("name", "")
            country: str = result.get("country", "")
            suggestion: str = f"{city_name}, {country}"
            suggestions.append(suggestion)

        return make_response(jsonify(suggestions), 200)
    except Exception as e:
        logging.error(f"Error in autocomplete: {str(e)}")
        return make_response(jsonify([]), 500)
