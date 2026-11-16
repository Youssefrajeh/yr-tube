"""YR Tube - web front end for the yt-dlp extraction engine. By Youssef Rajeh."""
import os
import sys
import threading
import time
from collections import defaultdict
from urllib.parse import urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request, send_from_directory  # noqa: E402

from yt_dlp import YoutubeDL  # noqa: E402

app = Flask(__name__, static_folder='static', static_url_path='/static')

RATE_LIMIT = int(os.environ.get('RATE_LIMIT_PER_MIN', '10'))
_hits = defaultdict(list)
_lock = threading.Lock()


def _rate_limited(ip):
    now = time.time()
    with _lock:
        _hits[ip] = [t for t in _hits[ip] if now - t < 60]
        if len(_hits[ip]) >= RATE_LIMIT:
            return True
        _hits[ip].append(now)
    return False


def _valid_url(url):
    p = urlparse(url)
    return p.scheme in ('http', 'https') and bool(p.hostname) and len(url) < 2048


@app.get('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.post('/api/info')
def info():
    ip = (request.headers.get('X-Forwarded-For') or request.remote_addr or '').split(',')[0].strip()
    if _rate_limited(ip):
        return jsonify(error='Too many requests, try again in a minute.'), 429
    url = ((request.get_json(silent=True) or {}).get('url') or '').strip()
    if not _valid_url(url):
        return jsonify(error='Please provide a valid http(s) URL.'), 400
    opts = {'quiet': True, 'no_warnings': True, 'skip_download': True, 'noplaylist': True,
            'socket_timeout': 15}
    try:
        with YoutubeDL(opts) as ydl:
            data = ydl.extract_info(url, download=False)
    except Exception as e:
        return jsonify(error=str(e)[:300]), 422
    formats = [{
        'id': f.get('format_id'), 'ext': f.get('ext'),
        'resolution': f.get('resolution') or f.get('format_note'),
        'filesize': f.get('filesize') or f.get('filesize_approx'),
        'has_video': f.get('vcodec') not in (None, 'none'),
        'has_audio': f.get('acodec') not in (None, 'none'),
        'url': f.get('url'),
    } for f in (data.get('formats') or []) if f.get('url') and (f.get('protocol') or '').startswith('http')]
    return jsonify(title=data.get('title'), uploader=data.get('uploader'), duration=data.get('duration'),
                   thumbnail=data.get('thumbnail'), webpage_url=data.get('webpage_url'), formats=formats)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
