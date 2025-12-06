# 🛡️ Red Specter – AI Firewall Proxy

Lightweight Python wrapper that enforces security policies around AI / LLM prompts
before they reach the model. Designed to prevent sensitive data leakage and risky
prompt behaviour.

> Current Release: **v0.1 (MVP)**

## Features
- Policy-driven allow / warn / deny decisions
- Detects sensitive terms in prompts
- Blocks jailbreak-like instructions
- Metadata-only logging (no prompt content stored)
- Easy drop-in wrapper for any LLM backend

## Quick Demo

```bash
python -m examples.test_client
