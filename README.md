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
*before* they reach the model — preventing sensitive data leakage and unsafe prompt behavior.

---

## ✨ Features
- Policy-driven allow / warn / deny decisions
- Detects sensitive terms in prompts
- Blocks jailbreak-style manipulation
- Logs metadata only (no prompt contents stored)
- Easy drop-in wrapper for any LLM backend

---

## 🧪 Quick Demo (included)

```bash
python -m examples.test_client
Expected:

✔ Safe prompt → accepted by backend

❌ Risky prompt → blocked with reasons

📝 Logged to: ~/.redspecter_ai_firewall/logs/events.jsonl

🔌 Use with OpenAI (real backend example)
python
Copy code
from proxy.firewall import FirewallClient
from openai import OpenAI

# Your OpenAI configuration
client = OpenAI(api_key="YOUR_API_KEY")

# Backend function to call OpenAI
def openai_backend(prompt: str, **kwargs):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Wrap backend with the Firewall Proxy
fw = FirewallClient(
    backend=openai_backend,
    strict=True,
)

try:
    result = fw.call("Write a short secure coding checklist.")
    print("LLM Response:", result)
except PermissionError as e:
    print("🚫 Blocked by Firewall:", e)
Results
✔ Safe prompts → allowed

❌ Sensitive prompts → blocked with clear reason

📝 All events logged with hashed prompt IDs

Example log entry:

json
Copy code
{
  "timestamp": "2025-12-06T22:07:55Z",
  "component": "ai_firewall_proxy",
  "action": "deny",
  "reason": "Matched deny terms: internal_ip",
  "matches": {"deny": ["internal_ip"], "warn": []},
  "prompt_hash": "a27af91c...",
  "prompt_length": 67
}
🔐 Privacy-first: no raw prompts are ever stored.

🗺 Roadmap
Version	Goal	Status
v0.1	Agent MVP	✔ Released
v0.2	Local Proxy Mode	🔄 In Design
v0.3	SIEM Export + Fleet Policies	⏳ Planned

⭐ Support & Contribute
If you find this project useful, please star the repo — it really helps!

Have an idea or found a bug?
👉 https://github.com/RichardBarron27/redspecter-ai-firewall-proxy/issues

yaml
Copy code
