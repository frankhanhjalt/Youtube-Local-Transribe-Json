#!/usr/bin/env python3
"""
Video Transcription Tool

A command-line tool that downloads video from a URL and transcribes it
to JSON format with timestamps and sentences.
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Any
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VideoTranscriber:
    def __init__(self, model_size: str = "base"):
        """
        Initialize the VideoTranscriber with specified Whisper model size.
        
        Args:
            model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        """
        self.model_size = model_size
        self.temp_dir = None
        
    def extract_audio_to_file(self, video_url: str, output_audio_path: str, audio_format: str = "wav") -> bool:
        """
        Extract audio from video URL and save it to a local file.
        
        Args:
            video_url: URL of the video to extract audio from
            output_audio_path: Local path where audio file should be saved
            audio_format: Audio format ('wav', 'mp3', 'flac', 'm4a', etc.)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info(f"Extracting audio from: {video_url}")
            logger.info(f"Saving to: {output_audio_path} (will be placed in /audio)")
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_audio_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # Remove file extension from output path for yt-dlp template
            base_path = os.path.splitext(output_audio_path)[0]
            
            # yt-dlp command to extract audio in specified format
            cmd = [
                'yt-dlp',
                '--extract-audio',
                '--audio-format', audio_format,
                '--audio-quality', '0',  # Best quality
                '--output', f"{base_path}.%(ext)s",
                video_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Check if the file was created successfully
            expected_file = f"{base_path}.{audio_format}"
            if os.path.exists(expected_file):
                # If user specified a different extension, rename the file
                if expected_file != output_audio_path:
                    os.rename(expected_file, output_audio_path)
                
                logger.info(f"Audio extraction completed successfully: {output_audio_path}")
                return True
            else:
                logger.error(f"Expected audio file not found: {expected_file}")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Error extracting audio: {e}")
            logger.error(f"stderr: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during audio extraction: {e}")
            return False
    
    def transcribe_local_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe a local audio file using Whisper.
        
        Args:
            audio_path: Path to the local audio file
            
        Returns:
            Dict containing transcription results with timestamps
        """
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return None
            
        return self.transcribe_audio(audio_path)
    
    def download_audio(self, video_url: str, output_path: str) -> bool:
        """
        Download audio from video URL using yt-dlp.
        
        Args:
            video_url: URL of the video to download
            output_path: Path where audio file should be saved
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info(f"Downloading audio from: {video_url}")
            
            # yt-dlp command to extract audio as wav
            cmd = [
                'yt-dlp',
                '--extract-audio',
                '--audio-format', 'wav',
                '--audio-quality', '0',
                '--output', output_path,
                video_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info("Audio download completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error downloading audio: {e}")
            logger.error(f"stderr: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during download: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file using Whisper.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dict containing transcription results with timestamps
        """
        try:
            import whisper
            
            logger.info(f"Loading Whisper model: {self.model_size}")
            model = whisper.load_model(self.model_size)
            
            logger.info("Starting transcription...")
            result = model.transcribe(
                audio_path,
                word_timestamps=True,
                verbose=True
            )
            
            logger.info("Transcription completed successfully")
            return result
            
        except ImportError:
            logger.error("Whisper library not installed. Please install with: pip install openai-whisper")
            return None
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            return None
    
    def format_output(self, transcription_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Format transcription result into the desired JSON structure.
        
        Args:
            transcription_result: Raw transcription result from Whisper
            
        Returns:
            List of dictionaries with timestamp and sentence information
        """
        formatted_output = []
        
        if not transcription_result or 'segments' not in transcription_result:
            return formatted_output
        
        for segment in transcription_result['segments']:
            formatted_segment = {
                "timestamp": {
                    "start": round(segment['start'], 2),
                    "end": round(segment['end'], 2)
                },
                "sentence": segment['text'].strip()
            }
            formatted_output.append(formatted_segment)
        
        return formatted_output
    
    def process_video(self, video_url: str, output_file: str = None) -> bool:
        """
        Main processing function that handles the complete transcription workflow.
        
        Args:
            video_url: URL of the video to transcribe
            output_file: Optional output file path for JSON results
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Create temporary directory for audio file
        self.temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(self.temp_dir, "audio.%(ext)s")
        
        try:
            # Download audio
            if not self.download_audio(video_url, audio_path):
                return False
            
            # Find the actual audio file (yt-dlp adds extension)
            audio_files = list(Path(self.temp_dir).glob("audio.*"))
            if not audio_files:
                logger.error("No audio file found after download")
                return False
            
            actual_audio_path = str(audio_files[0])
            
            # Transcribe audio
            transcription_result = self.transcribe_audio(actual_audio_path)
            if not transcription_result:
                return False
            
            # Format output
            formatted_output = self.format_output(transcription_result)
            
            # Output results
            json_output = json.dumps(formatted_output, indent=2, ensure_ascii=False)
            
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(json_output)
                logger.info(f"Transcription saved to: {output_file}")
            else:
                print(json_output)
            
            return True
            
        except Exception as e:
            logger.error(f"Error processing video: {e}")
            return False
        
        finally:
            # Cleanup temporary files
            self.cleanup()
    
    def process_video_with_audio_save(self, video_url: str, audio_output_path: str, 
                                    transcription_output_file: str = None, 
                                    audio_format: str = "wav") -> bool:
        """
        Process video by extracting audio to a local file and then transcribing it.
        
        Args:
            video_url: URL of the video to transcribe
            audio_output_path: Path where audio file should be saved
            transcription_output_file: Optional output file path for JSON results
            audio_format: Audio format for the saved file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Always store audio in /audio subfolder
            audio_dir = os.path.join(os.getcwd(), "audio")
            if not os.path.exists(audio_dir):
                os.makedirs(audio_dir, exist_ok=True)
            audio_filename = os.path.basename(audio_output_path)
            audio_output_path = os.path.join(audio_dir, audio_filename)

            # Always store JSON in /result subfolder
            result_dir = os.path.join(os.getcwd(), "result")
            if transcription_output_file:
                if not os.path.exists(result_dir):
                    os.makedirs(result_dir, exist_ok=True)
                json_filename = os.path.basename(transcription_output_file)
                transcription_output_file = os.path.join(result_dir, json_filename)

            # Extract audio to local file
            if not self.extract_audio_to_file(video_url, audio_output_path, audio_format):
                return False

            # Transcribe the saved audio file
            transcription_result = self.transcribe_local_audio(audio_output_path)
            if not transcription_result:
                return False

            # Format output
            formatted_output = self.format_output(transcription_result)

            # Output results
            json_output = json.dumps(formatted_output, indent=2, ensure_ascii=False)

            if transcription_output_file:
                with open(transcription_output_file, 'w', encoding='utf-8') as f:
                    f.write(json_output)
                logger.info(f"Transcription saved to: {transcription_output_file}")
            else:
                print(json_output)

            return True

        except Exception as e:
            logger.error(f"Error processing video with audio save: {e}")
            return False
    
    def cleanup(self):
        """Clean up temporary files."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
            logger.info("Temporary files cleaned up")

def main():
    """Main entry point for the CLI tool."""
    parser = argparse.ArgumentParser(
        description="Transcribe video from URL to JSON format with timestamps",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python transcriber.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
  python transcriber.py https://www.youtube.com/watch?v=dQw4w9WgXcQ -o output.json
  python transcriber.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --model large
        """
    )
    
    parser.add_argument(
        'url',
        help='URL of the video to transcribe'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file path for JSON results (default: stdout)',
        default=None
    )
    
    parser.add_argument(
        '-a', '--audio-output',
        help='Save extracted audio to this file path',
        default=None
    )
    
    parser.add_argument(
        '-f', '--audio-format',
        help='Audio format for saved file (wav, mp3, flac, m4a)',
        choices=['wav', 'mp3', 'flac', 'm4a', 'aac'],
        default='wav'
    )
    
    parser.add_argument(
        '-m', '--model',
        help='Whisper model size (tiny, base, small, medium, large)',
        choices=['tiny', 'base', 'small', 'medium', 'large'],
        default='base'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        help='Enable verbose logging',
        action='store_true'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check dependencies
    try:
        import whisper
    except ImportError:
        logger.error("OpenAI Whisper not installed. Please install with: pip install openai-whisper")
        sys.exit(1)
    
    # Check if yt-dlp is available
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("yt-dlp not found. Please install with: pip install yt-dlp")
        sys.exit(1)
    
    # Create transcriber and process video
    transcriber = VideoTranscriber(model_size=args.model)
    
    try:
        if args.audio_output:
            # Use the new method that saves audio locally
            success = transcriber.process_video_with_audio_save(
                args.url, 
                args.audio_output, 
                args.output, 
                args.audio_format
            )
        else:
            # Use the original method with temporary audio
            success = transcriber.process_video(args.url, args.output)
            
        if not success:
            sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        transcriber.cleanup()
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        transcriber.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()