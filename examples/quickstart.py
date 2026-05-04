"""Quickstart: minimal THE_CRASH simulation.

Runs a 3-firm, 12-consumer THE_CRASH scenario for 5 timesteps. Useful as
a smoke test after installing the package or to verify your LLM service
credentials. Outputs land in ``logs/quickstart_demo/``.

Requires ``GOOGLE_API_KEY`` for the default Gemini model. To use a local
Ollama instead, change ``--llm`` to e.g. ``llama3.1:8b`` and add
``--service ollama --port 11434``.

Equivalent CLI invocation::

    python -m ai_bazaar.main \\
        --consumer-scenario THE_CRASH --firm-type LLM \\
        --num-firms 3 --num-consumers 12 \\
        --use-cost-pref-gen --no-diaries --prompt-algo cot \\
        --llm gemini-2.5-flash --max-timesteps 5 \\
        --name quickstart_demo
"""

import sys

from ai_bazaar.main import main

QUICKSTART_ARGV = [
    "ai_bazaar.main",
    "--consumer-scenario", "THE_CRASH",
    "--firm-type", "LLM",
    "--num-firms", "3",
    "--num-consumers", "12",
    "--use-cost-pref-gen",
    "--no-diaries",
    "--prompt-algo", "cot",
    "--llm", "gemini-2.5-flash",
    "--max-timesteps", "5",
    "--name", "quickstart_demo",
]


if __name__ == "__main__":
    sys.argv = QUICKSTART_ARGV
    main()
