import requests
import json

def test_get():
    response = requests.get('http://localhost:8000/Europe/Moscow')
    print('GET /Europe/Moscow:', response.text)

    response = requests.get('http://localhost:8000/')
    print('GET /:', response.text)

def test_post_convert():
    data = {
        'date': '12.20.2021 22:21:05',
        'tz': 'EST',
        'target_tz': 'Europe/Moscow'
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://localhost:8000/api/v1/convert', data=json.dumps(data), headers=headers)
    print('POST /api/v1/convert:', response.text)

def test_post_datediff():
    data = {
        'first_date': '12.06.2024 22:21:05',
        'first_tz': 'EST',
        'second_date': '12.30.2024 12:30:00',
        'second_tz': 'Europe/Moscow'
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://localhost:8000/api/v1/datediff', data=json.dumps(data), headers=headers)
    print('POST /api/v1/datediff:', response.text)

test_get()
test_post_convert()
test_post_datediff()