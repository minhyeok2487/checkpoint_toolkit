"""
CheckPoint 관리 도구 - 벌크 정책 생성 탭
CSV 기반 Access Rule 대량 생성
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import csv
import threading

from config import BRAND_BERRY
from lang import t, get_lang
from widgets import IconButton, RowDialog, PositionDialog, show_info, show_warning, show_error, ask_yesno


# 정책 컬럼 정의 (섹션 제거)
POLICY_COLUMNS = {
    "ko": ["룰이름", "소스", "목적지", "서비스", "액션", "트랙", "설명"],
    "en": ["RuleName", "Source", "Destination", "Service", "Action", "Track", "Comments"]
}

POLICY_API_COLUMNS = ["name", "source", "destination", "service", "action", "track", "comments"]

POLICY_TEMPLATE = [
    ["name", "source", "destination", "service", "action", "track", "comments"],
    ["web-to-db", "web_server", "db_server", "https", "Accept", "Log", "Web to DB access"],
    ["deny-all-db", "Any", "db_server", "Any", "Drop", "Log", "Block all to DB"],
    ["multi-src-dst", "src1;src2", "dst1;dst2", "http;https", "Accept", "Log", "Multiple sources and destinations"]
]


class PolicyTab(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self._build_package()
        self._build_options()
        self._build_table()
        self._build_bottom()
    
    def _build_package(self):
        frame = ctk.CTkFrame(self, corner_radius=8)
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=10)
        
        self.lbl_title = ctk.CTkLabel(inner, text="벌크 정책 생성" if get_lang() == "ko" else "Bulk Policy Generator", 
                                       font=ctk.CTkFont(size=12, weight="bold"), text_color=BRAND_BERRY)
        self.lbl_title.pack(anchor="w")
        
        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack(fill="x", pady=(5, 0))
        
        self.lbl_pkg = ctk.CTkLabel(row, text="패키지:" if get_lang() == "ko" else "Package:", font=ctk.CTkFont(size=11))
        self.lbl_pkg.pack(side="left")
        self.package_entry = ctk.CTkEntry(row, width=150, height=28)
        self.package_entry.pack(side="left", padx=(5, 15))
        self.package_entry.insert(0, "Standard")
        
        self.lbl_layer = ctk.CTkLabel(row, text="레이어:" if get_lang() == "ko" else "Layer:", font=ctk.CTkFont(size=11))
        self.lbl_layer.pack(side="left")
        self.layer_entry = ctk.CTkEntry(row, width=200, height=28, placeholder_text="비워두면 자동" if get_lang() == "ko" else "Auto if empty")
        self.layer_entry.pack(side="left", padx=(5, 15))
        
        self.btn_verify = IconButton(row, "확인" if get_lang() == "ko" else "Verify", self._verify_package, width=60)
        self.btn_verify.pack(side="left")
    
    def _build_options(self):
        frame = ctk.CTkFrame(self, corner_radius=8)
        frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=10)
        
        btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        self.btn_load = IconButton(btn_frame, "CSV 불러오기" if get_lang() == "ko" else "Load CSV", self._load_csv, width=95)
        self.btn_load.pack(side="left", padx=2)
        self.btn_add = IconButton(btn_frame, "+ 추가" if get_lang() == "ko" else "+ Add", self._add_row, "success", 70)
        self.btn_add.pack(side="left", padx=2)
        self.btn_edit = IconButton(btn_frame, "편집" if get_lang() == "ko" else "Edit", self._edit_row, "secondary", 60)
        self.btn_edit.pack(side="left", padx=2)
        self.btn_delete = IconButton(btn_frame, "삭제" if get_lang() == "ko" else "Delete", self._delete_row, "danger", 60)
        self.btn_delete.pack(side="left", padx=2)
        self.btn_save = IconButton(btn_frame, "CSV 저장" if get_lang() == "ko" else "Save CSV", self._save_csv, "secondary", 85)
        self.btn_save.pack(side="left", padx=2)
        self.btn_template = IconButton(btn_frame, "템플릿" if get_lang() == "ko" else "Template", self._create_template, "secondary", 70)
        self.btn_template.pack(side="left", padx=2)
        
        self.lbl_file = ctk.CTkLabel(btn_frame, text="파일:" if get_lang() == "ko" else "File:", font=ctk.CTkFont(size=10))
        self.lbl_file.pack(side="left", padx=(15, 5))
        self.csv_path = ctk.StringVar()
        ctk.CTkEntry(btn_frame, textvariable=self.csv_path, state="readonly", width=180, height=26, font=ctk.CTkFont(size=10)).pack(side="left")
        
        hint_frame = ctk.CTkFrame(inner, fg_color="transparent")
        hint_frame.pack(fill="x", pady=(8, 0))
        hint_ko = "⚠️ 오브젝트: 대량 등록 탭에서 먼저 등록 필요! (또는 자동생성 옵션 → 빈 그룹 생성)\n⚠️ 서비스: CheckPoint에 등록된 이름과 정확히 일치해야 함 (예: http, https, ssh, MSSQL 등)\n💡 다중 값: 세미콜론(;)으로 구분 | 액션: Accept, Drop, Reject | 트랙: Log, None"
        hint_en = "⚠️ Objects: Register first in Bulk Import tab! (or Auto objects option → creates empty groups)\n⚠️ Services: Must exactly match names registered in CheckPoint (e.g. http, https, ssh, MSSQL)\n💡 Multiple values: semicolon(;) separated | Action: Accept, Drop, Reject | Track: Log, None"
        self.hint_label = ctk.CTkLabel(hint_frame, text=hint_ko if get_lang() == "ko" else hint_en, 
                                        font=ctk.CTkFont(size=10), wraplength=900, justify="left")
        self.hint_label.pack(anchor="w")
    
    def _build_table(self):
        table_frame = ctk.CTkFrame(self, corner_radius=8)
        table_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        container = ctk.CTkFrame(table_frame, corner_radius=6)
        container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.tree = tk.ttk.Treeview(container, show="headings", selectmode="browse")
        scrollbar_y = ctk.CTkScrollbar(container, command=self.tree.yview)
        scrollbar_x = tk.ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        
        self._setup_columns()
        self.tree.bind("<Double-1>", lambda e: self._edit_row())
        self.bind("<Map>", lambda e: self._apply_tree_theme())
        self._apply_tree_theme()
    
    def _apply_tree_theme(self):
        mode = ctk.get_appearance_mode()
        style = tk.ttk.Style()
        style.theme_use("clam")
        if mode == "Dark":
            bg, fg, selbg, headbg = "#2b2b2b", "#ffffff", BRAND_BERRY, "#3b3b3b"
        else:
            bg, fg, selbg, headbg = "#ffffff", "#000000", BRAND_BERRY, "#e0e0e0"
        style.configure("Treeview", background=bg, foreground=fg, fieldbackground=bg, rowheight=28)
        style.configure("Treeview.Heading", background=headbg, foreground=fg, font=("", 10, "bold"))
        style.map("Treeview", background=[("selected", selbg)], foreground=[("selected", "white")])
    
    def _build_bottom(self):
        bottom = ctk.CTkFrame(self, corner_radius=8)
        bottom.grid(row=3, column=0, sticky="ew", padx=10, pady=(5, 10))
        inner = ctk.CTkFrame(bottom, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=10)
        
        self.chk_create_objects = ctk.CTkCheckBox(inner, text="오브젝트 자동생성" if get_lang() == "ko" else "Auto objects", 
                                                   font=ctk.CTkFont(size=11), fg_color=BRAND_BERRY)
        self.chk_create_objects.pack(side="left", padx=(0, 12))
        
        self.chk_dry = ctk.CTkCheckBox(inner, text="테스트" if get_lang() == "ko" else "Test", 
                                        font=ctk.CTkFont(size=11), fg_color=BRAND_BERRY)
        self.chk_dry.pack(side="left", padx=(0, 12))
        
        self.chk_publish = ctk.CTkCheckBox(inner, text="자동게시" if get_lang() == "ko" else "Auto publish", 
                                            font=ctk.CTkFont(size=11), fg_color=BRAND_BERRY)
        self.chk_publish.select()
        self.chk_publish.pack(side="left", padx=(0, 12))
        
        self.row_count_label = ctk.CTkLabel(inner, text="행: 0" if get_lang() == "ko" else "Rows: 0", font=ctk.CTkFont(size=11))
        self.row_count_label.pack(side="left", padx=(15, 0))
        
        self.generate_btn = IconButton(inner, "▶ 정책 생성" if get_lang() == "ko" else "▶ Generate", self._start_generate, "success", 100)
        self.generate_btn.pack(side="right")
        self.generate_btn.configure(state="disabled")
    
    def _get_columns(self):
        return POLICY_COLUMNS.get(get_lang(), POLICY_COLUMNS["en"])
    
    def _setup_columns(self):
        cols = self._get_columns()
        self.tree["columns"] = cols
        widths = [120, 150, 150, 120, 80, 80, 200]
        for i, col in enumerate(cols):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[i] if i < len(widths) else 100, anchor="w")
        self._update_row_count()
    
    def _update_row_count(self):
        if not hasattr(self, 'row_count_label'):
            return
        prefix = "행: " if get_lang() == "ko" else "Rows: "
        self.row_count_label.configure(text=f"{prefix}{len(self.tree.get_children())}")
    
    def refresh_lang(self):
        lang = get_lang()
        self.lbl_title.configure(text="벌크 정책 생성" if lang == "ko" else "Bulk Policy Generator")
        self.lbl_pkg.configure(text="패키지:" if lang == "ko" else "Package:")
        self.lbl_layer.configure(text="레이어:" if lang == "ko" else "Layer:")
        self.layer_entry.configure(placeholder_text="비워두면 자동" if lang == "ko" else "Auto if empty")
        self.btn_verify.configure(text="확인" if lang == "ko" else "Verify")
        self.btn_load.configure(text="CSV 불러오기" if lang == "ko" else "Load CSV")
        self.btn_add.configure(text="+ 추가" if lang == "ko" else "+ Add")
        self.btn_edit.configure(text="편집" if lang == "ko" else "Edit")
        self.btn_delete.configure(text="삭제" if lang == "ko" else "Delete")
        self.btn_save.configure(text="CSV 저장" if lang == "ko" else "Save CSV")
        self.btn_template.configure(text="템플릿" if lang == "ko" else "Template")
        self.lbl_file.configure(text="파일:" if lang == "ko" else "File:")
        
        hint_ko = "⚠️ 오브젝트: 대량 등록 탭에서 먼저 등록 필요! (또는 자동생성 옵션 → 빈 그룹 생성)\n⚠️ 서비스: CheckPoint에 등록된 이름과 정확히 일치해야 함 (예: http, https, ssh, MSSQL 등)\n💡 다중 값: 세미콜론(;)으로 구분 | 액션: Accept, Drop, Reject | 트랙: Log, None"
        hint_en = "⚠️ Objects: Register first in Bulk Import tab! (or Auto objects option → creates empty groups)\n⚠️ Services: Must exactly match names registered in CheckPoint (e.g. http, https, ssh, MSSQL)\n💡 Multiple values: semicolon(;) separated | Action: Accept, Drop, Reject | Track: Log, None"
        self.hint_label.configure(text=hint_ko if lang == "ko" else hint_en)
        
        self.chk_create_objects.configure(text="오브젝트 자동생성" if lang == "ko" else "Auto objects")
        self.chk_dry.configure(text="테스트" if lang == "ko" else "Test")
        self.chk_publish.configure(text="자동게시" if lang == "ko" else "Auto publish")
        self.generate_btn.configure(text="▶ 정책 생성" if lang == "ko" else "▶ Generate")
        self._setup_columns()
    
    def set_generate_enabled(self, enabled):
        self.generate_btn.configure(state="normal" if enabled else "disabled")
    
    # === CSV 관련 ===
    def _load_csv(self):
        path = filedialog.askopenfilename(
            title="CSV 파일 선택" if get_lang() == "ko" else "Select CSV",
            filetypes=[("CSV", "*.csv"), ("All", "*.*")]
        )
        if not path:
            return
        
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            with open(path, encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if row and any(row):
                        # 7개 컬럼으로 맞추기
                        while len(row) < 7:
                            row.append("")
                        self.tree.insert("", "end", values=row[:7])
            
            self.csv_path.set(path.split("/")[-1])
            self._update_row_count()
            self.app.log(f"{len(self.tree.get_children())}개 룰 로드" if get_lang() == "ko" else f"{len(self.tree.get_children())} rules loaded", "INFO")
        except Exception as e:
            show_error(self.app, t("error"), str(e))
    
    def _save_csv(self):
        path = filedialog.asksaveasfilename(
            title="CSV 저장" if get_lang() == "ko" else "Save CSV",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")]
        )
        if not path:
            return
        
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(POLICY_API_COLUMNS)
                for item in self.tree.get_children():
                    writer.writerow(self.tree.item(item)["values"])
            show_info(self.app, t("success"), f"저장 완료: {path}" if get_lang() == "ko" else f"Saved: {path}")
        except Exception as e:
            show_error(self.app, t("error"), str(e))
    
    def _create_template(self):
        path = filedialog.asksaveasfilename(
            title="템플릿 저장" if get_lang() == "ko" else "Save Template",
            defaultextension=".csv",
            initialfile="policy_template.csv",
            filetypes=[("CSV", "*.csv")]
        )
        if not path:
            return
        
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                for row in POLICY_TEMPLATE:
                    writer.writerow(row)
            show_info(self.app, t("success"), f"템플릿 저장: {path}" if get_lang() == "ko" else f"Template saved: {path}")
        except Exception as e:
            show_error(self.app, t("error"), str(e))
    
    # === 행 편집 ===
    def _add_row(self):
        cols = self._get_columns()
        dialog = RowDialog(self.app, cols, 
                          "새 룰 추가" if get_lang() == "ko" else "Add New Rule")
        self.app.wait_window(dialog)
        if dialog.result:
            self.tree.insert("", "end", values=dialog.result)
            self._update_row_count()
    
    def _edit_row(self):
        selected = self.tree.selection()
        if not selected:
            show_warning(self.app, t("warning"), "행을 선택하세요" if get_lang() == "ko" else "Select a row")
            return
        
        item = selected[0]
        current = list(self.tree.item(item)["values"])
        cols = self._get_columns()
        
        dialog = RowDialog(self.app, cols, 
                          "룰 편집" if get_lang() == "ko" else "Edit Rule",
                          current)
        self.app.wait_window(dialog)
        if dialog.result:
            self.tree.item(item, values=dialog.result)
    
    def _delete_row(self):
        selected = self.tree.selection()
        if not selected:
            show_warning(self.app, t("warning"), "행을 선택하세요" if get_lang() == "ko" else "Select a row")
            return
        
        if ask_yesno(self.app, t("confirm"), "삭제하시겠습니까?" if get_lang() == "ko" else "Delete?"):
            self.tree.delete(selected[0])
            self._update_row_count()
    
    # === 패키지 확인 ===
    def _verify_package(self):
        lang = get_lang()
        if not self.app.connected:
            show_warning(self.app, t("warning"), "서버에 연결하세요" if lang == "ko" else "Connect first")
            return
        
        pkg = self.package_entry.get().strip()
        if not pkg:
            show_warning(self.app, t("warning"), "패키지 입력" if lang == "ko" else "Enter package")
            return
        
        self.app.log(f"패키지 확인: {pkg}" if lang == "ko" else f"Checking package: {pkg}", "STEP")
        r = self.app.api.show_package(pkg)
        
        if "uid" in r:
            layers = r.get("access-layers", [])
            layer_name = layers[0].get("name") if layers else f"{pkg} Network"
            self.app.log(f"확인됨! 레이어: {layer_name}" if lang == "ko" else f"OK! Layer: {layer_name}", "SUCCESS")
            show_info(self.app, "OK", f"패키지: {pkg}\n레이어: {layer_name}" if lang == "ko" else f"Package: {pkg}\nLayer: {layer_name}")
        else:
            self.app.log(f"패키지 없음: {r.get('message')}" if lang == "ko" else f"Not found: {r.get('message')}", "ERROR")
            show_error(self.app, t("error"), f"'{pkg}' 없음" if lang == "ko" else f"'{pkg}' not found")
    
    # === 정책 생성 ===
    def _start_generate(self):
        lang = get_lang()
        
        if self.app.is_running:
            return
        if not self.app.connected:
            show_warning(self.app, t("warning"), "서버에 연결하세요" if lang == "ko" else "Connect first")
            return
        
        pkg = self.package_entry.get().strip()
        if not pkg:
            show_warning(self.app, t("warning"), "패키지 입력" if lang == "ko" else "Enter package")
            return
        
        count = len(self.tree.get_children())
        if count == 0:
            show_warning(self.app, t("warning"), "룰이 없습니다" if lang == "ko" else "No rules")
            return
        
        # 위치 다이얼로그
        dialog = PositionDialog(
            self.app,
            "룰 삽입 위치" if lang == "ko" else "Rule Position",
            "삽입할 룰 번호 입력 (빈칸: 맨 아래)" if lang == "ko" else "Enter rule number (empty: bottom)"
        )
        self.app.wait_window(dialog)
        
        if dialog.result is None:
            return
        
        position = dialog.result  # "" or number string
        
        if not ask_yesno(self.app, t("confirm"), f"{count}개 룰 생성?" if lang == "ko" else f"Create {count} rules?"):
            return
        
        self.app.is_running = True
        layer = self.layer_entry.get().strip()
        threading.Thread(target=self._run_generate, args=(pkg, layer, position), daemon=True).start()
    
    def _run_generate(self, package, layer, position):
        try:
            lang = get_lang()
            dry_run = self.chk_dry.get()
            auto_objects = self.chk_create_objects.get()
            
            self.app.log("=" * 40, "INFO")
            self.app.log("벌크 정책 생성 시작" if lang == "ko" else "Bulk policy generation started", "STEP")
            
            if dry_run:
                self.app.log("[테스트 모드]" if lang == "ko" else "[TEST MODE]", "WARNING")
            
            # 레이어 확인
            if not layer and not dry_run:
                self.app.log("레이어 감지 중..." if lang == "ko" else "Detecting layer...", "STEP")
                r = self.app.api.show_package(package)
                if "uid" not in r:
                    self.app.log("패키지 없음" if lang == "ko" else "Package not found", "ERROR")
                    return
                layers = r.get("access-layers", [])
                layer = layers[0].get("name") if layers else f"{package} Network"
                self.app.log(f"레이어: {layer}" if lang == "ko" else f"Layer: {layer}", "INFO")
            
            items = self.tree.get_children()
            total = len(items)
            
            # 위치 설정
            if position:
                pos_desc = f"위치 {position}" if lang == "ko" else f"Position {position}"
            else:
                pos_desc = "맨 아래" if lang == "ko" else "Bottom"
            self.app.log(f"삽입 위치: {pos_desc}" if lang == "ko" else f"Insert position: {pos_desc}", "INFO")
            
            # 룰 생성 (역순으로 생성하면 같은 위치에 순서대로 들어감)
            self.app.log("룰 생성 중..." if lang == "ko" else "Creating rules...", "STEP")
            success, fail = 0, 0
            
            # position이 있으면 역순으로, 없으면 정순으로 처리
            items_list = list(items)
            if position:
                items_list = list(reversed(items_list))
            
            for i, item in enumerate(items_list):
                row = [str(v).strip() for v in self.tree.item(item)["values"]]
                if not row or not row[0]:
                    continue
                
                name = row[0]
                source = row[1] if len(row) > 1 else "Any"
                destination = row[2] if len(row) > 2 else "Any"
                service = row[3] if len(row) > 3 else "Any"
                action = row[4] if len(row) > 4 else "Accept"
                track = row[5] if len(row) > 5 else "Log"
                comments = row[6] if len(row) > 6 else ""
                
                self.app.set_status(f"{i+1}/{total}: {name}")
                
                if dry_run:
                    self.app.log(f"  ✓ [DRY] {name}: {source} → {destination}", "SUCCESS")
                    success += 1
                    continue
                
                result = self._create_rule(layer, name, source, destination, service, action, track, comments, auto_objects, position)
                
                if result == "success":
                    success += 1
                    self.app.log(f"  ✓ {name}", "SUCCESS")
                else:
                    fail += 1
                    self.app.log(f"  ✗ {name}: {result}", "ERROR")
            
            level = "SUCCESS" if fail == 0 else "WARNING"
            self.app.log(f"완료! 성공:{success} 실패:{fail}" if lang == "ko" else f"Done! Success:{success} Failed:{fail}", level)
            
            if not dry_run and self.chk_publish.get() and success > 0:
                self.app.log("게시 중..." if lang == "ko" else "Publishing...", "STEP")
                self.app.set_status("게시 중..." if lang == "ko" else "Publishing...")
                r = self.app.api.publish()
                if "task-id" in r:
                    self.app.log("게시 완료!" if lang == "ko" else "Published!", "SUCCESS")
                else:
                    self.app.log(f"게시 실패: {r.get('message')}" if lang == "ko" else f"Publish failed: {r.get('message')}", "ERROR")
            
            self.app.log("=" * 40, "INFO")
            self.app.set_status("완료" if lang == "ko" else "Complete")
            
            if success > 0:
                self.after(0, lambda: show_info(
                    self.app,
                    "완료" if lang == "ko" else "Complete",
                    f"정책 생성 완료!\n성공: {success}, 실패: {fail}" if lang == "ko" else f"Policy generation complete!\nSuccess: {success}, Failed: {fail}"
                ))
            
        except Exception as e:
            self.app.log(f"오류: {e}" if get_lang() == "ko" else f"Error: {e}", "ERROR")
        finally:
            self.app.is_running = False
    
    def _create_rule(self, layer, name, source, destination, service, action, track, comments, auto_objects, position):
        try:
            sources = [s.strip() for s in source.split(";") if s.strip()] or ["Any"]
            destinations = [d.strip() for d in destination.split(";") if d.strip()] or ["Any"]
            services = [s.strip() for s in service.split(";") if s.strip()] or ["Any"]
            
            if auto_objects:
                for src in sources:
                    if src != "Any" and not self._object_exists(src):
                        self._create_placeholder(src)
                for dst in destinations:
                    if dst != "Any" and not self._object_exists(dst):
                        self._create_placeholder(dst)
            
            action_payload = self._parse_action(action)
            track_payload = {"type": track} if track in ["Log", "None", "Detailed Log", "Extended Log"] else {"type": "Log"}
            
            # position 설정
            if position:
                pos_payload = position  # 숫자 문자열
            else:
                pos_payload = "bottom"
            
            payload = {
                "layer": layer,
                "position": pos_payload,
                "name": name,
                "source": sources if len(sources) > 1 else sources[0],
                "destination": destinations if len(destinations) > 1 else destinations[0],
                "service": services if len(services) > 1 else services[0],
                "action": action_payload,
                "track": track_payload
            }
            if comments:
                payload["comments"] = comments
            
            result = self.app.api._call("add-access-rule", payload)
            return "success" if "uid" in result else result.get("message", "Unknown error")
        except Exception as e:
            return str(e)
    
    def _parse_action(self, action: str):
        action_lower = action.lower().strip()
        if action_lower == "accept":
            return "Accept"
        elif action_lower == "drop":
            return "Drop"
        elif action_lower == "reject":
            return "Reject"
        return "Accept"
    
    def _object_exists(self, name: str) -> bool:
        for obj_type in ["host", "network", "group", "security-zone"]:
            if "uid" in self.app.api.show_object(obj_type, name):
                return True
        return False
    
    def _create_placeholder(self, name: str):
        self.app.api._call("add-group", {"name": name, "comments": "Auto-created placeholder"})
        self.app.log(f"  → 그룹 생성: {name}" if get_lang() == "ko" else f"  → Group created: {name}", "INFO")
