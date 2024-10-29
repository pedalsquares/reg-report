# Alianza Registration Report Generator

This script is designed to interact with the Alianza API to check the registration status of devices based on account information from an input CSV file. The script retrieves and verifies device registration data, outputting a report in CSV format.

## Table of Contents
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Script Details](#script-details)
- [Error Handling](#error-handling)

---

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
