"""In-process tools for the finance agent.

`get_holdings` and `evaluate_investment` are stubs: they return
plausible-shaped data so the agent is runnable end-to-end today. Swap
the bodies for real calls to your brokerage API (e.g. Plaid) and a
market data provider (e.g. Alpha Vantage, Polygon.io, Finnhub) — the
tool signatures and return shapes are the contract the agent relies on,
so keep those stable.
"""

from __future__ import annotations

from claude_agent_sdk import create_sdk_mcp_server, tool

# Placeholder portfolio used until a real brokerage/account API is wired in.
_SAMPLE_HOLDINGS = [
    {"symbol": "VTI", "shares": 42.0, "cost_basis": 210.15, "price": 268.30},
    {"symbol": "VXUS", "shares": 60.0, "cost_basis": 55.20, "price": 61.85},
    {"symbol": "BND", "shares": 80.0, "cost_basis": 72.10, "price": 70.40},
    {"symbol": "AAPL", "shares": 15.0, "cost_basis": 145.00, "price": 230.10},
]


@tool(
    "get_holdings",
    "Return the user's current portfolio holdings (symbol, shares, cost basis, current price).",
    {},
)
async def get_holdings(args: dict) -> dict:
    return {
        "content": [
            {
                "type": "text",
                "text": str({"holdings": _SAMPLE_HOLDINGS}),
            }
        ]
    }


@tool(
    "calc_portfolio_metrics",
    "Compute portfolio-level metrics (total value, total cost basis, unrealized gain/loss, "
    "per-position weight) from a list of holdings.",
    {
        "holdings": list,
    },
)
async def calc_portfolio_metrics(args: dict) -> dict:
    holdings = args.get("holdings") or _SAMPLE_HOLDINGS

    total_value = 0.0
    total_cost = 0.0
    positions = []

    for h in holdings:
        shares = float(h["shares"])
        price = float(h["price"])
        cost_basis = float(h["cost_basis"])
        market_value = shares * price
        cost_value = shares * cost_basis
        total_value += market_value
        total_cost += cost_value
        positions.append(
            {
                "symbol": h["symbol"],
                "market_value": round(market_value, 2),
                "unrealized_gain_loss": round(market_value - cost_value, 2),
            }
        )

    for p in positions:
        p["weight_pct"] = round(
            (p["market_value"] / total_value) * 100, 2
        ) if total_value else 0.0

    result = {
        "total_market_value": round(total_value, 2),
        "total_cost_basis": round(total_cost, 2),
        "total_unrealized_gain_loss": round(total_value - total_cost, 2),
        "positions": positions,
    }

    return {"content": [{"type": "text", "text": str(result)}]}


@tool(
    "evaluate_investment",
    "Look up a ticker symbol and return a basic fundamentals/quote snapshot to help "
    "evaluate a potential investment. STUB: wire this to a real market data API.",
    {
        "symbol": str,
    },
)
async def evaluate_investment(args: dict) -> dict:
    symbol = str(args["symbol"]).upper()

    # STUB — replace with a real HTTP call, e.g.:
    #   resp = httpx.get(f"https://www.alphavantage.co/query", params={
    #       "function": "OVERVIEW", "symbol": symbol,
    #       "apikey": os.environ["MARKET_DATA_API_KEY"],
    #   })
    #   data = resp.json()
    placeholder = {
        "symbol": symbol,
        "note": (
            "No market data provider configured. Set MARKET_DATA_API_KEY and "
            "replace this stub in agents/tools/finance_tools.py with a real API call."
        ),
    }

    return {"content": [{"type": "text", "text": str(placeholder)}]}


finance_tools_server = create_sdk_mcp_server(
    name="finance-tools",
    version="1.0.0",
    tools=[get_holdings, calc_portfolio_metrics, evaluate_investment],
)
