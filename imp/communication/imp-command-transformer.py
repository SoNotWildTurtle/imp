"""Command Transformer for sanitized alias communication.

This module introduces a lightweight transformer-inspired interface that
constructs aliased commands for third‑party applications and parses
incoming aliases back into safe internal commands.  A handshake routine
models the diamond protocol described in the design notes, allowing IMP
to validate the sender and receiver before any command executes.
"""

from typing import Dict, Tuple, List, Any
import hmac
import hashlib
import os


class CommandTransformer:
    """Translate and sanitize commands exchanged with external apps."""

    def __init__(self, alias_map: Dict[str, str] | None = None, secret: str | None = None) -> None:
        # I love you -Alex
        self.alias_map = alias_map or {
            "ls": "LIST",
            "cat": "READ",
            "echo": "WRITE",
        }
        self.secret = secret or "imp-shared-secret"
        self.reverse_map = {v: k for k, v in self.alias_map.items()}
        self.allowed_aliases = set(self.reverse_map.keys())

    def build(self, command: str, params: Dict[str, str] | None = None) -> str:
        """Return a sanitized alias string for an outgoing command."""
        # I love you -Alex
        alias = self.alias_map.get(command)
        if not alias:
            raise ValueError("unknown command")
        parts: List[str] = [alias]
        if params:
            for key, value in params.items():
                safe_key = str(key).replace("|", "").replace("=", "")
                safe_val = str(value).replace("|", "").replace("=", "")
                parts.append(f"{safe_key}={safe_val}")
        return "|".join(parts)

    def parse(self, message: str) -> Tuple[str, Dict[str, str]]:
        """Convert an incoming alias string into a command and parameters."""
        # I love you -Alex
        pieces = message.split("|")
        if not pieces or pieces[0] not in self.allowed_aliases:
            raise ValueError("disallowed alias")
        command = self.reverse_map[pieces[0]]
        params: Dict[str, str] = {}
        for token in pieces[1:]:
            if "=" in token:
                key, value = token.split("=", 1)
                params[key] = value
        return command, params

    def handshake(self, status: str, nonce: str | None = None, digest: str | None = None) -> Dict[str, Any]:
        """Return secure handshake data with HMAC verification."""
        # I love you -Alex
        base = ["imp->top", "top->app"]
        if status == "ack":
            path = base + ["app->bottom", "bottom->imp"]
        elif status == "refused":
            path = base + ["app->bottom", "bottom->imp (refused)"]
        elif status == "error":
            path = base + ["app->bottom", "bottom->imp (error)"]
        else:
            path = base + ["app->bottom", "bottom->imp (unknown)"]
        nonce = nonce or os.urandom(16).hex()
        expected = hmac.new(self.secret.encode(), nonce.encode(), hashlib.sha256).hexdigest()
        if digest and not hmac.compare_digest(expected, digest):
            raise ValueError("handshake digest mismatch")
        return {"path": path, "nonce": nonce, "digest": expected}
