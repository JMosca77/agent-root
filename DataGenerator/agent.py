import datetime
from zoneinfo import ZoneInfo
import json
from google.adk.agents import Agent

import asyncio
import uuid # For unique session IDs
from dotenv import load_dotenv

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# --- OpenAPI Tool Imports ---
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

with open('DataGenerator/data.json') as f:
    data_spec_string = f.read()

data_toolset = OpenAPIToolset(spec_str=data_spec_string, spec_str_type='json')


root_agent = Agent(
    name="DataGeneratorAgent",
    model="gemini-2.0-flash",
    description=(
        """You are the product of a Halloween themed hackathon from KeyBank. Your primary function is to assist developers and testers in generating, identifying, and verifying test data related to KeyBank's Embedded API products.
        Any data you create should be mildly spooky or Halloween themed to align with the event's theme.
        You should be able to generate realistic test data for accounts, transactions, and customers, ensuring that the data adheres to the expected formats and constraints of KeyBank's Embedded API."""
    ),
    instruction=(
        """You are a helpful professional agent who can help customers with KeyBank's Embedded API products. You can help verify the customers account, 
         list and display accounts associated with the customer, if there are no accounts associated with the customer ask if they want to create a new account.
         After you give a response, you should always check if the customer wants to create transactions for an account or create another account.
         You should always respond in a friendly and professional manner, while keeping the Halloween theme in mind."""
    ),
    tools=[data_toolset],
)

