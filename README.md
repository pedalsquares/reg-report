# Alianza Registration Report Generator

This script is designed to interact with the Alianza API to check the registration status of devices based on account information from an input CSV file. The script retrieves and verifies device registration data, outputting a report in CSV format. 

## Table of Contents
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Script Details](#script-details)
- [Error Handling](#error-handling)

---
<br><br>
## Requirements

- Python 3.7 or higher
- The following Python libraries:
  - `csv`
  - `json`
  - `logging`
  - `getpass`
  - `requests`
  - `datetime`
  - `sys`

To install dependencies:
```bash
pip install requests
```
<br><br><br>


## Setup

1. Clone the repository or download the script.
2. Replace `PartitionId` in the script with your actual partition ID. You will find your `PartitionId` in the url path name visible in your browser when loging into the admin portal. You want the string of characters which comes immediatly after the admin.alianza.com/THIS-IS-YOUR_PARTITION-ID/accounts/recent 
![PartitionId](https://raw.githubusercontent.com/pedalsquares/reg-report/main/images/image_partitionId.png)<br>
![Variable](https://raw.githubusercontent.com/pedalsquares/reg-report/main/images/image_variable.png)

3. If your enviroment does not already have the `requests` libary, follow install dependancies step above


<br><br><br>
## Usage

Run the script using the following command:

```bash
python alianza_regreport.py <inputfile>
```

- `<inputfile>`: Path to your input CSV file with the following columns:
  - `accountNumber`: Account number associated with the device.
  - `macAddress`: MAC address of the device.
  - `lineNumber`: Line number associated with the device.
    
<br>

EXAMPLE:
```bash
python alianza_regreport.py example-input.csv
```
_Example input file showing the correct headers and a ficticious account/device/line is in repo. See file `example-input.csv`_

<br>
On execution:

1. You will be prompted to enter your Alianza Admin username and password to authenticate with the API.
2. The script will generate a report CSV file in the same directory, named `inputfilename_REPORT_<timestamp>.csv`.


<br><br><br>
## Script Details
Key Functions
- `authenticate()`: Authenticates the user with the Alianza API and retrieves an authentication token.
- `get_account_id()`: Retrieves the account ID based on the account number.
- `get_device_id()`: Fetches the device ID based on the account ID, MAC address, and line number.
- `get_registration_status()`: Checks if the device is registered.

Logging and Output
- Logging has been removed to help protect passwords that are entered from remaining in log files.
- It prints the registration status for each device to the console and writes the result to the output CSV file.

Error Handling
- `FileNotFoundError`: Triggered if the input file is not found.
- `PermissionError`: Raised if there is no permission to read the input or write to the output file.
- `requests.exceptions.RequestException`: Catches API errors related to connectivity or response issues.
