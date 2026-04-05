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
4. **Reporting:**
   - Generate a markdown table summarizing the "Pulse" for each asset, including the gathered metrics, overbought/oversold status, and the overall macro sentiment. Write this table directly to the root of the user's workspace as `market_pulse.md` instead of creating an internal Agent Artifact.