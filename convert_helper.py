"""
MP3 to WAV Converter Helper
===========================

This script provides you with several options to convert your MP3 file to WAV format
so it can be transcribed to text.
"""

import os
import glob

def main():
    print("🎵 MP3 to WAV Conversion Helper")
    print("=" * 35)
    
    # Find MP3 files
    mp3_files = glob.glob("*.mp3")
    
    if not mp3_files:
        print("❌ No MP3 files found in current directory")
        return
    
    latest_mp3 = max(mp3_files, key=os.path.getctime)
    wav_file = latest_mp3.replace('.mp3', '.wav')
    
    print(f"📁 Found MP3 file: {latest_mp3}")
    print(f"🎯 Target WAV file: {wav_file}")
    print()
    
    print("🌐 RECOMMENDED: Online Conversion")
    print("   1. Go to: https://convertio.co/mp3-wav/")
    print("   2. Click 'Choose Files' and select your MP3")
    print("   3. Click 'Convert'")
    print("   4. Download the WAV file to this folder")
    print("   5. Run the transcription script again")
    print()
    
    print("🎵 ALTERNATIVE: VLC Media Player")
    print("   1. Open VLC Media Player")
    print("   2. Go to Media → Convert/Save")
    print("   3. Add your MP3 file")
    print("   4. Set output format to WAV")
    print("   5. Convert and save to this folder")
    print()
    
    print("💻 COMMAND LINE: If you have FFmpeg installed")
    print(f'   ffmpeg -i "{latest_mp3}" "{wav_file}"')
    print()
    
    print("✅ After conversion, run:")
    print("   python simple_audio_to_text.py")

if __name__ == "__main__":
    main()
