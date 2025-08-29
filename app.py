from flask import Flask, render_template_string, request, send_file, redirect, url_for, flash, session
import yt_dlp
import os
import tempfile
import threading
import time
import shutil

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages and session

# HTML template with Bootstrap and progress bar
TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>YouTube Audio Extractor</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    .progress { height: 30px; }
    .container { max-width: 600px; margin-top: 60px; }
  </style>
</head>
<body>
<div class="container">
  <h2 class="mb-4">YouTube Audio Extractor</h2>
  <form method="post" id="extractForm">
    <div class="mb-3">
      <label for="url" class="form-label">YouTube URL:</label>
      <input type="text" class="form-control" name="url" id="url" required placeholder="Paste YouTube link here">
    </div>
    <button type="submit" class="btn btn-primary">Extract Audio</button>
  </form>
  <div id="progressSection" class="mt-4" style="display:none;">
    <label class="form-label">Processing:</label>
    <div class="progress">
      <div id="progressBar" class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%">0%</div>
    </div>
  </div>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <div class="alert alert-danger mt-4">
        {% for message in messages %}
          <div>{{ message }}</div>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}
  {% if filename %}
    <div class="alert alert-success mt-4">
      <b>Download your audio file:</b> <a href="{{ url_for('download', filename=filename) }}" class="btn btn-success">{{ filename }}</a>
    </div>
  {% endif %}
</div>
<script>
  const form = document.getElementById('extractForm');
  const progressSection = document.getElementById('progressSection');
  const progressBar = document.getElementById('progressBar');
  form.addEventListener('submit', function() {
    progressSection.style.display = 'block';
    let progress = 0;
    progressBar.style.width = '0%';
    progressBar.innerText = '0%';
    // Simulate progress bar
    let interval = setInterval(function() {
      if (progress < 90) {
        progress += Math.floor(Math.random() * 10) + 1;
        if (progress > 90) progress = 90;
        progressBar.style.width = progress + '%';
        progressBar.innerText = progress + '%';
      } else {
        clearInterval(interval);
      }
    }, 400);
  });
</script>
</body>
</html>
'''

def download_audio(url):
    temp_dir = tempfile.mkdtemp()
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'cookiefile': 'cookies.txt',  
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        mp3_file = os.path.splitext(filename)[0] + '.mp3'
        return mp3_file

@app.route('/', methods=['GET', 'POST'])
def index():
    filename = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            mp3_file = download_audio(url)
            filename = os.path.basename(mp3_file)
            # Move file to static folder for download
            static_path = os.path.join('static', filename)
            os.makedirs('static', exist_ok=True)
            shutil.move(mp3_file, static_path)
            return render_template_string(TEMPLATE, filename=filename)
        except Exception as e:
            flash(f"Error: {e}")
    return render_template_string(TEMPLATE, filename=None)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join('static', filename), as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
