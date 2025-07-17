#!/usr/bin/env python3
"""
Test script to verify URL handling and dependencies
"""

import sys
import subprocess

def test_dependencies():
    """Test if required dependencies are available."""
    print("Testing dependencies...")
    
    # Test yt-dlp
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True, check=True)
        print(f"✓ yt-dlp version: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ yt-dlp not found. Install with: pip install yt-dlp")
        return False
    
    # Test whisper
    try:
        import whisper
        print("✓ OpenAI Whisper is available")
    except ImportError:
        print("✗ OpenAI Whisper not found. Install with: pip install openai-whisper")
        return False
    
    # Test torch
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
    except ImportError:
        print("✗ PyTorch not found. Install with: pip install torch")
        return False
    
    return True

def test_url_access(url):
    """Test if we can access the URL with yt-dlp."""
    print(f"\nTesting URL access: {url}")
    
    try:
        # Test if yt-dlp can extract info from the URL
        cmd = ['yt-dlp', '--print', 'title', url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)
        print(f"✓ Video title: {result.stdout.strip()}")
        return True
    except subprocess.TimeoutExpired:
        print("✗ Timeout accessing URL")
        return False
    except subprocess.CalledProcessError as e:
        print(f"✗ Error accessing URL: {e.stderr}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False

def main():
    """Main test function."""
    print("Video Transcriber Dependency Test")
    print("=" * 40)
    
    # Test dependencies
    if not test_dependencies():
        print("\nPlease install missing dependencies and try again.")
        sys.exit(1)
    
    # Test with a simple URL first
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
        print(f"Using provided URL: {test_url}")
    
    if test_url_access(test_url):
        print("\n✓ All tests passed! The transcriber should work.")
    else:
        print("\n✗ URL access failed. Check your internet connection or try a different URL.")

if __name__ == "__main__":
    main()