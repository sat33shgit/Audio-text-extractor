# Audio Extractor & Transcription Tool

A complete solution for downloading audio from YouTube and converting it to text using OpenAI Whisper.

## 🚀 Features

- **Audio Extraction**: Download audio from YouTube videos in MP3 format
- **AI Transcription**: Convert audio to text using OpenAI Whisper
- **Multi-language Support**: Automatic language detection or specify language
- **High Accuracy**: State-of-the-art speech recognition
- **Offline Processing**: No API limits, runs completely offline

## 📁 Files

- `audioExtract_PY.py` - Downloads audio from YouTube videos
- `whisper_audio_to_text.py` - Converts audio to text using Whisper AI
- `requirements.txt` - Python dependencies

## 🛠️ Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download Audio from YouTube**:
   - Edit the URL in `audioExtract_PY.py`
   - Run: `python audioExtract_PY.py`

3. **Convert Audio to Text**:
   - Run: `python whisper_audio_to_text.py`
   - Or specify custom settings in the script

## 🎯 Usage Examples

### Basic Transcription
```python
python whisper_audio_to_text.py
```

### Custom Settings
Edit the bottom of `whisper_audio_to_text.py`:
```python
transcribe_specific_file("your_audio.mp3", 
                        model_size="base",     # tiny, base, small, medium, large
                        language=None,         # Auto-detect or 'en', 'hi', 'te', etc.
                        task="transcribe")     # or "translate" for English
```

## 🤖 Whisper Models

- **tiny**: Fast, lower accuracy
- **base**: Good balance of speed and accuracy ⭐ (recommended)
- **small**: Better accuracy, slower
- **medium**: High accuracy
- **large**: Highest accuracy, slowest

## 🌍 Supported Languages

Whisper supports 99+ languages including:
- English, Hindi, Telugu, Tamil, Kannada
- Spanish, French, German, Japanese, Chinese
- And many more...

## 📝 Output

The transcription creates a timestamped text file with:
- Detected language
- Precise timing for each segment
- Clean, readable format

---
Created with ❤️ using OpenAI Whisper
