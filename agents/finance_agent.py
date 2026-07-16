"""Finance agent: portfolio and investment analysis.

Run with:  python -m agents.finance_agent
"""

from __future__ import annotations

from claude_agent_sdk import ClaudeAgentOptions

from agents.runner import run
from agents.tools.finance_tools import finance_tools_server

SYSTEM_PROMPT = """\
You are a personal finance assistant. You help the user understand their
portfolio, evaluate potential investments, and reason about risk and
diversification.

Rules:
- Use the provided tools to fetch holdings and compute metrics rather than
  guessing numbers.
- Always show your work: state the numbers you used before giving an
  opinion or recommendation.
- You are not a licensed financial advisor. Frame recommendations as
  educational analysis, not personalized financial advice, and say so when
  the user asks for a concrete buy/sell decision.
- Be concise. Prefer tables for multi-position breakdowns.
"""


def build_options() -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={"finance": finance_tools_server},
        allowed_tools=[
            "mcp__finance__get_holdings",
            "mcp__finance__calc_portfolio_metrics",
            "mcp__finance__evaluate_investment",
        ],
    )


def main() -> None:
    run(build_options(), welcome_message="Finance agent ready.")


if __name__ == "__main__":
    main()
