import speech_recognition as sr
import pydub
from pydub import AudioSegment
import os
import glob

def convert_mp3_to_wav(mp3_file):
    """Convert MP3 to WAV format for better speech recognition"""
    try:
        # Load MP3 file
        audio = AudioSegment.from_mp3(mp3_file)
        
        # Convert to WAV with optimal settings for speech recognition
        wav_file = mp3_file.replace('.mp3', '.wav')
        audio.export(wav_file, format="wav", parameters=["-ac", "1", "-ar", "16000"])
        
        print(f"✓ Converted {mp3_file} to {wav_file}")
        return wav_file
    except Exception as e:
        print(f"✗ Error converting MP3 to WAV: {e}")
        return None

def transcribe_audio(audio_file, language="auto", chunk_duration=60):
    """
    Transcribe audio file to text
    
    Args:
        audio_file: Path to audio file (WAV format preferred)
        language: Language code (e.g., 'en-US', 'hi-IN', 'te-IN', 'auto' for auto-detection)
        chunk_duration: Duration of each chunk in seconds for processing large files
    """
    recognizer = sr.Recognizer()
    
    try:
        # Load audio file
        audio = AudioSegment.from_wav(audio_file)
        duration = len(audio) / 1000  # Duration in seconds
        
        print(f"✓ Audio duration: {duration:.2f} seconds")
        print(f"✓ Processing audio in {chunk_duration}-second chunks...")
        
        full_text = ""
        
        # Process audio in chunks for better accuracy and memory management
        for start_time in range(0, int(duration), chunk_duration):
            end_time = min(start_time + chunk_duration, int(duration))
            
            # Extract chunk
            chunk = audio[start_time * 1000:end_time * 1000]
            chunk_file = f"temp_chunk_{start_time}_{end_time}.wav"
            chunk.export(chunk_file, format="wav")
            
            try:
                # Transcribe chunk
                with sr.AudioFile(chunk_file) as source:
                    recognizer.adjust_for_ambient_noise(source)
                    audio_data = recognizer.record(source)
                
                # Try different languages/engines for better recognition
                text = ""
                
                if language == "auto":
                    # Try multiple languages for auto-detection
                    languages_to_try = ['en-US', 'hi-IN', 'te-IN', 'ta-IN', 'kn-IN']
                    
                    for lang in languages_to_try:
                        try:
                            text = recognizer.recognize_google(audio_data, language=lang)
                            print(f"✓ Chunk {start_time}-{end_time}s recognized in {lang}")
                            break
                        except sr.UnknownValueError:
                            continue
                        except sr.RequestError as e:
                            print(f"✗ Error with {lang}: {e}")
                            continue
                else:
                    text = recognizer.recognize_google(audio_data, language=language)
                    print(f"✓ Chunk {start_time}-{end_time}s processed")
                
                if text:
                    full_text += f"[{start_time//60:02d}:{start_time%60:02d} - {end_time//60:02d}:{end_time%60:02d}] {text}\n\n"
                else:
                    full_text += f"[{start_time//60:02d}:{start_time%60:02d} - {end_time//60:02d}:{end_time%60:02d}] [No speech detected]\n\n"
                
                if start_time >= 300:  # Stop after processing the first 5 minutes
                    print("✓ Processed first 5 minutes of audio")
                    break
            except sr.UnknownValueError:
                print(f"✗ Could not understand audio in chunk {start_time}-{end_time}s")
                full_text += f"[{start_time//60:02d}:{start_time%60:02d} - {end_time//60:02d}:{end_time%60:02d}] [Could not understand audio]\n\n"
            except sr.RequestError as e:
                print(f"✗ Error with speech recognition service in chunk {start_time}-{end_time}s: {e}")
                full_text += f"[{start_time//60:02d}:{start_time%60:02d} - {end_time//60:02d}:{end_time%60:02d}] [Recognition service error]\n\n"
            finally:
                # Clean up temporary chunk file
                if os.path.exists(chunk_file):
                    os.remove(chunk_file)
        
        return full_text.strip()
        
    except Exception as e:
        print(f"✗ Error transcribing audio: {e}")
        return None

def process_latest_mp3():
    """Find and process the most recently created MP3 file"""
    # Find all MP3 files in current directory
    mp3_files = glob.glob("*.mp3")
    
    if not mp3_files:
        print("✗ No MP3 files found in current directory")
        return
    
    # Get the most recent MP3 file
    latest_mp3 = max(mp3_files, key=os.path.getctime)
    print(f"✓ Processing latest MP3 file: {latest_mp3}")
    
    # Convert MP3 to WAV
    wav_file = convert_mp3_to_wav(latest_mp3)
    if not wav_file:
        return
    
    # Transcribe audio
    print("✓ Starting transcription...")
    transcript = transcribe_audio(wav_file, language="auto")
    
    if transcript:
        # Save transcript to text file
        txt_file = latest_mp3.replace('.mp3', '_transcript.txt')
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"Transcript of: {latest_mp3}\n")
            f.write("=" * 50 + "\n\n")
            f.write(transcript)
        
        print(f"✓ Transcript saved to: {txt_file}")
        print("\n" + "=" * 50)
        print("TRANSCRIPT PREVIEW:")
        print("=" * 50)
        print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
        
    else:
        print("✗ Failed to transcribe audio")
    
    # Clean up WAV file
    if os.path.exists(wav_file):
        os.remove(wav_file)
        print(f"✓ Cleaned up temporary WAV file: {wav_file}")

def transcribe_specific_file(mp3_file, language="auto"):
    """Transcribe a specific MP3 file"""
    if not os.path.exists(mp3_file):
        print(f"✗ File not found: {mp3_file}")
        return
    
    print(f"✓ Processing: {mp3_file}")
    
    # Convert MP3 to WAV
    wav_file = convert_mp3_to_wav(mp3_file)
    if not wav_file:
        return
    
    # Transcribe audio
    print("✓ Starting transcription...")
    transcript = transcribe_audio(wav_file, language=language)
    
    if transcript:
        # Save transcript to text file
        txt_file = mp3_file.replace('.mp3', '_transcript.txt')
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(f"Transcript of: {mp3_file}\n")
            f.write("=" * 50 + "\n\n")
            f.write(transcript)
        
        print(f"✓ Transcript saved to: {txt_file}")
        print("\n" + "=" * 50)
        print("TRANSCRIPT PREVIEW:")
        print("=" * 50)
        print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
        
    else:
        print("✗ Failed to transcribe audio")
    
    # Clean up WAV file
    if os.path.exists(wav_file):
        os.remove(wav_file)
        print(f"✓ Cleaned up temporary WAV file: {wav_file}")

if __name__ == "__main__":
    print("🎵 Audio to Text Converter")
    print("=" * 30)
    
    # Process the latest MP3 file automatically
    process_latest_mp3()
    
    # Uncomment below to transcribe a specific file:
    # transcribe_specific_file("Hair Fall - Dr.Bhanu Prasad Gadde.mp3", language="auto")
