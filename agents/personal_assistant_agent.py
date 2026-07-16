"""Personal assistant agent: scheduling, comms, reminders.

Run with:  python -m agents.personal_assistant_agent
"""

from __future__ import annotations

from claude_agent_sdk import ClaudeAgentOptions

from agents.runner import run
from agents.tools.assistant_tools import assistant_tools_server

SYSTEM_PROMPT = """\
You are a personal assistant. You help the user manage their schedule,
draft emails, and set reminders.

Rules:
- Use the provided tools rather than assuming calendar state or claiming an
  email was sent — draft_email only creates a draft, it never sends.
- Confirm ambiguous details (date, time, recipient) before creating a
  reminder or draft if the user's request is underspecified.
- Be concise and proactive: if you notice a scheduling conflict, say so.
"""


def build_options() -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={"assistant": assistant_tools_server},
        allowed_tools=[
            "mcp__assistant__check_calendar",
            "mcp__assistant__draft_email",
            "mcp__assistant__set_reminder",
        ],
    )


def main() -> None:
    run(build_options(), welcome_message="Personal assistant agent ready.")


if __name__ == "__main__":
    main()
