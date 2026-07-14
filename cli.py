"""
ViralVadoo Command-Line Interface (CLI)

Enables interacting with all Vadoo AI capabilities directly from the terminal.
Configure your API key in a .env file or export VADOO_API_KEY environment variable.
"""

import sys
import os
import argparse
import asyncio
import json
from typing import Any
from dotenv import load_dotenv

import vadoo_client as vc

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# Helper printers
# ─────────────────────────────────────────────────────────────────────────────

def print_result(data: Any) -> None:
    if isinstance(data, dict) and "error" in data:
        print(f"\033[91mError: {data['error']}\033[0m", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(data, indent=2))


# ─────────────────────────────────────────────────────────────────────────────
# CLI Commands implementation
# ─────────────────────────────────────────────────────────────────────────────

async def cmd_balance(args: argparse.Namespace) -> None:
    res = await vc.get("/api/get_my_balance")
    print_result(res)


async def cmd_video(args: argparse.Namespace) -> None:
    payload = {
        "topic": args.topic,
        "prompt": args.prompt,
        "duration": args.duration,
        "voice": args.voice,
        "language": args.language,
        "aspect_ratio": args.aspect_ratio,
        "style": args.style,
        "theme": args.theme,
        "bg_music": args.bg_music,
        "bg_music_volume": args.bg_music_volume,
        "speed": args.speed,
        "use_ai": args.use_ai,
        "include_voiceover": args.include_voiceover,
        "custom_instructions": args.custom_instructions,
        "url": args.url,
        "webhook": args.webhook,
    }
    res = await vc.post("/api/generate_video", payload)
    print_result(res)


async def cmd_video_status(args: argparse.Namespace) -> None:
    res = await vc.get("/api/get_video_url", {"id": args.id})
    print_result(res)


async def cmd_captions(args: argparse.Namespace) -> None:
    payload = {
        "url": args.url,
        "language": args.language,
        "theme": args.theme,
        "webhook": args.webhook,
    }
    res = await vc.post("/api/add_captions", payload)
    print_result(res)


async def cmd_clips(args: argparse.Namespace) -> None:
    payload = {
        "video_url": args.video_url,
        "num_highlights": args.num_highlights,
        "aspect_ratio": args.aspect_ratio,
        "return_coordinates_only": args.return_coordinates_only,
        "webhook": args.webhook,
    }
    res = await vc.post("/api/create_ai_clips", payload)
    print_result(res)


async def cmd_podcast(args: argparse.Namespace) -> None:
    payload = {
        "url": args.url,
        "text": args.text,
        "name1": args.name1,
        "name2": args.name2,
        "voice1": args.voice1,
        "voice2": args.voice2,
        "language": args.language,
        "duration": args.duration,
        "tone": args.tone,
        "theme": args.theme,
        "webhook": args.webhook,
    }
    res = await vc.post("/api/generate_podcast", payload)
    print_result(res)


async def cmd_list(args: argparse.Namespace) -> None:
    target = args.target
    if target == "voices":
        res = await vc.get("/api/get_voices")
    elif target == "languages":
        res = await vc.get("/api/get_languages")
    elif target == "styles":
        res = await vc.get("/api/get_styles")
    elif target == "themes":
        res = await vc.get("/api/get_themes")
    elif target == "topics":
        res = await vc.get("/api/get_topics")
    elif target == "music":
        res = await vc.get("/api/get_background_music")
    elif target == "characters":
        res = await vc.get("/api/get_all_characters")
    else:
        print(f"Unknown list target: {target}", file=sys.stderr)
        sys.exit(1)
    print_result(res)


async def cmd_character_image(args: argparse.Namespace) -> None:
    payload = {
        "id": args.id,
        "prompt": args.prompt,
        "ratio": args.ratio,
    }
    res = await vc.post("/api/generate_character_image", payload)
    print_result(res)


async def cmd_character_image_status(args: argparse.Namespace) -> None:
    res = await vc.get("/api/get_character_image", {"id": args.id})
    print_result(res)


# ─────────────────────────────────────────────────────────────────────────────
# CLI parser configuration
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="ViralVadoo CLI — Access Vadoo AI services directly from the command line."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="CLI Command")

    # Command: balance
    subparsers.add_parser("balance", help="Retrieve remaining credit balance.")

    # Command: video
    video_parser = subparsers.add_parser("video", help="Generate a new AI video.")
    video_parser.add_argument("--topic", default="Random AI Story", help="Predefined topic name (e.g. Motivational, Bedtime Stories, or Custom).")
    video_parser.add_argument("--prompt", help="Verbatim script or topic description. Required if topic is Custom.")
    video_parser.add_argument("--duration", choices=["30-60", "60-90", "90-120", "120-180", "5 min", "10 min"], default="30-60", help="Duration code.")
    video_parser.add_argument("--voice", default="Onyx", help="AI Voice name.")
    video_parser.add_argument("--language", default="English", help="Video language.")
    video_parser.add_argument("--aspect_ratio", choices=["9:16", "1:1", "16:9"], default="9:16", help="Output aspect ratio.")
    video_parser.add_argument("--style", default="None", help="Image/visual style.")
    video_parser.add_argument("--theme", default="Hormozi_1", help="Caption style/theme name.")
    video_parser.add_argument("--bg-music", help="Background music track name.")
    video_parser.add_argument("--bg-music-volume", type=int, default=100, help="Music volume (0-100).")
    video_parser.add_argument("--speed", type=float, default=1.0, help="Voice speed multiplier (0.5 to 2.0).")
    video_parser.add_argument("--use-ai", type=int, choices=[0, 1], default=1, help="1 = use prompt as guideline, 0 = prompt is exact voiceover script.")
    video_parser.add_argument("--include-voiceover", type=int, choices=[0, 1], default=1, help="1 = include voice, 0 = silent/music only.")
    video_parser.add_argument("--custom-instructions", help="Extra instructions for video generation.")
    video_parser.add_argument("--url", help="Blog post or article URL to convert to video.")
    video_parser.add_argument("--webhook", help="Webhook URL to receive completion status.")

    # Command: video-status
    status_parser = subparsers.add_parser("video-status", help="Get progress/status of a video.")
    status_parser.add_argument("id", help="The video ID (vid) returned during creation.")

    # Command: captions
    captions_parser = subparsers.add_parser("captions", help="Add captions to a video.")
    captions_parser.add_argument("url", help="Direct URL of the video file to caption.")
    captions_parser.add_argument("--language", default="English", help="Video language.")
    captions_parser.add_argument("--theme", default="Hormozi_1", help="Caption theme style.")
    captions_parser.add_argument("--webhook", help="Callback URL for notification.")

    # Command: clips
    clips_parser = subparsers.add_parser("clips", help="Extract viral clips from long video.")
    clips_parser.add_argument("video_url", help="YouTube link or direct MP4 URL.")
    clips_parser.add_argument("--num-highlights", type=int, default=3, help="Number of clips to extract.")
    clips_parser.add_argument("--aspect_ratio", choices=["9:16", "1:1", "16:9"], default="9:16", help="Target aspect ratio.")
    clips_parser.add_argument("--return-coordinates-only", action="store_true", help="Only get clip timestamps/coordinates without rendering video.")
    clips_parser.add_argument("--webhook", help="Callback URL for notification.")

    # Command: podcast
    podcast_parser = subparsers.add_parser("podcast", help="Generate a 2-person AI podcast.")
    podcast_parser.add_argument("--name1", required=True, help="Speaker 1 name.")
    podcast_parser.add_argument("--name2", required=True, help="Speaker 2 name.")
    podcast_parser.add_argument("--url", help="Source blog or document URL. Required if text is not provided.")
    podcast_parser.add_argument("--text", help="Source plain text. Required if url is not provided.")
    podcast_parser.add_argument("--voice1", default="Onyx", help="Speaker 1 voice.")
    podcast_parser.add_argument("--voice2", default="Alloy", help="Speaker 2 voice.")
    podcast_parser.add_argument("--language", default="English", help="Language.")
    podcast_parser.add_argument("--duration", choices=["1-2", "2-5"], default="1-2", help="Duration code.")
    podcast_parser.add_argument("--tone", default="Friendly", help="Conversation tone.")
    podcast_parser.add_argument("--theme", default="Hormozi_1", help="Caption theme.")
    podcast_parser.add_argument("--webhook", help="Callback URL.")

    # Command: list
    list_parser = subparsers.add_parser("list", help="Discover Vadoo metadata lists.")
    list_parser.add_argument(
        "target",
        choices=["voices", "languages", "styles", "themes", "topics", "music", "characters"],
        help="Entity type to list."
    )

    # Command: character-image
    char_img_parser = subparsers.add_parser("character-image", help="Generate AI character image.")
    char_img_parser.add_argument("--id", type=int, required=True, help="AI Character base ID.")
    char_img_parser.add_argument("--prompt", required=True, help="Visual scene prompt description.")
    char_img_parser.add_argument("--ratio", choices=["1:1", "3:4", "4:3", "16:9", "9:16"], default="1:1", help="Aspect ratio.")

    # Command: character-image-status
    char_status_parser = subparsers.add_parser("character-image-status", help="Get status of character image.")
    char_status_parser.add_argument("id", help="The Image ID returned during creation.")

    args = parser.parse_args()

    # Map subcommands to handler functions
    cmd_handlers = {
        "balance": cmd_balance,
        "video": cmd_video,
        "video-status": cmd_video_status,
        "captions": cmd_captions,
        "clips": cmd_clips,
        "podcast": cmd_podcast,
        "list": cmd_list,
        "character-image": cmd_character_image,
        "character-image-status": cmd_character_image_status,
    }

    handler = cmd_handlers[args.command]
    
    try:
        asyncio.run(handler(args))
    except ValueError as exc:
        print(f"\033[91mConfiguration error: {exc}\033[0m", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        print(f"\033[91mExecution failed: {exc}\033[0m", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
