# AI analyst connection diagnosis

- Observation: the visitor received a generic startup/key error for provider failures.
- Live evidence: authenticated models GET HTTP 200; minimal Interactions request HTTP 200; full planner request timed out at 30 and 55 seconds. With forced tool selection, the full planner request returned a provider 5xx error (mapped to provider_unavailable). Successful recorded-data AI analysis remains unverified.
- Change: require function selection with generation_config.tool_choice=any per official Google function-calling documentation; server deadline 55s, browser deadline 60s. Separate timeout, connectivity, invalid request, provider 5xx, and other provider errors. No automatic retries or fabricated local fallback.
- Version preservation: previous v19 viewer retained. New viewer snapshot v20; previous server/bridge/test source preserved in v20. Canonical viewer and server updated locally. Public release version has not been advanced.
- Verification: 13 server checks, 48 Korean checks, 23 English checks pass. Provider tests use mocks; real AI planner failure recorded above. Browser and participant confirmation pending.
- Source: https://ai.google.dev/gemini-api/docs/function-calling
