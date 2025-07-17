# Video Transcription Tool

A Python command-line tool that downloads video from URLs and transcribes them to JSON format with timestamps and sentences.

## Features

- Download audio from video URLs (YouTube, Vimeo, and many other platforms)
- Extract and save audio files locally in multiple formats (WAV, MP3, FLAC, M4A, AAC)
- High-quality transcription using OpenAI's Whisper
- Transcribe local audio files
- Timestamped output in JSON format
- Multiple Whisper model sizes for different accuracy/speed trade-offs
- Clean command-line interface
- Robust error handling and logging

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. The tool also requires `ffmpeg` to be installed on your system:

**On macOS:**
```bash
brew install ffmpeg
```

**On Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**On Windows:**
Download from https://ffmpeg.org/download.html

## Usage

### Basic Usage

```bash
python transcriber.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Save to File

```bash
python transcriber.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o transcription.json
```

### Extract and Save Audio Locally

```bash
# Save audio as WAV and transcribe
python transcriber.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a audio.wav -o transcription.json

# Save audio as MP3
python transcriber.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -a music.mp3 -f mp3
```

### Extract Audio Only (No Transcription)

```bash
# Using the standalone audio extractor
python audio_extractor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o audio.wav

# Extract as MP3
python audio_extractor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o music.mp3 -f mp3
```

### Use Different Model Size

```bash
python transcriber.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --model large
```

### Verbose Output

```bash
python transcriber.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -v
```

## Command Line Options

- `url`: Video URL to transcribe (required)
- `-o, --output`: Output file path for JSON results (default: stdout)
- `-a, --audio-output`: Save extracted audio to this file path
- `-f, --audio-format`: Audio format for saved file (wav, mp3, flac, m4a, aac)
- `-m, --model`: Whisper model size - tiny, base, small, medium, large (default: base)
- `-v, --verbose`: Enable verbose logging

## Model Size Comparison

| Model  | Size  | Speed | Accuracy |
|--------|-------|-------|----------|
| tiny   | 39MB  | Fast  | Lower    |
| base   | 74MB  | Good  | Good     |
| small  | 244MB | Slow  | Better   |
| medium | 769MB | Slower| Better   |
| large  | 1550MB| Slowest| Best    |

## Output Format

The tool outputs JSON in the following format:

```json
[
  {
    "timestamp": {
      "start": 0.0,
      "end": 3.5
    },
    "sentence": "Hello, this is the first sentence."
  },
  {
    "timestamp": {
      "start": 3.5,
      "end": 7.2
    },
    "sentence": "This is the second sentence."
  }
]
```

## Supported Platforms

The tool supports any video platform that yt-dlp can handle, including:
- YouTube
- Vimeo
- TikTok
- Twitter
- Facebook
- Instagram
- And many more...

## Error Handling

The tool includes comprehensive error handling for:
- Network connectivity issues
- Invalid URLs
- Audio extraction failures
- Transcription errors
- File I/O problems

## Performance Tips

1. Use the `tiny` model for quick transcriptions of short videos
2. Use `base` or `small` for most use cases
3. Use `medium` or `large` for high-accuracy requirements
4. The tool automatically cleans up temporary files after processing

## Troubleshooting

### Shell URL Issues

If you get "no matches found" errors, try these solutions:

1. **Use double quotes around the URL:**
   ```bash
   python transcriber.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o output.json
   ```

2. **Disable glob expansion (zsh/bash):**
   ```bash
   set -o noglob
   python transcriber.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -o output.json
   set +o noglob
   ```

3. **Use a different shell or escape characters:**
   ```bash
   python transcriber.py 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' -o output.json
   ```

4. **Test your setup first:**
   ```bash
   python test_url.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   ```

### Common Issues

1. **ModuleNotFoundError**: Install missing dependencies with `pip install -r requirements.txt`

2. **ffmpeg not found**: Install ffmpeg on your system

3. **yt-dlp download fails**: Check if the URL is valid and accessible

4. **Out of memory**: Try using a smaller Whisper model size

### Debug Mode

Run with `-v` flag to see detailed logging information:

```bash
python transcriber.py "https://example.com/video" -v
```
