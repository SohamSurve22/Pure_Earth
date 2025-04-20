class AQICalculator:
    """
    Calculates Air Quality Index (AQI) based on company inputs.
    Uses a weighted formula to determine pollution levels.
    """
    
    # Weights for the AQI formula
    W1 = 0.3  # Energy consumption weight
    W2 = 0.25  # Fuel type weight
    W3 = 0.2  # Waste emissions weight
    W4 = 0.15  # Vehicles operated weight
    W5 = 0.05  # Wind speed weight
    W6 = 0.05  # Rainfall weight
    
    # Fuel factors by type
    FUEL_FACTORS = {
        'Coal': 1.5,
        'Diesel': 1.2,
        'Gas': 1.0,
        'Renewable': 0.5
    }
    
    # AQI Categories
    AQI_CATEGORIES = {
        (0, 50): 'Green',
        (51, 100): 'Good',
        (101, 150): 'Average',
        (151, float('inf')): 'Poor'
    }
    
    # Points allocation by AQI category
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
        # Normalize values to ensure the scale is reasonable
        normalized_energy = energy_consumption / 100  # Assuming average is around 1000 kWh
        fuel_factor = cls.FUEL_FACTORS.get(fuel_type, 1.0)
        normalized_waste = waste_emissions * 10  # Scale up for better visibility
        normalized_vehicles = vehicles_operated / 10  # Scale down for balance
        
        # Calculate AQI using the formula
        aqi = (cls.W1 * normalized_energy) + \
              (cls.W2 * fuel_factor) + \
              (cls.W3 * normalized_waste) + \
              (cls.W4 * normalized_vehicles) - \
              (cls.W5 * wind_speed) - \
              (cls.W6 * rainfall)
        
        # Ensure AQI is non-negative
        aqi = max(0, aqi)
        
        # Determine AQI category
        category = cls.get_category(aqi)
        
        # Calculate points based on category
        points = cls.POINTS_BY_CATEGORY.get(category, 0)
        
        return {
            'aqi_score': round(aqi, 2),
            'aqi_category': category,
            'points_earned': points
        }
    
    @classmethod
    def get_category(cls, aqi):
        """Determine the AQI category based on the score"""
        for (lower, upper), category in cls.AQI_CATEGORIES.items():
            if lower <= aqi <= upper:
                return category
        return 'Poor'  # Default if no range matches
