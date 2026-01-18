import aiohttp
from .const import VERIFY_URL, APIM_SUBSCRIPTION_KEY

class NationalGridApi:
    def __init__(self, access_token: str):
        self._access_token = access_token

    async def verify_token(self):
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Ocp-Apim-Subscription-Key": APIM_SUBSCRIPTION_KEY,
            "Accept": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(VERIFY_URL, headers=headers) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise Exception(f"Verify failed: {resp.status} {text}")

                return await resp.json()
