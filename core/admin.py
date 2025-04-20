from django.contrib import admin
from .models import Company, AQISubmission, ThermalAnalysis

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'created_at')
    search_fields = ('name', 'industry')
    list_filter = ('industry', 'created_at')

@admin.register(AQISubmission)
class AQISubmissionAdmin(admin.ModelAdmin):
    list_display = ('company', 'aqi_score', 'aqi_category', 'points_earned', 'submitted_at')
    list_filter = ('aqi_category', 'fuel_type', 'submitted_at')
    search_fields = ('company__name',)
    readonly_fields = ('aqi_score', 'aqi_category', 'points_earned')
    fieldsets = (
        ('Company Information', {
            'fields': ('company',)
        }),
        ('Input Data', {
            'fields': ('energy_consumption', 'fuel_type', 'production_output', 
                      'waste_emissions', 'vehicles_operated', 'wind_speed', 'rainfall')
        }),
        ('Results', {
            'fields': ('aqi_score', 'aqi_category', 'points_earned', 'submitted_at')
        }),
    )

@admin.register(ThermalAnalysis)
class ThermalAnalysisAdmin(admin.ModelAdmin):
    list_display = ('company', 'thermal_category', 'points_earned', 'analyzed_at')
    list_filter = ('thermal_category', 'analyzed_at')
    search_fields = ('company__name',)
    readonly_fields = ('min_temperature', 'max_temperature', 'hottest_region_x', 
                      'hottest_region_y', 'thermal_category', 'points_earned')
    fieldsets = (
        ('Company Information', {
            'fields': ('company',)
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Analysis Results', {
            'fields': ('min_temperature', 'max_temperature', 'hottest_region_x', 
                      'hottest_region_y', 'thermal_category', 'points_earned', 'analyzed_at')
        }),
    )
