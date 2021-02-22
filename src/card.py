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


class Monitor:
    def __init__(self, monitor_id, name, url):
        self.monitor_id = monitor_id
        self.name = name
        self.url = url


class Card:
    def __init__(self, name: str, suffix: str, subcards: list = None, status=None, status_color=None):
        if subcards is None:
            subcards = []

        if status is None:
            status = "System operational."

        if status_color is None:
            status_color = "success"

        self.name = name
        self.suffix = suffix
        self.subcards = subcards
        self.status = status
        self.status_color = status_color
        self.friendly_name = name.split(' ')[0]
        self.status_c2 = '#7ED321' if status_color == 'success' else 'red'

    def should_contain(self, name: str) -> bool:
        return name.lower().endswith(self.suffix.lower())

    def update(self):
        self.status_c2 = '#7ED321' if self.status_color == 'success' else '#FFBD55'


class Subcard:
    def __init__(self, name: str, monitor: Monitor, uptime_ratio: str = "100.00", status="System operational.",
                 status_color="success"):
        if len(uptime_ratio.split('.', 2)[1]) > 2:
            uptime_ratio = uptime_ratio.replace(uptime_ratio.split('.', 2)[1], uptime_ratio.split('.', 2)[1][:2])

        uptime_ratio = uptime_ratio + "%"

        self.name = name
        self.status = status
        self.status_color = status_color
        self.monitor = monitor
        self.uptime_ratio = uptime_ratio
        self.status_c2 = '#7ED321' if status_color == 'success' else 'red'


class Status:
    def __init__(self, alert, text):
        self.alert = alert
        self.text = text
