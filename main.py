import os
import sys
import subprocess
import threading
import customtkinter as ctk

ctk.set_appearance_mode("dark")


class YtDlpApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YT-DLP DOWNLOADER")
        self.geometry("850x720")
        self.configure(fg_color="#070708")

        self.BG_DARK = "#070708"
        self.CARD_BG = "#121215"
        self.ACCENT_COLOR = "#CCFF00"
        self.ACCENT_HOVER = "#B3E600"
        self.TEXT_COLOR = "#E2E8F0"
        self.SUBTEXT_COLOR = "#94A3B8"

        self.GUI_FONT = "SF Pro Display"

        self.main_frame = ctk.CTkFrame(self, fg_color=self.BG_DARK)
        self.main_frame.pack(fill="both", expand=True, padx=24, pady=24)

        self.header_label = ctk.CTkLabel(
            self.main_frame,
            text="YT-DLP DOWNLOADER",
            font=ctk.CTkFont(family=self.GUI_FONT, size=28, weight="bold"),
            text_color="#FFFFFF"
        )
        self.header_label.pack(anchor="w", pady=(0, 20))

        self.card_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.CARD_BG,
            corner_radius=12,
            border_width=1,
            border_color="#27272A"
        )
        self.card_frame.pack(fill="x", pady=(0, 16), ipadx=16, ipady=16)

        self.url_label = ctk.CTkLabel(
            self.card_frame,
            text="// ADRES URL (WIDEO / LIVE / PLAYLISTA)",
            font=ctk.CTkFont(family=self.GUI_FONT, size=11, weight="bold"),
            text_color=self.SUBTEXT_COLOR
        )
        self.url_label.pack(anchor="w", pady=(8, 4), padx=12)

        self.url_entry = ctk.CTkEntry(
            self.card_frame,
            placeholder_text="Wklej link z YouTube, Kick, Twitch...",
            font=ctk.CTkFont(family=self.GUI_FONT, size=13),
            fg_color="#000000",
            border_color="#27272A",
            border_width=1,
            text_color=self.TEXT_COLOR,
            height=42
        )
        self.url_entry.pack(fill="x", padx=12, pady=(0, 16))

        self.options_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.options_frame.pack(fill="x", padx=12, pady=(0, 12))

        self.format_label = ctk.CTkLabel(
            self.options_frame,
            text="// FORMAT",
            font=ctk.CTkFont(family=self.GUI_FONT, size=11, weight="bold"),
            text_color=self.SUBTEXT_COLOR
        )
        self.format_label.grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.format_option = ctk.CTkOptionMenu(
            self.options_frame,
            values=[
                "Wideo (MP4)",
                "Audio (MP3)",
                "Audio (WAV)",
                "Audio (FLAC)"
            ],
            command=self._on_format_change,
            font=ctk.CTkFont(family=self.GUI_FONT, size=13),
            dropdown_font=ctk.CTkFont(family=self.GUI_FONT, size=13),
            fg_color="#000000",
            button_color="#27272A",
            button_hover_color="#3F3F46",
            text_color=self.TEXT_COLOR,
            dropdown_fg_color=self.CARD_BG,
            height=36
        )
        self.format_option.grid(row=1, column=0, sticky="ew", padx=(0, 12))

        self.quality_label = ctk.CTkLabel(
            self.options_frame,
            text="// JAKOŚĆ WIDEO",
            font=ctk.CTkFont(family=self.GUI_FONT, size=11, weight="bold"),
            text_color=self.SUBTEXT_COLOR
        )
        self.quality_label.grid(row=0, column=1, sticky="w", pady=(0, 4))

        self.quality_option = ctk.CTkOptionMenu(
            self.options_frame,
            values=[
                "Najwyższa Dostępna",
                "1080p Full HD",
                "720p HD",
                "480p",
                "360p",
                "240p",
                "144p"
            ],
            font=ctk.CTkFont(family=self.GUI_FONT, size=13),
            dropdown_font=ctk.CTkFont(family=self.GUI_FONT, size=13),
            fg_color="#000000",
            button_color="#27272A",
            button_hover_color="#3F3F46",
            text_color=self.TEXT_COLOR,
            dropdown_fg_color=self.CARD_BG,
            height=36
        )
        self.quality_option.grid(row=1, column=1, sticky="ew", padx=(0, 12))

        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)

        # Opcje dodatkowe - Checkboxy
        self.checkboxes_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.checkboxes_frame.pack(fill="x", padx=12, pady=(0, 16))

        self.playlist_checkbox = ctk.CTkCheckBox(
            self.checkboxes_frame,
            text="Pobierz całą playlistę",
            font=ctk.CTkFont(family=self.GUI_FONT, size=12),
            text_color=self.TEXT_COLOR,
            fg_color=self.ACCENT_COLOR,
            hover_color=self.ACCENT_HOVER,
            checkmark_color="#000000"
        )
        self.playlist_checkbox.pack(side="left", padx=(0, 16))

        self.live_start_checkbox = ctk.CTkCheckBox(
            self.checkboxes_frame,
            text="Pobierz LIVE od początku",
            font=ctk.CTkFont(family=self.GUI_FONT, size=12),
            text_color=self.TEXT_COLOR,
            fg_color=self.ACCENT_COLOR,
            hover_color=self.ACCENT_HOVER,
            checkmark_color="#000000"
        )
        self.live_start_checkbox.pack(side="left")

        # Przyciski Akcji
        self.buttons_frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.buttons_frame.pack(fill="x", padx=12, pady=(4, 8))

        self.download_button = ctk.CTkButton(
            self.buttons_frame,
            text="ROZPOCZNIJ POBIERANIE",
            font=ctk.CTkFont(family=self.GUI_FONT, size=14, weight="bold"),
            fg_color=self.ACCENT_COLOR,
            hover_color=self.ACCENT_HOVER,
            text_color="#000000",
            height=46,
            corner_radius=8,
            command=self.start_download_thread
        )
        self.download_button.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.vlc_button = ctk.CTkButton(
            self.buttons_frame,
            text="ODTWÓRZ W VLC",
            font=ctk.CTkFont(family=self.GUI_FONT, size=14, weight="bold"),
            fg_color="#27272A",
            hover_color="#3F3F46",
            text_color="#FFFFFF",
            height=46,
            width=180,
            corner_radius=8,
            command=self.start_vlc_thread
        )
        self.vlc_button.pack(side="right")

        # Logi
        self.log_label = ctk.CTkLabel(
            self.main_frame,
            text="// LOGI POBIERANIA / STRUMIENIOWANIA",
            font=ctk.CTkFont(family=self.GUI_FONT, size=11, weight="bold"),
            text_color=self.SUBTEXT_COLOR
        )
        self.log_label.pack(anchor="w", pady=(8, 4))

        self.textbox = ctk.CTkTextbox(
            self.main_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#000000",
            text_color="#A1A1AA",
            border_width=1,
            border_color="#27272A",
            corner_radius=8
        )
        self.textbox.pack(fill="both", expand=True)
        self.log("Gotowy do pracy. Oczekiwanie na link...")

    def _on_format_change(self, choice):
        if "Audio" in choice:
            self.quality_option.configure(state="disabled")
        else:
            self.quality_option.configure(state="normal")

    def log(self, message):
        self.textbox.insert("end", f"> {message}\n")
        self.textbox.see("end")

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            self.log("BŁĄD: Podaj link do filmu lub transmisji!")
            return

        self.download_button.configure(state="disabled", text="POBIERANIE W TOKU...")
        self.vlc_button.configure(state="disabled")
        threading.Thread(target=self._run_yt_dlp, args=(url,), daemon=True).start()

    def start_vlc_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            self.log("BŁĄD: Podaj link do filmu lub transmisji!")
            return

        self.vlc_button.configure(state="disabled", text="URUCHAMIANIE...")
        self.download_button.configure(state="disabled")
        threading.Thread(target=self._run_vlc_stream, args=(url,), daemon=True).start()

    def _get_base_dir(self):
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    def _run_vlc_stream(self, url):
        base_dir = self._get_base_dir()
        yt_dlp_path = os.path.join(base_dir, "yt-dlp.exe")

        if not os.path.exists(yt_dlp_path):
            self.log(f"BŁĄD: Brak yt-dlp.exe w folderze: {base_dir}")
            self._reset_buttons()
            return

        self.log("Pobieranie bezpośredniego linku do strumienia...")

        cmd_get_url = [
            yt_dlp_path,
            "-g",
            "-f", "b/bv*+ba",
            url
        ]

        try:
            res = subprocess.run(cmd_get_url, capture_output=True, text=True, cwd=base_dir)
            stream_urls = res.stdout.strip().split('\n')

            if not stream_urls or not stream_urls[0]:
                self.log("BŁĄD: Nie udało się pobrać linku strumienia.")
                self._reset_buttons()
                return

            vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
            if not os.path.exists(vlc_path):
                vlc_path = r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"

            if not os.path.exists(vlc_path):
                self.log("BŁĄD: Nie znaleziono odtwarzacza VLC w C:\\Program Files\\VideoLAN\\VLC!")
                self._reset_buttons()
                return

            self.log("Otwieranie strumienia w odtwarzaczu VLC...")
            subprocess.Popen([vlc_path] + stream_urls)
            self.log("SUKCES: Uruchomiono VLC.")

        except Exception as e:
            self.log(f"Błąd uruchamiania VLC: {str(e)}")

        self._reset_buttons()

    def _run_yt_dlp(self, url):
        base_dir = self._get_base_dir()
        yt_dlp_path = os.path.join(base_dir, "yt-dlp.exe")
        ffmpeg_dir = base_dir

        if not os.path.exists(yt_dlp_path):
            self.log(f"BŁĄD: Brak yt-dlp.exe w folderze: {base_dir}")
            self._reset_buttons()
            return

        fmt = self.format_option.get()
        quality = self.quality_option.get()
        is_playlist = self.playlist_checkbox.get()
        live_start = self.live_start_checkbox.get()

        cmd = [
            yt_dlp_path,
            "--ffmpeg-location", ffmpeg_dir,
            "--progress",
            "--newline"
        ]

        if not is_playlist:
            cmd.append("--no-playlist")

        if live_start:
            cmd.append("--live-from-start")

        if "MP3" in fmt:
            cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0", "--embed-thumbnail", "--add-metadata"])
        elif "WAV" in fmt:
            cmd.extend(["-x", "--audio-format", "wav", "--add-metadata"])
        elif "FLAC" in fmt:
            cmd.extend(["-x", "--audio-format", "flac", "--embed-thumbnail", "--add-metadata"])
        else:
            if quality == "1080p Full HD":
                cmd.extend(["-f", "bv*[height<=1080]+ba/b[height<=1080]", "--merge-output-format", "mp4"])
            elif quality == "720p HD":
                cmd.extend(["-f", "bv*[height<=720]+ba/b[height<=720]", "--merge-output-format", "mp4"])
            elif quality == "480p":
                cmd.extend(["-f", "bv*[height<=480]+ba/b[height<=480]", "--merge-output-format", "mp4"])
            elif quality == "360p":
                cmd.extend(["-f", "bv*[height<=360]+ba/b[height<=360]", "--merge-output-format", "mp4"])
            elif quality == "240p":
                cmd.extend(["-f", "bv*[height<=240]+ba/b[height<=240]", "--merge-output-format", "mp4"])
            elif quality == "144p":
                cmd.extend(["-f", "bv*[height<=144]+ba/b[height<=144]", "--merge-output-format", "mp4"])
            else:
                cmd.extend(["-f", "bv*+ba/b", "--merge-output-format", "mp4"])

            cmd.extend(["--embed-thumbnail", "--add-metadata"])

        cmd.append(url)

        self.log(f"Rozpoczynanie pobierania: {url}")
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                cwd=base_dir
            )

            for line in process.stdout:
                line_str = line.strip()
                if line_str:
                    self.log(line_str)

            process.wait()

            if process.returncode == 0:
                self.log("SUKCES: Pobieranie zakończone.")
            else:
                self.log("BŁĄD: Coś poszło nie tak podczas operacji.")

        except Exception as e:
            self.log(f"Błąd uruchomienia: {str(e)}")

        self._reset_buttons()

    def _reset_buttons(self):
        self.download_button.configure(state="normal", text="ROZPOCZNIJ POBIERANIE")
        self.vlc_button.configure(state="normal", text="ODTWÓRZ W VLC")


if __name__ == "__main__":
    app = YtDlpApp()
    app.mainloop()
