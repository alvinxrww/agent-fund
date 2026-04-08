---
title: Market Scout
description: Perform a visual and sentiment analysis for BTC, GLD, and VOO.
---

# Market Scout Skill
**Objective:** Perform a visual and sentiment analysis for BTC, GLD, and VOO.

**Execution Steps:**
1. **Technical Data Extraction:**
   - Open the browser to the TradingView **Technicals** tab for each ticker (BTC, GLD, VOO). Proceeding to the "Technicals" text page ensures the agent can reliably extract HTML text values rather than attempting to parse canvas chart graphics.
   - Read and extract the RSI (Relative Strength Index) and 50-day Simple Moving Average (SMA).
   - Note if the asset is currently "Overbought" (RSI > 70) or "Oversold" (RSI < 30).
2. **Sentiment Check:**
   - Use a web search or browse top financial news sites (e.g., Google News, Yahoo Finance) for headers involving "Inflation," "Interest Rates," and "Crypto Regulation."
   - Based on recent headlines, categorize the current macro sentiment as "Risk-On" or "Risk-Off."
3. **Verification:**
   - Navigate to the BTC/USD daily chart. Keep the page open momentarily to ensure the chart is captured within the browser subagent's automated session recording.
4. **Reporting (IMPORTANT — do NOT use the browser subagent for this step):**
   - After **all** browser subagent calls from steps 1–3 have returned, collect the extracted data (RSI, SMA, status, sentiment) from their responses.
   - Write `market_pulse.md` at the root of the user's workspace using a **terminal command** via `run_command` (e.g., `echo` with redirect or a Python one-liner). Do **not** use `write_to_file` as it may be cancelled by the system during long-running pipelines. Do **not** create an internal Agent Artifact.
   - The file must contain a markdown table summarizing the "Pulse" for each asset, including the gathered metrics, overbought/oversold status, and the overall macro sentiment.