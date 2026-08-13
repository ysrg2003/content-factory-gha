#!/usr/bin/env python3
"""Convert a source video to a vertical short, burn Arabic captions, and create metadata."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import whisper


def run(command: list[str]) -> None:
    print("$ " + " ".join(command))
    subprocess.run(command, check=True)


def srt_timestamp(seconds: float) -> str:
    milliseconds = round((seconds - int(seconds)) * 1000)
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def write_srt(segments: list[dict[str, Any]], output: Path) -> None:
    with output.open("w", encoding="utf-8") as handle:
        for index, segment in enumerate(segments, start=1):
            text = segment["text"].strip()
            if not text:
                continue
            handle.write(
                f"{index}\n{srt_timestamp(segment['start'])} --> "
                f"{srt_timestamp(segment['end'])}\n{text}\n\n"
            )


def transcribe(audio: Path, language: str, model_name: str) -> tuple[str, list[dict[str, Any]]]:
    print(f"Transcribing audio with Whisper model: {model_name}")
    model = whisper.load_model(model_name)
    result = model.transcribe(str(audio), language=language, fp16=False, verbose=False)
    return result["text"].strip(), result["segments"]


def generate_metadata(transcript: str) -> dict[str, Any]:
    """Generate strict JSON through OpenAI; no silent publication if this stage fails."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required to generate publishing metadata.")

    from openai import OpenAI

    model = os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    prompt = f"""
أنت محرر محتوى قصير محترف. أنشئ بيانات وصفية عربية من النص التالي.
أعد كائناً JSON صالحاً فقط، بلا Markdown وبالمفاتيح التالية حصراً:
- title: عنوان قصير (حد أقصى 90 حرفاً)
- youtube_description: وصف مناسب ليوتيوب، حتى 3000 حرف
- instagram_caption: وصف Reel مناسب لإنستغرام، حتى 2200 حرف
- facebook_caption: وصف Reel مناسب لصفحة فيسبوك، حتى 5000 حرف
- tiktok_caption: وصف TikTok مناسب، حتى 2200 حرف
- tags: مصفوفة من 3 إلى 12 وسم يوتيوب من دون #
- contains_synthetic_media: true أو false

لا تدّعِ حقائق لا تظهر في النص، ولا تضف دعوات مضللة أو ادعاءات طبية/مالية.
النص:
{transcript}
""".strip()
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.45,
    )
    raw = response.choices[0].message.content or ""
    try:
        metadata = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Model returned invalid JSON: {raw[:300]}") from exc

    required = {
        "title", "youtube_description", "instagram_caption", "facebook_caption",
        "tiktok_caption", "tags", "contains_synthetic_media",
    }
    missing = required.difference(metadata)
    if missing or not isinstance(metadata.get("tags"), list):
        raise RuntimeError(f"Metadata schema is incomplete; missing: {sorted(missing)}")
    return metadata


def process_video(input_path: Path, output_path: Path, language: str, whisper_model: str) -> Path:
    temp_dir = output_path.parent / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    audio_path = temp_dir / "audio.wav"
    subtitles_path = temp_dir / "subtitles.srt"

    run([
        "ffmpeg", "-y", "-i", str(input_path), "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1", str(audio_path),
    ])
    transcript, segments = transcribe(audio_path, language, whisper_model)
    if not transcript:
        raise RuntimeError("Whisper produced an empty transcript; refusing to publish.")
    write_srt(segments, subtitles_path)

    escaped_srt = str(subtitles_path.resolve()).replace("\\", "\\\\").replace(":", "\\:").replace("'", r"\'")
    filter_graph = (
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        f"subtitles='{escaped_srt}':force_style="
        "'FontName=Arial,FontSize=20,Bold=1,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,BorderStyle=1,Outline=2,Alignment=2'"
    )
    run([
        "ffmpeg", "-y", "-i", str(input_path), "-vf", filter_graph,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
        str(output_path),
    ])

    metadata = generate_metadata(transcript)
    metadata["transcript"] = transcript
    metadata["generated_at"] = datetime.now(timezone.utc).isoformat()
    metadata["video_file"] = output_path.name
    metadata_path = temp_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Created {output_path} and {metadata_path}")
    return metadata_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--language", default="ar")
    parser.add_argument("--whisper-model", default=os.environ.get("WHISPER_MODEL", "base"))
    args = parser.parse_args()
    try:
        process_video(args.input, args.output, args.language, args.whisper_model)
    except (subprocess.CalledProcessError, RuntimeError) as error:
        print(f"Processing failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
