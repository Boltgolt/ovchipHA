"""
OV-chipkaart binary sensor.

Exposes the current check-in status though a binary sensor.
"""
import logging
from datetime import timedelta

from homeassistant.components.binary_sensor import BinarySensorDevice
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=2)
OVCHIP_HANDLE = 'ovchip_handle'


def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Setup sensor."""
    _LOGGER.warning(hass.data[OVCHIP_HANDLE])

    devices = []
    cards = hass.data[OVCHIP_HANDLE].get_cards_list()

    for card in cards:
        devices.append(OvchipSensor(hass, card['mediumId']))

    add_devices_callback(devices, True)

class OvchipSensor(BinarySensorDevice):
    """Representation of a sensor."""
    def __init__(self, hass, id):
        """Initialize the sensor."""
        self._id = id
        self._name = "ovchip_" + '-'.join([id[i:i+4] for i in range(0, len(id), 4)])
        self._state = True
        self._icon = "mdi:credit-card"
        self.ovchip = hass.data[OVCHIP_HANDLE]

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def is_on(self):
        """Return the status of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the mdi icon of the sensor."""
        return self._icon

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Update sensor state."""
        _LOGGER.warning("update")
        transactions = self.ovchip.get_transaction_list(self._id)

        if len(transactions) == 0:
            self._state = False
        elif transactions[0]["transactionName"] == "Check-in":
            self._state = True
        else:
            self._state = False
