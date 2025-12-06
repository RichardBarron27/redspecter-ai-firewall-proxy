# Red Specter - AI Firewall Proxy
# Core policy engine + wrapper client.

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List

import yaml  # make sure pyyaml is installed: pip install pyyaml

from .logger import write_event, DEFAULT_LOG_PATH


PolicyDict = Dict[str, Any]
BackendCallable = Callable[..., Any]


@dataclass
class PolicyDecision:
    action: str              # "allow", "warn", "deny"
    reason: str
    matches: Dict[str, List[str]]  # {"deny": [...], "warn": [...]}


class PolicyEngine:
    def __init__(self, policy_path: str) -> None:
        self.policy_path = Path(policy_path)
        self.policy: PolicyDict = self._load_policy()

    def _load_policy(self) -> PolicyDict:
        if not self.policy_path.exists():
            raise FileNotFoundError(f"Policy file not found: {self.policy_path}")
        with self.policy_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        # Set defaults
        data.setdefault("mode", "enforce")
        data.setdefault("deny_terms", [])
        data.setdefault("warn_terms", [])
        data.setdefault("block_jailbreak_like", True)
        return data

    def reload(self) -> None:
        """Reload policy from disk."""
        self.policy = self._load_policy()

    @staticmethod
    def _find_matches(text: str, terms: List[str]) -> List[str]:
        matches: List[str] = []
        lower = text.lower()
        for term in terms:
            if term.lower() in lower:
                matches.append(term)
        return matches

    @staticmethod
    def _looks_like_jailbreak(text: str) -> bool:
        jailbreak_patterns = [
            r"ignore (all )?previous instructions",
            r"\bjailbreak\b",
            r"you are no longer bound by",
            r"bypass .*safety",
        ]
        lower = text.lower()
        return any(re.search(pat, lower) for pat in jailbreak_patterns)

    def evaluate(self, prompt: str) -> PolicyDecision:
        deny_terms = self.policy.get("deny_terms", [])
        warn_terms = self.policy.get("warn_terms", [])
        block_jb = bool(self.policy.get("block_jailbreak_like", True))

        deny_matches = self._find_matches(prompt, deny_terms)
        warn_matches = self._find_matches(prompt, warn_terms)

        matches: Dict[str, List[str]] = {
            "deny": deny_matches,
            "warn": warn_matches,
        }

        if deny_matches:
            return PolicyDecision(
                action="deny",
                reason=f"Matched deny terms: {', '.join(deny_matches)}",
                matches=matches,
            )

        if block_jb and self._looks_like_jailbreak(prompt):
            matches.setdefault("deny", []).append("jailbreak_pattern")
            return PolicyDecision(
                action="deny",
                reason="Prompt looks like a jailbreak attempt",
                matches=matches,
            )

        if warn_matches:
            return PolicyDecision(
                action="warn",
                reason=f"Matched warn terms: {', '.join(warn_matches)}",
                matches=matches,
            )

        return PolicyDecision(
            action="allow",
            reason="No policy violations detected",
            matches=matches,
        )


class FirewallClient:
    """
    Wraps an LLM backend callable and enforces Red Specter AI firewall policies.

    backend: a callable like `lambda prompt, **kw: openai.ChatCompletion.create(...)`
    """

    def __init__(
        self,
        backend: BackendCallable,
        policy_path: str = "proxy/policies.yaml",
        log_path: str = DEFAULT_LOG_PATH,
        strict: bool = True,
    ) -> None:
        self.backend = backend
        self.engine = PolicyEngine(policy_path)
        self.log_path = log_path
        self.strict = strict  # if False, "deny" returns a stub instead of raising

    def _hash_prompt(self, prompt: str) -> str:
        # We never log raw prompts, only a hash for correlation.
        return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

    def call(self, prompt: str, **kwargs: Any) -> Any:
        decision = self.engine.evaluate(prompt)

        event = {
            "component": "ai_firewall_proxy",
            "action": decision.action,
            "reason": decision.reason,
            "matches": decision.matches,
            "prompt_hash": self._hash_prompt(prompt),
            "prompt_length": len(prompt),
        }
        write_event(event, path=self.log_path)

        if decision.action == "deny":
            if self.strict:
                raise PermissionError(
                    f"[AI FIREWALL] Prompt denied: {decision.reason}"
                )
            # Non-strict mode: return a stub response
            return {
                "blocked": True,
                "reason": decision.reason,
            }

        if decision.action == "warn":
            # Could print/log extra info here if desired
            pass

        # Forward to the real backend
        return self.backend(prompt=prompt, **kwargs)
