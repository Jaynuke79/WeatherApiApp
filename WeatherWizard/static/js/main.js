document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const weatherForm = document.getElementById('weatherForm');
    const cityInput = document.getElementById('cityInput');
    const citySuggestions = document.getElementById('citySuggestions');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    const weatherCard = document.getElementById('weatherCard');
    
    // Weather card elements
    const cityNameElement = document.getElementById('cityName');
    const coordinatesDisplay = document.getElementById('coordinatesDisplay');
    const weatherIcon = document.getElementById('weatherIcon');
    const weatherDescription = document.getElementById('weatherDescription');
    const temperatureElement = document.getElementById('temperature');
    const windSpeedElement = document.getElementById('windSpeed');
    const lastUpdatedElement = document.getElementById('lastUpdated');
    
    // Debounce function for autocomplete
    function debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
    
    // Function to get city suggestions
    const getSuggestions = debounce(async function(query) {
        if (!query || query.length < 2) {
            citySuggestions.innerHTML = '';
            citySuggestions.classList.add('d-none');
            return;
        }
        
        try {
            const response = await fetch(`/api/city/autocomplete?q=${encodeURIComponent(query)}`);
            if (!response.ok) throw new Error('Failed to fetch suggestions');
            
            const suggestions = await response.json();
            
            if (suggestions.length === 0) {
                citySuggestions.innerHTML = '';
                citySuggestions.classList.add('d-none');
                return;
            }
            
            citySuggestions.innerHTML = '';
            suggestions.forEach(suggestion => {
                const item = document.createElement('button');
                item.type = 'button';
                item.className = 'list-group-item list-group-item-action';
                item.textContent = suggestion;
                item.addEventListener('click', () => {
                    cityInput.value = suggestion;
                    citySuggestions.innerHTML = '';
                    citySuggestions.classList.add('d-none');
                    weatherForm.dispatchEvent(new Event('submit'));
                });
                citySuggestions.appendChild(item);
            });
            
            citySuggestions.classList.remove('d-none');
        } catch (error) {
            console.error('Error fetching city suggestions:', error);
        }
    }, 300);
    
    // Add event listener for city input
    cityInput.addEventListener('input', function() {
        getSuggestions(this.value);
    });
    
    // Hide suggestions when clicking outside
    document.addEventListener('click', function(event) {
        if (!cityInput.contains(event.target) && !citySuggestions.contains(event.target)) {
            citySuggestions.innerHTML = '';
            citySuggestions.classList.add('d-none');
        }
    });
    
    // Get weather icon based on description
    function getWeatherIcon(description) {
        const desc = description.toLowerCase();
        
        if (desc.includes('clear') || desc.includes('sunny')) {
            return '<i class="fas fa-sun text-warning"></i>';
        } else if (desc.includes('partly cloudy') || desc.includes('mainly clear')) {
            return '<i class="fas fa-cloud-sun text-warning"></i>';
        } else if (desc.includes('cloud') || desc.includes('overcast')) {
            return '<i class="fas fa-cloud text-secondary"></i>';
        } else if (desc.includes('drizzle') || desc.includes('light rain')) {
            return '<i class="fas fa-cloud-rain text-info"></i>';
        } else if (desc.includes('rain') || desc.includes('shower')) {
            return '<i class="fas fa-cloud-showers-heavy text-info"></i>';
        } else if (desc.includes('snow')) {
            return '<i class="fas fa-snowflake text-light"></i>';
        } else if (desc.includes('thunder')) {
            return '<i class="fas fa-bolt text-warning"></i>';
        } else if (desc.includes('fog')) {
            return '<i class="fas fa-smog text-secondary"></i>';
        } else {
            return '<i class="fas fa-cloud text-secondary"></i>';
        }
    }
    
    // Get background color class based on temperature
    function getTemperatureClass(temp) {
        if (temp <= 0) return 'bg-info';
        if (temp <= 10) return 'bg-primary';
        if (temp <= 20) return 'bg-success';
        if (temp <= 30) return 'bg-warning';
        return 'bg-danger';
    }
    
    // Submit event for weather form
    weatherForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const city = cityInput.value.trim();
        if (!city) return;
        
        // Clear previous results and show loading indicator
        weatherCard.classList.add('d-none');
        errorMessage.classList.add('d-none');
        loadingIndicator.classList.remove('d-none');
        
        try {
            const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch weather data');
            }
            
            // Update weather card with fetched data
            cityNameElement.textContent = data.city;
            coordinatesDisplay.textContent = `Lat: ${data.coordinates.lat.toFixed(4)}, Lon: ${data.coordinates.lon.toFixed(4)}`;
            weatherIcon.innerHTML = getWeatherIcon(data.description);
            weatherDescription.textContent = data.description;
            temperatureElement.textContent = `${data.temperature.toFixed(1)}°C`;
            windSpeedElement.textContent = `${data.windspeed.toFixed(1)} km/h`;
            
            // Set last updated time
            const now = new Date();
            lastUpdatedElement.textContent = now.toLocaleTimeString();
            
            // Apply temperature-based styling
            const headerClasses = ['bg-gradient', 'text-white'];
            weatherCard.querySelector('.card-header').className = 'card-header ' + headerClasses.join(' ') + ' ' + getTemperatureClass(data.temperature);
            
            // Show the weather card
            loadingIndicator.classList.add('d-none');
            weatherCard.classList.remove('d-none');
            
        } catch (error) {
            // Show error message
            loadingIndicator.classList.add('d-none');
            errorText.textContent = error.message;
            errorMessage.classList.remove('d-none');
            console.error('Error fetching weather:', error);
        }
    });
});
