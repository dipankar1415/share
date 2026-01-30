import os
import asyncio
import warnings
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model
from langgraph_supervisor import create_supervisor
from langchain_core.messages import convert_to_messages

warnings.filterwarnings('ignore', message='.*create_react_agent.*')
from langgraph.prebuilt import create_react_agent

load_dotenv()


def check_required_config():
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


def format_single_message(msg, add_indent=False):
    formatted = msg.pretty_repr(html=True)
    if not add_indent:
        print(formatted)
        return

    indented_lines = "\n".join("\t" + line for line in formatted.split("\n"))
    print(indented_lines)


def display_agent_updates(update_data, show_only_last=False):
    is_nested_graph = False
    if isinstance(update_data, tuple):
        namespace, update_data = update_data
        if len(namespace) == 0:
            return

        graph_identifier = namespace[-1].split(":")[0]
        print(f"Update from subgraph {graph_identifier}:")
        print("\n")
        is_nested_graph = True

    for node_id, node_data in update_data.items():
        label = f"Update from node {node_id}:"
        if is_nested_graph:
            label = "\t" + label

        print(label)
        print("\n")

        msg_list = convert_to_messages(node_data["messages"])
        if show_only_last:
            msg_list = msg_list[-1:]

        for msg in msg_list:
            format_single_message(msg, add_indent=is_nested_graph)
        print("\n")

async def process_stock_analysis(user_query):
    check_required_config()
    
    bright_data_config = {
        "API_TOKEN": os.getenv("BRIGHT_DATA_API_TOKEN")
    }
    
    web_unlocker_zone = os.getenv("WEB_UNLOCKER_ZONE")
    if web_unlocker_zone:
        bright_data_config["WEB_UNLOCKER_ZONE"] = web_unlocker_zone
    
    browser_zone = os.getenv("BROWSER_ZONE")
    if browser_zone:
        bright_data_config["BROWSER_ZONE"] = browser_zone
    
    mcp_client = MultiServerMCPClient(
        {
            "bright_data": {
                "command": "npx",
                "args": ["@brightdata/mcp"],
                "env": bright_data_config,
                "transport": "stdio",
            },
        }
    )
    agent_tools = await mcp_client.get_tools()
    base_model = init_chat_model(model="openai:gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

    stock_researcher = create_react_agent(
        base_model, 
        agent_tools, 
        prompt="""You are a stock research analyst specializing in the US Stock Market (NYSE and NASDAQ). 
        Your task is to select 2 promising, actively traded US-listed stocks for short term trading 
        (buy/sell) based on recent performance, news buzz, volume or technical strength.
        Avoid penny stocks and illiquid companies.
        Output should include stock names, tickers, and brief reasoning for each choice.
        Respond in structured plain text format.""", 
        name="stock_finder_agent"
    )

    data_collector = create_react_agent(
        base_model, 
        agent_tools, 
        prompt="""You are a market data analyst for US stocks listed on NYSE or NASDAQ. 
        Given a list of stock tickers (eg AAPL, MSFT, GOOGL), your task is to gather recent market 
        information for each stock, including:
        - Current price
        - Previous closing price
        - Today's volume
        - 7-day and 30-day price trend
        - Basic Technical indicators (RSI, 50/200-day moving averages)
        - Any notable spikes in volume or volatility
        
        Return your findings in a structured and readable format for each stock, suitable for 
        further analysis by a recommendation engine. Use USD as the currency. Be concise but complete.""", 
        name="market_data_agent"
    )

    news_analyst = create_react_agent(
        base_model, 
        agent_tools, 
        prompt="""You are a financial news analyst. Given the names or the tickers of US stocks 
        listed on NYSE or NASDAQ, your job is to:
        - Search for the most recent news articles (past 3-5 days)
        - Summarize key updates, announcements, and events for each stock
        - Classify each piece of news as positive, negative or neutral
        - Highlight how the news might affect short term stock price
                                            
        Present your response in a clear, structured format - one section per stock.
        Use bullet points where necessary. Keep it short, factual and analysis-oriented""", 
        name="news_analyst_agent"
    )

    trading_advisor = create_react_agent(
        base_model, 
        agent_tools, 
        prompt="""You are a trading strategy advisor for the US Stock Market. You are given:
        - Recent market data (current price, volume, trend, indicators)
        - News summaries and sentiment for each stock
        
        Based on this info, for each stock:
        1. Recommend an action: Buy, Sell or Hold
        2. Suggest a specific target price for entry or exit (USD)
        3. Briefly explain the reason behind your recommendation.
        
        Your goal is to provide practical, near-term trading advice for the next trading day.
        Keep the response concise and clearly structured.""", 
        name="price_recommender_agent"
    )

    coordinator = create_supervisor(
        model=init_chat_model("openai:gpt-4o-mini"),
        agents=[stock_researcher, data_collector, news_analyst, trading_advisor],
        prompt=(
            "You are a supervisor managing four agents:\n"
            "- stock_finder_agent: Assign research-related tasks to this agent to pick 2 promising US stocks\n"
            "- market_data_agent: Assign tasks to fetch current market data (price, volume, trends)\n"
            "- news_analyst_agent: Assign task to search and summarize recent news\n"
            "- price_recommender_agent: Assign task to give buy/sell decision with target price.\n"
            "Assign work to one agent at a time, do not call agents in parallel.\n"
            "Do not do any work yourself.\n"
            "Make sure you complete till end and do not ask for proceed in between the task."
        ),
        add_handoff_back_messages=True,
        output_mode="full_history",
    ).compile()

    last_chunk = None
    async for update_chunk in coordinator.astream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_query,
                }
            ]
        },
    ):
        display_agent_updates(update_chunk, show_only_last=True)
        last_chunk = update_chunk

    if last_chunk:
        final_history = last_chunk["supervisor"]["messages"]

if __name__ == "__main__":
    asyncio.run(process_stock_analysis("Give me good stock recommendations from US stock market"))