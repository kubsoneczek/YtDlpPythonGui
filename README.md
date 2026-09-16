# YT-DLP DOWNLOADER (GUI)

DOWNLOADER HAS ONLY POLISH LANGUAGE SUPPORT! 🇵🇱 🇵🇱 🇵🇱

PREREQUISITES

* Python 3.10+
* Required executables in the root folder: `yt-dlp.exe`, `ffmpeg.exe`

QUICK START (RUN FROM SOURCE)

1. Clone repo:
git clone https://github.com/kubsoneczek/YtDlpPythonGui.git
2. Install dependencies:
pip install customtkinter
3. Run app:
python main.py

BUILD STANDALONE EXE

1. Install PyInstaller:
pip install pyinstaller
2. Build executable:
pyinstaller --noconsole --onefile main.py
3. Move `main.exe` from `dist/` into the main directory alongside `yt-dlp.exe` and `ffmpeg.exe`.

FEATURES

* **Video Formats:** MP4, MOV
* **Video Quality:** 144p to 1080p Full HD / Best Quality
* **Audio Formats:** MP3, WAV, FLAC
* **Playback & Playlists:** Direct VLC stream playback & full playlist / live stream support
* **Speed Limiter:** Adjustable download speed caps (1 MB/s to 20 MB/s)
* **Tools Tab (🛠️ Narzędzia):**
  * Thumbnail Downloader (JPG)
  * Subtitle Downloader (.srt - PL, EN, All)
  * Local Video Trimmer (lossless FFmpeg cutting)
