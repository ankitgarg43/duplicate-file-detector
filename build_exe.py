import PyInstaller.__main__
import os
import sys
import platform

def build_executable():
    # Base configuration for PyInstaller
    options = [
        'main.py',  # Main script
        '--name=DuplicateFileDetector',  # Name of the executable
        '--clean',  # Clean PyInstaller cache
        '--add-data=README.md:.',  # Include README
    ]

    # Platform-specific configurations
    if platform.system() == 'Windows':
        options.extend([
            '--windowed',  # No console window
            '--icon=generated-icon.ico',  # Windows icon
            '--noconsole',
        ])
    elif platform.system() == 'Darwin':  # macOS
        options.extend([
            '--windowed',
            '--icon=generated-icon.icns',  # macOS icon
            '--target-arch=universal2',  # Support both Intel and Apple Silicon
        ])
    else:  # Linux
        options.extend([
            '--icon=generated-icon.png'
        ])

    # Add one-file mode last to ensure proper packaging
    options.append('--onefile')

    # Run PyInstaller
    PyInstaller.__main__.run(options)

if __name__ == "__main__":
    print(f"Building executable for {platform.system()}...")
    build_executable()
    print("Build complete! Check the 'dist' directory for your executable.")