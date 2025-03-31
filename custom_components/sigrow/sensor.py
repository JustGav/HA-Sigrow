import logging
import aiohttp
import async_timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_API_KEY
from .const import DOMAIN, API_BASE

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    api_key = entry.data[CONF_API_KEY]
    headers = {"Authorization": f"Bearer {api_key}"}
    entities = []

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with async_timeout.timeout(15):
                async with session.get(f"{API_BASE}/remote") as resp:
                    devices = await resp.json()
        except Exception as e:
            _LOGGER.error("Failed to load Sigrow remote units: %s", e)
            return

        for device in devices:
            remote_id = device.get("id")
            name = device.get("name", f"Remote {remote_id}")

            try:
                async with async_timeout.timeout(15):
                    async with session.get(f"{API_BASE}/remote/{remote_id}/data") as resp:
                        readings = await resp.json()
            except Exception as e:
                _LOGGER.warning("Failed to load data for remote %s: %s", remote_id, e)
                continue

            for reading in readings:
                sensor_type = reading.get("sensor_type")
                value = reading.get("value")
                timestamp = reading.get("timestamp")
                if sensor_type and value is not None:
                    entities.append(SigrowSensor(
                        name=f"{name} {sensor_type.capitalize()}",
                        unique_id=f"sigrow_{remote_id}_{sensor_type}",
                        value=value,
                        api_key=api_key,
                        remote_id=remote_id,
                        sensor_type=sensor_type
                    ))

    async_add_entities(entities, True)

class SigrowSensor(SensorEntity):
    def __init__(self, name, unique_id, value, api_key, remote_id, sensor_type):
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._state = value
        self._api_key = api_key
        self._remote_id = remote_id
        self._sensor_type = sensor_type

        if self._sensor_type.lower() == "temperature":
            self._attr_unit_of_measurement = "°C"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        headers = {"Authorization": f"Bearer {self._api_key}"}
        url = f"{API_BASE}/remote/{self._remote_id}/data"

        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with async_timeout.timeout(15):
                    async with session.get(url) as resp:
                        readings = await resp.json()
            except Exception as e:
                _LOGGER.warning("Failed to update %s: %s", self._attr_name, e)
                return

            for reading in readings:
                if reading["sensor_type"] == self._sensor_type:
                    self._state = reading["value"]
                    break
