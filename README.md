# WIFI agents

Three starter agents built on the [Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview) (Python).

| Agent | Purpose | Tools |
|---|---|---|
| Finance (`agents/finance_agent.py`) | Portfolio and investment analysis | `get_holdings`, `calc_portfolio_metrics`, `evaluate_investment` (stub — plug in a market data API) |
| Personal Assistant (`agents/personal_assistant_agent.py`) | Scheduling, comms, reminders | `check_calendar`, `draft_email`, `set_reminder` (stubs — plug in Calendar/Gmail APIs) |
| Deep Research (`agents/deep_research_agent.py`) | Multi-source research reports | SDK built-in `WebSearch` / `WebFetch` / `Write` — no stubs needed |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then set ANTHROPIC_API_KEY
```

## Run

```bash
python main.py finance      # portfolio Q&A, calc_portfolio_metrics, etc.
python main.py assistant    # calendar / email drafts / reminders
python main.py research     # web research -> markdown report in ./reports
```

Each is an interactive REPL — type a message, get a reply, `exit` to quit.

## Project layout

```
agents/
  runner.py                    # shared REPL loop (used by all three agents)
  finance_agent.py             # system prompt + tool wiring
  personal_assistant_agent.py
  deep_research_agent.py
  tools/
    finance_tools.py           # get_holdings, calc_portfolio_metrics, evaluate_investment
    assistant_tools.py         # check_calendar, draft_email, set_reminder
main.py                        # `python main.py <finance|assistant|research>`
```

## Wiring in real data

The finance and personal-assistant tools are stubs today (in-memory sample
data) so the agents run end-to-end out of the box:

- **Finance**: `get_holdings` returns a hardcoded sample portfolio; `evaluate_investment`
  returns a placeholder. Replace with a brokerage API (e.g. Plaid) for holdings and a
  market data API (e.g. Alpha Vantage, Polygon.io, Finnhub) for quotes/fundamentals —
  keep the tool's input/output shape the same so the agent's reasoning doesn't need to change.
- **Personal assistant**: `check_calendar` / `draft_email` / `set_reminder` operate on
  in-memory sample data. Replace with Google Calendar + Gmail (OAuth) or another
  provider of your choice.

The deep research agent needs no stubs — it uses the SDK's built-in `WebSearch`,
`WebFetch`, and `Write` tools directly.
