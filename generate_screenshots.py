from PIL import Image, ImageDraw, ImageFont
import os

def create_screenshot(filename, title, size=(800, 600)):
    # Create a new image with a white background
    img = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(img)
    
    # Draw a mock window frame
    draw.rectangle([(0, 0), size], outline='#cccccc', width=2)
    draw.rectangle([(0, 0), (size[0], 40)], fill='#f0f0f0')
    
    # Add title text
    draw.text((20, 10), title, fill='black')
    
    # Save the image
    os.makedirs('screenshots', exist_ok=True)
    img.save(f'screenshots/{filename}')

def generate_all_screenshots():
    create_screenshot('main_window.png', 'Duplicate File Detector - Main Window')
    create_screenshot('scan_results.png', 'Duplicate File Detector - Scan Results')
    create_screenshot('export_options.png', 'Duplicate File Detector - Export Options')

if __name__ == '__main__':
    generate_all_screenshots()
