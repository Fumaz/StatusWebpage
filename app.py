import json

from flask import Flask, render_template

import api
from card import Status, Monitor, Subcard, Card

app = Flask(__name__)


def get_monitors():
    result = json.loads(api.get_monitors())
    monitors = {'status': result['stat'], 'cards': []}
    for monitor in result['monitors']:
        mon = Monitor(monitor['id'], monitor['friendly_name'], monitor['url'])
        sub = Subcard(mon.name, mon, monitor['all_time_uptime_ratio'], get_status_name(monitor['status']),
                      get_status_color(monitor['status']))
        monitors['cards'].append(sub)
    return monitors


def get_status_name(status):
    if status == 2 or status == 0:
        return "Operational."
    else:
        return "Offline."


def get_status_color(status):
    if status == 2 or status == 0:
        return "success"
    else:
        return "danger"


def get_status(monitors):
    if monitors['status'] == 'ok':
        if (card.status_color == 'success' for card in monitors['cards']):
            return Status('success', 'All systems are online and operational.')
        else:
            return Status('warning', 'Some systems are undergoing problems.')
    else:
        return Status('danger', 'All systems are undergoing problems.')


def get_cards(monitors):
    cards = [Card('System node'), Card('Health node')]
    for subcard in monitors['cards']:
        if subcard.name == 'Main server node':
            cards[0].subcards.append(subcard)
        else:
            cards[1].subcards.append(subcard)

    for card in cards:
        success = (subcard.status == 'success' for subcard in card.subcards)
        if success:
            card.status = 'All systems are online and operational.'
            card.status_color = 'success'
        else:
            card.status = 'Some systems are undergoing problems.'
            card.status_color = 'warning'

    return cards


@app.route('/')
def hello_world():
    monitors = get_monitors()
    cards = get_cards(monitors)
    status = get_status(monitors)
    return render_template('index.html', status=status, cards=cards)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
