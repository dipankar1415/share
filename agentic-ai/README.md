# Stock Analysis Multi-Agent System

A practical implementation of coordinated AI agents that work together to analyze US stocks and provide trading recommendations. Built with LangGraph and powered by Bright Data's web scraping capabilities.

## What This Does

The system uses four specialized agents that collaborate to deliver actionable stock insights:

**Stock Researcher** - Scans the market and picks 2 promising stocks based on recent performance, news momentum, and trading volume. Filters out penny stocks and low-liquidity names.

**Market Data Collector** - Pulls current pricing, volume trends, and technical indicators (RSI, moving averages) for the selected stocks. Tracks 7-day and 30-day price movements.

**News Analyst** - Searches recent financial news (last 3-5 days), summarizes key events, and classifies sentiment as positive, negative, or neutral. Focuses on how news might move prices short-term.

**Trading Advisor** - Synthesizes the data and news to recommend Buy/Sell/Hold actions with specific target prices. Designed for next-day trading decisions.

A supervisor agent orchestrates the workflow, routing tasks between agents and ensuring the analysis completes end-to-end.

## Why This Exists

Most stock analysis tools either give you raw data dumps or generic recommendations. This project bridges that gap by combining real-time web data with structured AI reasoning. The multi-agent approach mirrors how a trading desk actually works - different specialists handling research, data, news, and strategy.

## Setup

You'll need API keys for:
- **OpenAI** (GPT-4o-mini for the agents)
- **Bright Data** (for web scraping and data collection)

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_key
BRIGHT_DATA_API_TOKEN=your_bright_data_token
WEB_UNLOCKER_ZONE=optional_zone_name
BROWSER_ZONE=optional_browser_zone
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Make sure you have Node.js installed since the Bright Data MCP server runs via `npx`.

## Running It

**Stock Analysis:**
```bash
python multi-agent-for-stock-analysis.py
```

The default query asks for US stock recommendations. You can modify the query in the `__main__` block to ask different questions.

**Web Search Agent (Standalone):**
```bash
python web-search-agent.py
```

This demonstrates a simpler single-agent setup that searches for flight information. Useful for testing the Bright Data integration.

## How It Works

The system uses LangGraph's supervisor pattern. When you run the stock analysis:

1. Supervisor receives your query
2. Routes it to the Stock Researcher to pick 2 stocks
3. Sends those tickers to the Market Data Collector
4. Passes the same tickers to the News Analyst
5. Combines all findings and sends to the Trading Advisor
6. Returns final recommendations with target prices

Each agent has access to Bright Data's tools for web scraping, which means they can pull live data from financial sites, news sources, and market data providers.

## Output Format

You'll see updates from each agent as they work. The final output includes:
- Stock names and tickers
- Current price and recent trends
- News summaries with sentiment
- Buy/Sell/Hold recommendation
- Target entry/exit prices
- Reasoning for each recommendation

## Limitations

- Focused on NYSE and NASDAQ stocks only
- Designed for short-term trading (not long-term investing)
- Recommendations are based on recent data and news, not fundamental analysis
- Requires active API keys with sufficient credits
- Not financial advice (obviously)

## Tech Stack

- **LangGraph** - Agent orchestration and workflow management
- **LangChain** - LLM integration and tooling
- **OpenAI GPT-4o-mini** - Language model for agent reasoning
- **Bright Data MCP** - Web scraping and data collection
- **Python asyncio** - Async execution for agent coordination

## Extending This

The supervisor pattern makes it easy to add more agents. Some ideas:

- Technical analysis agent for chart patterns
- Risk assessment agent for portfolio impact
- Earnings calendar agent for upcoming events
- Social sentiment agent for Reddit/Twitter buzz

Just create a new `create_react_agent` with a specific prompt and add it to the supervisor's agent list.

## License

Do whatever you want with this code. If it helps you make money, buy yourself something nice.
