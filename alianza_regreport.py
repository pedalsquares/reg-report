import csv
import json
import logging
import getpass
import requests
from datetime import datetime
import sys

# Variables for the API
PartitionId = 'REPLACE-WITH-YOUR-ID'  # Replace with your actual partition ID


def authenticate():
    while True:
        username = input("Enter your Alianza Admin username: ")
        password = getpass.getpass("Enter your Alianza Admin password: ")

        url = "https://api.alianza.com/v2/authorize"

        data = {"username": username, "password": password}

        # Send POST request with credentials
        response = requests.post(url, json=data)

        # Check for successful login (200 status code)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            XAuthToken = response_data['authToken']

            if XAuthToken:
                print("Login successful!")
                return XAuthToken
            else:
                print("Error: X-AUTH-TOKEN not found in response.")
        else:
            print("Login failed. Please try again.")


# Get the account ID from the account number
def get_account_id(account_number, headers):
    try:
        url = f'https://api.alianza.com/v2/partition/{PartitionId}/account/{account_number}?accountIdType=AccountNumber'
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        
        return response.json().get('id')
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to retrieve account ID for account number {account_number}. Error: {e}")
        return None

# Get the device ID from the accountId, MAC address, and line number
def get_device_id(account_id, mac_address, line_number, headers):
    try:
        url = f'https://api.alianza.com/v2/partition/{PartitionId}/account/{account_id}/device/{mac_address}'
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        response_data = response.json()
        # Check if the response is a list and match the device by line number
        if isinstance(response_data, list):
            for device in response_data:
                if device.get("lineNumber") == line_number:
                    return device.get("id")
            print(f"Warning: No device found with line number {line_number} for MAC address {mac_address}")
            return None
        elif isinstance(response_data, dict):
            return response_data.get('id')
        else:
            print(f"Unexpected response format for device data: {response_data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to retrieve device ID for MAC address {mac_address}. Error: {e}")
        return None

# Get the device registration status
def get_registration_status(account_id, device_id, headers):
    try:
        url = f'https://api.alianza.com/v2/partition/{PartitionId}/account/{account_id}/deviceline/{device_id}/registrationstatus'
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json().get('registered', False)
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to retrieve registration status for device ID {device_id}. Error: {e}")
        return None

# Main - process input CSV and output results to CSV reoport
def main():
    if len(sys.argv) != 2:
        print("Usage: python alianza_regreport.py <inputfile>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = f"{input_file.split('.')[0]}_REPORT_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    XAuthToken = authenticate()
    
    if XAuthToken:
        headers = {
            'X-AUTH-TOKEN': XAuthToken,
            'Content-Type': 'application/json'
        }
        try:
            with open(input_file, mode='r') as csvfile, open(output_file, mode='w', newline='') as outfile:
                reader = csv.DictReader(csvfile)
                fieldnames = ['accountNumber', 'macAddress', 'lineNumber', 'deviceStatus']
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

                for row in reader:
                    account_number = row['accountNumber']
                    mac_address = row['macAddress']
                    line_number = int(row['lineNumber'])

                    # Get account ID
                    account_id = get_account_id(account_number, headers)
                    if not account_id:
                        device_status = "Account Not Found"
                        writer.writerow({
                            'accountNumber': account_number,
                            'macAddress': mac_address,
                            'lineNumber': line_number,
                            'deviceStatus': device_status
                        })
                        continue

                    # Get device ID
                    device_id = get_device_id(account_id, mac_address, line_number, headers)
                    if not device_id:
                        device_status = "Device Not Found"
                        writer.writerow({
                            'accountNumber': account_number,
                            'macAddress': mac_address,
                            'lineNumber': line_number,
                            'deviceStatus': device_status
                        })
                        continue

                    # Get registration status
                    registered = get_registration_status(account_id, device_id, headers)
                    device_status = 'Registered' if registered else 'NOT Registered'
                
                    # Write output to screen
                    print(f"Account: {account_number}, MAC: {mac_address}, Status: {device_status}")

                    # Write the row to output csv file
                    writer.writerow({
                        'accountNumber': account_number,
                        'macAddress': mac_address,
                        'lineNumber': line_number,
                        'deviceStatus': device_status 
                    })

            print(f"Report generated successfully: {output_file}")

        except FileNotFoundError:
            print(f"Error: File {input_file} not found.")
        except PermissionError:
            print(f"Error: Permission denied for file {input_file} or {output_file}.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
