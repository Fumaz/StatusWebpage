import requests

import config

BASE_URL = "https://api.uptimerobot.com/v2/"


def get_params(params):
    string = f"api_key={config.API_KEY}&format=json&logs=1"
    for key, value in params.items():
        string += "&" + key + "=" + value

    return string


def request(url, params):
    payload = get_params(params)
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'cache-control': 'no-cache'
    }

    print(payload)
    print(url)
    print(url + payload)
    response = requests.request("POST", url, data=payload, headers=headers)

    return response.text


def urlify(endpoint):
    return BASE_URL + endpoint


def get_account():
    url = urlify("getAccountDetails")
    return request(url, {})


def get_monitors(state=None):
    url = urlify("getMonitors")
    params = {'statuses': state} if state is not None else {}
    params['all_time_uptime_ratio'] = '1'

    return request(url, params)
