#!/usr/bin/env python3
"""
Standalone Audio Extraction Tool

A simple command-line tool to extract audio from video URLs and save them locally.
"""

import argparse
import sys
from transcriber import VideoTranscriber

def main():
    """Main entry point for the audio extraction tool."""
    parser = argparse.ArgumentParser(
        description="Extract audio from video URLs and save locally",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python audio_extractor.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -o audio.wav
  python audio_extractor.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -o music.mp3 -f mp3
  python audio_extractor.py https://vimeo.com/123456789 -o podcast.flac -f flac
        """
    )
    
    parser.add_argument(
        'url',
        help='URL of the video to extract audio from'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path for the audio file',
        required=True
    )
    
    parser.add_argument(
        '-f', '--format',
        help='Audio format (wav, mp3, flac, m4a, aac)',
        choices=['wav', 'mp3', 'flac', 'm4a', 'aac'],
        default='wav'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        help='Enable verbose logging',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check if yt-dlp is available
    import subprocess
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: yt-dlp not found. Please install with: pip install yt-dlp")
        sys.exit(1)
    
    # Create transcriber instance (we only need it for audio extraction)
    transcriber = VideoTranscriber()
    
    try:
        success = transcriber.extract_audio_to_file(args.url, args.output, args.format)
        if success:
            print(f"Audio successfully extracted to: {args.output}")
        else:
            print("Audio extraction failed. Check the logs for details.")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()