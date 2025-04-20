class AQICalculator:
    """
    Calculates Air Quality Index (AQI) based on company inputs.
    Uses a weighted formula to determine pollution levels.
    """
    
    # Weights for the AQI calculation
    W1 = 0.3  # Energy consumption weight
    W2 = 0.25  # Fuel type weight
    W3 = 0.2  # Waste emissions weight
    W4 = 0.15  # Vehicles operated weight
    W5 = 0.05  # Wind speed weight
    W6 = 0.05  # Rainfall weight
    
    # Fuel type factors (higher values indicate more polluting fuels)
    FUEL_FACTORS = {
        'Coal': 1.5,
        'Diesel': 1.2,
        'Gas': 1.0,
        'Renewable': 0.5
    }
    
    # AQI categories
    AQI_CATEGORIES = {
        (0, 50): 'Green',
        (51, 100): 'Good',
        (101, 150): 'Average',
        (151, float('inf')): 'Poor'
    }
    
    # Points awarded by category (for leaderboard)
    POINTS_BY_CATEGORY = {
        'Green': 100,
        'Good': 75,
        'Average': 50,
        'Poor': 25
    }
    
    @classmethod
    def calculate_aqi(cls, energy_consumption, fuel_type, waste_emissions, 
                     vehicles_operated, wind_speed, rainfall):
        """
        Calculate AQI score based on the weighted formula:
        AQI = (W1 × Energy) + (W2 × FuelFactor) + (W3 × WasteEmissions) + 
              (W4 × Vehicles) − (W5 × WindSpeed) − (W6 × Rainfall)
        """
        # Normalize inputs (higher values mean more pollution)
        energy_norm = min(energy_consumption / 1000, 10)  # Normalize to 0-10 range
        fuel_factor = cls.FUEL_FACTORS.get(fuel_type, 1.0)
        waste_norm = min(waste_emissions / 10, 10)  # Normalize to 0-10 range
        vehicles_norm = min(vehicles_operated / 100, 10)  # Normalize to 0-10 range
        
        # Environmental factors (higher values mean less pollution)
        wind_norm = min(wind_speed / 10, 1)  # Normalize to 0-1 range
        rainfall_norm = min(rainfall / 50, 1)  # Normalize to 0-1 range
        
        # Calculate AQI
        aqi = (cls.W1 * energy_norm) + \
              (cls.W2 * fuel_factor * 10) + \
              (cls.W3 * waste_norm) + \
              (cls.W4 * vehicles_norm) - \
              (cls.W5 * wind_norm * 100) - \
              (cls.W6 * rainfall_norm * 100)
        
        # Ensure AQI is positive
        aqi = max(0, aqi)
        
        # Get category
        category = cls.get_category(aqi)
        
        # Get points
        points = cls.POINTS_BY_CATEGORY.get(category, 0)
        
        return {
            'aqi_score': round(aqi, 2),
            'category': category,
            'points': points
        }
    
    @classmethod
    def get_category(cls, aqi):
        """Determine the AQI category based on the score"""
        for (min_val, max_val), category in cls.AQI_CATEGORIES.items():
            if min_val <= aqi <= max_val:
                return category
        
        # Default fallback
        return 'Poor'
