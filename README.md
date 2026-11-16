# YR Tube

A web app for inspecting online videos (title, thumbnail, duration, available formats) and getting direct media links, built by **Youssef Rajeh**.

YR Tube is a fork of [yt-dlp](https://github.com/yt-dlp/yt-dlp) (Unlicense). The extraction engine in `yt_dlp/` is upstream's work; the web app in `app/`, the deployment config and the branding are mine. The original documentation is kept in [UPSTREAM_README.md](UPSTREAM_README.md).

## What I added
- `app/` - Flask API + single-page UI (paste a URL, see info and format list)
- `Dockerfile`, `render.yaml` - deploy on Render
- Rate limiting and URL validation to limit abuse

## Run locally
```
pip install -r app/requirements.txt
python -m app.main
```
Open http://localhost:8000

## Deploy
Push to GitHub, then create a Render Blueprint from the repo (`render.yaml` is picked up automatically).

## Responsible use
Only use this with content you have the right to access. Respect each site's terms of service and copyright law.

## License
Unlicense, inherited from yt-dlp. See [LICENSE](LICENSE) and [THIRD_PARTY_LICENSES.txt](THIRD_PARTY_LICENSES.txt).
