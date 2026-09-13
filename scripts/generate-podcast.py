#!/usr/bin/env python3
"""
═══════════════════════════════════════
GENERATE PODCAST (two-voice, NotebookLM-style)
1. Extracts the article text from an HTML file.
2. Asks Gemini to write a conversational dialogue between two hosts
   (target 4-6 minutes, engaging, approachable).
3. Synthesizes each speaker via Gemini TTS (different voices).
4. Stitches the audio with ffmpeg into a single MP3.

Requires:
    pip3 install google-genai beautifulsoup4
    brew install ffmpeg

Env:
    GEMINI_API_KEY

Usage:
    python3 scripts/generate-podcast.py blog/my-article/index.html
═══════════════════════════════════════
"""

import base64
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("google-genai not installed. Run: pip3 install google-genai beautifulsoup4", file=sys.stderr)
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("beautifulsoup4 not installed. Run: pip3 install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "assets" / "audio-blog"

SPEAKER_A = os.getenv("GEMINI_TTS_VOICE_A", "Kore")    # warm / clear
SPEAKER_B = os.getenv("GEMINI_TTS_VOICE_B", "Puck")    # curious / playful
MODEL_TEXT = os.getenv("GEMINI_TEXT_MODEL", "gemini-2.5-flash")
MODEL_TTS = os.getenv("GEMINI_TTS_MODEL", "gemini-2.5-flash-preview-tts")


def extract_text(html_path: Path) -> tuple[str, str]:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    title = (soup.title.string if soup.title else html_path.stem).strip()
    article = soup.find("article") or soup.find("main") or soup.body
    for tag in article.find_all(["script", "style", "nav", "footer"]):
        tag.decompose()
    text = re.sub(r"\n\s*\n", "\n\n", article.get_text("\n").strip())
    return title, text


def generate_dialogue(client: genai.Client, title: str, body: str) -> list[tuple[str, str]]:
    system = (
        "You write a short, conversational two-host podcast script in the language of the source article. "
        "Tone: NotebookLM-style — two hosts Alex and Sam chatting warmly, asking each other questions, "
        "reacting, building on each other. 4-6 minutes when read aloud (roughly 700-1000 words). "
        "No introduction music, no ads. Format as lines: 'Alex: ...' or 'Sam: ...'. No other text."
    )
    prompt = f"Source article title: {title}\n\nSource article text:\n{body}\n\nNow write the script."
    resp = client.models.generate_content(
        model=MODEL_TEXT,
        contents=[prompt],
        config=types.GenerateContentConfig(system_instruction=system, temperature=0.7),
    )
    raw = (resp.text or "").strip()
    lines = []
    for ln in raw.splitlines():
        m = re.match(r"^(Alex|Sam)\s*:\s*(.+)$", ln.strip())
        if m:
            lines.append((m.group(1), m.group(2).strip()))
    if not lines:
        sys.exit("Gemini did not return a parseable dialogue.")
    return lines


def synth_line(client: genai.Client, voice: str, text: str, out_path: Path) -> None:
    resp = client.models.generate_content(
        model=MODEL_TTS,
        contents=[text],
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)
                )
            ),
        ),
    )
    audio_data = resp.candidates[0].content.parts[0].inline_data.data
    if isinstance(audio_data, str):
        audio_data = base64.b64decode(audio_data)
    # Gemini returns 24 kHz 16-bit PCM mono; write raw, let ffmpeg wrap it.
    out_path.write_bytes(audio_data)


def concat_to_mp3(pcm_parts: list[Path], out_mp3: Path) -> None:
    with tempfile.TemporaryDirectory() as td:
        list_file = Path(td) / "list.txt"
        with list_file.open("w") as f:
            for p in pcm_parts:
                # Convert each PCM to a temp WAV
                wav = Path(td) / (p.stem + ".wav")
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1",
                        "-i", str(p), str(wav),
                    ],
                    check=True, capture_output=True,
                )
                f.write(f"file '{wav}'\n")
        subprocess.run(
            [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", str(list_file),
                "-c:a", "libmp3lame", "-q:a", "4",
                str(out_mp3),
            ],
            check=True, capture_output=True,
        )


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("Usage: generate-podcast.py <path/to/article.html>")
    html_path = Path(sys.argv[1]).resolve()
    if not html_path.exists():
        sys.exit(f"Not found: {html_path}")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        sys.exit("GEMINI_API_KEY not set.")

    slug = html_path.parent.name if html_path.name == "index.html" else html_path.stem
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    out_mp3 = AUDIO_DIR / f"{slug}.mp3"

    title, body = extract_text(html_path)
    print(f"→ Article: {title} ({len(body)} chars)")

    client = genai.Client(api_key=api_key)

    print("→ Generating dialogue…")
    dialogue = generate_dialogue(client, title, body)
    print(f"  {len(dialogue)} lines")

    print("→ Synthesizing voices…")
    parts: list[Path] = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for i, (speaker, text) in enumerate(dialogue):
            voice = SPEAKER_A if speaker == "Alex" else SPEAKER_B
            part = tmp / f"{i:03d}-{speaker}.pcm"
            synth_line(client, voice, text, part)
            parts.append(part)
            print(f"  [{i+1}/{len(dialogue)}] {speaker}")

        print("→ Encoding MP3…")
        concat_to_mp3(parts, out_mp3)

    print(f"✓ Written: {out_mp3} ({out_mp3.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
