from flask import Flask, render_template, request, redirect, url_for
import youtube_dl

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        audio_url = download_audio(youtube_url)
        if audio_url:
            return redirect(url_for('download', audio_url=audio_url))
    return render_template('index.html')

def download_audio(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(youtube_url, download=True)
            audio_url = info['entries'][0]['url']
            return audio_url
        except Exception as e:
            print(e)
            return None

@app.route('/download')
def download():
    audio_url = request.args.get('audio_url')
    return f'<a href="{audio_url}" download>Download Audio</a>'

if __name__ == '__main__':
    app.run(debug=True)
