import bisect
import json
import math
import os
import re
import threading
import time
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urlparse, parse_qs

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    IpBlocked,
    RequestBlocked,
    TranscriptsDisabled,
    VideoUnavailable,
)

# Optional proxy (only the transcript requests go through it, to save bandwidth):
#   Webshare "Residential":  export WEBSHARE_USER="..." WEBSHARE_PASS="..."
#   Any other provider:      export PROXY_URL="http://user:pass@host:port"
WEBSHARE_USER = os.environ.get("WEBSHARE_USER")
WEBSHARE_PASS = os.environ.get("WEBSHARE_PASS")
PROXY_URL = os.environ.get("PROXY_URL")


def make_api() -> YouTubeTranscriptApi:
    if WEBSHARE_USER and WEBSHARE_PASS:
        from youtube_transcript_api.proxies import WebshareProxyConfig

        return YouTubeTranscriptApi(
            proxy_config=WebshareProxyConfig(
                proxy_username=WEBSHARE_USER, proxy_password=WEBSHARE_PASS
            )
        )
    if PROXY_URL:
        from youtube_transcript_api.proxies import GenericProxyConfig

        return YouTubeTranscriptApi(
            proxy_config=GenericProxyConfig(http_url=PROXY_URL, https_url=PROXY_URL)
        )
    return YouTubeTranscriptApi()


app = FastAPI(title="YouTube Transcript API")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(Path(__file__).parent / "index.html")


class TranscriptRequest(BaseModel):
    url: str = Field(..., description="YouTube video link")
    timestamp: bool = Field(True, description="true: include timestamps, false: text only")
    languages: Optional[List[str]] = Field(
        None,
        description="Language of the transcript, e.g. ['ja']. Only the first value is used. "
        "Omit it (or use a language the video doesn't have) to get the video's default language.",
    )
    mergeSentences: bool = Field(
        True, description="true: merge caption lines into complete sentences"
    )


def extract_video_id(url: str) -> str:
    parsed = urlparse(url.strip())
    host = (parsed.hostname or "").replace("www.", "").replace("m.", "")
    video_id = None

    if host == "youtu.be":
        video_id = parsed.path.lstrip("/").split("/")[0]
    elif host in ("youtube.com", "music.youtube.com"):
        if parsed.path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        else:
            m = re.match(r"^/(shorts|embed|live|v)/([\w-]{11})", parsed.path)
            if m:
                video_id = m.group(2)

    if not video_id or not re.fullmatch(r"[\w-]{11}", video_id):
        raise HTTPException(status_code=400, detail="Invalid YouTube link")
    return video_id


def format_timestamp(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"


def get_watch_info(video_id: str) -> dict:
    """Duration (seconds) and description, read from the watch page (no API key)."""
    info = {"duration": None, "description": ""}
    try:
        r = requests.get(
            f"https://www.youtube.com/watch?v={video_id}",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            },
            cookies={"CONSENT": "YES+1", "SOCS": "CAI"},
            timeout=10,
        )
        m = re.search(r'"lengthSeconds":"(\d+)"', r.text)
        if m:
            info["duration"] = int(m.group(1))
        d = re.search(r'"shortDescription":"((?:[^"\\]|\\.)*)"', r.text)
        if d:
            info["description"] = json.loads(f'"{d.group(1)}"')
    except (requests.RequestException, ValueError):
        pass
    return info


def language_label(t) -> str:
    """e.g. 'de-DE (de-DE)' or, for auto-generated, 'a-en (en) [auto]'."""
    code = t.language_code
    if t.is_generated:
        return f"a-{code} ({code}) [auto]"
    return f"{code} ({code})"


def detect_original_language(text: str, transcripts):
    """Guess the spoken language from the title + description (written by the
    uploader, so normally in the video's language) and match it to a caption track."""
    try:
        from langdetect import DetectorFactory, detect_langs

        DetectorFactory.seed = 0
        candidates = detect_langs(text[:1500])
    except Exception:
        return None
    for c in candidates:
        if c.prob < 0.5:
            break
        base = c.lang.lower().split("-")[0]
        match = [t for t in transcripts if t.language_code.lower().split("-")[0] == base]
        if match:
            return next((t for t in match if not t.is_generated), match[0])
    return None


def default_transcript(transcripts, hint_text: str = ""):
    """The video's original language:
    1) exactly one auto-generated track -> it is the spoken language;
    2) several auto-generated tracks (auto-dubbed video) -> they cannot tell us
       which one is original, so detect it from the title/description;
    3) otherwise the first track (uploader-made captions are listed first)."""
    generated = [t for t in transcripts if t.is_generated]
    if len(generated) == 1:
        code = generated[0].language_code
        manual = [t for t in transcripts if not t.is_generated and t.language_code == code]
        return manual[0] if manual else generated[0]
    detected = detect_original_language(hint_text, transcripts) if hint_text.strip() else None
    return detected or transcripts[0]


def pick_transcript(transcripts, requested: Optional[List[str]], hint_text: str = ""):
    """Use the language the user typed (only the first entry counts).
    'en' also matches 'en-US'; uploader-made captions beat auto-generated ones,
    then an exact code beats a regional variant.
    Nothing typed, or the video doesn't have it -> the video's original language."""
    want = next((l.strip().lower() for l in requested or [] if l.strip()), "")
    if want:
        base = want.split("-")[0]
        matches = [t for t in transcripts if t.language_code.lower().split("-")[0] == base]
        if matches:
            return min(matches, key=lambda t: (t.is_generated, t.language_code.lower() != want))
    return default_transcript(transcripts, hint_text)


def get_video_title(url: str) -> str:
    try:
        r = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": url, "format": "json"},
            timeout=10,
        )
        if r.ok:
            return r.json().get("title", "")
    except requests.RequestException:
        pass
    return ""


# ---------- Gộp các dòng phụ đề thành câu hoàn chỉnh ----------

# (text, start, duration)
Segment = Tuple[str, float, float]

# Dấu kết thúc câu: . ! ? … (theo sau là khoảng trắng/hết chuỗi) hoặc 。！？
SENTENCE_END = re.compile(r'[.!?…]+["\'”’)\]]*(?=\s|$)|[。！？]+')
ABBREVIATIONS = {"mr", "mrs", "ms", "dr", "prof", "sr", "jr", "vs", "etc", "st"}


def split_sentences(text: str) -> List[Tuple[int, str]]:
    """Tách văn bản thành các câu. Trả về [(vị trí bắt đầu, câu)]."""
    out: List[Tuple[int, str]] = []
    start = 0

    def add(chunk_start: int, chunk: str):
        stripped = chunk.strip()
        if stripped:
            begin = chunk_start + (len(chunk) - len(chunk.lstrip()))
            out.append((begin, stripped))

    for m in SENTENCE_END.finditer(text):
        words = text[start:m.start()].split()
        last = words[-1].lower().strip("([\"'") if words else ""
        # Bỏ qua các từ viết tắt như "Mr.", "Dr."
        if m.group().startswith(".") and last in ABBREVIATIONS:
            continue
        add(start, text[start:m.end()])
        start = m.end()

    add(start, text[start:])
    return out


def has_punctuation(text: str) -> bool:
    """Phụ đề tự sinh thường không có dấu câu -> cần cách xử lý khác."""
    ends = len(SENTENCE_END.findall(text))
    return ends >= max(1, len(text.split()) / 40)


def group_by_pause(
    segments: List[Segment], gap: float = 1.0, max_chars: int = 200
) -> List[Tuple[str, float]]:
    """Fallback: gộp theo khoảng lặng hoặc độ dài tối đa."""
    groups: List[Tuple[str, float]] = []
    buf: List[str] = []
    buf_start = 0.0
    prev_end = 0.0
    for text, start, dur in segments:
        too_long = sum(len(t) + 1 for t in buf) > max_chars
        if buf and (start - prev_end > gap or too_long):
            groups.append((" ".join(buf), buf_start))
            buf = []
        if not buf:
            buf_start = start
        buf.append(text)
        prev_end = start + dur
    if buf:
        groups.append((" ".join(buf), buf_start))
    return groups


def merge_into_sentences(segments: List[Segment]) -> List[Tuple[str, float]]:
    segments = [s for s in segments if s[0]]
    if not segments:
        return []

    # Nối toàn bộ text, nhớ vị trí ký tự bắt đầu của từng dòng
    full, offsets = "", []
    for text, _, _ in segments:
        offsets.append(len(full))
        full += text + " "
    full = full.strip()

    if not has_punctuation(full):
        return group_by_pause(segments)

    result: List[Tuple[str, float]] = []
    for begin, sentence in split_sentences(full):
        i = max(bisect.bisect_right(offsets, begin) - 1, 0)
        text, start, dur = segments[i]
        # Ước lượng thời điểm câu bắt đầu nếu nó nằm giữa một dòng
        ratio = min((begin - offsets[i]) / max(len(text), 1), 1.0)
        result.append((sentence, start + dur * ratio))
    return result


# ---------- Cache + throttle: fewer requests to YouTube = fewer IP blocks ----------
CACHE_TTL = 6 * 3600   # seconds a video's data is reused
MIN_INTERVAL = 3.0     # minimum seconds between two live requests to YouTube
_cache: dict = {}
_lock = threading.Lock()
_last_call = 0.0


def load_video(url: str, video_id: str, requested: Optional[List[str]]) -> dict:
    """Title, duration, language list and raw caption lines. Cached, so changing
    options like timestamp / mergeSentences never hits YouTube again."""
    global _last_call
    want = next((l.strip().lower() for l in requested or [] if l.strip()), "")
    key = (video_id, want)
    hit = _cache.get(key)
    if hit and time.time() - hit["at"] < CACHE_TTL:
        return hit

    with _lock:  # one live request at a time, spaced out
        wait = MIN_INTERVAL - (time.time() - _last_call)
        if wait > 0:
            time.sleep(wait)
        try:
            title = get_video_title(url)
            info = get_watch_info(video_id)
            transcripts = list(make_api().list(video_id))  # manual first, then auto
            if not transcripts:
                raise HTTPException(status_code=404, detail="No transcript found")
            chosen = pick_transcript(transcripts, requested, f"{title}\n{info['description']}")
            fetched = chosen.fetch()
        except HTTPException:
            raise
        except (RequestBlocked, IpBlocked):
            raise HTTPException(
                status_code=429,
                detail="YouTube is blocking requests from this IP. Wait a while, switch "
                "network (or turn your VPN off/on), or use a residential proxy "
                "(see WEBSHARE_USER / PROXY_URL in main.py).",
            )
        except TranscriptsDisabled:
            raise HTTPException(status_code=404, detail="Transcripts are disabled for this video")
        except VideoUnavailable:
            raise HTTPException(status_code=404, detail="Video is unavailable")
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Failed to fetch transcript: {e}")
        finally:
            _last_call = time.time()

    segments = [(sn.text.replace("\n", " ").strip(), sn.start, sn.duration) for sn in fetched]
    duration = info["duration"]
    if duration is None and segments:  # fallback: end of the last caption line
        duration = math.ceil(segments[-1][1] + segments[-1][2])

    data = {
        "at": time.time(),
        "title": title,
        "duration": duration,
        "language": [language_label(t) for t in transcripts],
        "segments": segments,
    }
    if len(_cache) >= 200:
        _cache.pop(next(iter(_cache)))
    _cache[key] = data
    return data


@app.post("/api/transcript")
def get_transcript(req: TranscriptRequest):
    video_id = extract_video_id(req.url)
    data = load_video(req.url, video_id, req.languages)
    segments = data["segments"]

    if req.mergeSentences:
        pairs = merge_into_sentences(segments)
    else:
        pairs = [(t, s) for t, s, _ in segments]

    transcript = []
    for text, start in pairs:
        item = {"text": text}
        if req.timestamp:
            item["timestamp"] = format_timestamp(start)
        transcript.append(item)

    duration = data["duration"]
    return {
        "url": req.url,
        "title": data["title"],
        "duration": format_timestamp(duration) if duration is not None else "",
        "language": data["language"],
        "transcript": transcript,
    }
