# BMW Configuration Scraper

This project scrapes BMW car configuration data from the German BMW website. It collects information about different car models, their configurations, and pricing options.

## Features

- Scrapes all BMW car models from the German configurator
- Handles cookie consent popups automatically
- Saves progress to resume scraping if interrupted
- Exports data to CSV files organized by model
- Rotates user agents to avoid detection
- Handles shadow DOM elements

## Requirements

- Python 3.7+
- Chrome browser installed
- Required Python packages (install using `pip install -r requirements.txt`):
  - pandas
  - numpy
  - selenium
  - beautifulsoup4
  - webdriver-manager

## Installation

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the scraper using:

```bash
python main.py
```

The script will:
1. Start scraping from the BMW German configurator
2. Save progress automatically
3. Create CSV files in the `output/bmw/batch_2/` directory
4. Can be safely interrupted (Ctrl+C) and resumed later

## Output

The script creates CSV files in the `output/bmw/batch_2/` directory, with one file per model. Each file contains:
- Model information
- Configuration options
- Pricing details
- Financing options
- Country information
- Source URL

## Project Structure

- `main.py`: Entry point for running the scraper
- `scraper.py`: Contains the main scraping logic
- `config.py`: Configuration settings and constants
- `requirements.txt`: Required Python packages
- `output/bmw/batch_2/`: Directory for output files
- `output/bmw/progress.json`: Progress tracking file

## Notes

- The script includes delays to avoid overwhelming the server
- User agents are rotated to avoid detection
- Progress is saved after each model is processed
- The script can be safely interrupted and resumed 