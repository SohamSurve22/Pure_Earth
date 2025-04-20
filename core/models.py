from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class Company(models.Model):
    """Model for company information"""
    name = models.CharField(max_length=100, unique=True)
    industry = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Companies"

class GreenCalculation(models.Model):
    """Model for Green Calculator submissions"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='green_calculations')
    
    # Input metrics
    carbon_emissions = models.FloatField(validators=[MinValueValidator(0)])  # tons
    energy_consumption = models.FloatField(validators=[MinValueValidator(0)])  # kWh
    water_usage = models.FloatField(validators=[MinValueValidator(0)])  # liters
    waste_produced = models.FloatField(validators=[MinValueValidator(0)])  # kg
    air_quality_index = models.FloatField(validators=[MinValueValidator(0), MinValueValidator(0)])  # AQI
    recycling_rate = models.FloatField(validators=[MinValueValidator(0), MinValueValidator(0)])  # %
    
    # Individual scores (0-100)
    carbon_score = models.FloatField()
    energy_score = models.FloatField()
    water_score = models.FloatField()
    waste_score = models.FloatField()
    aqi_score = models.FloatField()
    recycling_score = models.FloatField()
    
    # Overall results
    green_score = models.FloatField()  # Total weighted score (0-100)
    status = models.CharField(max_length=50)  # Green Certified, On Track, Needs Improvement, Not Green
    
    # Recommendations stored as JSON
    recommendations_json = models.TextField(blank=True, null=True)
    
    # Metadata
    submitted_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.company.name} - {self.green_score} ({self.status}) - {self.submitted_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Green Calculation"
        verbose_name_plural = "Green Calculations"

# Keep the old AQI model for backward compatibility, but mark it as deprecated
class AQISubmission(models.Model):
    """Model for AQI calculation submissions (deprecated)"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='aqi_submissions')
    energy_consumption = models.FloatField(validators=[MinValueValidator(0)])  # kWh/day
    fuel_type = models.CharField(max_length=20)  # Coal, Diesel, Gas, Renewable
    production_output = models.FloatField(validators=[MinValueValidator(0)])  # Units/day
    waste_emissions = models.FloatField(validators=[MinValueValidator(0)])  # Tons/day
    vehicles_operated = models.IntegerField(validators=[MinValueValidator(0)])  # Count/day
    wind_speed = models.FloatField(validators=[MinValueValidator(0)])  # m/s
    rainfall = models.FloatField(validators=[MinValueValidator(0)])  # mm
    aqi_score = models.FloatField()
    aqi_category = models.CharField(max_length=20)
    points_earned = models.IntegerField()
    submitted_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.company.name} - {self.aqi_score} ({self.submitted_at.strftime('%Y-%m-%d')})"
    
    class Meta:
        ordering = ['-submitted_at']

class ThermalAnalysis(models.Model):
    """Model for thermal image analysis submissions"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='thermal_analyses')
    image = models.ImageField(upload_to='thermal_images/')
    hottest_region_x = models.IntegerField(null=True, blank=True)
    hottest_region_y = models.IntegerField(null=True, blank=True)
    min_temperature = models.FloatField(null=True, blank=True)
    max_temperature = models.FloatField(null=True, blank=True)
    heat_source_count = models.IntegerField(default=0)
    large_heat_source_count = models.IntegerField(default=0)
    total_heat_area = models.FloatField(default=0)
    pollution_status = models.CharField(max_length=20, default="Non-Polluted")
    heat_sources_json = models.TextField(blank=True, null=True)  # JSON string of heat sources
    temp_distribution_json = models.TextField(blank=True, null=True)  # JSON string of temperature distribution data
    
    # Multiple visualization types for dashboard display
    visualization_base64 = models.TextField(blank=True, null=True)  # Base64 of main visualization image with annotations
    heatmap_base64 = models.TextField(blank=True, null=True)  # Base64 of colorized heatmap
    rectangle_base64 = models.TextField(blank=True, null=True)  # Base64 of only rectangles around heat sources
    contour_base64 = models.TextField(blank=True, null=True)  # Base64 of contour overlay
    
    thermal_category = models.CharField(max_length=20)
    points_earned = models.IntegerField()
    analyzed_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.company.name} - {self.thermal_category} ({self.analyzed_at.strftime('%Y-%m-%d')})"
    
    class Meta:
        verbose_name_plural = "Thermal Analyses"
        ordering = ['-analyzed_at']
