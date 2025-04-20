from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Green Calculator (new primary functionality)
    path('green-calculator/', views.green_calculator, name='green_calculator'),
    path('green-result/<int:calculation_id>/', views.green_result, name='green_result'),
    # Legacy AQI Calculator (kept for backward compatibility)
    path('aqi-calculator/', views.aqi_calculator, name='aqi_calculator'),
    path('aqi-result/<int:submission_id>/', views.aqi_result, name='aqi_result'),
    # Thermal analysis
    path('image-analyzer/', views.image_analyzer, name='image_analyzer'),
    path('thermal-result/<int:analysis_id>/', views.thermal_result, name='thermal_result'),
    # Leaderboard and API
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('api/green-calculator/', views.api_green_calculator, name='api_green_calculator'),
    path('api/aqi-calculator/', views.api_aqi_calculator, name='api_aqi_calculator'),
]
