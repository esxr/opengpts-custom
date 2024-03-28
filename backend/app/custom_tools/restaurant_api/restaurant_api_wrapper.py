import json
from typing import Dict, List, Optional

import aiohttp
import requests
from pydantic import BaseModel, Extra, root_validator
from langchain_core.utils import get_from_dict_or_env

MENU_API_URL = "https://grumpy-camels-double.loca.lt"


class MenuAPIWrapper(BaseModel):
    """Wrapper for Menu API."""

    menu_api_key: Optional[str] = None  # API key for authentication, if needed

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator(pre=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that API key exists in environment, if necessary."""
        if "menu_api_key" in values:
            menu_api_key = get_from_dict_or_env(values, "menu_api_key", "MENU_API_KEY")
            values["menu_api_key"] = menu_api_key
        return values

    def get_menu(self) -> List[Dict]:
        """Get the full menu from the Menu API using a GET request."""
        headers = (
            {"Authorization": f"Bearer {self.menu_api_key}"}
            if self.menu_api_key
            else {}
        )
        response = requests.get(f"{MENU_API_URL}/menu", headers=headers)
        response.raise_for_status()
        return response.json()

    async def get_menu_async(self) -> List[Dict]:
        """Get the full menu from the Menu API asynchronously with a GET request."""
        headers = (
            {"Authorization": f"Bearer {self.menu_api_key}"}
            if self.menu_api_key
            else {}
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{MENU_API_URL}/menu", headers=headers) as res:
                if res.status == 200:
                    menu = await res.json()
                    return menu
                else:
                    raise Exception(f"Error {res.status}: {res.reason}")

    def place_order(self, items: List[int]) -> Dict:
        """Place an order through the Menu API using a POST request."""
        order_details = {"items": items}  # Adjusting to match the expected API format
        headers = (
            {
                "Authorization": f"Bearer {self.menu_api_key}",
                "Content-Type": "application/json",
            }
            if self.menu_api_key
            else {"Content-Type": "application/json"}
        )
        response = requests.post(
            f"{MENU_API_URL}/order", headers=headers, json=order_details
        )
        response.raise_for_status()
        return response.json()

    async def place_order_async(self, items: List[int]) -> Dict:
        """Place an order through the Menu API asynchronously with a POST request."""
        order_details = {"items": items}  # Adjusting to the new expected format
        headers = (
            {
                "Authorization": f"Bearer {self.menu_api_key}",
                "Content-Type": "application/json",
            }
            if self.menu_api_key
            else {"Content-Type": "application/json"}
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{MENU_API_URL}/order", headers=headers, json=order_details
            ) as res:
                if res.status == 200:
                    order_response = await res.json()
                    return order_response
                else:
                    raise Exception(f"Error {res.status}: {res.reason}")
