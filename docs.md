
# PureEarth - Documentation

## Overview
PureEarth is an environmental sustainability platform that helps companies track and improve their ecological impact. This documentation will help you understand and use the platform effectively.

## Features

### 1. Green Calculator
The Green Calculator evaluates your company's environmental performance based on:
- Carbon emissions (tons)
- Energy consumption (kWh)
- Water usage (liters)
- Waste production (kg)
- Air quality index
- Recycling rate (%)

To use:
1. Go to the Green Calculator page
2. Enter your company's metrics
3. Submit to receive a detailed sustainability score and recommendations

### 2. Thermal Image Analysis
Upload thermal images to detect potential environmental issues:
- Heat source detection
- Temperature distribution analysis
- Pollution hotspot identification

To analyze images:
1. Navigate to the Image Analyzer
2. Upload your thermal image
3. View the analysis results with visual heatmaps

### 3. Dashboard
The dashboard provides:
- Overview of your environmental metrics
- Historical trends
- Comparison with industry standards
- Interactive charts and graphs

### 4. Company Leaderboard
Compare your sustainability performance with other companies:
- Rankings based on green scores
- Industry-specific comparisons
- Best practices from top performers

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Setup
1. Create virtual environment and activate it
```
python -m venv .venv
.venv\scripts\activate
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Set up the database:
```
python manage.py migrate
```

4. Create superuser if not already creater
```
python manage.py createsuperuser
```
5. Run Server
```
python manage.py runserver
```
6. Access the application:
```
Open your web browser and go to: http://localhost:8000
```

### Project Structure
- `/core` - Main application logic
- `/templates` - HTML templates
- `/static` - CSS, JavaScript, and assets
- `/media` - Uploaded files

## Data Storage

### Django Use
1.Model-View-Template (MVT) Architecture:
	-Models (core/models.py): Defines database tables for Company, GreenCalculation, AQISubmission, and 	 	   	 ThermalAnalysis
	-Views (core/views.py): Handles business logic for calculations, data processing, and rendering
	-Templates (templates/core/*.html): Manages the UI presentation
2.URL Routing (core/urls.py):
	-Manages application endpoints like dashboard, calculators, and results pages
	-Handles both web pages and API endpoints
3.Database Management:
	-Uses Django's ORM with SQLite (pureearth/settings.py)
	-Handles data migrations and relationships between models
	-Provides query interfaces for filtering and aggregating data
4.Form Processing:
	-Handles form submissions for green calculations, AQI data, and image uploads
	-Provides validation and data cleaning
5.Template System:
	-Custom template tags (core/templatetags/core_extras.py)
	-Template inheritance for consistent layouts
	-Dynamic data rendering

### Database Structure
The application uses SQLite database (db.sqlite3) to store all data. Here's what's stored:

1. Company Information (`Company` model)
   - Company name
   - Industry type
   - Creation timestamp

2. Green Calculator Results (`GreenCalculation` model)
   - Carbon emissions
   - Energy consumption
   - Water usage
   - Waste production
   - Air quality index
   - Recycling rate
   - Individual scores for each metric
   - Overall green score
   - Status and recommendations

3. Thermal Analysis Results (`ThermalAnalysis` model)
   - Uploaded thermal images (stored in `/media/thermal_images/`)
   - Temperature data
   - Heat source locations
   - Analysis visualizations
   - Pollution status
   - Points earned

### File Storage
- Database file: `instance/pureearth.db`
- Media files: `/media/thermal_images/`
- Static assets: `/static/`
  - CSS files: `/static/css/`
  - JavaScript files: `/static/js/`
  - Images and other assets: `/static/assets/`

### Data Security
- User data is stored locally in the SQLite database
- Uploaded images are saved securely in the media directory
- Static files are served separately from user data
- Database is protected by Django's security middleware

## Scoring System

### Green Score Categories
- 80-100: Green Certified
- 60-79: On Track
- 40-59: Needs Improvement
- 0-39: Not Green

### Metrics Evaluation
Each metric is evaluated on a 100-point scale:
- Carbon Score: Based on emissions compared to industry standards
- Energy Score: Evaluates efficiency of energy usage
- Water Score: Measures water conservation efforts
- Waste Score: Assesses waste management practices
- AQI Score: Air quality impact assessment
- Recycling Score: Effectiveness of recycling programs

## Tips for Better Scores
1. Monitor energy consumption regularly
2. Implement recycling programs
3. Optimize water usage
4. Reduce carbon emissions through efficient processes
5. Maintain good air quality standards
6. Minimize waste production


## Best Practices
1. Regular Monitoring
   - Track metrics weekly or monthly
   - Document changes and improvements
   - Set realistic improvement goals

2. Data Accuracy
   - Use calibrated measurement tools
   - Keep detailed records
   - Verify unusual readings

3. Continuous Improvement
   - Review recommendations regularly
   - Implement suggested changes
   - Monitor impact of improvements
