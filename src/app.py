from flask import Flask, render_template, jsonify, request, abort

import card
import config
import uptimeapi
from category import Category

app = Flask(__name__)
categories = (
    Category('System Node', 'SYS'),
    Category('Services Node', 'SERVICE'),
    Category('Bots Node', 'BOT'),
    Category('Userbots Node', 'USERBOT'),
    Category('Web Node', 'WEB'),
    Category('Database Node', 'DB'),
    Category('Minecraft Node', 'MC'),
    Category('Misc Node')
)


def create_cards(monitors):
    cards = [category.create_card() for category in categories]

    for subcard in monitors['cards']:
        for card in cards:
            if card.should_contain(subcard.name):
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
    monitors = uptimeapi.get_pretty_monitors()
    cards = create_cards(monitors)
    status = card.get_status(monitors)

    return render_template('index.html', status=status, cards=cards)


@app.route('/api/getMonitors')
def api():
    if request.args.get('api_key', '') != config.API_KEY:
        return abort(403)

    monitors = uptimeapi.get_formatted_monitors()

    return jsonify(**monitors)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
