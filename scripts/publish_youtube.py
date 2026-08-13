#!/usr/bin/env python3
"""Publish the processed video to YouTube using the official Data API."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def env_json(name: str) -> dict:
    raw = os.environ.get(name)
    if not raw:
        raise RuntimeError(f"Missing required secret: {name}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"{name} must contain valid JSON.") from error


def load_credentials() -> Credentials:
    client_secret = env_json("YOUTUBE_CLIENT_SECRET_JSON")
    client = client_secret.get("installed") or client_secret.get("web")
    if not client:
        raise RuntimeError("YOUTUBE_CLIENT_SECRET_JSON must contain installed or web OAuth client data.")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")
    if not refresh_token:
        raise RuntimeError("Missing required secret: YOUTUBE_REFRESH_TOKEN")
    return Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client["client_id"],
        client_secret=client["client_secret"],
        scopes=SCOPES,
    )


def main() -> int:
    video = Path(os.environ.get("VIDEO_PATH", "processed_video.mp4"))
    metadata_path = Path(os.environ.get("METADATA_PATH", "temp/metadata.json"))
    if not video.is_file() or not metadata_path.is_file():
        raise RuntimeError("VIDEO_PATH and METADATA_PATH must point to existing files.")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    privacy = os.environ.get("YOUTUBE_PRIVACY_STATUS", "public")
    if privacy not in {"public", "private", "unlisted"}:
        raise RuntimeError("YOUTUBE_PRIVACY_STATUS must be public, private, or unlisted.")

    body = {
        "snippet": {
            "title": metadata["title"][:100],
            "description": metadata["youtube_description"][:5000],
            "tags": metadata.get("tags", [])[:15],
            "categoryId": os.environ.get("YOUTUBE_CATEGORY_ID", "22"),
            "defaultLanguage": "ar",
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": os.environ.get("YOUTUBE_MADE_FOR_KIDS", "false").lower() == "true",
            "containsSyntheticMedia": bool(metadata.get("contains_synthetic_media", False)),
        },
    }
    service = build("youtube", "v3", credentials=load_credentials(), cache_discovery=False)
    media = MediaFileUpload(str(video), mimetype="video/mp4", resumable=True, chunksize=8 * 1024 * 1024)
    request = service.videos().insert(part="snippet,status", body=body, media_body=media, notifySubscribers=False)

    response = None
    while response is None:
        _, response = request.next_chunk()
    result = {"platform": "youtube", "id": response["id"], "url": f"https://www.youtube.com/shorts/{response['id']}"}
    Path("publish-result-youtube.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"YouTube publishing failed: {error}", file=sys.stderr)
        raise SystemExit(1)
