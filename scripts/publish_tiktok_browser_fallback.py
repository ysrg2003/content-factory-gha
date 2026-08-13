#!/usr/bin/env python3
"""Emergency-only TikTok browser publisher, invoked only after official API failure."""

from __future__ import annotations

import base64
import json
import os
import re
import sys
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required secret: {name}")
    return value


def main() -> int:
    video = Path(os.environ.get("VIDEO_PATH", "processed_video.mp4"))
    metadata_path = Path(os.environ.get("METADATA_PATH", "temp/metadata.json"))
    if not video.is_file() or not metadata_path.is_file():
        raise RuntimeError("The processed video and metadata files must exist.")

    try:
        cookies = json.loads(base64.b64decode(required_env("TIKTOK_BROWSER_COOKIES_BASE64")).decode("utf-8"))
    except Exception as error:
        raise RuntimeError("TIKTOK_BROWSER_COOKIES_BASE64 must be valid base64-encoded cookie JSON.") from error
    if not isinstance(cookies, list):
        raise RuntimeError("Decoded TikTok cookie data must be a JSON list.")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    caption = metadata["tiktok_caption"][:2200]
    button_pattern = re.compile(os.environ.get("TIKTOK_FALLBACK_PUBLISH_LABEL", r"^(Post|Publish|نشر)$"), re.I)
    result: dict[str, str] = {"platform": "tiktok-browser-fallback", "status": "started"}

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(locale="en-US")
        context.add_cookies(cookies)
        page = context.new_page()
        try:
            page.goto("https://www.tiktok.com/tiktokstudio/upload", wait_until="domcontentloaded", timeout=60000)
            page.locator('input[type="file"]').first.set_input_files(str(video))
            caption_box = page.locator('[contenteditable="true"]').first
            caption_box.wait_for(state="visible", timeout=120000)
            caption_box.fill(caption)

            # Wait until the platform has enabled publication after video processing.
            publish_button = page.get_by_role("button", name=button_pattern).last
            publish_button.wait_for(state="visible", timeout=300000)
            publish_button.click(timeout=30000)
            page.wait_for_timeout(10000)
            result["status"] = "publish_click_submitted"
        except PlaywrightTimeoutError as error:
            raise RuntimeError("TikTok Studio did not reach an expected upload/publish state in time.") from error
        finally:
            context.close()
            browser.close()

    Path("publish-result-tiktok-browser.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"TikTok browser fallback failed: {error}", file=sys.stderr)
        raise SystemExit(1)
