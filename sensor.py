"""Support for Freebox devices (Freebox v6 and Freebox mini 4K)."""
import logging

from homeassistant.helpers.entity import Entity

from . import DATA_FREEBOX

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensors."""
    fbx = hass.data[DATA_FREEBOX]
    async_add_entities([FbxRXSensor(fbx), FbxTXSensor(fbx), FbxCpuBTemp(fbx), FbxCpuMTemp(fbx), FbxSwitchTemp(fbx)], True)


class FbxConnSensor(Entity):
    """Representation of a freebox sensor."""

    _name = "generic"

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

    async def async_update(self):
        """Fetch status from freebox."""
        self._datas = await self._fbx.connection.get_status()

class FbxSysSensor(Entity):
    """Representation of a freebox system sensor."""

    _name = "generic"

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
    def device_class(self):
        """Returns the device class."""
        return self._device_class

    @property
    def unit_of_measurement(self):
        """Returns unit of measeurement."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch status from freebox."""
        self._datas = await self._fbx.system.get_config()

class FbxCpuBTemp(FbxSysSensor):
    """Update the system sensor."""
    _name = "Freebox CPUB Temperature"
    _device_class = "temperature"
    _unit_of_measurement = "°C"
    
    async def async_update(self):
        """Get value from fetched datas."""
        await super().async_update()
        if self._datas is not None:
            self._state = self._datas["temp_cpub"]

class FbxCpuMTemp(FbxSysSensor):
    """Update the system sensor."""
    _name = "Freebox CPUM Temperature"
    _device_class = "temperature"
    _unit_of_measurement = "°C"
    
    async def async_update(self):
        """Get value from fetched datas."""
        await super().async_update()
        if self._datas is not None:
            self._state = self._datas["temp_cpum"]

class FbxSwitchTemp(FbxSysSensor):
    """Update the system sensor."""
    _name = "Freebox switch Temperature"
    _device_class = "temperature"
    _unit_of_measurement = "°C"
    
    async def async_update(self):
        """Get value from fetched datas."""
        await super().async_update()
        if self._datas is not None:
            self._state = self._datas["temp_sw"]

class FbxConnState(FbxConnSensor):
    """Update The connection status sensor."""
    
    _name = "Freebox connection status"
    
    async def async_update(self):
        """Get the value from fetched datas."""
        await super().async_update()
        if self._datas is not None:
            self._state = self._datas["state"]

class FbxRXSensor(FbxConnSensor):
    """Update the Freebox RxSensor."""

    _name = "Freebox download speed"
    _unit = "KB/s"

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

    @property
    def unit_of_measurement(self):
        """Define the unit."""
        return self._unit

    async def async_update(self):
        """Get the value from fetched datas."""
        await super().async_update()
        if self._datas is not None:
            self._state = round(self._datas["rate_up"] / 1000, 2)
