from PIL import Image, ImageDraw
import platform

def create_app_icon():
    # Create a 256x256 image with a white background
    size = (256, 256)
    icon = Image.new('RGBA', size, 'white')
    draw = ImageDraw.Draw(icon)
    
    # Draw a simple icon - blue circle with a checkmark
    # Circle
    circle_bounds = (20, 20, 236, 236)
    draw.ellipse(circle_bounds, fill='#2196F3')
    
    # Save for all platforms
    icon.save('generated-icon.png', 'PNG')
    
    # Windows ICO
    icon.save('generated-icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
    
    # macOS ICNS
    icon.save('generated-icon.icns', format='ICNS')

if __name__ == '__main__':
    create_app_icon()
