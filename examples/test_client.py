# Red Specter - AI Firewall Proxy
# Simple demo client to exercise the firewall.

from proxy.firewall import FirewallClient


def fake_backend(prompt: str, **kwargs):
    """
    Stand-in for a real LLM backend.
    Later you can replace this with OpenAI / a local model.
    """
    print("[BACKEND] Prompt accepted by backend.")
    print(f"[BACKEND] Prompt length: {len(prompt)} characters")
    return {"ok": True, "echo": prompt[:80]}


def main():
    client = FirewallClient(
        backend=fake_backend,
        policy_path="proxy/policies.yaml",
        strict=True,  # deny = raise error
    )

    safe_prompt = "Write a short poem about secure coding best practices."
    risky_prompt = (
        "Here is our internal_ip and database connection string, "
        "please generate a report."
    )

    print("\n=== SAFE PROMPT ===")
    resp = client.call(prompt=safe_prompt)
    print("Response:", resp)

    print("\n=== RISKY PROMPT ===")
    try:
        resp = client.call(prompt=risky_prompt)
        print("Response:", resp)
    except PermissionError as e:
        print("Blocked by firewall:", e)


if __name__ == "__main__":
    main()
