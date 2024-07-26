import requests
from datetime import datetime, timedelta
import os

def parse_sunset_time(sunset_time_str):
    return datetime.strptime(sunset_time_str, '%I:%M:%S %p')

def get_sunset_time():
    url = "https://api.sunrisesunset.io/json"
    params = {
        'lat': 40.7128,  # Latitude for NYC
        'lng': -74.0060, # Longitude for NYC
        'timezone': "America/New_York"
    }
    response = requests.get(url, params=params)
    sunset_time_str = response.json()['results']['sunset']
    sunset_datetime = parse_sunset_time(sunset_time_str)
    return sunset_datetime

def send_pushover_notification(user_key, app_token, message):
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": app_token,
        "user": user_key,
        "message": message,
        "title": "Sunset Alert"
    }
    response = requests.post(url, data=data)
    print(response.text)

def main():
    sunset_time = get_sunset_time()
    current_time = datetime.now()
    best_time = sunset_time - timedelta(hours=1)  
    print(f"Current time: {current_time}, Sunset time: {sunset_time.strftime('%I:%M %p')}, Best time for a reminder: {best_time.strftime('%I:%M %p')}")
    message = f"Sunset is at {sunset_time.strftime('%I:%M %p')} today. You should go for your run today at {best_time.strftime('%I:%M %p')}"
    send_pushover_notification(os.environ.get('PUSHOVER_USER_KEY'), os.environ.get('PUSHOVER_APP_TOKEN'), message)
    

if __name__ == "__main__":
    main()