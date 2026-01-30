import os
import asyncio
import warnings
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model

warnings.filterwarnings('ignore', message='.*create_react_agent.*')
from langgraph.prebuilt import create_react_agent

load_dotenv()


def validate_env_vars():
    required_vars = {
        "BRIGHT_DATA_API_TOKEN": "Bright Data API token is required",
        "OPENAI_API_KEY": "OpenAI API key is required"
    }
    missing = []
    for var_name, error_msg in required_vars.items():
        if not os.getenv(var_name):
            missing.append(f"{var_name}: {error_msg}")
    
    if missing:
        raise ValueError(
            "Missing required environment variables:\n" + 
            "\n".join(f"  - {msg}" for msg in missing) +
            "\n\nPlease set these in your .env file or environment."
        )


async def execute_web_search():
    validate_env_vars()
    
    bright_data_env = {
        "API_TOKEN": os.getenv("BRIGHT_DATA_API_TOKEN")
    }
    
    web_unlocker_zone = os.getenv("WEB_UNLOCKER_ZONE")
    if web_unlocker_zone:
        bright_data_env["WEB_UNLOCKER_ZONE"] = web_unlocker_zone
    
    browser_zone = os.getenv("BROWSER_ZONE")
    if browser_zone:
        bright_data_env["BROWSER_ZONE"] = browser_zone
    
    mcp_connection = MultiServerMCPClient(
        {
            "bright_data": {
                "command": "npx",
                "args": ["@brightdata/mcp"],
                "env": bright_data_env,
                "transport": "stdio",
            },
        }
    )
    available_tools = await mcp_connection.get_tools()
    llm_model = init_chat_model(model="openai:gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
    search_agent = create_react_agent(
        llm_model, 
        available_tools, 
        prompt="You are a web search agent with access to brightdata tool to get latest data"
    )
    result = await search_agent.ainvoke({"messages": "Tell me available flights from San Francisco to Austin, TX on Dec 1 2025"})
    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(execute_web_search())