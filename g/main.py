from flask import Flask, render_template_string, request
from pytube import YouTube
import re

app = Flask(__name__)

# HTMLテンプレート
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Downloader</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container my-5">
        <h1 class="text-center">YouTube Downloader</h1>
        <form method="POST" class="my-4">
            <div class="mb-3">
                <label for="video_url" class="form-label">Enter YouTube URL:</label>
                <input type="text" id="video_url" name="video_url" class="form-control" placeholder="e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ" required>
            </div>
            <div class="mb-3">
                <label for="itag" class="form-label">Select Format (itag):</label>
                <select id="itag" name="itag" class="form-select">
                    <option value="18">MP4 (360p)</option>
                    <option value="22">MP4 (720p)</option>
                    <option value="137">MP4 (1080p, no audio)</option>
                    <option value="140">Audio (m4a)</option>
                </select>
            </div>
            <div class="mb-3">
                <label for="filename" class="form-label">Enter File Name (Optional):</label>
                <input type="text" id="filename" name="filename" class="form-control" placeholder="e.g., my_video.mp4">
            </div>
            <button type="submit" class="btn btn-primary w-100">Generate Download Link</button>
        </form>

        {% if download_link %}
        <div class="alert alert-success text-center">
            <h3>Download Link</h3>
            <p>Title: {{ title }}</p>
            <a href="{{ download_link }}" download="{{ filename }}" class="btn btn-success">Download {{ filename }}</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def extract_video_id(url):
    """
    YouTube URLから動画IDを抽出する。
    """
    pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    download_link = None
    filename = None
    title = None

    if request.method == "POST":
        video_url = request.form.get("video_url")
        itag = request.form.get("itag")
        filename = request.form.get("filename")

        try:
            # 動画IDを抽出
            videoid = extract_video_id(video_url)
            if not videoid:
                raise ValueError("Invalid YouTube URL")

            # YouTubeオブジェクトを作成
            yt = YouTube(f"https://www.youtube.com/watch?v={videoid}")
            title = yt.title  # 動画タイトル

            # ファイル名が未入力ならタイトルを使用
            if not filename:
                filename = f"{title}.mp4"

            # ダウンロードリンクを生成
            download_link = f"https://inv-ca1-c.nadeko.net/latest_version?id={videoid}&itag={itag}"
        except Exception as e:
            title = "Error: Unable to retrieve video details"
            filename = "error.mp4"

    return render_template_string(HTML_TEMPLATE, download_link=download_link, filename=filename, title=title)

if __name__ == "__main__":
    app.run(debug=True)
