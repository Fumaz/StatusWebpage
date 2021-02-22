import requests

import config
from card import Monitor, Subcard, get_status_name, get_status_color

BASE_URL = "https://api.uptimerobot.com/v2/"


def default_params() -> dict:
    return {'api_key': config.UPTIMEROBOT_KEY, 'format': 'json', 'logs': 1}


def create_params(params: dict) -> str:
    params = default_params() | params
    string = ""

    for k, v in params.items():
        string += k + "=" + str(v) + "&"  # I hate this API, you can't send the params in any other way ._.

    return string[:-1]


def request(url, params):
    payload = create_params(params)
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'cache-control': 'no-cache'
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    return response.json()


def urlify(endpoint):
    return BASE_URL + endpoint


def get_account():
    url = urlify("getAccountDetails")
    return request(url, {})


def get_monitors(state=None):
    url = urlify("getMonitors")
    params = {'statuses': state} if state is not None else {}
    params['custom_uptime_ratios'] = '30'

    return request(url, params)


def get_formatted_monitors(state=None):
    result = get_monitors(state)
    data = {'status': result['stat'], 'monitors': []}

    for monitor in result['monitors']:
        data['monitors'].append({'id': monitor['id'],
                                 'name': monitor['friendly_name'],
                                 'url': monitor['url'],
                                 'uptime': monitor.get('all_time_uptime_ratio', monitor.get('custom_uptime_ratio')),
                                 'status': monitor['status']})

    return data


def get_pretty_monitors(state=None):
    result = get_monitors(state)
    monitors = {'status': result['stat'], 'cards': []}

    for monitor in result['monitors']:
        mon = Monitor(monitor['id'], monitor['friendly_name'], monitor['url'])
        sub = Subcard(mon.name, mon,
                      monitor.get('all_time_uptime_ratio', monitor.get('custom_uptime_ratio')),
                      get_status_name(monitor['status']),
                      get_status_color(monitor['status']))

        if sub.name.strip():
            monitors['cards'].append(sub)

    return monitors
