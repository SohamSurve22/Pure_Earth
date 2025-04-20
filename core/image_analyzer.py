import os
import cv2
import numpy as np
import base64
import json
from io import BytesIO
from PIL import Image
import tempfile

class ThermalImageAnalyzer:
    """
    Analyzes thermal images to detect heat sources and categorize pollution levels
    based on heat intensity.
    """

    # Thermal image categories
    THERMAL_CATEGORIES = {
        (0, 25): 'Green',    # Low heat
        (26, 50): 'Good',    # Moderate heat
        (51, 75): 'Average', # High heat
        (76, 100): 'Poor'    # Extreme heat
    }

    # Points awarded for each category
    POINTS_BY_CATEGORY = {
        'Green': 100,
        'Good': 75,
        'Average': 50,
        'Poor': 25
    }

    # Analysis thresholds
    HEAT_THRESHOLD = 200  # Threshold for binary heat detection
    MIN_HEAT_AREA = 800   # Minimum area to consider as a significant heat source
    LARGE_HEAT_AREA = 5000  # Area threshold for considering a heat source as potentially polluting

    @classmethod
    def analyze_thermal_image(cls, image_file):
        """
        Analyze a thermal image using OpenCV to:
        1. Detect the hottest region
        2. Analyze the total thermal range
        3. Identify multiple heat sources and their sizes
        4. Categorize pollution level based on intensity
        5. Generate visualization data for dashboard display
        6. Generate heatmap visualization for temperature distribution
        """
        try:
            # Save the uploaded file to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_filename = temp_file.name
                for chunk in image_file.chunks():
                    temp_file.write(chunk)

            # Read image with OpenCV
            img = cv2.imread(temp_filename)
            if img is None:
                raise ValueError("Failed to decode image")

            # Make a copy for visualization
            original = img.copy()
            visualization = img.copy()

            # Convert to grayscale (thermal images are often grayscale)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Find minimum and maximum temperature (pixel value)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray)

            # Calculate a normalized value (0-100) representing the overall heat level
            normalized_value = (max_val / 255) * 100

            # Determine the thermal category
            thermal_category = cls.get_category(normalized_value)

            # Calculate points earned based on category
            points_earned = cls.POINTS_BY_CATEGORY[thermal_category]

            # Noise reduction
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            _, heat_map = cv2.threshold(blurred, cls.HEAT_THRESHOLD, 255, cv2.THRESH_BINARY)

            # Find contours for heat sources
            contours, _ = cv2.findContours(heat_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Image for just showing rectangles
            rectangle_overlay = np.zeros_like(img)

            # Image for just showing contours
            contour_overlay = np.zeros_like(img)
            cv2.drawContours(contour_overlay, contours, -1, (0, 255, 0), 2)

            # Analyze heat sources
            heat_source_count = 0
            large_heat_source_count = 0
            total_heat_area = 0
            heat_sources = []

            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > cls.MIN_HEAT_AREA:  # Ignore small noise
                    heat_source_count += 1
                    total_heat_area += area

                    # Rectangle
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(visualization, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red rectangle
                    cv2.rectangle(rectangle_overlay, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red rectangle

                    # Centroid
                    M = cv2.moments(contour)
                    cx, cy = x + w//2, y + h//2  # Default to center of bounding box
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        cv2.circle(visualization, (cx, cy), 5, (0, 255, 255), -1)  # Yellow pinpoint
                        cv2.putText(visualization, f"Heat {heat_source_count}", (cx - 20, cy - 10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                    # Get average temperature in this region
                    mask = np.zeros(gray.shape, np.uint8)
                    cv2.drawContours(mask, [contour], 0, 255, -1)
                    mean_temp = cv2.mean(gray, mask=mask)[0]

                    # Check if this is a large heat source
                    is_large = area > cls.LARGE_HEAT_AREA
                    if is_large:
                        large_heat_source_count += 1

                    # Store heat source data
                    heat_sources.append({
                        'id': heat_source_count,
                        'x': cx,
                        'y': cy,
                        'area': area,
                        'width': w,
                        'height': h,
                        'temperature': mean_temp,
                        'is_large': is_large
                    })

            # Pollution assessment based on number of heat sources and their sizes
            pollution_status = "Polluted" if large_heat_source_count > 0 or heat_source_count > 5 else "Non-Polluted"

            # Mark the hottest point with a circle
            cv2.circle(visualization, max_loc, 20, (255, 0, 0), 2)  # Blue circle at hottest point
            cv2.circle(visualization, max_loc, 5, (255, 255, 0), -1)  # Yellow dot at center

            # Add text for temperature and statistics
            cv2.putText(visualization, f"Max Temp: {max_val:.1f}", (max_loc[0]-50, max_loc[1]-30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(visualization, f"Status: {pollution_status}", (20, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(visualization, f"Heat Sources: {heat_source_count}", (20, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(visualization, f"Category: {thermal_category}", (20, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Generate a colorized heatmap
            heatmap = cls.generate_heatmap(gray, min_val, max_val)

            # Convert visualizations to base64 for display
            def img_to_base64(img):
                _, buffer = cv2.imencode('.png', img)
                return base64.b64encode(buffer).decode('utf-8')

            visualization_base64 = img_to_base64(visualization)
            heatmap_base64 = img_to_base64(heatmap)
            rectangle_base64 = img_to_base64(rectangle_overlay)
            contour_base64 = img_to_base64(contour_overlay)

            # Generate interactive heatmap data
            interactive_data = cls.generate_interactive_heatmap_data(
                heat_sources, img.shape[1], img.shape[0]
            )

            # Clean up the temporary file
            os.unlink(temp_filename)

            # Ensure all required fields are present
            result = {
                'min_temperature': float(min_val),
                'max_temperature': float(max_val),
                'hottest_region_x': int(max_loc[0]),
                'hottest_region_y': int(max_loc[1]),
                'heat_source_count': heat_source_count,
                'large_heat_source_count': large_heat_source_count,
                'total_heat_area': float(total_heat_area),
                'pollution_status': pollution_status,
                'thermal_category': thermal_category,
                'points_earned': points_earned,
                'heat_sources_json': json.dumps(heat_sources),
                'temp_distribution_json': json.dumps(interactive_data),
                'visualization_base64': visualization_base64,
                'heatmap_base64': heatmap_base64,
                'rectangle_base64': rectangle_base64,
                'contour_base64': contour_base64
            }
            return result

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                'error': str(e)
            }

    @classmethod
    def get_category(cls, normalized_value):
        """Determine the thermal category based on the normalized temperature value"""
        for (min_val, max_val), category in cls.THERMAL_CATEGORIES.items():
            if min_val <= normalized_value <= max_val:
                return category
        return 'Poor'  # Default to worst category if out of range

    @classmethod
    def generate_heatmap(cls, gray_img, min_val=None, max_val=None):
        """Generate a heatmap colorization of the grayscale thermal image"""
        if min_val is None or max_val is None:
            min_val, max_val, _, _ = cv2.minMaxLoc(gray_img)

        # Normalize the image for better visualization
        normalized = cv2.normalize(gray_img, None, 0, 255, cv2.NORM_MINMAX)

        # Apply colormap (COLORMAP_JET is commonly used for thermal imaging)
        heatmap = cv2.applyColorMap(normalized, cv2.COLORMAP_JET)

        return heatmap

    @classmethod
    def generate_interactive_heatmap_data(cls, heat_sources, img_width, img_height):
        """Generate data for interactive heatmap visualization on the dashboard"""
        # Simple temperature distribution data for visualization
        temp_data = []

        # Extract temperature values from heat sources
        if heat_sources:
            for source in heat_sources:
                temp_data.append({
                    'value': source['temperature'],
                    'x': source['x'] / img_width,  # Normalize to 0-1 range
                    'y': source['y'] / img_height  # Normalize to 0-1 range
                })

        return temp_data