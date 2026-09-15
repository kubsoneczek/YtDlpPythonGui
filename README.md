# YtDlpPythonGui
GUI For Yt-Dlp Pycharm

# YT-DLP DOWNLOADER (GUI)

PREREQUISITES

* Python 3.10+
* Required executables in the root folder: `yt-dlp.exe`, `ffmpeg.exe`, `ffprobe.exe`

QUICK START (RUN FROM SOURCE)

1. Clone repo:
git clone [https://github.com/kubsoneczek/YtDlpPythonGui.git](https://www.google.com/search?q=https://github.com/kubsoneczek/YtDlpPythonGui.git)
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

* Video: MP4 (144p to 1080p / Best Quality)
* Audio: MP3, WAV, FLAC (with embedded cover art & metadata)
* Support for full playlists & live stream downloading from the start
* Direct VLC stream playback
