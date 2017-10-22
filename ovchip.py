"""
OV-chipkaart status support.

Exposes the current check-in status though a binary sensor.
"""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import load_platform
from homeassistant.const import (CONF_USERNAME, CONF_PASSWORD)

from ovstat.OvApi import OvApi

REQUIREMENTS = ['ovchipapi==1.1']

_LOGGER = logging.getLogger(__name__)

OVCHIP_HANDLE = 'ovchip_handle'
DOMAIN = 'ovchip'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string
    })
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    """Setup ovchip."""

    # TODO: Catch auth exception
    try:
        hass.data[OVCHIP_HANDLE] = OvApi(config['ovchip']['username'], config['ovchip']['password'])
    except Exception as e:
        raise


    load_platform(hass, "binary_sensor", DOMAIN, {}, config)

    # Initialization successfull
    return True
