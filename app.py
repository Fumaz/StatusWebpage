import json

from flask import Flask, render_template, jsonify, request, abort

import uptimeapi
from card import Status, Monitor, Subcard, Card

app = Flask(__name__)
categories = (
    ('System Node', '| SYS'),
    ('Services Node', '| SERVICE'),
    ('Bots Node', '| BOT'),
    ('Userbots Node', '| USERBOT'),
    ('Web Node', '| WEB'),
    ('Database Node', '| DB'),
    ('Minecraft Node', '| MC'),
    ('Misc Node', '')
)


def get_api_monitors():
    result = json.loads(uptimeapi.get_monitors())
    data = {'status': result['stat'], 'monitors': []}

    for monitor in result['monitors']:
        data['monitors'].append({'id': monitor['id'],
                                 'name': monitor['friendly_name'],
                                 'url': monitor['url'],
                                 'uptime': monitor.get('all_time_uptime_ratio', monitor.get('custom_uptime_ratio')),
                                 'status': monitor['status']})

    return data


def get_monitors():
    result = json.loads(uptimeapi.get_monitors())
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


def get_status_name(status):
    if status == 2 or status == 0:
        return "Operational"
    else:
        return "Offline"


def get_status_color(status):
    if status == 2 or status == 0:
        return "success"
    else:
        return "danger"


def get_status(monitors):
    if monitors['status'] == 'ok':
        if all(card.status_color == 'success' for card in monitors['cards']):
            return Status('success', 'All systems are online and operational.')
        else:
            return Status('warning', 'Some systems are undergoing problems.')
    else:
        return Status('danger', 'All systems are undergoing problems.')


def get_cards(monitors):
    cards = [Card(name=name, suffix=suffix) for name, suffix in categories]
    for subcard in monitors['cards']:
        for card in cards:
            if card.should(subcard.name):
                subcard.name = subcard.name[:-len(card.suffix)]
                card.subcards.append(subcard)
                break

    for card in cards:
        if len(card.subcards) < 1:
            cards.remove(card)
            continue

        success = all(subcard.status == 'Operational' for subcard in card.subcards)
        if success:
            card.status = 'All systems are online and operational.'
            card.status_color = 'success'
        else:
            card.status = 'Some systems are undergoing problems.'
            card.status_color = 'warning'

        card.update()

    return cards


@app.route('/')
def display():
    monitors = get_monitors()
    cards = get_cards(monitors)
    status = get_status(monitors)

    return render_template('index.html', status=status, cards=cards)


@app.route('/api/getMonitors')
def api():
    if request.args.get('api_key', '') != '3Qyc2x7RF6WkjzaqVQiAC76z9rx':
        return abort(403)

    monitors = get_api_monitors()

    return jsonify(**monitors)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
