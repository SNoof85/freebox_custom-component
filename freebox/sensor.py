"""Support for Freebox devices (Freebox v6 and Freebox mini 4K)."""
import logging

from homeassistant.helpers.entity import Entity

from . import DATA_FREEBOX

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensors."""
    fbx = hass.data[DATA_FREEBOX]
    sys_config = await fbx.system.get_config()
    fbx_sensors = []
    for temp_sensor_id in sys_config['sensors']:
        fbx_sensors.append(FbxTempSensor(fbx, temp_sensor_id['id']))

    fbx_sensors.extend([FbxRXSensor(fbx), FbxTXSensor(fbx)])
    async_add_entities(fbx_sensors, True)

class FbxTempSensor(Entity):

    def __init__(self, fbx, sensor_id):
        self._fbx = fbx
        self._datas = None
        self._state = None
        self._sensor_id = sensor_id
        self._unit_of_measurement = "°C"

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    async def async_update(self):
        self._datas = await self._fbx.system.get_config()
        for temp_sensor in self._datas['sensors']:
            if temp_sensor['id'] == self._sensor_id:
                self._name = "Freebox "+temp_sensor['name']
                self._state = temp_sensor['value']

class FbxConnSensor(Entity):
    """Representation of a freebox sensor."""

    _name = "generic"
    _unit = None
    _icon = None

    def __init__(self, fbx):
        """Initialize the sensor."""
        self._fbx = fbx
        self._state = None
        self._datas = None

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
        """Return the unit of the sensor."""
        return self._unit

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    async def async_update(self):
        """Fetch status from freebox."""
        self._datas = await self._fbx.connection.get_status()


class FbxRXSensor(FbxConnSensor):
    """Update the Freebox RxSensor."""

    _name = "Freebox download speed"
    _unit = "KB/s"
    _icon = "mdi:download-network"

    @property
    def unit_of_measurement(self):
        """Define the unit."""
        return self._unit

    async def async_update(self):
        """Get the value from fetched datas."""
        await super().async_update()
        if self._datas is not None:
            self._state = round(self._datas["rate_down"] / 1000, 2)


class FbxTXSensor(FbxConnSensor):
    """Update the Freebox TxSensor."""

    _name = "Freebox upload speed"
    _unit = "KB/s"
    _icon = "mdi:upload-network"

    @property
    def unit_of_measurement(self):
        """Define the unit."""
        return self._unit

    async def async_update(self):
        """Get the value from fetched datas."""
        await super().async_update()
        if self._datas is not None:
            self._state = round(self._datas["rate_up"] / 1000, 2)
