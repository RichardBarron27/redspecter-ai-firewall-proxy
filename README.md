<p align="center">
  <img src="https://raw.githubusercontent.com/RichardBarron27/red-specter-offensive-framework/main/assets/red-specter-logo.png" alt="Red Specter Logo" width="200">
</p>

 # 🛡️ Red Specter – AI Firewall Proxy

![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)
![Language](https://img.shields.io/badge/Python-3.10+-blue)
![Status](https://img.shields.io/badge/Status-MVP_v0.1-orange)
![Version](https://img.shields.io/github/v/release/RichardBarron27/redspecter-ai-firewall-proxy?label=Release)
> Part of the **Red Specter Purple Team AI Defense Suite**
> Offense-driven defense against AI-enabled threats.

Lightweight Python wrapper that enforces security policies around AI / LLM prompts
before they reach the model. Designed to prevent sensitive data leakage and risky
prompt behaviour.

---


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
## ⭐ Support & Contribute

If you find this project useful, please **star the repo** — it really helps!

Found a bug or have an idea?  
👉 Open an Issue here: https://github.com/RichardBarron27/redspecter-ai-firewall-proxy/issues
