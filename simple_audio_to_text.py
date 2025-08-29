import speech_recognition as sr
import os
import glob

def transcribe_audio_simple(audio_file, language="auto", max_duration=300):
    """
    Simple transcription using speech_recognition directly
    Works with WAV files without requiring FFmpeg
    """
    recognizer = sr.Recognizer()
    
    try:
        print(f"✓ Processing audio file: {audio_file}")
        
        # Use speech_recognition directly with the audio file
        with sr.AudioFile(audio_file) as source:
            print("✓ Loading audio data...")
            
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Record the first 5 minutes (or maximum duration)
            print(f"✓ Recording first {max_duration} seconds of audio...")
            audio_data = recognizer.record(source, duration=max_duration)
            
            print("✓ Starting transcription...")
            
            # Try different languages for auto-detection
            if language == "auto":
                languages_to_try = ['en-US', 'hi-IN', 'te-IN', 'ta-IN', 'kn-IN']
                
                for lang in languages_to_try:
                    try:
                        text = recognizer.recognize_google(audio_data, language=lang)
                        print(f"✓ Successfully recognized in {lang}")
                        return text, lang
                    except sr.UnknownValueError:
                        print(f"✗ Could not understand audio in {lang}")
                        continue
                    except sr.RequestError as e:
                        print(f"✗ Error with {lang}: {e}")
                        continue
                
                return None, None
            else:
                text = recognizer.recognize_google(audio_data, language=language)
                return text, language
                
    except Exception as e:
        print(f"✗ Error transcribing audio: {e}")
        return None, None

def process_wav_files():
    """Find and process WAV files directly"""
    # Look for WAV files first
    wav_files = glob.glob("*.wav")
    
    if wav_files:
        latest_wav = max(wav_files, key=os.path.getctime)
        print(f"✓ Found WAV file: {latest_wav}")
        
        transcript, detected_lang = transcribe_audio_simple(latest_wav, language="auto")
        
        if transcript:
            # Save transcript to text file
            txt_file = latest_wav.replace('.wav', '_transcript.txt')
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(f"Transcript of: {latest_wav}\n")
                f.write(f"Detected Language: {detected_lang}\n")
                f.write("=" * 50 + "\n\n")
                f.write(transcript)
            
            print(f"✓ Transcript saved to: {txt_file}")
            print("\n" + "=" * 50)
            print("TRANSCRIPT PREVIEW:")
            print("=" * 50)
            print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
            
        else:
            print("✗ Failed to transcribe audio")
        
        return True
    
    return False

def manual_convert_mp3():
    """Provide instructions for manual conversion"""
    mp3_files = glob.glob("*.mp3")
    
    if mp3_files:
        latest_mp3 = max(mp3_files, key=os.path.getctime)
        print(f"\n📋 MANUAL CONVERSION REQUIRED:")
        print(f"   MP3 file found: {latest_mp3}")
        print(f"   Please convert to WAV format using one of these methods:")
        print(f"   ")
        print(f"   🌐 Option 1 - Online Converter (Recommended):")
        print(f"   • Go to https://convertio.co/mp3-wav/")
        print(f"   • Upload: {latest_mp3}")
        print(f"   • Download the WAV file to this directory")
        print(f"   • Run this script again!")
        print(f"   ")
        print(f"   🎵 Option 2 - VLC Media Player:")
        print(f"   • Open VLC → Media → Convert/Save")
        print(f"   • Add file: {latest_mp3}")
        print(f"   • Choose WAV format and convert")
        print(f"   ")
        print(f"   💻 Option 3 - FFmpeg (if available):")
        print(f"   • Command: ffmpeg -i \"{latest_mp3}\" \"{latest_mp3.replace('.mp3', '.wav')}\"")
        print(f"   ")
        
        # Try to extract just a sample using an alternative method
        try_extract_sample(latest_mp3)

def try_extract_sample(mp3_file):
    """Try to extract a small sample for testing"""
    print(f"\n🔬 ATTEMPTING SAMPLE EXTRACTION:")
    print(f"   Trying to extract a small sample from {mp3_file}...")
    
    # This is a placeholder - in a real scenario, you might use:
    # - Windows built-in audio tools
    # - Third-party libraries that don't require FFmpeg
    # - Alternative audio processing methods
    
    print(f"   ❌ Sample extraction requires additional tools.")
    print(f"   📥 Please use the online converter option above for best results.")

if __name__ == "__main__":
    print("🎵 Simple Audio to Text Converter")
    print("=" * 40)
    
    # First try to process any existing WAV files
    if not process_wav_files():
        # If no WAV files, provide manual conversion instructions
        manual_convert_mp3()
        print("\n✓ Script will work once you have a WAV file in this directory.")
