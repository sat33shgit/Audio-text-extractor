import yt_dlp
import sys

def test_setup():
    """Test if all dependencies are properly installed"""
    try:
        # Test yt_dlp import
        print("✓ yt_dlp imported successfully")
        
        # Test if yt_dlp can initialize
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("✓ YoutubeDL initialized successfully")
        
        print("✓ All dependencies are properly installed and working!")
        print(f"✓ Python version: {sys.version}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    test_setup()
