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

🔌 Use with OpenAI (real backend example)
from proxy.firewall import FirewallClient
from openai import OpenAI

# Your normal OpenAI config
client = OpenAI(api_key="YOUR_API_KEY")

# This is the backend the firewall will call if allowed
def openai_backend(prompt: str, **kwargs):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Wrap the backend with the Firewall Proxy
fw = FirewallClient(
    backend=openai_backend,
    policy_path="proxy/policies.yaml",  # optional override
    strict=True,  # strict=True → deny prompts on violation
)

try:
    result = fw.call("Write a short secure coding checklist.")
    print("LLM Response:", result)
except PermissionError as e:
    print("🚫 Blocked by Firewall:", e)

Results

Safe prompts → ✔ allowed

Sensitive prompts → ❌ blocked with clear policy reason

All activity is logged without storing prompt contents

Logs at:

~/.redspecter_ai_firewall/logs/events.jsonl


Example of a logged event:

{
  "timestamp": "2025-12-06T22:07:55Z",
  "component": "ai_firewall_proxy",
  "action": "deny",
  "reason": "Matched deny terms: internal_ip",
  "matches": {"deny": ["internal_ip"], "warn": []},
  "prompt_hash": "a27af91c...",
  "prompt_length": 67
}


⚠️ No raw prompts are stored — privacy-first by design.

## ⭐ Support & Contribute

If you find this project useful, please **star the repo** — it really helps!

Found a bug or have an idea?  
👉 Open an Issue here: https://github.com/RichardBarron27/redspecter-ai-firewall-proxy/issues
