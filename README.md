# ViralVadoo Command Line Interface (CLI)

Interactive terminal client for **Vadoo AI** capabilities.

## Setup

### 1. Set your API key
Make sure you copy or set your Vadoo API key:
```cmd
# Create a .env file in this directory:
echo VADOO_API_KEY=your_actual_key_here > .env
```

### 2. Install requirements
```cmd
pip install -r requirements.txt
```

---

## Commands Reference

### Account
* Check remaining credit balance:
  ```bash
  python cli.py balance
  ```

### AI Video Generation
* Generate a new video from custom script:
  ```bash
  python cli.py video --topic Custom --prompt "Write a short fun fact about honeybees" --duration "30-60" --voice "Onyx"
  ```
* Poll progress and retrieve video URL:
  ```bash
  python cli.py video-status <your_video_id>
  ```

### AI Captions
* Subtitle a public video link:
  ```bash
  python cli.py captions "https://example.com/raw_video.mp4" --theme Hormozi_1
  ```

### AI Clips Extraction
* Extract 3 short highlights from long YouTube URL:
  ```bash
  python cli.py clips "https://youtube.com/watch?v=xxxxxx" --num-highlights 3
  ```

### AI Podcast Generation
* Generate a two-person podcast conversation:
  ```bash
  python cli.py podcast --name1 "Alice" --name2 "Bob" --text "Explain quantum computing like I'm five years old." --voice1 "Onyx" --voice2 "Alloy"
  ```

### AI Characters
* List your AI characters:
  ```bash
  python cli.py list characters
  ```
* Generate an image for AI character ID `1`:
  ```bash
  python cli.py character-image --id 1 --prompt "flying in spaceship" --ratio "16:9"
  ```
* Check character image generation status:
  ```bash
  python cli.py character-image-status <image_id>
  ```

### Discovery Lists
* List voices: `python cli.py list voices`
* List languages: `python cli.py list languages`
* List caption themes: `python cli.py list themes`
* List video styles: `python cli.py list styles`
* List video topics: `python cli.py list topics`
* List background music: `python cli.py list music`
