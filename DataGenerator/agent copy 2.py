import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from typing import Optional

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


def inspect_developer_portal(query: Optional[str] = None) -> dict:
    """Inspects KeyBank's Developer Portal for information.

    Args:
        query (Optional[str]): Specific topic or area to query about. If None, returns general portal information.

    Returns:
        dict: status and information about the developer portal or specific query.
    """
    # This is a mock implementation. In a real scenario, you would integrate with the actual developer portal API
    portal_info = {
        "base_url": "https://developer.keybank.com",
        "sections": {
            "api_documentation": {
                "path": "/docs",
                "description": "Comprehensive API documentation for all KeyBank APIs"
            },
            "test_data": {
                "path": "/test-data",
                "description": "Access to test data and sandbox environments"
            },
            "authentication": {
                "path": "/auth",
                "description": "Authentication methods and security guidelines"
            },
            "getting_started": {
                "path": "/getting-started",
                "description": "Quick start guides and tutorials"
            }
        },
        "available_apis": [
            "Embedded Banking API",
            "Payment Services API",
            "Account Information API",
            "Transaction Data API"
        ]
    }
    
    if query is None:
        return {
            "status": "success",
            "info": {
                "description": "KeyBank Developer Portal - Your gateway to banking APIs",
                "base_url": portal_info["base_url"],
                "available_apis": portal_info["available_apis"]
            }
        }
    
    query = query.lower()
    if "api" in query:
        return {
            "status": "success",
            "info": {
                "available_apis": portal_info["available_apis"],
                "documentation_url": f"{portal_info['base_url']}/docs"
            }
        }
    elif "test" in query or "sandbox" in query:
        return {
            "status": "success",
            "info": portal_info["sections"]["test_data"]
        }
    elif "auth" in query or "security" in query:
        return {
            "status": "success",
            "info": portal_info["sections"]["authentication"]
        }
    elif "guide" in query or "tutorial" in query:
        return {
            "status": "success",
            "info": portal_info["sections"]["getting_started"]
        }
    else:
        return {
            "status": "error",
            "error_message": f"No specific information found for query: '{query}'"
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

# --- Sample OpenAPI Specification (JSON String) ---
# A basic Pet Store API example using httpbin.org as a mock server
openapi_spec_string = """
{
  "openapi": "3.0.0",
  "info": {
    "title": "Simple Pet Store API (Mock)",
    "version": "1.0.1",
    "description": "An API to manage pets in a store, using httpbin for responses."
  },
  "servers": [
    {
      "url": "https://randomuser.me",
      "description": "Mock server (httpbin.org)"
    }
  ],
  "paths": {
    "/api": {
      "get": {
        "summary": "List all pets (Simulated)",
        "operationId": "listPets",
        "description": "Simulates returning a list of pets. Uses httpbin's /get endpoint which echoes query parameters.",
        "parameters": [
          {
            "name": "limit",
            "in": "query",
            "description": "Maximum number of pets to return",
            "required": false,
            "schema": { "type": "integer", "format": "int32" }
          },
          {
             "name": "status",
             "in": "query",
             "description": "Filter pets by status",
             "required": false,
             "schema": { "type": "string", "enum": ["available", "pending", "sold"] }
          }
        ],
        "responses": {
          "200": {
            "description": "A list of pets (echoed query params).",
            "content": { "application/json": { "schema": { "type": "object" } } }
          }
        }
      }
    },
    "/post": {
      "post": {
        "summary": "Create a pet (Simulated)",
        "operationId": "createPet",
        "description": "Simulates adding a new pet. Uses httpbin's /post endpoint which echoes the request body.",
        "requestBody": {
          "description": "Pet object to add",
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": ["name"],
                "properties": {
                  "name": {"type": "string", "description": "Name of the pet"},
                  "tag": {"type": "string", "description": "Optional tag for the pet"}
                }
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Pet created successfully (echoed request body).",
            "content": { "application/json": { "schema": { "type": "object" } } }
          }
        }
      }
    },
    "/get?petId={petId}": {
      "get": {
        "summary": "Info for a specific pet (Simulated)",
        "operationId": "showPetById",
        "description": "Simulates returning info for a pet ID. Uses httpbin's /get endpoint.",
        "parameters": [
          {
            "name": "petId",
            "in": "path",
            "description": "This is actually passed as a query param to httpbin /get",
            "required": true,
            "schema": { "type": "integer", "format": "int64" }
          }
        ],
        "responses": {
          "200": {
            "description": "Information about the pet (echoed query params)",
            "content": { "application/json": { "schema": { "type": "object" } } }
          },
          "404": { "description": "Pet not found (simulated)" }
        }
      }
    }
  }
}
"""

# --- Create OpenAPIToolset ---
petstore_toolset = OpenAPIToolset(
    spec_str=openapi_spec_string,
    spec_str_type='json',
    # No authentication needed for httpbin.org
)



root_agent = Agent(
    name="DataGeneratorAgent",
    model="gemini-2.0-flash",
    description=(
        "Agent to help external API consumers navigate KeyBank's Developer Portal, access documentation, and work with test data."
    ),
    instruction=(
        "You are a helpful agent who assists customers with KeyBank's API products and developer resources. You can help customers: \n"
        "1. Navigate the KeyBank Developer Portal at developer.keybank.com\n"
        "2. Find relevant API documentation and guides\n"
        "3. Access test data and sandbox environments\n"
        "4. Understand authentication and security requirements\n"
        "5. Locate specific API endpoints and their usage\n"
        "Use the available tools to provide accurate information about KeyBank's developer resources and help customers find what they need."
    ),
    tools=[petstore_toolset, get_weather, get_current_time, inspect_developer_portal],
)