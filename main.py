import os
import sys
import re
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog

ctk.set_appearance_mode("dark")


class YtDlpApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YT-DLP DOWNLOADER")
        self.geometry("900x750")
        self.configure(fg_color="#070708")

        self.BG_DARK = "#070708"
        self.CARD_BG = "#121215"
        self.ACCENT_COLOR = "#8767f0"
        self.ACCENT_HOVER = "#7252da"
        self.TEXT_COLOR = "#E2E8F0"
        self.SUBTEXT_COLOR = "#94A3B8"
        self.GUI_FONT = "SF Pro Display"

        self.selected_trim_file = ""
        self.settings_win = None

        self.speed_limit_var = ctk.StringVar(value="Brak limitu")

        self.main_frame = ctk.CTkFrame(self, fg_color=self.BG_DARK)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 10))

        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="YT-DLP DOWNLOADER",
            font=ctk.CTkFont(family=self.GUI_FONT, size=26, weight="bold"),
            text_color="#FFFFFF"
        )
        self.header_label.pack(side="left")

        self.gear_button = ctk.CTkButton(
            self.header_frame,
            text="⚙",
            font=ctk.CTkFont(size=20),
            fg_color="#121215",
            hover_color="#27272A",
            text_color=self.ACCENT_COLOR,
            width=42,
            height=42,
            corner_radius=10,
            command=self._open_settings_window
        )
        self.gear_button.pack(side="right")

        self.tabview = ctk.CTkTabview(
            self.main_frame,
            fg_color=self.BG_DARK,
            segmented_button_fg_color="#121215",
            segmented_button_selected_color=self.ACCENT_COLOR,
            segmented_button_selected_hover_color=self.ACCENT_HOVER,
            segmented_button_unselected_color="#121215",
            segmented_button_unselected_hover_color="#27272A",
            text_color="#FFFFFF"
        )
        self.tabview.pack(fill="both", expand=True)

        self.tab_home = self.tabview.add("Pobieranie")
        self.tab_tools = self.tabview.add("🛠️ Narzędzia")

        self._build_home_tab()
        self._build_tools_tab()

        self.log_label = ctk.CTkLabel(
            self.main_frame,
            text="// LOGI OPERACJI",
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
            corner_radius=8,
            height=130
        )
        self.textbox.pack(fill="both", expand=False)
        self.log("System gotowy. Wybierz funkcję i rozpocznij pracę.")

    def _open_settings_window(self):
        if self.settings_win is not None and self.settings_win.winfo_exists():
            self.settings_win.focus()
            return

        self.settings_win = ctk.CTkToplevel(self)
        self.settings_win.title("Ustawienia")
        self.settings_win.geometry("440x160")
        self.settings_win.configure(fg_color="#070708")
        self.settings_win.resizable(False, False)
        self.settings_win.attributes("-topmost", True)

        card = ctk.CTkFrame(self.settings_win, fg_color=self.CARD_BG, corner_radius=12, border_width=1,
                            border_color="#27272A")
        card.pack(fill="both", expand=True, padx=16, pady=16)

        lbl_title = ctk.CTkLabel(card, text="// USTAWIENIA APLIKACJI",
                                 font=ctk.CTkFont(family=self.GUI_FONT, size=14, weight="bold"),
                                 text_color=self.ACCENT_COLOR)
        lbl_title.pack(anchor="w", padx=10, pady=(8, 10))

        f_speed = ctk.CTkFrame(card, fg_color="transparent")
        f_speed.pack(fill="x", padx=10, pady=6)
        lbl_speed = ctk.CTkLabel(f_speed, text="Limit Prędkości Pobierania:",
                                 font=ctk.CTkFont(family=self.GUI_FONT, size=12), text_color=self.TEXT_COLOR)
        lbl_speed.pack(side="left")
        opt_speed_limit = ctk.CTkOptionMenu(f_speed,
                                            values=["Brak limitu", "1 MB/s", "2 MB/s", "5 MB/s", "10 MB/s", "20 MB/s"],
                                            variable=self.speed_limit_var,
                                            font=ctk.CTkFont(family=self.GUI_FONT, size=12), fg_color="#000000",
                                            button_color="#27272A", dropdown_fg_color=self.CARD_BG, width=140)
        opt_speed_limit.pack(side="right")

    def _build_home_tab(self):
        card = ctk.CTkFrame(self.tab_home, fg_color=self.CARD_BG, corner_radius=12, border_width=1,
                            border_color="#27272A")
        card.pack(fill="x", pady=10, ipadx=12, ipady=12)

        url_label = ctk.CTkLabel(card, text="// ADRES URL",
                                 font=ctk.CTkFont(family=self.GUI_FONT, size=11, weight="bold"),
                                 text_color=self.SUBTEXT_COLOR)
        url_label.pack(anchor="w", pady=(4, 2), padx=10)

        self.url_entry = ctk.CTkEntry(card, placeholder_text="Wklej link z YouTube, Kick, Twitch...",
                                      font=ctk.CTkFont(family=self.GUI_FONT, size=13), fg_color="#000000",
                                      border_color="#27272A", text_color=self.TEXT_COLOR, height=40)
        self.url_entry.pack(fill="x", padx=10, pady=(0, 10))

        opts_frame = ctk.CTkFrame(card, fg_color="transparent")
        opts_frame.pack(fill="x", padx=10, pady=(0, 10))

        format_label = ctk.CTkLabel(opts_frame, text="// FORMAT",
                                    font=ctk.CTkFont(family=self.GUI_FONT, size=10, weight="bold"),
                                    text_color=self.SUBTEXT_COLOR)
        format_label.grid(row=0, column=0, sticky="w")
        self.format_option = ctk.CTkOptionMenu(opts_frame,
                                               values=["Wideo (MP4)", "Audio (MP3)", "Audio (WAV)", "Audio (FLAC)"],
                                               command=self._on_format_change,
                                               font=ctk.CTkFont(family=self.GUI_FONT, size=12), fg_color="#000000",
                                               button_color="#27272A", dropdown_fg_color=self.CARD_BG, height=34)
        self.format_option.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        quality_label = ctk.CTkLabel(opts_frame, text="// JAKOŚĆ",
                                     font=ctk.CTkFont(family=self.GUI_FONT, size=10, weight="bold"),
                                     text_color=self.SUBTEXT_COLOR)
        quality_label.grid(row=0, column=1, sticky="w")
        self.quality_option = ctk.CTkOptionMenu(opts_frame,
                                                values=["Najwyższa Dostępna", "1080p Full HD", "720p HD", "480p",
                                                        "360p", "240p", "144p"],
                                                font=ctk.CTkFont(family=self.GUI_FONT, size=12), fg_color="#000000",
                                                button_color="#27272A", dropdown_fg_color=self.CARD_BG, height=34)
        self.quality_option.grid(row=1, column=1, sticky="ew")

        opts_frame.grid_columnconfigure(0, weight=1)
        opts_frame.grid_columnconfigure(1, weight=1)

        chk_frame = ctk.CTkFrame(card, fg_color="transparent")
        chk_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.playlist_checkbox = ctk.CTkCheckBox(chk_frame, text="Playlista",
                                                 font=ctk.CTkFont(family=self.GUI_FONT, size=12),
                                                 fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER,
                                                 text_color=self.TEXT_COLOR, checkmark_color="#FFFFFF")
        self.playlist_checkbox.pack(side="left", padx=(0, 12))

        self.live_start_checkbox = ctk.CTkCheckBox(chk_frame, text="LIVE od początku",
                                                   font=ctk.CTkFont(family=self.GUI_FONT, size=12),
                                                   fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER,
                                                   text_color=self.TEXT_COLOR, checkmark_color="#FFFFFF")
        self.live_start_checkbox.pack(side="left")

        progress_frame = ctk.CTkFrame(card, fg_color="transparent")
        progress_frame.pack(fill="x", padx=10, pady=(4, 10))

        self.progress_bar = ctk.CTkProgressBar(progress_frame, fg_color="#000000", progress_color=self.ACCENT_COLOR,
                                               height=12)
        self.progress_bar.set(0.0)
        self.progress_bar.pack(fill="x", side="left", expand=True, padx=(0, 10))

        self.progress_label = ctk.CTkLabel(progress_frame, text="0.0%",
                                           font=ctk.CTkFont(family=self.GUI_FONT, size=12, weight="bold"),
                                           text_color=self.ACCENT_COLOR, width=50)
        self.progress_label.pack(side="right")

        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(4, 4))

        self.download_button = ctk.CTkButton(btn_frame, text="ROZPOCZNIJ POBIERANIE",
                                             font=ctk.CTkFont(family=self.GUI_FONT, size=14, weight="bold"),
                                             fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER,
                                             text_color="#FFFFFF", height=44, corner_radius=8,
                                             command=self.start_download_thread)
        self.download_button.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.vlc_button = ctk.CTkButton(btn_frame, text="ODTWÓRZ W VLC",
                                        font=ctk.CTkFont(family=self.GUI_FONT, size=14, weight="bold"),
                                        fg_color="#27272A", hover_color="#3F3F46", text_color="#FFFFFF", height=44,
                                        width=160, corner_radius=8, command=self.start_vlc_thread)
        self.vlc_button.pack(side="right")

    def _build_tools_tab(self):
        t1_card = ctk.CTkFrame(self.tab_tools, fg_color=self.CARD_BG, corner_radius=10, border_width=1,
                               border_color="#27272A")
        t1_card.pack(fill="x", pady=6, ipadx=10, ipady=10)

        lbl1 = ctk.CTkLabel(t1_card, text="// POBIERANIE MINIATURKI (JPG)",
                            font=ctk.CTkFont(family=self.GUI_FONT, size=12, weight="bold"),
                            text_color=self.ACCENT_COLOR)
        lbl1.pack(anchor="w", padx=10, pady=(2, 4))

        f1 = ctk.CTkFrame(t1_card, fg_color="transparent")
        f1.pack(fill="x", padx=10)
        self.tool_thumb_url = ctk.CTkEntry(f1, placeholder_text="Wklej link z YouTube...",
                                           font=ctk.CTkFont(family=self.GUI_FONT, size=12), fg_color="#000000",
                                           border_color="#27272A", height=36)
        self.tool_thumb_url.pack(side="left", fill="x", expand=True, padx=(0, 8))
        btn_thumb = ctk.CTkButton(f1, text="Pobierz Miniaturkę",
                                  font=ctk.CTkFont(family=self.GUI_FONT, size=12, weight="bold"),
                                  fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER, text_color="#FFFFFF",
                                  height=36, width=150, command=self.start_thumb_thread)
        btn_thumb.pack(side="right")

        t2_card = ctk.CTkFrame(self.tab_tools, fg_color=self.CARD_BG, corner_radius=10, border_width=1,
                               border_color="#27272A")
        t2_card.pack(fill="x", pady=6, ipadx=10, ipady=10)

        lbl2 = ctk.CTkLabel(t2_card, text="// POBIERANIE NAPISÓW",
                            font=ctk.CTkFont(family=self.GUI_FONT, size=12, weight="bold"),
                            text_color=self.ACCENT_COLOR)
        lbl2.pack(anchor="w", padx=10, pady=(2, 4))

        f2 = ctk.CTkFrame(t2_card, fg_color="transparent")
        f2.pack(fill="x", padx=10)
        self.tool_sub_url = ctk.CTkEntry(f2, placeholder_text="Wklej link z YouTube...",
                                         font=ctk.CTkFont(family=self.GUI_FONT, size=12), fg_color="#000000",
                                         border_color="#27272A", height=36)
        self.tool_sub_url.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.tool_sub_lang = ctk.CTkOptionMenu(f2, values=["Polski (pl)", "Angielski (en)", "Wszystkie (all)"],
                                               font=ctk.CTkFont(family=self.GUI_FONT, size=11), fg_color="#000000",
                                               button_color="#27272A", height=36, width=120)
        self.tool_sub_lang.pack(side="left", padx=(0, 8))

        btn_sub = ctk.CTkButton(f2, text="Pobierz Napisy",
                                font=ctk.CTkFont(family=self.GUI_FONT, size=12, weight="bold"),
                                fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER, text_color="#FFFFFF",
                                height=36, width=130, command=self.start_sub_thread)
        btn_sub.pack(side="right")

        t3_card = ctk.CTkFrame(self.tab_tools, fg_color=self.CARD_BG, corner_radius=10, border_width=1,
                               border_color="#27272A")
        t3_card.pack(fill="x", pady=6, ipadx=10, ipady=10)

        lbl3 = ctk.CTkLabel(t3_card, text="// PRZYCINANIE LOKALNEGO WIDEO (FFMPEG)",
                            font=ctk.CTkFont(family=self.GUI_FONT, size=12, weight="bold"),
                            text_color=self.ACCENT_COLOR)
        lbl3.pack(anchor="w", padx=10, pady=(2, 4))

        f3_top = ctk.CTkFrame(t3_card, fg_color="transparent")
        f3_top.pack(fill="x", padx=10, pady=(0, 6))

        btn_file = ctk.CTkButton(f3_top, text="Wybierz plik wideo", font=ctk.CTkFont(family=self.GUI_FONT, size=12),
                                 fg_color="#27272A", hover_color="#3F3F46", height=34,
                                 command=self._select_file_for_trim)
        btn_file.pack(side="left", padx=(0, 8))

        self.lbl_selected_file = ctk.CTkLabel(f3_top, text="Nie wybrano pliku",
                                              font=ctk.CTkFont(family=self.GUI_FONT, size=11),
                                              text_color=self.SUBTEXT_COLOR)
        self.lbl_selected_file.pack(side="left")

        f3_bot = ctk.CTkFrame(t3_card, fg_color="transparent")
        f3_bot.pack(fill="x", padx=10)

        self.entry_start = ctk.CTkEntry(f3_bot, placeholder_text="Start (np. 00:01:00)",
                                        font=ctk.CTkFont(family=self.GUI_FONT, size=12), fg_color="#000000",
                                        border_color="#27272A", height=36)
        self.entry_start.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.entry_end = ctk.CTkEntry(f3_bot, placeholder_text="Koniec (np. 00:02:30)",
                                      font=ctk.CTkFont(family=self.GUI_FONT, size=12), fg_color="#000000",
                                      border_color="#27272A", height=36)
        self.entry_end.pack(side="left", fill="x", expand=True, padx=(0, 8))

        btn_trim = ctk.CTkButton(f3_bot, text="Przytnij Wideo",
                                 font=ctk.CTkFont(family=self.GUI_FONT, size=12, weight="bold"),
                                 fg_color=self.ACCENT_COLOR, hover_color=self.ACCENT_HOVER, text_color="#FFFFFF",
                                 height=36, width=130, command=self.start_trim_thread)
        btn_trim.pack(side="right")

    def _select_file_for_trim(self):
        filePath = filedialog.askopenfilename(title="Wybierz plik wideo",
                                              filetypes=[("Wideo", "*.mp4 *.mkv *.avi *.mov *.webm"),
                                                         ("Wszystkie pliki", "*.*")])
        if filePath:
            self.selected_trim_file = filePath
            filename = os.path.basename(filePath)
            self.lbl_selected_file.configure(text=filename[:30] + "..." if len(filename) > 30 else filename)

    def _get_base_dir(self):
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

    def _on_format_change(self, choice):
        if "Audio" in choice:
            self.quality_option.configure(state="disabled")
        else:
            self.quality_option.configure(state="normal")

    def log(self, message):
        self.textbox.insert("end", f"> {message}\n")
        self.textbox.see("end")

    def _reset_buttons(self):
        self.download_button.configure(state="normal", text="ROZPOCZNIJ POBIERANIE")
        self.vlc_button.configure(state="normal", text="ODTWÓRZ W VLC")
        self.progress_bar.set(0.0)
        self.progress_label.configure(text="0.0%")

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            self.log("BŁĄD: Podaj link do filmu!")
            return
        self.download_button.configure(state="disabled", text="POBIERANIE...")
        self.vlc_button.configure(state="disabled")
        threading.Thread(target=self._run_yt_dlp, args=(url,), daemon=True).start()

    def start_vlc_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            self.log("BŁĄD: Podaj link do filmu!")
            return
        self.vlc_button.configure(state="disabled", text="URUCHAMIANIE...")
        self.download_button.configure(state="disabled")
        threading.Thread(target=self._run_vlc_stream, args=(url,), daemon=True).start()

    def start_thumb_thread(self):
        url = self.tool_thumb_url.get().strip()
        if not url:
            self.log("BŁĄD: Podaj link do filmu!")
            return
        threading.Thread(target=self._run_thumb_download, args=(url,), daemon=True).start()

    def start_sub_thread(self):
        url = self.tool_sub_url.get().strip()
        if not url:
            self.log("BŁĄD: Podaj link do filmu!")
            return
        lang_choice = self.tool_sub_lang.get()
        lang_code = "pl" if "Polski" in lang_choice else ("en" if "Angielski" in lang_choice else "all")
        threading.Thread(target=self._run_sub_download, args=(url, lang_code), daemon=True).start()

    def start_trim_thread(self):
        if not self.selected_trim_file:
            self.log("BŁĄD: Najpierw wybierz plik wideo!")
            return
        start_t = self.entry_start.get().strip()
        end_t = self.entry_end.get().strip()
        if not start_t or not end_t:
            self.log("BŁĄD: Podaj czas Start i Koniec!")
            return
        threading.Thread(target=self._run_video_trim, args=(self.selected_trim_file, start_t, end_t),
                         daemon=True).start()

    def _run_thumb_download(self, url):
        base_dir = self._get_base_dir()
        yt_dlp_path = os.path.join(base_dir, "yt-dlp.exe")
        if not os.path.exists(yt_dlp_path):
            self.log("BŁĄD: Brak yt-dlp.exe w folderze!")
            return
        self.log("Pobieranie miniaturki...")
        cmd = [yt_dlp_path, "--write-thumbnail", "--skip-download", "--convert-thumbnails", "jpg", url]
        subprocess.run(cmd, cwd=base_dir)
        self.log("SUKCES: Miniaturka została pobrana (JPG).")

    def _run_sub_download(self, url, lang_code):
        base_dir = self._get_base_dir()
        yt_dlp_path = os.path.join(base_dir, "yt-dlp.exe")
        ffmpeg_dir = base_dir

        if not os.path.exists(yt_dlp_path):
            self.log("BŁĄD: Brak yt-dlp.exe w folderze!")
            return

        self.log(f"Pobieranie napisów ({lang_code})...")

        cmd = [
            yt_dlp_path,
            "--ffmpeg-location", ffmpeg_dir,
            "--write-subs",
            "--write-auto-subs",
            "--convert-subs", "srt",
            "--skip-download",
            url
        ]

        if lang_code != "all":
            cmd.extend(["--sub-lang", lang_code])

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
                self.log("SUKCES: Napisy zapisane w folderze z aplikacją (.srt).")
            else:
                self.log("BŁĄD: Nie udało się pobrać napisów.")
        except Exception as e:
            self.log(f"Błąd uruchomienia: {str(e)}")

    def _run_video_trim(self, file_path, start_time, end_time):
        base_dir = self._get_base_dir()
        ffmpeg_path = os.path.join(base_dir, "ffmpeg.exe")
        if not os.path.exists(ffmpeg_path):
            self.log("BŁĄD: Brak ffmpeg.exe w folderze!")
            return
        out_file = os.path.join(base_dir, "przycięte_" + os.path.basename(file_path))
        self.log(f"Przycinanie pliku: {os.path.basename(file_path)}...")
        cmd = [ffmpeg_path, "-y", "-ss", start_time, "-to", end_time, "-i", file_path, "-c", "copy", out_file]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            self.log(f"SUKCES: Zapisano plik: przycięte_{os.path.basename(file_path)}")
        else:
            self.log("BŁĄD: Nie udało się przyciąć pliku. Sprawdź format czasu (np. 00:01:00).")

    def _run_vlc_stream(self, url):
        base_dir = self._get_base_dir()
        yt_dlp_path = os.path.join(base_dir, "yt-dlp.exe")
        if not os.path.exists(yt_dlp_path):
            self.log(f"BŁĄD: Brak yt-dlp.exe w folderze: {base_dir}")
            self._reset_buttons()
            return

        self.log("Pobieranie linku strumienia...")
        cmd_get_url = [yt_dlp_path, "-g", "-f", "b/bv*+ba", url]
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
                self.log("BŁĄD: Nie znaleziono odtwarzacza VLC.")
                self._reset_buttons()
                return

            self.log("Otwieranie w VLC...")
            subprocess.Popen([vlc_path] + stream_urls)
            self.log("SUKCES: Uruchomiono VLC.")
        except Exception as e:
            self.log(f"Błąd uruchomienia VLC: {str(e)}")

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

        speed_val = self.speed_limit_var.get()
        if speed_val != "Brak limitu":
            limit_mb = speed_val.split(" ")[0] + "M"
            cmd.extend(["--limit-rate", limit_mb])

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

            progress_regex = re.compile(r"\[download\]\s+(\d+\.\d+)%")

            for line in process.stdout:
                line_str = line.strip()
                if line_str:
                    match = progress_regex.search(line_str)
                    if match:
                        pct = float(match.group(1))
                        self.progress_bar.set(pct / 100.0)
                        self.progress_label.configure(text=f"{pct:.1f}%")

                    self.log(line_str)

            process.wait()

            if process.returncode == 0:
                self.progress_bar.set(1.0)
                self.progress_label.configure(text="100.0%")
                self.log("SUKCES: Pobieranie zakończone.")
            else:
                self.log("BŁĄD: Coś poszło nie tak podczas pobierania.")

        except Exception as e:
            self.log(f"Błąd uruchomienia: {str(e)}")

        self._reset_buttons()


if __name__ == "__main__":
    app = YtDlpApp()
    app.mainloop()
