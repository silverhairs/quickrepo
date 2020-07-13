import urllib.request
import json

current = "1.0.5"

response = urllib.request.urlopen(
    "http://pypi.python.org/pypi/quickrepo/json?callback=?"
)
data = json.load(response)
latest = data["info"]["version"]

current_int = int(current.replace(".", ""))
latest_int = int(latest.replace(".", ""))


def upgrade_alert():
    if latest_int > current_int:
        return "New version available, run pip install --upgrade quickrepo to upgrade"

