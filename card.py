class Monitor:
    def __init__(self, monitor_id, name, url):
        self.monitor_id = monitor_id
        self.name = name
        self.url = url


class Card:
    def __init__(self, name: str, subcards: [] = None, status=None, status_color=None):
        if subcards is None:
            subcards = []

        if status is None:
            status = "System operational."

        if status_color is None:
            status_color = "success"

        self.name = name
        self.subcards = subcards
        self.status = status
        self.status_color = status_color
        self.friendly_name = name.split(' ')[0]
        self.status_c2 = '#7ED321' if status_color == 'success' else 'red'


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
