from typing import Dict, List, Optional, Type, Union

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

# Adjust the import according to your project structure
from app.custom_tools.restaurant_api.restaurant_api_wrapper import MenuAPIWrapper

class OrderInput(BaseModel):
    """Input for placing orders."""
    # Since the API now expects an array of item IDs, adjust the input model accordingly
    items: Optional[List[int]] = Field(None, description="Array of item IDs to order")

class MenuOrderTool(BaseTool):
    """Tool that handles menu retrieval and order placement for a restaurant."""

    name: str = "menu_order_tool"
    description: str = (
        "A comprehensive tool for interacting with the restaurant's Menu API, "
        "allowing users to search the menu and place orders directly."
    )
    api_wrapper: MenuAPIWrapper = Field(default_factory=MenuAPIWrapper)
    args_schema: Type[BaseModel] = OrderInput

    def _run(
        self,
        items: Optional[List[int]] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[List[Dict], str]:
        """Use the tool for placing orders."""
        try:
            if items:
                # Directly pass the items list to place_order method
                return self.api_wrapper.place_order(items)
            else:
                # If no items are provided, fetch the menu instead
                return self.api_wrapper.get_menu()
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        items: Optional[List[int]] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Union[List[Dict], str]:
        """Use the tool asynchronously for placing orders."""
        try:
            if items:
                # Asynchronously place the order with the given items
                return await self.api_wrapper.place_order_async(items)
            else:
                # If no items are specified, asynchronously fetch the menu
                return await self.api_wrapper.get_menu_async()
        except Exception as e:
            return repr(e)
