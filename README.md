# Ryanair Cheapest Round Trip Finder

This project helps you find the cheapest round trips from a specified departure airport within a given date range and vacation length. The results are saved to an Excel file.

## Features

- Fetch possible destinations from a given departure airport.
- Find the cheapest round trips within a specified date range and vacation length.
- Save the results to an Excel file.

## Requirements

- Python 3.x
- Requests library
- Openpyxl library

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/KasperSvendsen/ryanair.git
    cd ryanair
    ```

2. Set up a virtual environment (optional but recommended):

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required libraries:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Update the configuration variables in `run.py` as needed:

    ```python
    DEPARTURE_AIRPORT_CODE = 'CPH'
    START_DATE = '2024-09-01'
    END_DATE = '2024-09-30'
    MIN_VACATION_LENGTH = 4
    MAX_VACATION_LENGTH = 6
    CURRENCY = 'DKK'
    OUTPUT_FILE = 'cheapest_round_trips.xlsx'
    ```

2. Run the script:

    ```sh
    python run.py
    ```

3. The results will be saved to the specified output file (e.g., `cheapest_round_trips.xlsx`).