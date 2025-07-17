#!/usr/bin/env python3
"""
Example usage of the VideoTranscriber class
"""

import json
from transcriber import VideoTranscriber

def example_usage():
    """Demonstrate how to use the VideoTranscriber class programmatically."""
    
    # Create transcriber instance
    transcriber = VideoTranscriber(model_size="base")
    
    # Example video URL (replace with actual URL)
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Example 1: Process video with temporary audio (original method)
    print("Starting transcription...")
    success = transcriber.process_video(video_url, output_file="example_output.json")
    
    if success:
        print("Transcription completed successfully!")
        
        # Read and display the results
        with open("example_output.json", "r", encoding="utf-8") as f:
            results = json.load(f)
        
        print(f"\nTranscription contains {len(results)} segments:")
        for i, segment in enumerate(results[:3]):  # Show first 3 segments
            print(f"\nSegment {i+1}:")
            print(f"  Time: {segment['timestamp']['start']}s - {segment['timestamp']['end']}s")
            print(f"  Text: {segment['sentence']}")
        
        if len(results) > 3:
            print(f"\n... and {len(results) - 3} more segments")
    else:
        print("Transcription failed. Check the logs for details.")

def example_audio_extraction():
    """Demonstrate audio extraction and transcription."""
    
    transcriber = VideoTranscriber(model_size="base")
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Example 2: Extract audio to local file and transcribe
    print("\n" + "="*50)
    print("Example 2: Extract audio and transcribe")
    print("="*50)
    
    audio_file = "extracted_audio.wav"
    transcription_file = "transcription_with_audio.json"
    
    success = transcriber.process_video_with_audio_save(
        video_url, 
        audio_file, 
        transcription_file, 
        audio_format="wav"
    )
    
    if success:
        print(f"Audio saved to: {audio_file}")
        print(f"Transcription saved to: {transcription_file}")
    else:
        print("Process failed. Check the logs for details.")
    
    # Example 3: Extract audio only (no transcription)
    print("\n" + "="*50)
    print("Example 3: Extract audio only")
    print("="*50)
    
    audio_only_file = "audio_only.mp3"
    success = transcriber.extract_audio_to_file(video_url, audio_only_file, "mp3")
    
    if success:
        print(f"Audio extracted to: {audio_only_file}")
        
        # Later, you can transcribe the saved audio file
        print("Now transcribing the saved audio file...")
        transcription_result = transcriber.transcribe_local_audio(audio_only_file)
        
        if transcription_result:
            formatted_output = transcriber.format_output(transcription_result)
            print(f"Transcription completed with {len(formatted_output)} segments")
        else:
            print("Transcription of saved audio failed")
    else:
        print("Audio extraction failed")
if __name__ == "__main__":
    example_usage()
    example_audio_extraction()