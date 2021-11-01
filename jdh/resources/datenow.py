import requests

url = 'http://worldtimeapi.org/api/timezone/America/Mexico_City'


def today():
    response = requests.get(url).json()
    return response['datetime'][:10]


def day_of_week():
    response = requests.get(url).json()
    return response['day_of_week']