"""
Green Company Calculator

This module calculates a company's environmental sustainability score based on various
metrics and provides personalized recommendations for improvement.
"""

# Scoring functions for each sustainability metric
def carbon_score(tons_emitted):
    """Calculate score for carbon emissions."""
    if tons_emitted < 10:
        return 100, "Excellent", "Your carbon emissions are very low."
    elif tons_emitted < 50:
        return 70, "Good", "Consider offsetting remaining carbon emissions through reforestation projects."
    elif tons_emitted < 100:
        return 40, "Fair", "Implement a carbon reduction plan targeting 20% reduction annually."
    else:
        return 10, "Poor", "Urgent action needed: Consider energy audits and switching to renewable energy sources."

def energy_score(kwh_used):
    """Calculate score for energy consumption."""
    if kwh_used < 1000:
        return 100, "Excellent", "Your energy usage is minimal."
    elif kwh_used < 5000:
        return 70, "Good", "Consider installing energy-efficient lighting and equipment."
    elif kwh_used < 10000:
        return 40, "Fair", "Implement an energy management system and consider solar panels."
    else:
        return 10, "Poor", "Conduct a full energy audit and create a reduction strategy immediately."

def water_score(liters_used):
    """Calculate score for water usage."""
    if liters_used < 500:
        return 100, "Excellent", "Your water conservation efforts are exceptional."
    elif liters_used < 2000:
        return 70, "Good", "Install water-saving fixtures and consider rainwater harvesting."
    elif liters_used < 5000:
        return 40, "Fair", "Implement a water recycling system for non-potable needs."
    else:
        return 10, "Poor", "Conduct a water audit and prioritize high-impact conservation measures."

def waste_score(kgs_waste):
    """Calculate score for waste production."""
    if kgs_waste < 100:
        return 100, "Excellent", "Your waste management is exemplary."
    elif kgs_waste < 500:
        return 70, "Good", "Implement composting for organic waste and improve recycling."
    elif kgs_waste < 1000:
        return 40, "Fair", "Adopt a zero-waste policy and train staff on waste reduction."
    else:
        return 10, "Poor", "Urgent action needed: Conduct waste audit and implement comprehensive reduction plan."

def aqi_score(aqi):
    """Calculate score for air quality index."""
    if aqi < 50:
        return 100, "Excellent", "Your air quality is exceptional and healthy."
    elif aqi < 100:
        return 70, "Good", "Consider upgrading filtration systems and monitoring air quality regularly."
    elif aqi < 150:
        return 40, "Fair", "Implement pollution control measures and air purification systems."
    else:
        return 10, "Poor", "Urgent action needed: Identify pollution sources and implement emission controls."

def recycling_score(percent):
    """Calculate score for recycling rate."""
    if percent >= 80:
        return 100, "Excellent", "Your recycling program is outstanding."
    elif percent >= 60:
        return 70, "Good", "Improve recycling education and add more recycling stations."
    elif percent >= 30:
        return 40, "Fair", "Implement a comprehensive recycling program with clear guidelines."
    else:
        return 10, "Poor", "Develop a recycling strategy and set incremental improvement targets."

class GreenCalculator:
    """Calculate green scores and sustainability status for companies."""
    
    # Weights for each sustainability metric
    WEIGHTS = {
        'carbon': 0.3,
        'energy': 0.2,
        'water': 0.15,
        'waste': 0.15,
        'aqi': 0.1,
        'recycling': 0.1
    }
    
    # Status categories based on score ranges
    STATUS_CATEGORIES = {
        (80, 100): ("✅ Green Certified", "Your company meets high sustainability standards!"),
        (60, 79): ("🟡 On Track", "Your company is making good progress toward sustainability."),
        (40, 59): ("🔴 Needs Improvement", "Significant sustainability improvements are needed."),
        (0, 39): ("❌ Not Green", "Urgent action needed to improve environmental performance.")
    }
    
    @classmethod
    def calculate_green_score(cls, data):
        """
        Calculate the overall green score using weighted metrics.
        
        Args:
            data: Dictionary with keys 'carbon', 'energy', 'water', 'waste', 'aqi', 'recycling'
                 containing the respective metric values
        
        Returns:
            Dictionary with total_score, individual_scores, ratings, weights, and recommendations
        """
        # Calculate individual scores
        score_results = {
            'carbon': carbon_score(data['carbon']),
            'energy': energy_score(data['energy']),
            'water': water_score(data['water']),
            'waste': waste_score(data['waste']),
            'aqi': aqi_score(data['aqi']),
            'recycling': recycling_score(data['recycling'])
        }
        
        # Extract numerical scores from the score_results tuples
        scores = {key: value[0] for key, value in score_results.items()}
        ratings = {key: value[1] for key, value in score_results.items()}
        recommendations = {key: value[2] for key, value in score_results.items()}
        
        # Calculate weighted green score
        green_score = sum(scores[key] * cls.WEIGHTS[key] for key in scores)
        
        return {
            'total_score': round(green_score, 2),
            'individual_scores': scores,
            'ratings': ratings,
            'weights': cls.WEIGHTS,
            'recommendations': recommendations
        }
    
    @classmethod
    def get_green_status(cls, score):
        """
        Determine the company's green certification status.
        
        Args:
            score: The total green score (0-100)
            
        Returns:
            Tuple with (status, description)
        """
        for (min_score, max_score), (status, description) in cls.STATUS_CATEGORIES.items():
            if min_score <= score <= max_score:
                return status, description
        
        # Fallback in case the score is out of expected range
        return "Status Unknown", "Unable to determine sustainability status."