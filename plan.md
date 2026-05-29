# Pinggy-Tunneled Ollama and Intent Model Plan

## Summary

Users will not run Ollama or the intent model locally. The app services run with Docker Compose, while both model services are reached through Pinggy-tunneled HTTP URLs:

- Backend response drafting calls a Pinggy-tunneled Ollama endpoint.
- Intent Service remains a gRPC microservice, but internally calls a Pinggy-tunneled intent `/predict` API.
- API Gateway still calls Intent Service through gRPC to satisfy the PDF requirement.

## Key Changes

- Docker Compose runs only:
  - `api-gateway`
  - `intent-service`
  - `frontend`
- Remove local/Compose-managed Ollama as a default assumption.
- Backend uses:
  - `OLLAMA_BASE_URL=https://your-ollama-pinggy-url`
  - `LLM_MODEL=gpt-oss:20b`
  - Calls `${OLLAMA_BASE_URL}/api/generate`
- Intent Service uses:
  - `INTENT_API_URL=https://your-intent-pinggy-url/predict`
  - Sends `POST {"message": "..."}`
  - Expects `{intent, confidence, reason?}`
  - If `reason` is absent, generates a default reason.
- Keep gRPC boundary:
  - `backend -> intent-service` through gRPC.
  - `intent-service -> Pinggy intent API` through HTTP.
- Do not commit real Pinggy URLs.
- Use named placeholder URLs in docs and `.env.example`.

## Implementation Changes

- Update `docker-compose.yml`:
  - Remove `ollama` service and `ollama_data` volume.
  - Remove `depends_on: ollama`.
  - Pass `OLLAMA_BASE_URL` and `LLM_MODEL` to `api-gateway`.
  - Pass `INTENT_API_URL` to `intent-service`.
- Update backend:
  - Keep response drafting through Ollama HTTP.
  - Require `OLLAMA_BASE_URL`.
  - Keep `LLM_MODEL`, defaulting to `gpt-oss:20b` if unset.
- Update intent service:
  - Replace Ollama JSON classifier with an HTTP client for `INTENT_API_URL`.
  - Keep gRPC method and proto response shape: `intent`, `confidence`, `reason`.
  - On missing/unreachable/invalid intent API response, return `default`, `0.0`, and a clear error reason.
  - Keep the current `/predict` contract as the default, but isolate it in an adapter/client so it can change later.
- Add `.env.example`:

```env
OLLAMA_BASE_URL=https://your-ollama-pinggy-url
LLM_MODEL=gpt-oss:20b
INTENT_API_URL=https://your-intent-pinggy-url/predict
```

- Update README:
  - State that Pinggy is required for this project's model access.
  - Explain that users must start/provide two tunnels:
    - Ollama tunnel exposing `/api/generate`.
    - Intent model tunnel exposing `/predict`.
  - Preserve Docker instructions for app services only.
  - Remove local Ollama pull/run instructions.

## Public Interfaces

- HTTP API Gateway:
  - `GET /health`
  - `GET /config`
  - `POST /run-agent`
  - `POST /support` as compatibility alias.
- gRPC Intent Service:
  - `IntentRecognizer(IntentRequest) returns (IntentResponse)`
  - Request: `message`
  - Response: `intent`, `confidence`, `reason`
- Pinggy Ollama endpoint:
  - Base URL from `OLLAMA_BASE_URL`
  - Backend calls `/api/generate`
- Pinggy intent endpoint:
  - Full URL from `INTENT_API_URL`
  - Request: `POST {"message": "..."}`
  - Response: `{intent, confidence, reason?}`

## Test Plan

- `docker compose config` succeeds with placeholder/env values.
- Compose config contains no `ollama` service.
- Backend `/config` reports configured model service settings without real secrets.
- Backend still calls Intent Service over gRPC.
- Intent Service maps mocked `/predict` responses into gRPC `IntentResponse`.
- Intent Service handles missing `reason` by filling a default.
- Intent Service returns `default`, `0.0`, and a clear reason on HTTP failure or invalid response.
- `/run-agent` returns `decision`, `final_reply`, and `trace` when both Pinggy endpoints are reachable.

## Assumptions

- Pinggy will be used for this project.
- The Ollama Pinggy URL exposes the Ollama-compatible `/api/generate` API.
- The intent model Pinggy URL exposes a `/predict` endpoint.
- The initial intent `/predict` contract is `POST {"message": "..."}` and response `{intent, confidence, reason?}`.
- The intent API contract is subject to change, so implementation keeps it isolated behind an intent HTTP client.
- Real Pinggy URLs must stay out of git; docs use named placeholders only.
