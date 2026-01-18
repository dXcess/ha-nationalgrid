from homeassistant import config_entries
from homeassistant.core import HomeAssistant
import voluptuous as vol
import aiohttp

from .const import DOMAIN, TOKEN_URL
from .api import NationalGridApi

class NationalGridConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("username"): str,
                    vol.Required("password"): str,
                })
            )

        try:
            token = await self._get_token(
                user_input["username"],
                user_input["password"]
            )

            api = NationalGridApi(token)
            await api.verify_token()  # 🔥 FIRST SUCCESS CHECK

        except Exception as err:
            return self.async_show_form(
                step_id="user",
                errors={"base": "auth_failed"},
            )

        return self.async_create_entry(
            title="National Grid",
            data={"access_token": token},
        )

    async def _get_token(self, username, password):
        payload = {
            "username": username,
            "password": password,
            "grant_type": "password"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(TOKEN_URL, json=payload) as resp:
                data = await resp.json()
                return data["access_token"]
