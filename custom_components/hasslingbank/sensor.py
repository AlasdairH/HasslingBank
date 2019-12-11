"""Sensor platform for Starling Bank"""
import logging
from homeassistant.helpers.entity import Entity

from .const import CATEGORY_ERROR, DOMAIN, DOMAIN_DATA, ICON

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
):  # pylint: disable=unused-argument
    """Setup sensor platform."""
    async_add_entities([HasslingBankSensor(hass, discovery_info)], True)


class HasslingBankSensor(Entity):
    """HasslingBank Sensor class."""

    def __init__(self, hass, config):
        self.hass = hass
        self.attr = {}
        self._state = None
        self._name = config["name"]
        self._measurement = config["currency"]

    async def async_update(self):
        """Update the sensor."""
        await self.hass.data[DOMAIN_DATA]["client"].update_data()

        # set attributes
        self.attr["account_balance"] = float(self.hass.data[DOMAIN_DATA].get("account_balance"))
                    
        self._state = self.attr["account_balance"]

    @property
    def should_poll(self):
        """Return the name of the sensor."""
        return True

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        return self._measurement

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.attr
