#!/usr/bin/env python3
"""Static verification for repository structure and direct-publishing invariants."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "pipeline.py",
    "publish_youtube.py",
    "publish_meta.py",
    "publish_tiktok_api.py",
    "publish_tiktok_browser_fallback.py",
]


def main() -> None:
    for script in SCRIPTS:
        ast.parse((ROOT / "scripts" / script).read_text(encoding="utf-8"), filename=script)

    workflow = (ROOT / ".github/workflows/publish.yml").read_text(encoding="utf-8").lower()
    assert "telegram.org" not in workflow, "Telegram API calls are not allowed."
    assert "telegram_bot_token" not in workflow, "Telegram secrets are not allowed."
    assert "repository_dispatch" not in workflow, "No approval dispatcher is allowed."
    assert "workflow_dispatch" in workflow, "Manual start form is required."
    assert "publish_tiktok_api.py" in workflow, "Official TikTok API must remain primary."
    assert "steps.tiktok_api.outcome == 'failure'" in workflow, "Fallback must only run after API failure."
    assert "allow_tiktok_browser_fallback" in workflow, "Fallback must require explicit selection."
    assert "retention-days: 1" in workflow, "Generated videos must have short retention."

    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    for protected in (".env", "processed_video.mp4", "storage_state.json"):
        assert protected in gitignore, f"{protected} must be ignored."
    print("Static project validation passed.")


if __name__ == "__main__":
    main()
