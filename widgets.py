"""
CheckPoint Management Toolkit - 위젯
"""

import customtkinter as ctk
from config import BRAND_BERRY, BRAND_BERRY_DARK, SUCCESS, ERROR
from lang import t


class IconButton(ctk.CTkButton):
    def __init__(self, master, text: str, command=None, style: str = "default", width: int = 90, **kwargs):
        styles = {
            "default": (BRAND_BERRY, BRAND_BERRY_DARK),
            "success": (SUCCESS, "#00b359"),
            "danger": (ERROR, "#cc3344"),
            "secondary": ("gray50", "gray40"),
        }
        fg, hover = styles.get(style, styles["default"])
        super().__init__(master, text=text, command=command, fg_color=fg, hover_color=hover,
                         text_color="white", corner_radius=6, width=width, height=28,
                         font=ctk.CTkFont(size=11, weight="bold"), **kwargs)


class LogPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, corner_radius=10, **kwargs)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        self.log_title = ctk.CTkLabel(header, text=t("log_title"), font=ctk.CTkFont(size=12, weight="bold"))
        self.log_title.pack(side="left")
        self.clear_btn = IconButton(header, t("clear"), self.clear, "secondary", 60)
        self.clear_btn.pack(side="right")
        
        self.textbox = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12), corner_radius=6)
        self.textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.textbox.configure(state="disabled")
        
        self.status_label = ctk.CTkLabel(self, text=t("ready"), font=ctk.CTkFont(size=10), anchor="w")
        self.status_label.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
    
    def refresh_lang(self):
        self.log_title.configure(text=t("log_title"))
        self.clear_btn.configure(text=t("clear"))
    
    def log(self, message: str, level: str = "INFO"):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"[{ts}] [{level}] {message}\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")
    
    def clear(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")
    
    def set_status(self, text: str):
        self.status_label.configure(text=text)


class PositionDialog(ctk.CTkToplevel):
    def __init__(self, parent, title: str, message: str):
        super().__init__(parent)
        self.title(title)
        self.geometry("380x200")
        self.resizable(False, False)
        self.result = None
        self.transient(parent)
        self.grab_set()

        # 부모 창 기준 중앙 배치
        self.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        x = parent_x + (parent_w - self.winfo_width()) // 2
        y = parent_y + (parent_h - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
        ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=11), wraplength=340).pack(padx=15, pady=5)
        
        inp = ctk.CTkFrame(self, fg_color="transparent")
        inp.pack(pady=10)
        ctk.CTkLabel(inp, text=t("position")).pack(side="left", padx=5)
        self.entry = ctk.CTkEntry(inp, width=100, placeholder_text=t("position_hint"))
        self.entry.pack(side="left")
        
        btn = ctk.CTkFrame(self, fg_color="transparent")
        btn.pack(pady=15)
        IconButton(btn, t("confirm"), self._ok, width=70).pack(side="left", padx=5)
        IconButton(btn, t("cancel"), self._cancel, "secondary", 70).pack(side="left", padx=5)
        
        self.entry.focus_set()
        self.bind("<Return>", lambda e: self._ok())
        self.bind("<Escape>", lambda e: self._cancel())
    
    def _ok(self):
        self.result = self.entry.get().strip()
        self.destroy()
    
    def _cancel(self):
        self.result = None
        self.destroy()


class RowDialog(ctk.CTkToplevel):
    def __init__(self, parent, columns: list, title: str, values: list = None):
        super().__init__(parent)
        self.title(title)
        self.geometry("420x380")
        self.resizable(False, False)
        self.result = None
        self.transient(parent)
        self.grab_set()

        # 부모 창 기준 중앙 배치
        self.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        x = parent_x + (parent_w - self.winfo_width()) // 2
        y = parent_y + (parent_h - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        
        ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=14, weight="bold"), text_color=BRAND_BERRY).pack(pady=(10, 5))

        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(fill="x", padx=20, pady=5)
        form.grid_columnconfigure(0, weight=0, minsize=80)
        form.grid_columnconfigure(1, weight=1)

        self.entries = {}
        for i, col in enumerate(columns):
            ctk.CTkLabel(form, text=f"{col}:", anchor="e").grid(row=i, column=0, sticky="e", padx=(0, 10), pady=3)
            e = ctk.CTkEntry(form, width=260)
            e.grid(row=i, column=1, sticky="w", pady=3)
            if values and i < len(values):
                e.insert(0, str(values[i]))
            self.entries[col] = e
        
        hint_cols = ["멤버", "URL목록", "Members", "URL List"]
        if any(c in columns for c in hint_cols):
            ctk.CTkLabel(self, text=t("multi_value_hint"), font=ctk.CTkFont(size=10)).pack(pady=5)
        
        btn = ctk.CTkFrame(self, fg_color="transparent")
        btn.pack(pady=15)
        IconButton(btn, t("save"), self._save, "success", 80).pack(side="left", padx=5)
        IconButton(btn, t("cancel"), self.destroy, "secondary", 80).pack(side="left", padx=5)
        
        list(self.entries.values())[0].focus_set()
        self.bind("<Return>", lambda e: self._save())
    
    def _save(self):
        first = list(self.entries.values())[0]
        if not first.get().strip():
            return
        self.result = [e.get().strip() for e in self.entries.values()]
        self.destroy()


class MessageDialog(ctk.CTkToplevel):
    def __init__(self, parent, title: str, message: str, msg_type: str = "info", ask: bool = False):
        super().__init__(parent)
        self.title(title)
        self.geometry("350x170")
        self.resizable(False, False)
        self.result = None
        self.transient(parent)
        self.grab_set()

        # 부모 창 기준 중앙 배치
        self.update_idletasks()
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()
        x = parent_x + (parent_w - self.winfo_width()) // 2
        y = parent_y + (parent_h - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        
        icons = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "success": "✅", "question": "❓"}
        icon = icons.get(msg_type, "ℹ️")
        
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)
        ctk.CTkLabel(content, text=icon, font=ctk.CTkFont(size=32)).pack(side="left", padx=(0, 15))
        ctk.CTkLabel(content, text=message, font=ctk.CTkFont(size=12), wraplength=230, justify="left").pack(side="left", fill="both", expand=True)
        
        btn = ctk.CTkFrame(self, fg_color="transparent")
        btn.pack(pady=(0, 15))
        
        if ask:
            IconButton(btn, t("yes"), self._yes, "success", 70).pack(side="left", padx=5)
            IconButton(btn, t("no"), self._no, "secondary", 70).pack(side="left", padx=5)
        else:
            IconButton(btn, t("confirm"), self._ok, width=80).pack()
        
        self.focus_force()
        self.bind("<Return>", lambda e: self._ok() if not ask else self._yes())
        self.bind("<Escape>", lambda e: self._no() if ask else self._ok())
    
    def _ok(self): self.result = True; self.destroy()
    def _yes(self): self.result = True; self.destroy()
    def _no(self): self.result = False; self.destroy()


def show_info(parent, title, msg):
    d = MessageDialog(parent, title, msg, "info"); parent.wait_window(d)

def show_warning(parent, title, msg):
    d = MessageDialog(parent, title, msg, "warning"); parent.wait_window(d)

def show_error(parent, title, msg):
    d = MessageDialog(parent, title, msg, "error"); parent.wait_window(d)

def ask_yesno(parent, title, msg) -> bool:
    d = MessageDialog(parent, title, msg, "question", ask=True); parent.wait_window(d); return d.result
