---
name: seeai-image
description: Generate images through the SeeAI let5see OpenAI-compatible image API. Use when the user asks Codex to create images with api.ai.let5see.xyz, gpt-image-2, response_format b64_json, or wants a cross-platform Windows/macOS/Linux image generation workflow using GEN_IMAGE_API_KEY from .env or environment variables.
---

# SeeAI Image

Use the bundled Python script for real image generation. It uses only the Python standard library, so it works on Windows without curl, jq, Bash, or WSL.

## Quick Start

macOS/Linux:

```bash
python3 ~/.codex/skills/seeai-image/scripts/generate_image.py \
  --env /path/to/.env \
  --prompt "一只橘猫戴着橙色围巾抱着水獭，温暖插画风格" \
  --out image.png
```

Windows PowerShell or CMD:

```powershell
py -3 %USERPROFILE%\.codex\skills\seeai-image\scripts\generate_image.py --env C:\path\to\.env --prompt "一只橘猫戴着橙色围巾抱着水獭，温暖插画风格" --out image.png
```

## Defaults

The script sends this request by default:

- URL: `https://api.ai.let5see.xyz/v1/images/generations`
- env key: `GEN_IMAGE_API_KEY`
- model: `gpt-image-2`
- size: `3840x2160`
- quality: `high`
- output format: `png`
- response format: `b64_json`
- n: `1`

Override with `--model`, `--size`, `--quality`, `--format`, `--n`, `--api-url`, or `--api-key-env`.

## Rules

- Never print or paste API keys in chat, logs, or files.
- Prefer `--env .env` when the user provides a local `.env`; otherwise read `GEN_IMAGE_API_KEY` from the process environment.
- Save decoded image bytes to disk; do not show raw base64.
- If the API returns `503` with `No available compatible accounts`, report that the SeeAI backend account pool is unavailable. The local script and key loading may still be correct.

## Check

Run the local self-check after edits:

```bash
python3 ~/.codex/skills/seeai-image/scripts/generate_image.py --self-test
```
