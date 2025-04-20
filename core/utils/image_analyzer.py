
import cv2
import numpy as np
import tempfile
from PIL import Image
import os
import base64

class ThermalImageAnalyzer:
    """
    Analyzes thermal images to detect heat sources and categorize pollution levels
    based on heat intensity.
    """
    
    # Thermal categories based on normalized intensity (0-100)
    THERMAL_CATEGORIES = {
        (0, 25): 'Green',    # Low heat
        (26, 50): 'Good',    # Moderate heat
        (51, 75): 'Average', # High heat
        (76, 100): 'Poor'    # Extreme heat
    }
    
    # Points awarded by category
    POINTS_BY_CATEGORY = {
        'Green': 100,
        'Good': 75,
        'Average': 50,
        'Poor': 25
    }

    # Analysis thresholds
    HEAT_THRESHOLD = 200  # Threshold for binary heat detection
    MIN_HEAT_AREA = 100   # Minimum area to consider as a significant heat source
    
    @classmethod
    def analyze_thermal_image(cls, image_file):
        """
        Analyze a thermal image using OpenCV to detect heat sources and pollution
        """
        try:
            # Save uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_name = temp_file.name
                for chunk in image_file.chunks():
                    temp_file.write(chunk)
            
            # Read the image
            image = cv2.imread(temp_name)
            if image is None:
                raise ValueError("Failed to read image")
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Find hottest region
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)
            
            # Create heat map
            _, heat_map = cv2.threshold(gray, cls.HEAT_THRESHOLD, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(heat_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Count heat sources
            heat_sources = []
            heat_source_count = 0
            large_heat_source_count = 0
            total_heat_area = 0
            
            # Draw visualization
            visualization = image.copy()
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > cls.MIN_HEAT_AREA:
                    heat_source_count += 1
                    total_heat_area += area
                    if area > cls.MIN_HEAT_AREA * 5:
                        large_heat_source_count += 1
                    
                    # Draw rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(visualization, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    
                    # Store heat source data
                    heat_sources.append({
                        'id': heat_source_count,
                        'x': int(x + w/2),
                        'y': int(y + h/2),
                        'area': float(area),
                        'temperature': float(cv2.mean(gray, mask=cv2.inRange(gray, max_val-20, max_val))[0]),
                        'is_large': area > cls.MIN_HEAT_AREA * 5
                    })
            
            # Convert visualization to base64
            _, buffer = cv2.imencode('.png', visualization)
            visualization_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Normalize temperature value
            normalized_temp = (max_val / 255.0) * 100
            category = cls.get_category(normalized_temp)
            points = cls.POINTS_BY_CATEGORY[category]
            
            # Cleanup
            os.unlink(temp_name)
            
            return {
                'min_temperature': float(min_val),
                'max_temperature': float(max_val),
                'hottest_region_x': int(max_loc[0]),
                'hottest_region_y': int(max_loc[1]),
                'heat_source_count': heat_source_count,
                'large_heat_source_count': large_heat_source_count,
                'total_heat_area': float(total_heat_area),
                'pollution_status': 'Polluted' if large_heat_source_count > 0 else 'Non-Polluted',
                'thermal_category': category,
                'points_earned': points,
                'heat_sources': heat_sources,
                'visualization_base64': visualization_base64,
                'heatmap_base64': visualization_base64,  # Using same visualization for demo
                'rectangle_base64': visualization_base64,  # Using same visualization for demo
                'contour_base64': visualization_base64,   # Using same visualization for demo
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                'error': str(e)
            }
    
    @classmethod
    def get_category(cls, normalized_value):
        """Determine thermal category based on normalized temperature"""
        for (min_val, max_val), category in cls.THERMAL_CATEGORIES.items():
            if min_val <= normalized_value <= max_val:
                return category
        return 'Poor'  # Default to worst category if out of range
