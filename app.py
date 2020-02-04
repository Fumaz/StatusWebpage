from flask import Flask

import api
app = Flask(__name__)


@app.route('/')
def hello_world():
    return api.get_monitors()


if __name__ == '__main__':
    app.run()
