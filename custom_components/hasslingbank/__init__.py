"""Starling Bank Integration."""

import logging
import os
from datetime import timedelta, date
import requests
import json

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_API_KEY
from homeassistant.helpers import discovery
from homeassistant.util import Throttle

import voluptuous as vol

from .const import (
    CONF_NAME,
    DEFAULT_NAME,
    DEFAULT_CURRENCY,
    DOMAIN,
    DOMAIN_DATA,
    ISSUE_URL,
    PLATFORMS,
    REQUIRED_FILES,
    STARTUP,
    VERSION
)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=300)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_API_KEY): cv.string,
                vol.Optional(CONF_NAME, default = DEFAULT_NAME): cv.string,
                vol.Optional("currency", default = DEFAULT_CURRENCY): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    # startup message
    startup = STARTUP.format(name = DOMAIN, version = VERSION, issueurl = ISSUE_URL)
    _LOGGER.info(startup)

    # check all required files
    file_check = await check_files(hass)
    if not file_check:
        return False

    url_check = await check_url()
    if not url_check:
        return False

    # create data dictionary
    hass.data[DOMAIN_DATA] = {}
    hass.data[DOMAIN_DATA]["client"] = StarlingData(hass, config)

    # load platforms
    for platform in PLATFORMS:
        # get platform specific configuration
        platform_config = config[DOMAIN]

        hass.async_create_task(
            discovery.async_load_platform(
                hass, platform, DOMAIN, platform_config, config
            )
        )

    return True


class StarlingData:
    def __init__(self, hass, config):
        """Initialize the class."""
        self.hass = hass
        self.api_key = config[DOMAIN].get(CONF_API_KEY)
        self.budget = config[DOMAIN].get("budget")
        self.categories = config[DOMAIN].get("categories")
        self.base_url = "https://api.starlingbank.com/api/v2"

    def make_request(self, endpoint: str):
        request_url = f"{self.base_url}{endpoint}"
        auth_header = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.get(request_url, headers = auth_header)
        return response.status_code, json.loads(response.text)

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def update_data(self):
        """Update data."""

        # get account id
        response = self.make_request("/accounts")
        if response[0] != 200:
            _LOGGER.error("Unable to get accounts from Starling API")
            return
        account_id = response[1]["accounts"][0]["accountUid"]

        # get account balance
        response = self.make_request(f"/accounts/{account_id}/balance")
        if response[0] != 200:
            _LOGGER.error("Unable to get balance from Starling API")
            return
        account_balance = float(response[1]["availableToSpend"]["minorUnits"]) / 100
                
        # set account balance data
        self.hass.data[DOMAIN_DATA]["account_balance"] = account_balance
        _LOGGER.debug(f"Recieved data for: account balance: {account_balance}")


async def check_files(hass):
    """Return bool that indicates if all files are present."""
    base = "{}/custom_components/{}/".format(hass.config.path(), DOMAIN)
    missing = []
    for file in REQUIRED_FILES:
        fullpath = "{}{}".format(base, file)
        if not os.path.exists(fullpath):
            missing.append(file)

    if missing:
        _LOGGER.critical("The following files are missing: %s", str(missing))
        returnvalue = False
    else:
        returnvalue = True

    return returnvalue


async def check_url():
    """Return a bool that indicates Starling v2 API is accessible"""
    url = "https://api.starlingbank.com/api/v2/accounts"
    response = requests.get(url)

    result = False

    if response.status_code != 404:
        _LOGGER.info(f"Connection with Starling Bank API established with code {response.status_code}")
        result = True
    else:
        _LOGGER.error(f"Unable to establish connection with Starling Bank API, status code: {response.status_code}")
        result = False

    return result
