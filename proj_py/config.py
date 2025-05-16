import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'bmw')

# Create output directories if they don't exist
os.makedirs(os.path.join(OUTPUT_DIR, 'batch_2'), exist_ok=True)

# File paths
PROGRESS_FILE = os.path.join(OUTPUT_DIR, 'progress.json')

# User agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
]

# Desired parameter IDs for data collection
DESIRED_PARAM_IDS = {
    "Price_Leasing", "Term", "DepositAmountLeasing",
    "MonthlyPaymentWithoutServices", "Mileage", "TotalPaymentWithoutServices",
    "Price", "CreditAmount", "DepositAmount", "NominalInterestRate", "InterestRate",
    "MonthlyPayment_Ziel", "TotalCredit", "BallonAmount"
}

# Dropdown order for configuration
DROPDOWN_ORDER = [
    "Weitere Finanzierungs- und Leasingbeispiele:",
    "Laufzeit",
    "Laufleistung p.a."
]

# Base URL
BASE_URL = "https://www.bmw.de/de/konfigurator.html" 