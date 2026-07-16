"""Entry point to launch one of the three agents.

Usage:
    python main.py finance
    python main.py assistant
    python main.py research
"""

from __future__ import annotations

import sys

AGENTS = {
    "finance": "agents.finance_agent",
    "assistant": "agents.personal_assistant_agent",
    "research": "agents.deep_research_agent",
}


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in AGENTS:
        print(f"Usage: python main.py <{'|'.join(AGENTS)}>")
        raise SystemExit(1)

    module_name = AGENTS[sys.argv[1]]
    module = __import__(module_name, fromlist=["main"])
    module.main()


if __name__ == "__main__":
    main()
