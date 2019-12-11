DOMAIN = "hasslingbank"
DOMAIN_DATA = "{}_data".format(DOMAIN)

PLATFORMS = ["sensor"]
REQUIRED_FILES = ["const.py", "manifest.json", "sensor.py"]
VERSION = "0.0.1"
ISSUE_URL = ""

STARTUP = """
-------------------------------------------------------------------
{name}
Version: {version}
This is a custom component
If you have any issues with this you need to open an issue here:
{issueurl}
-------------------------------------------------------------------
"""

CATEGORY_ERROR = """ TODO """

DEFAULT_NAME = "starling"
DEFAULT_ACCOUNT = "first"
DEFAULT_CURRENCY = "£"

ICON = "mdi:finance"

CONF_NAME = "name"
CONF_ENABLED = "enabled"
CONF_SENSOR = "sensor"
