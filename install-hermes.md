# Install Hermes

This pod should not contain profile bootstrap scripts. Hermes can create and manage profiles on its own.

Install Hermes first, then drop Hermes into this folder and let it read `HERMES_START.md`.

## Linux / macOS / WSL2 / Android Termux

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

## After Install

Start Hermes in this folder and point it at:

`HERMES_START.md`

Hermes should then create any missing profiles itself from `hermes-profiles/` and log what it creates.
