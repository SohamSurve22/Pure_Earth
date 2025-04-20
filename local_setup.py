"""
Local setup helper script for PureEarth application.
Run this script to generate a requirements.txt file and provide
instructions for running the application locally.
"""
import os
import sys
import subprocess
import shutil

# Define required packages
REQUIRED_PACKAGES = [
    "django>=4.2.0,<5.0.0",
    "pillow>=9.5.0",
    "numpy>=1.24.0",
    "opencv-python-headless>=4.7.0",  # Headless version for server deployment
    "gunicorn>=20.1.0",
    "psycopg2-binary>=2.9.5",  # PostgreSQL adapter (binary version for easier installation)
]

def create_requirements_file():
    """Create a requirements.txt file with the required packages."""
    with open('requirements.txt', 'w') as f:
        for package in REQUIRED_PACKAGES:
            f.write(f"{package}\n")
    print("✅ Created requirements.txt file")

def create_local_settings():
    """Create a local_settings.py file for SQLite configuration."""
    settings_content = """
# Local settings for development - Created by local_setup.py
# This file configures the application to use SQLite for local development

import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent

# Database configuration - SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Set debug to True for development
DEBUG = True

# Set a secret key for development (do not use this in production!)
SECRET_KEY = 'django-insecure-local-development-key-change-in-production'
"""
    
    # Create pureearth directory if it doesn't exist
    os.makedirs('pureearth', exist_ok=True)
    
    # Write the settings file
    with open(os.path.join('pureearth', 'local_settings.py'), 'w') as f:
        f.write(settings_content)
    
    print("✅ Created local database settings for SQLite")

def create_readme():
    """Create or update README.md with installation instructions."""
    readme_content = """# PureEarth - Environmental Sustainability Platform

A comprehensive environmental sustainability platform that enables companies to track, analyze, and improve their ecological impact through advanced calculation tools and interactive reporting.

## Key Features

- **Green Company Calculator**: Comprehensive sustainability scoring based on multiple environmental metrics
- **Thermal Image Analysis**: Analyze thermal images to detect heat sources and potential pollution
- **Multi-Factor Assessment**: Evaluate carbon emissions, energy consumption, water usage, waste production, air quality, and recycling rates
- **Interactive Reporting**: Visual dashboards and detailed recommendations for improvement
- **Company Leaderboard**: Compare sustainability performance across different companies

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Setup Instructions

1. **Clone or download this repository**

2. **Install the required dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   ```
   python manage.py migrate
   ```

4. **Run the application**:
   ```
   python run.py
   ```
   OR
   ```
   python manage.py runserver
   ```

5. **Access the application**:
   Open your web browser and go to: http://localhost:8000

## Environmental Metrics

The Green Calculator evaluates companies based on six key metrics:

- **Carbon Emissions**: The amount of carbon dioxide released (tons)
- **Energy Consumption**: Total energy use across operations (kWh)
- **Water Usage**: Total water consumption (liters)
- **Waste Production**: Amount of waste generated (kg)
- **Air Quality**: Overall air quality around facilities (AQI)
- **Recycling Rate**: Percentage of waste materials recycled (%)

## Sustainability Classifications

Companies are classified into four categories based on their Green Score:

- **Green Certified** (80-100): Meets high sustainability standards
- **On Track** (60-79): Making good progress toward sustainability
- **Needs Improvement** (40-59): Significant sustainability improvements needed
- **Not Green** (0-39): Urgent action needed to improve environmental performance

## Thermal Image Analysis

Upload thermal images to:
- Detect heat sources and potential pollution points
- Analyze temperature distributions
- Identify environmental hotspots
- Receive visual heatmaps and detailed analysis reports

## License

This project is licensed under the MIT License - see the LICENSE file for details.
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("✅ Updated README.md with installation instructions")

def create_sample_data_script():
    """Create a script to generate sample data for demonstration."""
    script_content = """
# sample_data.py - Create sample data for the PureEarth platform
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pureearth.settings')
django.setup()

# Import models
from core.models import Company, GreenCalculation, ThermalAnalysis, AQISubmission
from core.utils.green_calculator import GreenCalculator

def create_sample_companies(num_companies=5):
    # Create sample companies
    companies = []
    
    company_data = [
        {"name": "EcoTech Solutions", "industry": "Technology"},
        {"name": "GreenManufacturing Co.", "industry": "Manufacturing"},
        {"name": "Sustainable Energy Ltd", "industry": "Energy"},
        {"name": "Clean Logistics", "industry": "Transportation"},
        {"name": "EarthFriendly Foods", "industry": "Food Production"},
        {"name": "Renewable Resources Inc", "industry": "Resources"},
        {"name": "Natural Textiles", "industry": "Textiles"},
        {"name": "Green Construction", "industry": "Construction"},
    ]
    
    # Use slice to limit to requested number
    for data in company_data[:num_companies]:
        company, created = Company.objects.get_or_create(
            name=data["name"],
            defaults={"industry": data["industry"]}
        )
        companies.append(company)
        action = "Created" if created else "Using existing"
        print(f"{action} company: {company.name}")
    
    return companies

def create_green_calculations(companies, num_per_company=2):
    # Create sample green calculations for each company
    for company in companies:
        for i in range(num_per_company):
            # Generate realistic sample data
            carbon_emissions = random.uniform(20, 200)  # tons
            energy_consumption = random.uniform(5000, 50000)  # kWh
            water_usage = random.uniform(10000, 100000)  # liters
            waste_produced = random.uniform(100, 2000)  # kg
            air_quality_index = random.uniform(20, 150)  # AQI
            recycling_rate = random.uniform(10, 90)  # %
            
            # Calculate Green Score
            data = {
                'carbon': carbon_emissions,
                'energy': energy_consumption,
                'water': water_usage,
                'waste': waste_produced,
                'aqi': air_quality_index,
                'recycling': recycling_rate
            }
            
            result = GreenCalculator.calculate_green_score(data)
            status, _ = GreenCalculator.get_green_status(result['total_score'])
            
            # Create the calculation with a date slightly in the past
            days_ago = i * 30  # Each submission is separated by ~30 days
            submission_date = datetime.now() - timedelta(days=days_ago)
            
            calc = GreenCalculation.objects.create(
                company=company,
                # Input metrics
                carbon_emissions=carbon_emissions,
                energy_consumption=energy_consumption,
                water_usage=water_usage,
                waste_produced=waste_produced,
                air_quality_index=air_quality_index,
                recycling_rate=recycling_rate,
                # Individual scores
                carbon_score=result['individual_scores']['carbon'],
                energy_score=result['individual_scores']['energy'],
                water_score=result['individual_scores']['water'],
                waste_score=result['individual_scores']['waste'],
                aqi_score=result['individual_scores']['aqi'],
                recycling_score=result['individual_scores']['recycling'],
                # Overall results
                green_score=result['total_score'],
                status=status,
                # Recommendations as JSON
                recommendations_json=django.core.serializers.json.DjangoJSONEncoder().encode(result['recommendations']),
                # Set the date
                submitted_at=submission_date
            )
            
            print(f"Created green calculation for {company.name}: Score {calc.green_score:.1f}, Status: {calc.status}")

def main():
    # Main function to create sample data
    print("Creating sample data for PureEarth platform...")
    
    # Create sample companies
    companies = create_sample_companies(num_companies=5)
    
    # Create green calculations
    create_green_calculations(companies, num_per_company=2)
    
    print("Sample data creation complete!")

if __name__ == "__main__":
    main()
"""
    
    with open('sample_data.py', 'w') as f:
        f.write(script_content)
    
    print("✅ Created sample_data.py script for demonstration purposes")

def print_instructions():
    """Print instructions for running the application locally."""
    print("\n" + "="*60)
    print("🌿 PureEarth Local Setup Instructions 🌿")
    print("="*60)
    print("\n1. Install the required dependencies:")
    print("   pip install -r requirements.txt")
    print("\n2. Set up the database:")
    print("   python manage.py migrate")
    print("\n3. (Optional) Create sample data for testing:")
    print("   python sample_data.py")
    print("\n4. Run the application:")
    print("   python run.py")
    print("   OR")
    print("   python manage.py runserver")
    print("\n5. Access the application:")
    print("   Open your web browser and go to: http://localhost:8000")
    print("\nThe application includes:")
    print("- Green Calculator for comprehensive sustainability scoring")
    print("- Thermal image analysis for environmental monitoring")
    print("- Company leaderboard for sustainability comparison")
    print("- Interactive dashboards for data visualization")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        # Create output directory for zipped project if it doesn't exist
        os.makedirs('dist', exist_ok=True)
        
        # Create requirements file
        create_requirements_file()
        
        # Create local settings for SQLite database
        create_local_settings()
        
        # Create or update readme
        create_readme()
        
        # Create sample data generator
        create_sample_data_script()
        
        # Print setup instructions
        print_instructions()
        
        # Create a ZIP file of the project for easy download
        print("\nCreating distributable ZIP file...")
        # Create a clean directory for zipping
        temp_dir = os.path.join('dist', 'temp_zip')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Copy all files except the ones we want to exclude
        for root, dirs, files in os.walk('.'):
            # Skip dist directory and git directory
            if '/dist' in root or '/.git' in root:
                continue
                
            # Create corresponding directories in temp_dir
            rel_dir = root[2:]  # Remove './' from the beginning
            if rel_dir:
                os.makedirs(os.path.join(temp_dir, rel_dir), exist_ok=True)
                
            # Copy files
            for file in files:
                src_path = os.path.join(root, file)
                dst_path = os.path.join(temp_dir, rel_dir, file)
                shutil.copy2(src_path, dst_path)
        
        # Create the ZIP archive
        shutil.make_archive(
            os.path.join('dist', 'pureearth-sustainability-platform'), 
            'zip', 
            temp_dir
        )
        
        # Clean up temp directory
        shutil.rmtree(temp_dir)
        print(f"✅ Created ZIP file at: dist/pureearth-sustainability-platform.zip")
        
    except Exception as e:
        print(f"Error during setup: {e}")
        sys.exit(1)