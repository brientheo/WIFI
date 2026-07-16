"""Deep research agent: multi-source research reports.

Uses the SDK's built-in WebSearch, WebFetch, and Write tools directly —
no custom tools needed. Reports are written to ./reports.

Run with:  python -m agents.deep_research_agent
"""

from __future__ import annotations

import os

from claude_agent_sdk import ClaudeAgentOptions

from agents.runner import run

SYSTEM_PROMPT = """\
You are a deep research agent. Given a question or topic, you investigate
it thoroughly across multiple independent sources before answering.

Process:
1. Break the topic into sub-questions if it's broad.
2. Use WebSearch to find multiple independent, credible sources — do not
   rely on a single source for a claim that matters.
3. Use WebFetch to read the most promising sources in full.
4. Cross-check claims across sources; note where sources disagree.
5. Synthesize findings into a clear report with inline citations (source
   name + URL) for each non-obvious claim.
6. When asked for a written report, use Write to save it as Markdown under
   ./reports/<slug>.md, then summarize the key findings in your reply.

Be skeptical of low-quality or single-source claims, and say explicitly
when evidence is thin or conflicting rather than papering over it.
"""


def build_options() -> ClaudeAgentOptions:
    reports_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    return ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        allowed_tools=["WebSearch", "WebFetch", "Write"],
        cwd=reports_dir,
    )


def main() -> None:
    run(build_options(), welcome_message="Deep research agent ready.")


if __name__ == "__main__":
    main()
