"""In-process tools for the personal assistant agent.

All three tools are stubs backed by in-memory state so the agent is
runnable end-to-end today. Replace the bodies with real calls to
Google Calendar / Gmail (or your provider of choice) — keep the
signatures and return shapes stable since the agent relies on them.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from claude_agent_sdk import create_sdk_mcp_server, tool

# In-memory placeholders, reset each process run.
_SAMPLE_EVENTS = [
    {
        "title": "1:1 with manager",
        "start": (datetime.now() + timedelta(hours=3)).isoformat(timespec="minutes"),
        "end": (datetime.now() + timedelta(hours=3, minutes=30)).isoformat(timespec="minutes"),
    },
    {
        "title": "Dentist appointment",
        "start": (datetime.now() + timedelta(days=2, hours=9)).isoformat(timespec="minutes"),
        "end": (datetime.now() + timedelta(days=2, hours=10)).isoformat(timespec="minutes"),
    },
]

_reminders: list[dict] = []
_drafts: list[dict] = []


@tool(
    "check_calendar",
    "List upcoming calendar events. STUB: wire this to a real calendar API "
    "(e.g. Google Calendar).",
    {},
)
async def check_calendar(args: dict) -> dict:
    return {"content": [{"type": "text", "text": str({"events": _SAMPLE_EVENTS})}]}


@tool(
    "draft_email",
    "Create a draft email (not sent) with a recipient, subject, and body. "
    "STUB: wire this to a real email API (e.g. Gmail).",
    {
        "to": str,
        "subject": str,
        "body": str,
    },
)
async def draft_email(args: dict) -> dict:
    draft = {
        "to": args["to"],
        "subject": args["subject"],
        "body": args["body"],
        "status": "drafted (not sent — no email provider configured)",
    }
    _drafts.append(draft)
    return {"content": [{"type": "text", "text": str(draft)}]}


@tool(
    "set_reminder",
    "Create a reminder for a given time with a short note. STUB: wire this to a "
    "real reminders/tasks API or notification service.",
    {
        "when": str,
        "note": str,
    },
)
async def set_reminder(args: dict) -> dict:
    reminder = {"when": args["when"], "note": args["note"], "status": "set (in-memory only)"}
    _reminders.append(reminder)
    return {"content": [{"type": "text", "text": str(reminder)}]}


assistant_tools_server = create_sdk_mcp_server(
    name="assistant-tools",
    version="1.0.0",
    tools=[check_calendar, draft_email, set_reminder],
)
