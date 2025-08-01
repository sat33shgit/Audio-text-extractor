import whisper
import os
import glob
import time

def transcribe_with_whisper(audio_file, model_size="base", language=None, task="transcribe"):
    """
    Transcribe audio file using OpenAI Whisper
    
    Args:
        audio_file: Path to audio file (supports MP3, WAV, FLAC, M4A, etc.)
        model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large', 'turbo')
        language: Language code (e.g., 'en', 'hi', 'te', 'ta', 'kn') or None for auto-detection
        task: 'transcribe' or 'translate' (translate converts to English)
    
    Returns:
        dict: Transcription result with text, language, and segments
    """
    print(f"🎵 Whisper Audio Transcription")
    print(f"=" * 35)
    print(f"📁 File: {audio_file}")
    print(f"🤖 Model: {model_size}")
    print(f"🌐 Language: {language if language else 'Auto-detect'}")
    print(f"⚙️ Task: {task}")
    print()
    
    try:
        # Load the Whisper model
        print(f"⏳ Loading Whisper model '{model_size}'...")
        model = whisper.load_model(model_size)
        print(f"✅ Model loaded successfully")
        
        # Configure transcription options
        options = {
            "task": task,
            "fp16": False,  # Use FP32 for better compatibility
        }
        
        if language:
            options["language"] = language
        
        print(f"🎙️ Starting transcription...")
        start_time = time.time()
        
        # Transcribe the audio
        result = model.transcribe(audio_file, **options)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Transcription completed in {duration:.2f} seconds")
        print(f"🔤 Detected language: {result.get('language', 'Unknown')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return None

def format_transcript(result, include_timestamps=True):
    """Format the Whisper result into a readable transcript"""
    if not result:
        return None
    
    formatted_text = f"Language: {result.get('language', 'Unknown')}\n"
    formatted_text += "=" * 50 + "\n\n"
    
    if include_timestamps and 'segments' in result:
        # Format with timestamps
        for segment in result['segments']:
            start = segment['start']
            end = segment['end']
            text = segment['text'].strip()
            
            start_min = int(start // 60)
            start_sec = int(start % 60)
            end_min = int(end // 60)
            end_sec = int(end % 60)
            
            formatted_text += f"[{start_min:02d}:{start_sec:02d} - {end_min:02d}:{end_sec:02d}] {text}\n\n"
    else:
        # Simple format without timestamps
        formatted_text += result['text'].strip()
    
    return formatted_text

def process_latest_audio():
    """Find and process the most recently created audio file"""
    # Look for various audio formats
    audio_extensions = ["*.mp3", "*.wav", "*.flac", "*.m4a", "*.aac", "*.ogg"]
    audio_files = []
    
    for ext in audio_extensions:
        audio_files.extend(glob.glob(ext))
    
    if not audio_files:
        print("❌ No audio files found in current directory")
        return
    
    # Get the most recent audio file
    latest_audio = max(audio_files, key=os.path.getctime)
    print(f"📁 Processing latest audio file: {latest_audio}")
    
    # Transcribe audio
    result = transcribe_with_whisper(latest_audio, model_size="base", language=None)
    
    if result:
        # Format transcript
        transcript = format_transcript(result, include_timestamps=True)
        
        # Save transcript to text file
        base_name = os.path.splitext(latest_audio)[0]
        txt_file = f"{base_name}_whisper_transcript.txt"
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"Whisper Transcript of: {latest_audio}\n")
            f.write(transcript)
        
        print(f"💾 Transcript saved to: {txt_file}")
        print("\n" + "=" * 50)
        print("📄 TRANSCRIPT PREVIEW:")
        print("=" * 50)
        preview_text = result['text'][:800] + "..." if len(result['text']) > 800 else result['text']
        print(preview_text)
        
    else:
        print("❌ Failed to transcribe audio")

def transcribe_specific_file(audio_file, model_size="base", language=None, task="transcribe"):
    """Transcribe a specific audio file with Whisper"""
    if not os.path.exists(audio_file):
        print(f"❌ File not found: {audio_file}")
        return
    
    print(f"📁 Processing: {audio_file}")
    
    # Transcribe audio
    result = transcribe_with_whisper(audio_file, model_size=model_size, language=language, task=task)
    
    if result:
        # Format transcript
        transcript = format_transcript(result, include_timestamps=True)
        
        # Save transcript to text file
        base_name = os.path.splitext(audio_file)[0]
        txt_file = f"{base_name}_whisper_transcript.txt"
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"Whisper Transcript of: {audio_file}\n")
            f.write(transcript)
        
        print(f"💾 Transcript saved to: {txt_file}")
        print("\n" + "=" * 50)
        print("📄 TRANSCRIPT PREVIEW:")
        print("=" * 50)
        preview_text = result['text'][:800] + "..." if len(result['text']) > 800 else result['text']
        print(preview_text)
        
    else:
        print("❌ Failed to transcribe audio")

def list_available_models():
    """List available Whisper model sizes"""
    models = {
        "tiny": "~39M params, ~1GB memory, ~10x speed, lowest accuracy",
        "base": "~74M params, ~1GB memory, ~7x speed, good balance",
        "small": "~244M params, ~2GB memory, ~4x speed, better accuracy", 
        "medium": "~769M params, ~5GB memory, ~2x speed, high accuracy",
        "large": "~1550M params, ~10GB memory, 1x speed, highest accuracy",
        "turbo": "~809M params, ~6GB memory, ~8x speed, optimized large"
    }
    
    print("🤖 Available Whisper Models:")
    print("=" * 40)
    for model, description in models.items():
        print(f"{model:8} - {description}")
    print()
    print("💡 Recommendation:")
    print("   • For speed: 'tiny' or 'base'")
    print("   • For balance: 'small' or 'turbo'") 
    print("   • For accuracy: 'medium' or 'large'")

if __name__ == "__main__":
    print("🎵 Whisper Audio to Text Converter")
    print("=" * 40)
    print()
    
    # Show available models
    list_available_models()
    print()
    
    # Process the latest audio file automatically
    process_latest_audio()
    
    # Uncomment below to transcribe a specific file with custom settings:
    # transcribe_specific_file("Hair Fall - Dr.Bhanu Prasad Gadde.mp3", 
    #                         model_size="base", 
    #                         language=None,  # Auto-detect or specify: 'en', 'hi', 'te', etc.
    #                         task="transcribe")  # or "translate" to convert to English
