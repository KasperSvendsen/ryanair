import requests
from datetime import datetime, timedelta
from collections import defaultdict
from openpyxl import Workbook

# Configuration variables
DEPARTURE_AIRPORT_CODE = 'CPH'
START_DATE = '2024-09-01'
END_DATE = '2024-09-30'
MIN_VACATION_LENGTH = 4
MAX_VACATION_LENGTH = 6
CURRENCY = 'DKK'
OUTPUT_FILE = 'cheapest_round_trips.xlsx'

def get_possible_destinations(departure_airport_code):
    url = f'https://www.ryanair.com/api/views/locate/searchWidget/routes/da/airport/{departure_airport_code}'
    response = requests.get(url)
    print(f"Fetching possible destinations from {departure_airport_code}...")
    if response.status_code == 200:
        print("Successfully fetched destinations.")
        return response.json()
    else:
        print(f"Failed to fetch destinations: {response.status_code}")
        return []

def get_cheapest_tickets(departure_airport_code, arrival_airport_code, start_date, end_date, currency):
    url = f'https://www.ryanair.com/api/farfnd/v4/oneWayFares/{departure_airport_code}/{arrival_airport_code}/cheapestPerDay?outboundMonthOfDate={start_date}&currency={currency}&promoCode='
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

def process_fares(tickets):
    fares = defaultdict(lambda: {'price': float('inf'), 'unavailable': True, 'soldOut': True})
    if 'outbound' in tickets and 'fares' in tickets['outbound']:
        for fare in tickets['outbound']['fares']:
            fares[fare['day']] = fare
    return fares

def find_cheapest_round_trip(departure_airport_code, start_date, end_date, min_vacation_length, max_vacation_length, currency):
    print(f"Finding cheapest round trips from {departure_airport_code} between {start_date} and {end_date} with vacation length between {min_vacation_length} and {max_vacation_length} days...")
    destinations = get_possible_destinations(departure_airport_code)
    results = []

    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

    for destination in destinations:
        arrival_airport_code = destination['arrivalAirport']['code']
        print(f"Evaluating destination: {arrival_airport_code}")

        outbound_tickets = get_cheapest_tickets(departure_airport_code, arrival_airport_code, start_date, end_date, currency)
        return_tickets = get_cheapest_tickets(arrival_airport_code, departure_airport_code, start_date, end_date, currency)

        outbound_fares = process_fares(outbound_tickets)
        return_fares = process_fares(return_tickets)

        results.extend(find_trips(destination, outbound_fares, return_fares, start_date_dt, end_date_dt, min_vacation_length, max_vacation_length, currency))

    return sorted(results, key=lambda x: x['total_price'])

def find_trips(destination, outbound_fares, return_fares, start_date_dt, end_date_dt, min_vacation_length, max_vacation_length, currency):
    trips = []
    for outbound_date in (start_date_dt + timedelta(n) for n in range((end_date_dt - start_date_dt).days + 1)):
        outbound = outbound_fares[outbound_date.strftime("%Y-%m-%d")]
        if outbound['unavailable'] or outbound['soldOut']:
            continue

        for days in range(min_vacation_length, max_vacation_length + 1):
            return_date = outbound_date + timedelta(days=days)
            if return_date > end_date_dt:
                continue

            return_ticket = return_fares[return_date.strftime("%Y-%m-%d")]
            if return_ticket['unavailable'] or return_ticket['soldOut']:
                continue

            total_price = outbound['price']['value'] + return_ticket['price']['value']

            trips.append({
                'destination': destination['arrivalAirport']['name'],
                'outbound_date': outbound_date.strftime("%Y-%m-%d"),
                'return_date': return_date.strftime("%Y-%m-%d"),
                'total_price': round(total_price, 2),
                'currency': currency
            })
    return trips

def save_results_to_xlsx(results, filename):
    if not results:
        print("No results to save.")
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Cheapest Round Trips"

    headers = list(results[0].keys())
    ws.append(headers)

    for result in results:
        ws.append(list(result.values()))

    wb.save(filename)
    print(f"Results saved to {filename}")

def main():
    cheapest_round_trips = find_cheapest_round_trip(DEPARTURE_AIRPORT_CODE, START_DATE, END_DATE, MIN_VACATION_LENGTH, MAX_VACATION_LENGTH, CURRENCY)
    
    if cheapest_round_trips:
        print("Cheapest round trips:")
        for trip in cheapest_round_trips:
            print(f"Destination: {trip['destination']}, Outbound: {trip['outbound_date']}, Return: {trip['return_date']}, Total Price: {trip['total_price']} {trip['currency']}")
        save_results_to_xlsx(cheapest_round_trips, OUTPUT_FILE)
    else:
        print("No round trips found.")

if __name__ == "__main__":
    main()