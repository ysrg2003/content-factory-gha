#!/usr/bin/env python3
"""Publish a processed local video via TikTok Content Posting API Direct Post."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests

API = "https://open.tiktokapis.com"
CHUNK_SIZE = 10 * 1024 * 1024


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required secret: {name}")
    return value


def api_response(response: requests.Response) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text[:500]}
    if not response.ok or payload.get("error", {}).get("code") not in {None, "ok"}:
        raise RuntimeError(f"TikTok API {response.status_code}: {json.dumps(payload, ensure_ascii=False)}")
    return payload


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json; charset=UTF-8"}


def get_creator_info(token: str) -> dict[str, Any]:
    return api_response(requests.post(
        f"{API}/v2/post/publish/creator_info/query/", headers=auth_headers(token), json={}, timeout=30
    )).get("data", {})


def upload_file(upload_url: str, video: Path) -> None:
    total_size = video.stat().st_size
    with video.open("rb") as handle:
        offset = 0
        while offset < total_size:
            chunk = handle.read(min(CHUNK_SIZE, total_size - offset))
            if not chunk:
                raise RuntimeError("Unexpected end of file during TikTok upload.")
            end = offset + len(chunk) - 1
            response = requests.put(
                upload_url,
                headers={
                    "Content-Type": "video/mp4",
                    "Content-Length": str(len(chunk)),
                    "Content-Range": f"bytes {offset}-{end}/{total_size}",
                },
                data=chunk,
                timeout=900,
            )
            if not response.ok:
                raise RuntimeError(f"TikTok upload failed at byte {offset}: {response.status_code} {response.text[:500]}")
            offset = end + 1
            print(f"Uploaded TikTok bytes {offset}/{total_size}")


def wait_for_status(token: str, publish_id: str, timeout_seconds: int = 900) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        data = api_response(requests.post(
            f"{API}/v2/post/publish/status/fetch/",
            headers=auth_headers(token),
            json={"publish_id": publish_id},
            timeout=30,
        )).get("data", {})
        status = data.get("status")
        print(f"TikTok publish {publish_id}: {status}")
        if status == "PUBLISH_COMPLETE":
            return data
        if status in {"FAILED", "PUBLISH_FAILED"}:
            raise RuntimeError(f"TikTok publishing failed: {data}")
        time.sleep(10)
    raise RuntimeError("Timed out waiting for TikTok publishing.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", default=os.environ.get("VIDEO_PATH", "processed_video.mp4"))
    parser.add_argument("--metadata", default=os.environ.get("METADATA_PATH", "temp/metadata.json"))
    args = parser.parse_args()
    video, metadata_path = Path(args.video), Path(args.metadata)
    if not video.is_file() or not metadata_path.is_file():
        raise RuntimeError("The processed video and metadata files must exist.")

    token = required_env("TIKTOK_ACCESS_TOKEN")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    creator = get_creator_info(token)
    requested_privacy = os.environ.get("TIKTOK_PRIVACY_LEVEL", "PUBLIC_TO_EVERYONE")
    options = creator.get("privacy_level_options", [])
    if requested_privacy not in options:
        raise RuntimeError(
            f"TIKTOK_PRIVACY_LEVEL={requested_privacy} is not authorized. Available values: {options}"
        )

    total_size = video.stat().st_size
    payload = {
        "post_info": {
            "title": metadata["tiktok_caption"][:2200],
            "privacy_level": requested_privacy,
            "disable_duet": os.environ.get("TIKTOK_DISABLE_DUET", "false").lower() == "true",
            "disable_stitch": os.environ.get("TIKTOK_DISABLE_STITCH", "false").lower() == "true",
            "disable_comment": os.environ.get("TIKTOK_DISABLE_COMMENT", "false").lower() == "true",
            "brand_content_toggle": os.environ.get("TIKTOK_BRAND_CONTENT", "false").lower() == "true",
            "brand_organic_toggle": os.environ.get("TIKTOK_BRAND_ORGANIC", "false").lower() == "true",
            "is_aigc": bool(metadata.get("contains_synthetic_media", False)),
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": total_size,
            "chunk_size": min(CHUNK_SIZE, total_size),
            "total_chunk_count": math.ceil(total_size / CHUNK_SIZE),
        },
    }
    initialized = api_response(requests.post(
        f"{API}/v2/post/publish/video/init/", headers=auth_headers(token), json=payload, timeout=30
    )).get("data", {})
    publish_id, upload_url = initialized.get("publish_id"), initialized.get("upload_url")
    if not publish_id or not upload_url:
        raise RuntimeError(f"TikTok did not return publish_id/upload_url: {initialized}")
    upload_file(upload_url, video)
    status = wait_for_status(token, publish_id)
    result = {"platform": "tiktok", "publish_id": publish_id, "status": status}
    Path("publish-result-tiktok.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"TikTok publishing failed: {error}", file=sys.stderr)
        raise SystemExit(1)
