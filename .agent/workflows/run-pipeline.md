---
description: Run the complete Agent Fund Market Scout and Portfolio Manager execution pipeline.
---

1. Execute the `Market Scout` skill (reference exactly `@[.agent/skills/market-scout/SKILL.md]`) to analyze the market and generate the pulse file directly into the workspace.
2. After the scout finishes, run the command `venv\Scripts\python.exe engine\signal_generator.py` to parse the pulse data into `engine/signal.json`.
3. Assume the role of the Portfolio Manager according to `@[CLAUDE.md]`. Read the `engine/signal.json` signals, summarize them, and wait for my explicit "Y" approval before executing the trade script via terminal.