from PIL import Image, ImageDraw
import numpy as np
import os

# Create a directory for the image
os.makedirs('media/thermal_images', exist_ok=True)

# Create a thermal-like gradient image
width, height = 400, 300
image = Image.new('RGB', (width, height), color='black')
draw = ImageDraw.Draw(image)

# Create a gradient that resembles a thermal image
for y in range(height):
    for x in range(width):
        # Create a hotspot in the upper right quadrant
        distance = np.sqrt((x - 300)**2 + (y - 100)**2)
        
        if distance < 50:
            # Hot spot (red/yellow)
            intensity = int(max(0, 255 - distance * 3))  # Convert to int
            draw.point((x, y), fill=(intensity, intensity // 2, 0))
        else:
            # Background gradient (blue to green to yellow)
            gradient = int(255 * (1 - y / height))
            if y < height // 3:
                # Blue to cyan
                draw.point((x, y), fill=(0, gradient, 255 - gradient // 2))
            elif y < 2 * height // 3:
                # Cyan to green
                draw.point((x, y), fill=(0, 255 - gradient // 2, gradient // 2))
            else:
                # Green to yellow
                draw.point((x, y), fill=(gradient, 255 - gradient // 2, 0))

# Save the image
image.save('media/thermal_images/sample_thermal.png')
print("Sample thermal image created at 'media/thermal_images/sample_thermal.png'")
