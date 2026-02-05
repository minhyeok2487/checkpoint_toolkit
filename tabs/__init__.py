"""
CheckPoint 관리 도구 - 대량 등록 탭
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import csv
import threading

from config import BRAND_BERRY, get_object_types
from lang import t, get_lang
from widgets import IconButton, RowDialog, show_info, show_warning, show_error, ask_yesno


class ImportTab(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._build_top()
        self._build_table()
        self._build_bottom()
    
    def _build_top(self):
        top = ctk.CTkFrame(self, corner_radius=8)
        top.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        inner = ctk.CTkFrame(top, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=10)
        
        self.type_label = ctk.CTkLabel(inner, text=t("object_type"), font=ctk.CTkFont(size=12, weight="bold"), text_color=BRAND_BERRY)
        self.type_label.pack(anchor="w")
        
        self.obj_type = ctk.StringVar(value="host")
        types_frame = ctk.CTkFrame(inner, fg_color="transparent")
        types_frame.pack(fill="x", pady=(5, 0))
        
        for text, value in [("Host", "host"), ("Network", "network"), ("Group", "group"),
                            ("Service-TCP", "service-tcp"), ("Service-UDP", "service-udp"),
                            ("Address-Range", "address-range"), ("App Site(URL)", "application-site"),
                            ("DNS Domain", "dns-domain")]:
            ctk.CTkRadioButton(types_frame, text=text, variable=self.obj_type, value=value,
                               command=self._on_type_change, font=ctk.CTkFont(size=11), fg_color=BRAND_BERRY).pack(side="left", padx=(0, 15))
        
        self.format_label = ctk.CTkLabel(inner, text=t("format") + " " + self._get_format(), font=ctk.CTkFont(size=10))
        self.format_label.pack(anchor="w", pady=(5, 0))
        
        btn_frame = ctk.CTkFrame(inner, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        self.btn_load = IconButton(btn_frame, t("load_csv"), self._load_csv, width=95)
        self.btn_load.pack(side="left", padx=2)
        self.btn_add = IconButton(btn_frame, t("add"), self._add_row, "success", 70)
        self.btn_add.pack(side="left", padx=2)
        self.btn_edit = IconButton(btn_frame, t("edit"), self._edit_row, "secondary", 60)
        self.btn_edit.pack(side="left", padx=2)
        self.btn_delete = IconButton(btn_frame, t("delete"), self._delete_row, "danger", 60)
        self.btn_delete.pack(side="left", padx=2)
        self.btn_save = IconButton(btn_frame, t("save_csv"), self._save_csv, "secondary", 85)
        self.btn_save.pack(side="left", padx=2)
        self.btn_fetch = IconButton(btn_frame, t("fetch_server"), self._fetch_objects, "secondary", 110)
        self.btn_fetch.pack(side="left", padx=2)
        self.btn_template = IconButton(btn_frame, t("template"), self._create_template, "secondary", 70)
        self.btn_template.pack(side="left", padx=2)
        
        self.lbl_file = ctk.CTkLabel(btn_frame, text=t("file"), font=ctk.CTkFont(size=10))
        self.lbl_file.pack(side="left", padx=(15, 5))
        self.csv_path = ctk.StringVar()
        ctk.CTkEntry(btn_frame, textvariable=self.csv_path, state="readonly", width=200, height=26, font=ctk.CTkFont(size=10)).pack(side="left")
    
    def _build_table(self):
        table_frame = ctk.CTkFrame(self, corner_radius=8)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        container = ctk.CTkFrame(table_frame, corner_radius=6)
        container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.tree = tk.ttk.Treeview(container, show="headings", selectmode="browse")
        scrollbar = ctk.CTkScrollbar(container, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=2)
        
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
        style.configure("Treeview", background=bg, foreground=fg, fieldbackground=bg, borderwidth=0, rowheight=26)
        style.configure("Treeview.Heading", background=headbg, foreground=fg, borderwidth=0)
        style.map("Treeview", background=[("selected", selbg)], foreground=[("selected", "#ffffff")])
    
    def _build_bottom(self):
        bottom = ctk.CTkFrame(self, corner_radius=8)
        bottom.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        
        inner = ctk.CTkFrame(bottom, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=10)
        
        self.chk_update = ctk.CTkCheckBox(inner, text=t("update_existing"), font=ctk.CTkFont(size=11), fg_color=BRAND_BERRY)
        self.chk_update.pack(side="left", padx=(0, 15))
        
        self.chk_dry = ctk.CTkCheckBox(inner, text=t("test_mode"), font=ctk.CTkFont(size=11), fg_color=BRAND_BERRY)
        self.chk_dry.pack(side="left", padx=(0, 15))
        
        self.chk_publish = ctk.CTkCheckBox(inner, text=t("auto_publish"), font=ctk.CTkFont(size=11), fg_color=BRAND_BERRY)
        self.chk_publish.select()
        self.chk_publish.pack(side="left", padx=(0, 15))
        
        self.row_count_label = ctk.CTkLabel(inner, text=t("row_count") + " 0", font=ctk.CTkFont(size=11))
        self.row_count_label.pack(side="left", padx=(15, 0))
        
        self.import_btn = IconButton(inner, t("start_import"), self._start_import, "success", 100)
        self.import_btn.pack(side="right")
        self.import_btn.configure(state="disabled")
    
    def refresh_lang(self):
        self.type_label.configure(text=t("object_type"))
        self.format_label.configure(text=t("format") + " " + self._get_format())
        self.btn_load.configure(text=t("load_csv"))
        self.btn_add.configure(text=t("add"))
        self.btn_edit.configure(text=t("edit"))
        self.btn_delete.configure(text=t("delete"))
        self.btn_save.configure(text=t("save_csv"))
        self.btn_fetch.configure(text=t("fetch_server"))
        self.btn_template.configure(text=t("template"))
        self.lbl_file.configure(text=t("file"))
        self.chk_update.configure(text=t("update_existing"))
        self.chk_dry.configure(text=t("test_mode"))
        self.chk_publish.configure(text=t("auto_publish"))
        self._update_row_count()
        self.import_btn.configure(text=t("start_import"))
        self._setup_columns()
    
    def _get_format(self):
        return get_object_types(get_lang()).get(self.obj_type.get(), {}).get("format", "")
    
    def _get_columns(self):
        return get_object_types(get_lang()).get(self.obj_type.get(), {}).get("columns", ["Name", "Value"])
    
    def _get_api_columns(self):
        return get_object_types(get_lang()).get(self.obj_type.get(), {}).get("api_columns", ["name", "value"])
    
    def _setup_columns(self):
        cols = self._get_columns()
        self.tree["columns"] = cols
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="w")
        self._update_row_count()
    
    def _update_row_count(self):
        if hasattr(self, 'row_count_label'):
            self.row_count_label.configure(text=t("row_count") + f" {len(self.tree.get_children())}")
    
    def _on_type_change(self):
        self.format_label.configure(text=t("format") + " " + self._get_format())
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._setup_columns()
    
    def set_import_enabled(self, enabled: bool):
        self.import_btn.configure(state="normal" if enabled else "disabled")
    
    def _load_csv(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not filepath: return
        self.csv_path.set(filepath)
        for item in self.tree.get_children(): self.tree.delete(item)
        cols = self._get_columns()
        try:
            with open(filepath, 'r', encoding='utf-8-sig') as f:
                rows = list(csv.reader(f))
            for row in rows[1:]:
                if row and row[0].strip():
                    while len(row) < len(cols): row.append("")
                    self.tree.insert("", "end", values=row[:len(cols)])
            self._update_row_count()
            self.app.log(t("msg_rows_loaded", count=len(self.tree.get_children())), "INFO")
        except Exception as e:
            show_error(self.app, t("error"), str(e))
    
    def _add_row(self):
        d = RowDialog(self.app, self._get_columns(), t("add_row"))
        self.app.wait_window(d)
        if d.result:
            self.tree.insert("", "end", values=d.result)
            self._update_row_count()
    
    def _edit_row(self):
        sel = self.tree.selection()
        if not sel: show_warning(self.app, t("warning"), t("msg_select_row_edit")); return
        vals = self.tree.item(sel[0])["values"]
        d = RowDialog(self.app, self._get_columns(), t("edit_row"), vals)
        self.app.wait_window(d)
        if d.result: self.tree.item(sel[0], values=d.result)
    
    def _delete_row(self):
        sel = self.tree.selection()
        if not sel: show_warning(self.app, t("warning"), t("msg_select_row_delete")); return
        if ask_yesno(self.app, t("confirm"), t("msg_confirm_delete")):
            self.tree.delete(sel[0])
            self._update_row_count()
    
    def _save_csv(self):
        if not self.tree.get_children():
            show_warning(self.app, t("warning"), t("msg_no_save_data")); return
        obj_type = self.obj_type.get()
        default_name = f"export_{obj_type}.csv"
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=default_name, filetypes=[("CSV", "*.csv")])
        if not filepath: return
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(self._get_api_columns())
            for item in self.tree.get_children():
                writer.writerow(self.tree.item(item)["values"])
        self.csv_path.set(filepath)
        show_info(self.app, t("complete"), t("msg_saved", path=filepath))
    
    def _create_template(self):
        obj_type = self.obj_type.get()
        template = get_object_types(get_lang()).get(obj_type, {}).get("template", [])
        filepath = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=f"template_{obj_type}.csv", filetypes=[("CSV", "*.csv")])
        if not filepath: return
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            for row in template: writer.writerow(row)
        show_info(self.app, t("complete"), t("msg_template_created", path=filepath))

    def _fetch_objects(self):
        """서버에서 오브젝트 불러오기"""
        if not self.app.connected:
            show_warning(self.app, t("warning"), t("msg_connect_first"))
            return

        obj_type = self.obj_type.get()
        # 테이블 초기화
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 진행 상황 콜백
        def on_progress(current, total):
            self.app.set_status(t("msg_fetching", current=current, total=total))

        # API 호출 (페이징 처리)
        self.app.set_status(t("msg_fetching_start"))
        result = self.app.api.show_all_objects(obj_type, on_progress)
        if "objects" not in result:
            show_error(self.app, t("error"), result.get("message", "Failed"))
            self.app.set_status(t("ready"))
            return

        # 결과를 테이블에 표시
        for obj in result["objects"]:
            row = self._parse_object(obj_type, obj)
            self.tree.insert("", "end", values=row)

        self._update_row_count()
        self.app.set_status(t("ready"))
        self.app.log(t("msg_fetched", count=len(result["objects"])), "SUCCESS")

    def _parse_object(self, obj_type: str, obj: dict) -> list:
        """API 응답을 테이블 행으로 변환"""
        if obj_type == "host":
            return [obj.get("name"), obj.get("ipv4-address", ""), obj.get("comments", "")]
        elif obj_type == "network":
            return [obj.get("name"), obj.get("subnet4", ""), obj.get("mask-length4", ""), obj.get("comments", "")]
        elif obj_type == "group":
            members = ";".join([m.get("name", "") for m in obj.get("members", [])])
            return [obj.get("name"), members, obj.get("comments", "")]
        elif obj_type in ("service-tcp", "service-udp"):
            return [obj.get("name"), obj.get("port", ""), obj.get("comments", "")]
        elif obj_type == "address-range":
            return [obj.get("name"), obj.get("ipv4-address-first", ""), obj.get("ipv4-address-last", ""), obj.get("comments", "")]
        elif obj_type == "application-site":
            urls = ";".join(obj.get("url-list", []))
            return [obj.get("name"), urls, obj.get("primary-category", ""), obj.get("description", "")]
        elif obj_type == "dns-domain":
            fqdn_only = "true" if not obj.get("is-sub-domain", False) else "false"
            return [obj.get("name"), fqdn_only, obj.get("comments", "")]
        return [obj.get("name", "")]
    
    def _start_import(self):
        if self.app.is_running: return
        if not self.app.connected and not self.chk_dry.get():
            show_warning(self.app, t("warning"), t("msg_connect_first")); return
        if not self.tree.get_children():
            show_warning(self.app, t("warning"), t("msg_no_data")); return
        self.app.is_running = True
        threading.Thread(target=self._run_import, daemon=True).start()
    
    def _run_import(self):
        try:
            obj_type = self.obj_type.get()
            update_mode = self.chk_update.get()
            dry_run = self.chk_dry.get()
            
            self.app.log(t("log_import_start", type=obj_type), "STEP")
            self.app.set_status(t("log_import_start", type=obj_type))
            if dry_run: self.app.log(t("log_test_mode"), "WARNING")
            
            success, skip, fail = 0, 0, 0
            items = self.tree.get_children()
            
            for i, item in enumerate(items):
                row = [str(v).strip() for v in self.tree.item(item)["values"]]
                if not row or not row[0]: continue
                self.app.set_status(t("log_importing", current=i+1, total=len(items), name=row[0]))
                result = self._do_import(obj_type, row, update_mode, dry_run)
                if result == "success": success += 1; self.app.log(t("log_created", name=row[0]), "SUCCESS")
                elif result == "updated": success += 1; self.app.log(t("log_updated", name=row[0]), "SUCCESS")
                elif result == "skipped": skip += 1; self.app.log(t("log_skipped", name=row[0]), "WARNING")
                else: fail += 1; self.app.log(t("log_failed_item", name=row[0], error=result), "ERROR")
            
            level = "SUCCESS" if fail == 0 else "WARNING"
            self.app.log(t("log_complete", success=success, skip=skip, fail=fail), level)
            
            if not dry_run and self.chk_publish.get() and success > 0:
                self.app.log(t("log_publishing"), "STEP")
                self.app.set_status(t("log_publishing"))
                result = self.app.api.publish()
                if "task-id" in result: self.app.log(t("log_published"), "SUCCESS")
                else: self.app.log(t("log_publish_failed", msg=result.get('message')), "ERROR")
            
            self.app.set_status(t("log_import_complete"))
        finally:
            self.app.is_running = False
    
    def _mask_to_cidr(self, mask_str):
        """Convert subnet mask string to CIDR notation (e.g., 255.255.255.0 -> 24)"""
        try:
            octets = mask_str.strip().split(".")
            binary = "".join(format(int(o), "08b") for o in octets)
            return binary.count("1")
        except:
            return 24  # Default fallback
    
    def _do_import(self, obj_type, row, update_mode, dry_run):
        name = row[0]
        if obj_type in ("service-tcp", "service-udp") and name and name[0].isdigit():
            return "Name cannot start with digit"
        if dry_run: return "success"
        
        check = self.app.api.show_object(obj_type, name)
        exists = "uid" in check
        if exists and not update_mode: return "skipped"
        
        if obj_type == "host":
            ip, comments = row[1] if len(row) > 1 else "", row[2] if len(row) > 2 else ""
            r = self.app.api.set_host(name, ip, comments) if exists else self.app.api.add_host(name, ip, comments)
        elif obj_type == "network":
            subnet = row[1] if len(row) > 1 else ""
            mask_str = row[2] if len(row) > 2 and row[2] else "24"
            # Convert subnet mask to CIDR if needed (e.g., 255.255.255.0 -> 24)
            if "." in str(mask_str):
                mask = self._mask_to_cidr(mask_str)
            else:
                mask = int(mask_str)
            comments = row[3] if len(row) > 3 else ""
            r = self.app.api.set_network(name, subnet, mask, comments) if exists else self.app.api.add_network(name, subnet, mask, comments)
        elif obj_type == "group":
            members = [x.strip() for x in (row[1] if len(row) > 1 else "").split(";") if x.strip()]
            comments = row[2] if len(row) > 2 else ""
            r = self.app.api.add_group(name, members, comments)
        elif obj_type == "service-tcp":
            port, comments = row[1] if len(row) > 1 else "", row[2] if len(row) > 2 else ""
            r = self.app.api.add_service_tcp(name, port, comments)
        elif obj_type == "service-udp":
            port, comments = row[1] if len(row) > 1 else "", row[2] if len(row) > 2 else ""
            r = self.app.api.add_service_udp(name, port, comments)
        elif obj_type == "address-range":
            first, last = row[1] if len(row) > 1 else "", row[2] if len(row) > 2 else ""
            comments = row[3] if len(row) > 3 else ""
            r = self.app.api.add_address_range(name, first, last, comments)
        elif obj_type == "application-site":
            urls = [x.strip() for x in (row[1] if len(row) > 1 else "").split(";") if x.strip()]
            if not urls: return "URL list required"
            category = row[2] if len(row) > 2 else ""
            desc = row[3] if len(row) > 3 else ""
            r = self.app.api.add_application_site(name, urls, category, desc)
        elif obj_type == "dns-domain":
            fqdn_only = (row[1] if len(row) > 1 else "true").lower() == "true"
            is_sub = not fqdn_only  # FQDN전용=true면 is-sub-domain=false
            comments = row[2] if len(row) > 2 else ""
            r = self.app.api.set_dns_domain(name, is_sub, comments) if exists else self.app.api.add_dns_domain(name, is_sub, comments)
        else:
            return "Unknown type"
        
        return ("updated" if exists else "success") if "uid" in r else r.get("message", "Error")
