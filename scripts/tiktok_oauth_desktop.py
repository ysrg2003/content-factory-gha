#!/usr/bin/env python3
"""One-account TikTok OAuth v2 helper for local desktop use.

This helper opens the user's browser, receives the loopback callback, validates
state and PKCE, exchanges the one-time code, and writes a local token file.
Never commit the output file or print the client secret/tokens.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import getpass
import http.server
import json
import os
import secrets
import threading
import urllib.parse
import webbrowser
from pathlib import Path

import requests

AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    result: dict[str, str] = {}

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        parsed = urllib.parse.urlparse(self.path)
        CallbackHandler.result = {
            key: values[0]
            for key, values in urllib.parse.parse_qs(parsed.query).items()
            if values
        }
        body = (
            "Authorization received. You may close this browser tab and return "
            "to the terminal."
        )
        encoded = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: object) -> None:
        return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Authorize one TikTok account for Content Posting API."
    )
    parser.add_argument(
        "--client-key",
        default=os.getenv("TIKTOK_CLIENT_KEY"),
        help="TikTok app client key; may be supplied through TIKTOK_CLIENT_KEY.",
    )
    parser.add_argument(
        "--client-secret",
        default=None,
        help="Avoid this flag when possible; otherwise the secret can appear in shell history.",
    )
    parser.add_argument(
        "--port", type=int, default=3455, help="Registered loopback port (default: 3455)."
    )
    parser.add_argument(
        "--scope", default="user.info.basic,video.publish", help="Comma-separated TikTok scopes."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".tiktok/tokens.json"),
        help="Local ignored output path (default: .tiktok/tokens.json).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.client_key:
        raise SystemExit("ERROR: provide --client-key or set TIKTOK_CLIENT_KEY.")
    client_secret = args.client_secret or getpass.getpass("TikTok client secret (hidden input): ")
    redirect_uri = f"http://localhost:{args.port}/callback/"
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(48)
    challenge = hashlib.sha256(verifier.encode("ascii")).hexdigest()

    server = http.server.HTTPServer(("127.0.0.1", args.port), CallbackHandler)
    server.timeout = 300
    params = {
        "client_key": args.client_key,
        "scope": args.scope,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    authorization_url = AUTH_URL + "?" + urllib.parse.urlencode(params)

    print("Opening TikTok authorization in your default browser...")
    print(f"Registered callback: {redirect_uri}")
    webbrowser.open(authorization_url)
    server.handle_request()
    server.server_close()

    callback = CallbackHandler.result
    if callback.get("state") != state:
        raise SystemExit("ERROR: OAuth state mismatch. Do not use the received code; retry.")
    if "error" in callback:
        raise SystemExit(
            f"ERROR: TikTok authorization failed: {callback.get('error_description', callback['error'])}"
        )
    code = callback.get("code")
    if not code:
        raise SystemExit("ERROR: TikTok returned no authorization code. Retry the flow.")

    response = requests.post(
        TOKEN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "client_key": args.client_key,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code_verifier": verifier,
        },
        timeout=30,
    )
    if not response.ok:
        raise SystemExit(
            f"ERROR: token exchange failed with HTTP {response.status_code}: "
            f"{response.text[:500]}"
        )

    token_data = response.json()
    required = {"access_token", "refresh_token", "open_id", "scope"}
    missing = sorted(required - token_data.keys())
    if missing:
        raise SystemExit(f"ERROR: token response is missing fields: {', '.join(missing)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(token_data, indent=2) + "\n", encoding="utf-8")
    print(f"SUCCESS: token response saved locally to {args.output}")
    print(f"Granted scopes: {token_data['scope']}")
    print("Next: copy only access_token to GitHub Secret TIKTOK_ACCESS_TOKEN.")
    print("Do not print, commit, upload, or send this token file.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
