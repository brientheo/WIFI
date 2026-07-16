"""Shared REPL runner for all agents in this repo.

Each agent module builds a `ClaudeAgentOptions` (system prompt, allowed
tools, in-process MCP servers) and hands it to `run_agent_repl`, which
owns the interactive loop: read user input, stream the agent's reply,
print any tool calls it makes along the way.
"""

from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
    ToolUseBlock,
)


def _print_assistant_message(message: AssistantMessage) -> None:
    for block in message.content:
        if isinstance(block, TextBlock):
            print(block.text, end="", flush=True)
        elif isinstance(block, ToolUseBlock):
            print(f"\n[calling tool: {block.name}]", flush=True)


async def run_agent_repl(options: ClaudeAgentOptions, welcome_message: str) -> None:
    load_dotenv()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit(
            "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and fill it in."
        )

    print(welcome_message)
    print("Type 'exit' or 'quit' to end the session.\n")

    async with ClaudeSDKClient(options=options) as client:
        while True:
            try:
                user_input = input("\nyou> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye.")
                return

            if user_input.lower() in {"exit", "quit"}:
                print("Goodbye.")
                return
            if not user_input:
                continue

            await client.query(user_input)

            print("\nagent> ", end="", flush=True)
            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    _print_assistant_message(message)
            print()


def run(options: ClaudeAgentOptions, welcome_message: str) -> None:
    asyncio.run(run_agent_repl(options, welcome_message))
