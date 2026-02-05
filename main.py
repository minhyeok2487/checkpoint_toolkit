#!/usr/bin/env python3
"""
CheckPoint 관리 도구 v3.5 (Stable)
현대오토에버 보안팀

Changelog:
- v3.5: Stable - Management API 전용 (GAIA API 제외), 듀얼모니터 DPI 최적화
- v3.4: Zone Policy 생성 로직 안정화 (섹션 이름 기반 position.below)
- v3.3: 섹션 위치 지정 수정
- v3.2: Zone Policy 탭 추가
- v3.1: Bulk Policy 탭 추가  
- v3.0: 한/영 지원, 모듈화
"""

import sys
import os

# Windows DPI Awareness 설정 (듀얼 모니터 최적화)
if sys.platform == "win32":
    try:
        import ctypes
        # Per-Monitor DPI Aware v2 (Windows 10 1703+)
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

# CustomTkinter DPI 자동 스케일링 비활성화 (수동 제어)
os.environ["CTK_SCALING"] = "1.0"

import customtkinter as ctk

# CustomTkinter 자동 DPI 감지 비활성화 (랙 감소)
ctk.deactivate_automatic_dpi_awareness()

from datetime import datetime
import json

from config import APP_GEOMETRY, APP_MIN_SIZE, BRAND_BERRY, BRAND_BERRY_DARK, SUCCESS, ERROR
from lang import t, get_lang, set_lang
from api import CheckPointAPI
from widgets import IconButton, LogPanel, show_warning, show_error, ask_yesno
from tabs import ImportTab
from tabs.policy_tab import PolicyTab
from tabs.zone_policy_tab import ZonePolicyTab

SETTINGS_FILE = "connection_settings.json"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self._load_preferences()
        
        self.title(t("app_title"))
        self.geometry(APP_GEOMETRY)
        self.minsize(*APP_MIN_SIZE)
        
        self.api = None
        self.connected = False
        self.is_running = False
        self.log_file = f"cp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        ctk.set_appearance_mode(self._current_theme)
        ctk.set_default_color_theme("blue")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._build_header()
        self._build_body()
        self._load_connection_settings()
        
        self.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _load_preferences(self):
        self._current_theme = "dark"
        self._current_lang = "ko"
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
                    self._current_theme = data.get("theme", "dark")
                    self._current_lang = data.get("lang", "ko")
            except: pass
        set_lang(self._current_lang)
    
    def _build_header(self):
        header = ctk.CTkFrame(self, corner_radius=0, height=95)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)
        header.grid_columnconfigure(1, weight=1)
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        ctk.CTkLabel(title_frame, text="🛡️", font=ctk.CTkFont(size=28)).pack(side="left", padx=(0, 10))
        
        txt = ctk.CTkFrame(title_frame, fg_color="transparent")
        txt.pack(side="left")
        self.title_label = ctk.CTkLabel(txt, text=t("app_title").replace(" v3.2", ""), font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.pack(anchor="w")
        self.subtitle_label = ctk.CTkLabel(txt, text=t("app_subtitle"), font=ctk.CTkFont(size=10))
        self.subtitle_label.pack(anchor="w")
        
        conn = ctk.CTkFrame(header, corner_radius=8)
        conn.grid(row=0, column=1, sticky="e", padx=20, pady=10)
        
        inner = ctk.CTkFrame(conn, fg_color="transparent")
        inner.pack(padx=12, pady=8)
        
        r1 = ctk.CTkFrame(inner, fg_color="transparent")
        r1.pack(fill="x", pady=1)
        
        self.lbl_server = ctk.CTkLabel(r1, text=t("server"), width=45, font=ctk.CTkFont(size=11))
        self.lbl_server.pack(side="left")
        self.server_entry = ctk.CTkEntry(r1, width=110, height=24, font=ctk.CTkFont(size=11))
        self.server_entry.pack(side="left", padx=2)
        
        self.lbl_port = ctk.CTkLabel(r1, text=t("port"), width=30, font=ctk.CTkFont(size=11))
        self.lbl_port.pack(side="left", padx=(8,0))
        self.port_entry = ctk.CTkEntry(r1, width=45, height=24, font=ctk.CTkFont(size=11))
        self.port_entry.pack(side="left", padx=2)
        
        self.lbl_user = ctk.CTkLabel(r1, text=t("user"), width=45, font=ctk.CTkFont(size=11))
        self.lbl_user.pack(side="left", padx=(8,0))
        self.user_entry = ctk.CTkEntry(r1, width=70, height=24, font=ctk.CTkFont(size=11))
        self.user_entry.pack(side="left", padx=2)
        
        self.lbl_pass = ctk.CTkLabel(r1, text=t("password"), width=55, font=ctk.CTkFont(size=11))
        self.lbl_pass.pack(side="left", padx=(8,0))
        self.pass_entry = ctk.CTkEntry(r1, width=70, height=24, show="●", font=ctk.CTkFont(size=11))
        self.pass_entry.pack(side="left", padx=2)
        
        r2 = ctk.CTkFrame(inner, fg_color="transparent")
        r2.pack(fill="x", pady=1)
        
        self.lbl_domain = ctk.CTkLabel(r2, text=t("domain"), width=45, font=ctk.CTkFont(size=11))
        self.lbl_domain.pack(side="left")
        self.domain_entry = ctk.CTkEntry(r2, width=110, height=24, font=ctk.CTkFont(size=11), placeholder_text=t("domain_hint"))
        self.domain_entry.pack(side="left", padx=2)
        
        self.connect_btn = IconButton(r2, t("connect"), self._connect, width=55)
        self.connect_btn.pack(side="left", padx=(12, 3))
        
        self.disconnect_btn = IconButton(r2, t("disconnect"), self._disconnect, "secondary", 45)
        self.disconnect_btn.pack(side="left", padx=2)
        self.disconnect_btn.configure(state="disabled")
        
        self.status_dot = ctk.CTkLabel(r2, text="●", font=ctk.CTkFont(size=10), text_color=ERROR)
        self.status_dot.pack(side="left", padx=(8, 2))
        
        self.status_label = ctk.CTkLabel(r2, text=t("disconnected"), font=ctk.CTkFont(size=10))
        self.status_label.pack(side="left")
        
        self.theme_btn = ctk.CTkButton(
            r2, text="🌙" if self._current_theme == "dark" else "☀️",
            width=30, height=24, corner_radius=6,
            fg_color="gray50", hover_color="gray40",
            command=self._toggle_theme
        )
        self.theme_btn.pack(side="left", padx=(8, 0))
        
        self.lang_btn = ctk.CTkButton(
            r2, text="EN" if self._current_lang == "ko" else "한",
            width=30, height=24, corner_radius=6,
            fg_color="gray50", hover_color="gray40",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self._toggle_lang
        )
        self.lang_btn.pack(side="left", padx=(4, 0))
    
    def _build_body(self):
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        body.grid_columnconfigure(1, weight=3)
        body.grid_columnconfigure(2, weight=1)
        body.grid_rowconfigure(0, weight=1)
        
        self.sidebar = ctk.CTkFrame(body, corner_radius=10, width=160)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.sidebar.grid_propagate(False)
        
        self.menu_label = ctk.CTkLabel(self.sidebar, text=t("menu"), font=ctk.CTkFont(size=11, weight="bold"), text_color=("gray10", "gray90"))
        self.menu_label.pack(pady=(12, 8), padx=12, anchor="w")
        
        self.current_page = ctk.StringVar(value="import")
        
        self.menu_import = ctk.CTkButton(
            self.sidebar, text=t("menu_import"), font=ctk.CTkFont(size=12),
            fg_color=BRAND_BERRY, hover_color=BRAND_BERRY_DARK,
            text_color="white",
            anchor="w", height=36, corner_radius=6,
            command=lambda: self._switch_page("import")
        )
        self.menu_import.pack(fill="x", padx=8, pady=2)
        
        self.menu_policy = ctk.CTkButton(
            self.sidebar, text=t("menu_policy"), font=ctk.CTkFont(size=12),
            fg_color="transparent", hover_color="gray70",
            text_color=("gray10", "gray90"),
            anchor="w", height=36, corner_radius=6,
            command=lambda: self._switch_page("policy")
        )
        self.menu_policy.pack(fill="x", padx=8, pady=2)
        
        self.menu_zone = ctk.CTkButton(
            self.sidebar, text=t("menu_zone"), font=ctk.CTkFont(size=12),
            fg_color="transparent", hover_color="gray70",
            text_color=("gray10", "gray90"),
            anchor="w", height=36, corner_radius=6,
            command=lambda: self._switch_page("zone")
        )
        self.menu_zone.pack(fill="x", padx=8, pady=2)
        
        self.content = ctk.CTkFrame(body, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew", padx=5)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)
        
        self.import_tab = ImportTab(self.content, self)
        self.policy_tab = PolicyTab(self.content, self)
        self.zone_tab = ZonePolicyTab(self.content, self)
        
        self.import_tab.grid(row=0, column=0, sticky="nsew")
        self.policy_tab.grid(row=0, column=0, sticky="nsew")
        self.zone_tab.grid(row=0, column=0, sticky="nsew")
        self.import_tab.tkraise()
        
        self.log_panel = LogPanel(body, width=400)
        self.log_panel.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        self.log_panel.grid_propagate(False)
    
    def _switch_page(self, page: str):
        self.current_page.set(page)
        # 모든 메뉴 비활성화
        self.menu_import.configure(fg_color="transparent", text_color=("gray10", "gray90"))
        self.menu_policy.configure(fg_color="transparent", text_color=("gray10", "gray90"))
        self.menu_zone.configure(fg_color="transparent", text_color=("gray10", "gray90"))
        
        if page == "import":
            self.menu_import.configure(fg_color=BRAND_BERRY, text_color="white")
            self.import_tab.tkraise()
        elif page == "policy":
            self.menu_policy.configure(fg_color=BRAND_BERRY, text_color="white")
            self.policy_tab.tkraise()
        elif page == "zone":
            self.menu_zone.configure(fg_color=BRAND_BERRY, text_color="white")
            self.zone_tab.tkraise()
    
    def _toggle_theme(self):
        self._current_theme = "light" if self._current_theme == "dark" else "dark"
        ctk.set_appearance_mode(self._current_theme)
        self.theme_btn.configure(text="🌙" if self._current_theme == "dark" else "☀️")
        self._save_settings()
    
    def _toggle_lang(self):
        self._current_lang = "en" if self._current_lang == "ko" else "ko"
        set_lang(self._current_lang)
        self._save_settings()
        self._refresh_ui()
    
    def _refresh_ui(self):
        self.title(t("app_title"))
        self.title_label.configure(text=t("app_title").replace(" v3.2", ""))
        self.subtitle_label.configure(text=t("app_subtitle"))
        
        self.lbl_server.configure(text=t("server"))
        self.lbl_port.configure(text=t("port"))
        self.lbl_user.configure(text=t("user"))
        self.lbl_pass.configure(text=t("password"))
        self.lbl_domain.configure(text=t("domain"))
        self.domain_entry.configure(placeholder_text=t("domain_hint"))
        
        self.connect_btn.configure(text=t("connect"))
        self.disconnect_btn.configure(text=t("disconnect"))
        self.status_label.configure(text=t("connected") if self.connected else t("disconnected"))
        
        self.lang_btn.configure(text="EN" if self._current_lang == "ko" else "한")
        
        self.menu_label.configure(text=t("menu"))
        self.menu_import.configure(text=t("menu_import"))
        self.menu_policy.configure(text=t("menu_policy"))
        self.menu_zone.configure(text=t("menu_zone"))
        self.menu_gaia.configure(text=t("menu_gaia"))
        
        self.log_panel.refresh_lang()
        self.import_tab.refresh_lang()
        self.policy_tab.refresh_lang()
        self.zone_tab.refresh_lang()
    
    def _connect(self):
        server = self.server_entry.get().strip()
        port = self.port_entry.get().strip()
        user = self.user_entry.get().strip()
        password = self.pass_entry.get()
        domain = self.domain_entry.get().strip() or None
        
        if not all([server, user, password]):
            show_warning(self, t("warning"), t("msg_fill_required"))
            return
        
        self.log(t("log_connecting", server=server, port=port), "STEP")
        self.set_status(t("connecting"))
        
        self.api = CheckPointAPI(server, int(port))
        result = self.api.login(user, password, domain)
        
        if "sid" in result:
            self.connected = True
            self.log(t("log_connected"), "SUCCESS")
            self.set_status(t("connected"))
            self._set_connected(True)
            self._save_settings()
            
            self.connect_btn.configure(state="disabled")
            self.disconnect_btn.configure(state="normal")
            self.import_tab.set_import_enabled(True)
            self.policy_tab.set_generate_enabled(True)
            self.zone_tab.set_generate_enabled(True)
        else:
            self.log(t("log_failed", msg=result.get('message')), "ERROR")
            self.set_status(t("disconnected"))
            show_error(self, t("error"), result.get("message", "Unknown error"))
    
    def _disconnect(self):
        if self.api:
            self.api.logout()
            self.log(t("log_disconnected"), "INFO")
        
        self.connected = False
        self.api = None
        self.set_status(t("disconnected"))
        self._set_connected(False)
        
        self.connect_btn.configure(state="normal")
        self.disconnect_btn.configure(state="disabled")
        self.import_tab.set_import_enabled(False)
        self.policy_tab.set_generate_enabled(False)
        self.zone_tab.set_generate_enabled(False)
    
    def _set_connected(self, connected: bool):
        if connected:
            self.status_dot.configure(text_color=SUCCESS)
            self.status_label.configure(text=t("connected"))
        else:
            self.status_dot.configure(text_color=ERROR)
            self.status_label.configure(text=t("disconnected"))
    
    def log(self, message: str, level: str = "INFO"):
        self.log_panel.log(message, level)
        ts = datetime.now().strftime("%H:%M:%S")
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{ts}] [{level}] {message}\n")
    
    def set_status(self, text: str):
        self.log_panel.set_status(text)
    
    def _on_close(self):
        if self.is_running:
            show_warning(self, t("warning"), t("msg_task_running"))
            return
        if self.connected:
            if ask_yesno(self, t("confirm"), t("msg_confirm_exit")):
                self._disconnect()
            else:
                return
        self.destroy()
    
    def _save_settings(self):
        settings = {
            "server": self.server_entry.get().strip(),
            "port": self.port_entry.get().strip(),
            "user": self.user_entry.get().strip(),
            "domain": self.domain_entry.get().strip(),
            "theme": self._current_theme,
            "lang": self._current_lang
        }
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
        except: pass
    
    def _load_connection_settings(self):
        defaults = {"server": "192.168.1.1", "port": "443", "user": "admin", "domain": ""}
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    defaults.update(json.load(f))
            except: pass
        
        self.server_entry.insert(0, defaults.get("server", ""))
        self.port_entry.insert(0, defaults.get("port", ""))
        self.user_entry.insert(0, defaults.get("user", ""))
        if defaults.get("domain"):
            self.domain_entry.insert(0, defaults["domain"])


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
