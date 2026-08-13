#!/usr/bin/env python3
"""Publish a local processed video as an Instagram Reel and/or Facebook Page Reel."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import requests

VERSION = os.environ.get("META_GRAPH_VERSION", "v26.0")
GRAPH = f"https://graph.facebook.com/{VERSION}"
UPLOAD = "https://rupload.facebook.com"


def required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required secret: {name}")
    return value


def response_json(response: requests.Response) -> dict[str, Any]:
    try:
        payload = response.json()
    except ValueError:
        payload = {"raw": response.text[:500]}
    if not response.ok:
        raise RuntimeError(f"Meta API {response.status_code}: {json.dumps(payload, ensure_ascii=False)}")
    return payload


def wait_for_instagram_container(container_id: str, token: str, timeout_seconds: int = 900) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        data = response_json(requests.get(
            f"{GRAPH}/{container_id}",
            params={"fields": "status_code,status", "access_token": token},
            timeout=30,
        ))
        status = data.get("status_code")
        print(f"Instagram container {container_id}: {status}")
        if status == "FINISHED":
            return
        if status in {"ERROR", "EXPIRED"}:
            raise RuntimeError(f"Instagram media processing failed: {data}")
        time.sleep(10)
    raise RuntimeError("Timed out waiting for Instagram media processing.")


def publish_instagram(video: Path, metadata: dict[str, Any], token: str) -> dict[str, Any]:
    account_id = required_env("META_INSTAGRAM_ACCOUNT_ID")
    create = response_json(requests.post(
        f"{GRAPH}/{account_id}/media",
        data={
            "media_type": "REELS",
            "upload_type": "resumable",
            "caption": metadata["instagram_caption"][:2200],
            "share_to_feed": "true",
            "access_token": token,
        },
        timeout=30,
    ))
    container_id = create["id"]
    print(f"Created Instagram container {container_id}")

    with video.open("rb") as handle:
        uploaded = response_json(requests.post(
            f"{UPLOAD}/ig-api-upload/{container_id}",
            headers={
                "Authorization": f"OAuth {token}",
                "offset": "0",
                "file_size": str(video.stat().st_size),
                "Content-Type": "application/octet-stream",
            },
            data=handle,
            timeout=900,
        ))
    print(f"Instagram upload response: {uploaded}")
    wait_for_instagram_container(container_id, token)
    published = response_json(requests.post(
        f"{GRAPH}/{account_id}/media_publish",
        data={"creation_id": container_id, "access_token": token},
        timeout=30,
    ))
    return {"platform": "instagram", "container_id": container_id, "id": published.get("id")}


def wait_for_facebook_video(video_id: str, token: str, timeout_seconds: int = 900) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        data = response_json(requests.get(
            f"{GRAPH}/{video_id}",
            params={"fields": "status", "access_token": token},
            timeout=30,
        ))
        status = data.get("status", {})
        processing = status.get("processing_phase", {}).get("status")
        print(f"Facebook video {video_id}: {processing or status}")
        if processing == "complete":
            return
        if processing in {"error", "failed"} or status.get("video_status") == "error":
            raise RuntimeError(f"Facebook video processing failed: {data}")
        time.sleep(10)
    raise RuntimeError("Timed out waiting for Facebook video processing.")


def publish_facebook(video: Path, metadata: dict[str, Any], token: str) -> dict[str, Any]:
    page_id = required_env("META_FACEBOOK_PAGE_ID")
    started = response_json(requests.post(
        f"{GRAPH}/{page_id}/video_reels",
        json={"upload_phase": "start", "access_token": token},
        timeout=30,
    ))
    video_id = started["video_id"]
    upload_url = started.get("upload_url") or f"{UPLOAD}/video-upload/{VERSION}/{video_id}"
    print(f"Created Facebook Reel upload session {video_id}")

    with video.open("rb") as handle:
        uploaded = response_json(requests.post(
            upload_url,
            headers={
                "Authorization": f"OAuth {token}",
                "offset": "0",
                "file_size": str(video.stat().st_size),
                "Content-Type": "application/octet-stream",
            },
            data=handle,
            timeout=900,
        ))
    if not uploaded.get("success", True):
        raise RuntimeError(f"Facebook upload was not accepted: {uploaded}")
    wait_for_facebook_video(video_id, token)
    published = response_json(requests.post(
        f"{GRAPH}/{page_id}/video_reels",
        data={
            "access_token": token,
            "video_id": video_id,
            "upload_phase": "finish",
            "video_state": "PUBLISHED",
            "title": metadata["title"][:100],
            "description": metadata["facebook_caption"][:5000],
        },
        timeout=60,
    ))
    if not published.get("success", True):
        raise RuntimeError(f"Facebook publish was not accepted: {published}")
    return {"platform": "facebook", "id": video_id, "url": f"https://www.facebook.com/{video_id}"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", default=os.environ.get("VIDEO_PATH", "processed_video.mp4"))
    parser.add_argument("--metadata", default=os.environ.get("METADATA_PATH", "temp/metadata.json"))
    parser.add_argument("--instagram", action="store_true")
    parser.add_argument("--facebook", action="store_true")
    args = parser.parse_args()
    if not args.instagram and not args.facebook:
        raise RuntimeError("Choose --instagram and/or --facebook.")

    video = Path(args.video)
    metadata_path = Path(args.metadata)
    if not video.is_file() or not metadata_path.is_file():
        raise RuntimeError("The processed video and metadata files must exist.")
    token = required_env("META_PAGE_ACCESS_TOKEN")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    if args.instagram:
        results.append(publish_instagram(video, metadata, token))
    if args.facebook:
        results.append(publish_facebook(video, metadata, token))
    for result in results:
        Path(f"publish-result-{result['platform']}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(json.dumps(results, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Meta publishing failed: {error}", file=sys.stderr)
        raise SystemExit(1)
