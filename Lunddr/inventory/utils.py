# sms_service.py
import requests

def send_sms(phone_number, message):
    """
    Sends an SMS to a Nigerian phone number using BulkSMS Nigeria API.
    
    :param phone_number: The recipient's phone number (e.g., "07012345678").
    :param message: The SMS message to send.
    :return: API response.
    """
    # BulkSMS Nigeria API details
    api_token = "rk4FZbkGhg6w7Lz0v0Z8GJAkcvL85ZsZnKMdWNQ9IGHBsBYOHUJopgcdpzoo"  # Replace with your actual API token
    url = "https://www.bulksmsnigeria.com/api/v1/sms/create"

    # Prepare the payload
    payload = {
        "api_token": api_token,
        "to": phone_number,
        "from": "LaundryApp",  # Sender ID (optional, but recommended)
        "body": message,
        "dnd": 2  # Do Not Disturb setting (optional)
    }

    # Send the request
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Return the API response
    except requests.exceptions.RequestException as e:
        print(f"Failed to send SMS: {e}")
        return None