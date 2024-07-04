# Ryanair Cheapest Round Trip Finder

This project finds the cheapest round trips from a specified departure airport within a given date range and vacation length. The results are saved to an Excel file.

## Features
- Fetches possible destinations from a specified departure airport.
- Finds the cheapest round trips within a given date range and vacation length.
- Saves the results to an Excel file.

## Requirements
- Python 3.12+
- `requests`
- `openpyxl`

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/ryanair-cheapest-round-trip-finder.git
    cd ryanair-cheapest-round-trip-finder
    ```

2. **Create a virtual environment:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Modify the script parameters:**
   Edit the configuration variables at the top of `run.py` to set your preferred departure airport, date range, vacation length, and currency.

    ```python
    # Configuration variables
    DEPARTURE_AIRPORT_CODE = 'CPH'  # Change to your departure airport code
    START_DATE = '2024-09-01'       # Change to your start date
    END_DATE = '2024-09-30'         # Change to your end date
    MIN_VACATION_LENGTH = 4         # Change to your minimum vacation length in days
    MAX_VACATION_LENGTH = 6         # Change to your maximum vacation length in days
    CURRENCY = 'DKK'                # Change to your preferred currency
    OUTPUT_FILE = 'cheapest_round_trips.xlsx'  # Output file name
    ```

2. **Run the script:**

    ```sh
    python run.py
    ```

3. **Check the results:**
   The results will be saved in `cheapest_round_trips.xlsx` in the project directory.
