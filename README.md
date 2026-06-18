# agents

## seeai-image

SeeAI image generation Skill. It reads `GEN_IMAGE_API_KEY` from the environment or a local `.env` file and writes decoded PNG files to disk.

### One-line LLM install prompts

Codex:

```text
Install the seeai-image Skill from https://github.com/let5sne/agents by copying only skills/seeai-image into ~/.codex/skills/seeai-image, or %USERPROFILE%\.codex\skills\seeai-image on Windows.
```

Claude Code:

```text
Install the seeai-image Skill from https://github.com/let5sne/agents by copying only skills/seeai-image into ~/.claude/skills/seeai-image, or %USERPROFILE%\.claude\skills\seeai-image on Windows.
```

### Install for Codex

macOS/Linux:

```bash
tmp="$(mktemp -d)"
git clone --depth 1 https://github.com/let5sne/agents.git "$tmp/agents"
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/seeai-image
cp -R "$tmp/agents/skills/seeai-image" ~/.codex/skills/
```

Windows PowerShell:

```powershell
$tmp = Join-Path $env:TEMP "let5sne-agents"
Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
git clone --depth 1 https://github.com/let5sne/agents.git $tmp
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Remove-Item -Recurse -Force "$env:USERPROFILE\.codex\skills\seeai-image" -ErrorAction SilentlyContinue
Copy-Item -Recurse "$tmp\skills\seeai-image" "$env:USERPROFILE\.codex\skills\"
```

### Install for Claude Code

macOS/Linux:

```bash
tmp="$(mktemp -d)"
git clone --depth 1 https://github.com/let5sne/agents.git "$tmp/agents"
mkdir -p ~/.claude/skills
rm -rf ~/.claude/skills/seeai-image
cp -R "$tmp/agents/skills/seeai-image" ~/.claude/skills/
```

Windows PowerShell:

```powershell
$tmp = Join-Path $env:TEMP "let5sne-agents"
Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
git clone --depth 1 https://github.com/let5sne/agents.git $tmp
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude\skills\seeai-image" -ErrorAction SilentlyContinue
Copy-Item -Recurse "$tmp\skills\seeai-image" "$env:USERPROFILE\.claude\skills\"
```

### Configure

macOS/Linux:

```bash
export GEN_IMAGE_API_KEY="your-key"
```

Windows PowerShell:

```powershell
[Environment]::SetEnvironmentVariable("GEN_IMAGE_API_KEY", "your-key", "User")
```

Restart Codex or Claude Code after setting a persistent environment variable.

### Use

Ask the agent:

```text
Use $seeai-image to generate a PNG: 一只橘猫戴着橙色围巾抱着水獭，温暖插画风格. Save it as image.png.
```

Or run the script directly:

```bash
python3 ~/.codex/skills/seeai-image/scripts/generate_image.py --prompt "一只橘猫戴着橙色围巾" --out image.png
```
