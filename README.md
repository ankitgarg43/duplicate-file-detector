# Duplicate File Detector

A modern, cross-platform desktop application for detecting and managing duplicate files with an intuitive user interface.

## Features

- Advanced file scanning and comparison using SHA-256 hashing
- Real-time progress tracking with a modern UI
- Multiple file selection and management options
- Backup functionality for safe file management
- Export capabilities (JSON/CSV formats)
- Cross-platform compatibility

## Requirements

- Python 3.11 or higher
- Required packages are listed in pyproject.toml

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/duplicate-file-detector.git
cd duplicate-file-detector
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

1. Click "Browse" to select a directory to scan
2. Click "Scan" to start searching for duplicates
3. Review the results in the tree view
4. Select files and use the action buttons to:
   - Delete selected files
   - Move files to backup location
   - Export report in JSON/CSV format

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
