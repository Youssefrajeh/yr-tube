FROM python:3.12-slim
WORKDIR /srv
COPY app/requirements.txt app/requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt
COPY yt_dlp yt_dlp
COPY app app
ENV PORT=8000
CMD gunicorn app.main:app --bind 0.0.0.0:${PORT} --workers 2 --timeout 60
