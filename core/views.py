from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Avg, Count, Sum, F, Value, FloatField
from django.db.models.functions import Coalesce
from django.contrib import messages
import os
import json

from .models import Company, AQISubmission, ThermalAnalysis, GreenCalculation
from .utils.aqi_calculator import AQICalculator
from .utils.image_analyzer import ThermalImageAnalyzer
from .utils.green_calculator import GreenCalculator

def index(request):
    """Home page with overview and navigation"""
    company_count = Company.objects.count()
    green_calculations_count = GreenCalculation.objects.count()
    aqi_submissions_count = AQISubmission.objects.count()
    thermal_analyses_count = ThermalAnalysis.objects.count()
    
    recent_green = GreenCalculation.objects.order_by('-submitted_at')[:5]
    recent_aqi = AQISubmission.objects.order_by('-submitted_at')[:5]
    recent_thermal = ThermalAnalysis.objects.order_by('-analyzed_at')[:5]
    
    return render(request, 'core/index.html', {
        'company_count': company_count,
        'green_calculations_count': green_calculations_count,
        'aqi_submissions_count': aqi_submissions_count, 
        'thermal_analyses_count': thermal_analyses_count,
        'recent_green': recent_green,
        'recent_aqi': recent_aqi,
        'recent_thermal': recent_thermal,
    })

def dashboard(request):
    """Dashboard with overall stats and charts"""
    # Get counts
    company_count = Company.objects.count()
    green_calculations_count = GreenCalculation.objects.count()
    aqi_submissions_count = AQISubmission.objects.count()
    thermal_analyses_count = ThermalAnalysis.objects.count()
    
    # Get Green Calculator stats
    avg_green_score = GreenCalculation.objects.aggregate(avg=Avg('green_score'))['avg'] or 0
    green_status_data = GreenCalculation.objects.values('status').annotate(count=Count('id')).order_by('status')
    
    # Calculate average scores for each sustainability metric
    avg_carbon_score = GreenCalculation.objects.aggregate(avg=Avg('carbon_score'))['avg'] or 0
    avg_energy_score = GreenCalculation.objects.aggregate(avg=Avg('energy_score'))['avg'] or 0
    avg_water_score = GreenCalculation.objects.aggregate(avg=Avg('water_score'))['avg'] or 0
    avg_waste_score = GreenCalculation.objects.aggregate(avg=Avg('waste_score'))['avg'] or 0
    avg_aqi_score = GreenCalculation.objects.aggregate(avg=Avg('aqi_score'))['avg'] or 0
    avg_recycling_score = GreenCalculation.objects.aggregate(avg=Avg('recycling_score'))['avg'] or 0
    
    # Legacy AQI Stats (for backward compatibility)
    avg_legacy_aqi = AQISubmission.objects.aggregate(avg=Avg('aqi_score'))['avg'] or 0
    avg_aqi_points = AQISubmission.objects.aggregate(avg=Avg('points_earned'))['avg'] or 0
    aqi_categories = AQISubmission.objects.values('aqi_category').annotate(count=Count('id')).order_by('aqi_category')
    
    # Thermal Analysis Stats
    avg_thermal_points = ThermalAnalysis.objects.aggregate(avg=Avg('points_earned'))['avg'] or 0
    thermal_categories = ThermalAnalysis.objects.values('thermal_category').annotate(count=Count('id')).order_by('thermal_category')
    
    # Get recent thermal analyses with visualizations
    recent_thermal_analyses = ThermalAnalysis.objects.filter(
        visualization_base64__isnull=False
    ).exclude(
        visualization_base64=''
    ).order_by('-analyzed_at')[:3]
    
    # Get pollution status distribution
    pollution_status_data = ThermalAnalysis.objects.values('pollution_status').annotate(
        count=Count('id')
    ).order_by('pollution_status')
    
    # Get heat source stats
    avg_heat_sources = ThermalAnalysis.objects.aggregate(avg=Avg('heat_source_count'))['avg'] or 0
    avg_large_heat_sources = ThermalAnalysis.objects.aggregate(avg=Avg('large_heat_source_count'))['avg'] or 0
    total_heat_sources = ThermalAnalysis.objects.aggregate(sum=Sum('heat_source_count'))['sum'] or 0
    
    # Get recent green calculations
    recent_green_calculations = GreenCalculation.objects.order_by('-submitted_at')[:5]
    
    return render(request, 'core/dashboard.html', {
        # Company stats
        'company_count': company_count,
        
        # Green Calculator stats
        'green_calculations_count': green_calculations_count,
        'avg_green_score': avg_green_score,
        'green_status_data': green_status_data,
        'avg_carbon_score': avg_carbon_score,
        'avg_energy_score': avg_energy_score,
        'avg_water_score': avg_water_score,
        'avg_waste_score': avg_waste_score,
        'avg_aqi_score': avg_aqi_score,
        'avg_recycling_score': avg_recycling_score,
        'recent_green_calculations': recent_green_calculations,
        
        # Legacy AQI stats
        'aqi_submissions_count': aqi_submissions_count,
        'avg_legacy_aqi': avg_legacy_aqi,
        'avg_aqi_points': avg_aqi_points,
        'aqi_categories': aqi_categories,
        
        # Thermal Analysis stats
        'thermal_analyses_count': thermal_analyses_count,
        'avg_thermal_points': avg_thermal_points,
        'thermal_categories': thermal_categories,
        'recent_thermal_analyses': recent_thermal_analyses,
        'pollution_status_data': pollution_status_data,
        'avg_heat_sources': avg_heat_sources,
        'avg_large_heat_sources': avg_large_heat_sources,
        'total_heat_sources': total_heat_sources,
    })

def aqi_calculator(request):
    """AQI calculation form and results"""
    if request.method == 'POST':
        # Get form data
        company_name = request.POST.get('company_name')
        company_industry = request.POST.get('company_industry', '')
        
        # Get or create company
        company, created = Company.objects.get_or_create(
            name=company_name,
            defaults={'industry': company_industry}
        )
        
        # If company exists but industry is provided, update it
        if not created and company_industry and not company.industry:
            company.industry = company_industry
            company.save()
        
        # Get numeric inputs
        try:
            energy_consumption = float(request.POST.get('energy_consumption'))
            fuel_type = request.POST.get('fuel_type')
            production_output = float(request.POST.get('production_output'))
            waste_emissions = float(request.POST.get('waste_emissions'))
            vehicles_operated = int(request.POST.get('vehicles_operated'))
            wind_speed = float(request.POST.get('wind_speed'))
            rainfall = float(request.POST.get('rainfall'))
        except (ValueError, TypeError):
            messages.error(request, "Invalid input values. Please check your data and try again.")
            return redirect('aqi_calculator')
        
        # Calculate AQI
        result = AQICalculator.calculate_aqi(
            energy_consumption=energy_consumption,
            fuel_type=fuel_type,
            waste_emissions=waste_emissions,
            vehicles_operated=vehicles_operated,
            wind_speed=wind_speed,
            rainfall=rainfall
        )
        
        # Save submission
        submission = AQISubmission.objects.create(
            company=company,
            energy_consumption=energy_consumption,
            fuel_type=fuel_type,
            production_output=production_output,
            waste_emissions=waste_emissions,
            vehicles_operated=vehicles_operated,
            wind_speed=wind_speed,
            rainfall=rainfall,
            aqi_score=result['aqi_score'],
            aqi_category=result['category'],
            points_earned=result['points']
        )
        
        # Redirect to results page
        return redirect('aqi_result', submission_id=submission.id)
    
    # For GET request, show the form
    companies = Company.objects.all()
    fuel_types = list(AQICalculator.FUEL_FACTORS.keys())
    
    return render(request, 'core/aqi_calculator.html', {
        'companies': companies,
        'fuel_types': fuel_types
    })

def aqi_result(request, submission_id):
    """Show AQI calculation results"""
    submission = get_object_or_404(AQISubmission, id=submission_id)
    
    return render(request, 'core/aqi_result.html', {
        'submission': submission
    })

def image_analyzer(request):
    """Thermal image analysis form and results"""
    if request.method == 'POST':
        # Get form data
        company_name = request.POST.get('company_name')
        company_industry = request.POST.get('company_industry', '')
        thermal_image = request.FILES.get('thermal_image')
        
        # Validate image
        if not thermal_image:
            messages.error(request, "Please upload an image file.")
            return redirect('image_analyzer')
        
        # Get or create company
        company, created = Company.objects.get_or_create(
            name=company_name,
            defaults={'industry': company_industry}
        )
        
        # If company exists but industry is provided, update it
        if not created and company_industry and not company.industry:
            company.industry = company_industry
            company.save()
        
        # Analyze the image
        try:
            analysis_result = ThermalImageAnalyzer.analyze_thermal_image(thermal_image)
            
            if not analysis_result:
                messages.error(request, "Failed to analyze the image. Please try a different image.")
                return redirect('image_analyzer')
            
            # Check if there's an error in the analysis result
            if 'error' in analysis_result:
                messages.error(request, f"Error analyzing image: {analysis_result['error']}")
                return redirect('image_analyzer')
                
            # Convert heat sources to JSON string for storage
            import json
            heat_sources_json = json.dumps(analysis_result.get('heat_sources', []))
            
            # Convert temperature distribution to JSON if available
            temp_distribution_json = None
            if 'temp_distribution' in analysis_result:
                temp_distribution_json = json.dumps(analysis_result['temp_distribution'])

            # Save the analysis with enhanced data
            analysis = ThermalAnalysis.objects.create(
                company=company,
                image=thermal_image,
                hottest_region_x=analysis_result['hottest_region_x'],
                hottest_region_y=analysis_result['hottest_region_y'],
                min_temperature=analysis_result['min_temperature'],
                max_temperature=analysis_result['max_temperature'],
                heat_source_count=analysis_result.get('heat_source_count', 0),
                large_heat_source_count=analysis_result.get('large_heat_source_count', 0),
                total_heat_area=analysis_result.get('total_heat_area', 0),
                pollution_status=analysis_result.get('pollution_status', 'Non-Polluted'),
                heat_sources_json=heat_sources_json,
                temp_distribution_json=temp_distribution_json,
                # Multiple visualization types
                visualization_base64=analysis_result.get('visualization_base64', ''),
                heatmap_base64=analysis_result.get('heatmap_base64', ''),
                rectangle_base64=analysis_result.get('rectangle_base64', ''),
                contour_base64=analysis_result.get('contour_base64', ''),
                thermal_category=analysis_result['thermal_category'],
                points_earned=analysis_result['points_earned']
            )
            
            # Redirect to results page
            return redirect('thermal_result', analysis_id=analysis.id)
            
        except Exception as e:
            messages.error(request, f"Error analyzing image: {str(e)}")
            return redirect('image_analyzer')
    
    # For GET request, show the form
    companies = Company.objects.all()
    
    return render(request, 'core/image_analyzer.html', {
        'companies': companies
    })

def thermal_result(request, analysis_id):
    """Show thermal image analysis results"""
    analysis = get_object_or_404(ThermalAnalysis, id=analysis_id)
    
    return render(request, 'core/thermal_result.html', {
        'analysis': analysis
    })

def leaderboard(request):
    """Sustainability leaderboard of companies"""
    # Get all companies with their submissions
    companies = Company.objects.all()
    
    # Calculate scores and create leaderboard
    leaderboard_entries = []
    
    for company in companies:
        # Get average Green Score if available
        green_score = company.green_calculations.aggregate(avg=Avg('green_score'))['avg'] or 0
        
        # For legacy compatibility, get average AQI and thermal points
        aqi_points = company.aqi_submissions.aggregate(avg=Avg('points_earned'))['avg'] or 0
        thermal_points = company.thermal_analyses.aggregate(avg=Avg('points_earned'))['avg'] or 0
        
        # Get submission counts
        green_count = company.green_calculations.count()
        aqi_count = company.aqi_submissions.count()
        thermal_count = company.thermal_analyses.count()
        total_submissions = green_count + aqi_count + thermal_count
        
        # Only include companies with at least one submission
        if total_submissions > 0:
            # Calculate the weighted score based on all available metrics
            weighted_score = 0
            weights_applied = 0
            
            # Green Calculator: 60% weight
            if green_count > 0:
                weighted_score += green_score * 0.6
                weights_applied += 0.6
            
            # AQI: 15% weight
            if aqi_count > 0:
                weighted_score += aqi_points * 0.15
                weights_applied += 0.15
            
            # Thermal: 25% weight
            if thermal_count > 0:
                weighted_score += thermal_points * 0.25
                weights_applied += 0.25
            
            # Normalize the score if not all components are available
            if weights_applied > 0:
                total_score = weighted_score / weights_applied
            else:
                total_score = 0
                
            # Determine score type
            if green_count > 0 and aqi_count > 0 and thermal_count > 0:
                score_type = "Complete Score"
            elif green_count > 0:
                score_type = "Green Score Based"
            else:
                score_type = "Partial Score"
            
            # Get status based on score
            if green_count > 0:
                latest_status = company.green_calculations.order_by('-submitted_at').first().status
            else:
                # Approximate status for legacy scores
                if total_score >= 80:
                    latest_status = "✅ Green Certified"
                elif total_score >= 60:
                    latest_status = "🟡 On Track"
                elif total_score >= 40:
                    latest_status = "🔴 Needs Improvement"
                else:
                    latest_status = "❌ Not Green"
            
            leaderboard_entries.append({
                'company': company,
                'green_score': green_score if green_count > 0 else None,
                'aqi_points': aqi_points if aqi_count > 0 else None,
                'thermal_points': thermal_points if thermal_count > 0 else None,
                'total_score': total_score,
                'score_type': score_type,
                'status': latest_status,
                'green_count': green_count,
                'aqi_count': aqi_count,
                'thermal_count': thermal_count,
                'submissions_count': total_submissions
            })
    
    # Sort by total score (descending)
    leaderboard_entries.sort(key=lambda x: x['total_score'], reverse=True)
    
    return render(request, 'core/leaderboard.html', {
        'leaderboard_entries': leaderboard_entries
    })

def green_calculator(request):
    """Green Calculator form and results"""
    if request.method == 'POST':
        # Get form data
        company_name = request.POST.get('company_name')
        company_industry = request.POST.get('company_industry', '')
        
        # Get or create company
        company, created = Company.objects.get_or_create(
            name=company_name,
            defaults={'industry': company_industry}
        )
        
        # If company exists but industry is provided, update it
        if not created and company_industry and not company.industry:
            company.industry = company_industry
            company.save()
        
        # Get numeric inputs
        try:
            carbon_emissions = float(request.POST.get('carbon_emissions'))
            energy_consumption = float(request.POST.get('energy_consumption'))
            water_usage = float(request.POST.get('water_usage'))
            waste_produced = float(request.POST.get('waste_produced'))
            air_quality_index = float(request.POST.get('air_quality_index'))
            recycling_rate = float(request.POST.get('recycling_rate'))
        except (ValueError, TypeError):
            messages.error(request, "Invalid input values. Please check your data and try again.")
            return redirect('green_calculator')
        
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
        status, description = GreenCalculator.get_green_status(result['total_score'])
        
        # Save calculation
        calculation = GreenCalculation.objects.create(
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
            recommendations_json=json.dumps(result['recommendations'])
        )
        
        # Redirect to results page
        return redirect('green_result', calculation_id=calculation.id)
    
    # For GET request, show the form
    companies = Company.objects.all()
    
    return render(request, 'core/green_calculator.html', {
        'companies': companies
    })

def green_result(request, calculation_id):
    """Show Green Calculator results"""
    calculation = get_object_or_404(GreenCalculation, id=calculation_id)
    
    # Parse recommendations from JSON
    recommendations = json.loads(calculation.recommendations_json) if calculation.recommendations_json else {}
    
    # Sort recommendations by score (focusing on lowest scores first)
    scores = {
        'carbon': calculation.carbon_score,
        'energy': calculation.energy_score,
        'water': calculation.water_score,
        'waste': calculation.waste_score,
        'aqi': calculation.aqi_score,
        'recycling': calculation.recycling_score
    }
    
    # Get the three lowest scoring areas
    priority_areas = sorted([(key, scores[key]) for key in scores], key=lambda x: x[1])[:3]
    priority_recommendations = [(area, recommendations.get(area, "No recommendation available.")) 
                               for area, score in priority_areas if score < 100]
    
    # Prepare metrics for display
    metrics = {
        'carbon': {'label': 'Carbon Emissions', 'value': calculation.carbon_emissions, 'unit': 'tons', 'score': calculation.carbon_score},
        'energy': {'label': 'Energy Consumption', 'value': calculation.energy_consumption, 'unit': 'kWh', 'score': calculation.energy_score},
        'water': {'label': 'Water Usage', 'value': calculation.water_usage, 'unit': 'liters', 'score': calculation.water_score},
        'waste': {'label': 'Waste Produced', 'value': calculation.waste_produced, 'unit': 'kg', 'score': calculation.waste_score},
        'aqi': {'label': 'Air Quality Index', 'value': calculation.air_quality_index, 'unit': '', 'score': calculation.aqi_score},
        'recycling': {'label': 'Recycling Rate', 'value': calculation.recycling_rate, 'unit': '%', 'score': calculation.recycling_score}
    }
    
    return render(request, 'core/green_result.html', {
        'calculation': calculation,
        'metrics': metrics,
        'priority_recommendations': priority_recommendations,
        'weights': GreenCalculator.WEIGHTS
    })

def api_green_calculator(request):
    """API endpoint for Green Calculator"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    # Get JSON data
    try:
        data = request.POST if request.POST else request.json()
        
        # Extract parameters
        company_name = data.get('company_name')
        
        # Green metrics
        carbon_emissions = float(data.get('carbon_emissions', 0))
        energy_consumption = float(data.get('energy_consumption', 0))
        water_usage = float(data.get('water_usage', 0))
        waste_produced = float(data.get('waste_produced', 0))
        air_quality_index = float(data.get('air_quality_index', 0))
        recycling_rate = float(data.get('recycling_rate', 0))
        
        # Validate company name
        if not company_name:
            return JsonResponse({'error': 'Company name is required'}, status=400)
        
        # Calculate Green Score
        calculation_data = {
            'carbon': carbon_emissions,
            'energy': energy_consumption,
            'water': water_usage,
            'waste': waste_produced,
            'aqi': air_quality_index,
            'recycling': recycling_rate
        }
        
        result = GreenCalculator.calculate_green_score(calculation_data)
        status, description = GreenCalculator.get_green_status(result['total_score'])
        
        # Return result
        return JsonResponse({
            'company_name': company_name,
            'green_score': result['total_score'],
            'status': status,
            'description': description,
            'individual_scores': result['individual_scores'],
            'recommendations': result['recommendations']
        })
    
    except (ValueError, TypeError, KeyError) as e:
        return JsonResponse({'error': f'Invalid input: {str(e)}'}, status=400)

def api_aqi_calculator(request):
    """API endpoint for AQI calculation (deprecated)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    # Get JSON data
    try:
        data = request.POST if request.POST else request.json()
        
        # Extract parameters
        company_name = data.get('company_name')
        energy_consumption = float(data.get('energy_consumption', 0))
        fuel_type = data.get('fuel_type', 'Gas')
        waste_emissions = float(data.get('waste_emissions', 0))
        vehicles_operated = int(data.get('vehicles_operated', 0))
        wind_speed = float(data.get('wind_speed', 0))
        rainfall = float(data.get('rainfall', 0))
        
        # Validate company name
        if not company_name:
            return JsonResponse({'error': 'Company name is required'}, status=400)
        
        # Calculate AQI
        result = AQICalculator.calculate_aqi(
            energy_consumption=energy_consumption,
            fuel_type=fuel_type,
            waste_emissions=waste_emissions,
            vehicles_operated=vehicles_operated,
            wind_speed=wind_speed,
            rainfall=rainfall
        )
        
        # Return result
        return JsonResponse({
            'company_name': company_name,
            'aqi_score': result['aqi_score'],
            'category': result['category'],
            'points': result['points']
        })
    
    except (ValueError, TypeError, KeyError) as e:
        return JsonResponse({'error': f'Invalid input: {str(e)}'}, status=400)
