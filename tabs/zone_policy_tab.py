"""
CheckPoint 관리 도구 - Zone 정책 탭
Zone 기반 정책 자동 생성 기능 (현대오토에버 전용)
"""

import customtkinter as ctk
from tkinter import messagebox
import threading

from config import BRAND_BERRY
from lang import get_lang
from widgets import IconButton, PositionDialog


class ZonePolicyTab(ctk.CTkFrame):
    """Zone 정책 생성기 탭"""
    
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self._build_package_section()
        self._build_zone_section()
        self._build_info_section()
        self._build_button_section()
    
    def _build_package_section(self):
        frame = ctk.CTkFrame(self, corner_radius=8)
        frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=10)
        
        self.lbl_title = ctk.CTkLabel(inner, text="Zone 정책 생성" if get_lang() == "ko" else "Zone Policy Generator", 
                                       font=ctk.CTkFont(size=12, weight="bold"), text_color=BRAND_BERRY)
        self.lbl_title.pack(anchor="w")
        
        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack(fill="x", pady=(5, 0))
        
        self.lbl_pkg = ctk.CTkLabel(row, text="패키지:" if get_lang() == "ko" else "Package:", font=ctk.CTkFont(size=11))
        self.lbl_pkg.pack(side="left")
        self.package_entry = ctk.CTkEntry(row, width=200, height=28)
        self.package_entry.pack(side="left", padx=10)
        self.package_entry.insert(0, "Standard")
        
        self.btn_verify = IconButton(row, "확인" if get_lang() == "ko" else "Verify", self._verify_package, width=60)
        self.btn_verify.pack(side="left")
    
    def _build_zone_section(self):
        frame = ctk.CTkFrame(self, corner_radius=8)
        frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(fill="x", padx=15, pady=10)
        
        self.lbl_zone = ctk.CTkLabel(inner, text="Zone 설정" if get_lang() == "ko" else "Zone Settings", 
                                      font=ctk.CTkFont(size=12, weight="bold"), text_color=BRAND_BERRY)
        self.lbl_zone.pack(anchor="w")
        
        name_row = ctk.CTkFrame(inner, fg_color="transparent")
        name_row.pack(fill="x", pady=(5, 0))
        self.lbl_base = ctk.CTkLabel(name_row, text="기본 이름:" if get_lang() == "ko" else "Base Name:", 
                                      font=ctk.CTkFont(size=11), width=80)
        self.lbl_base.pack(side="left")
        self.base_name_entry = ctk.CTkEntry(name_row, width=150, height=28, 
                                             placeholder_text="예: CCS, APP" if get_lang() == "ko" else "e.g. CCS, APP")
        self.base_name_entry.pack(side="left", padx=5)
        
        type_row = ctk.CTkFrame(inner, fg_color="transparent")
        type_row.pack(fill="x", pady=(5, 0))
        self.lbl_type = ctk.CTkLabel(type_row, text="Zone 타입:" if get_lang() == "ko" else "Zone Type:", 
                                      font=ctk.CTkFont(size=11), width=80)
        self.lbl_type.pack(side="left")
        
        self.zone_type = ctk.StringVar(value="DMZ")
        self.rb_dmz = ctk.CTkRadioButton(type_row, text="DMZ (internet_DMZ, gs_dc_dmz)", 
                                          variable=self.zone_type, value="DMZ", 
                                          font=ctk.CTkFont(size=11), fg_color=BRAND_BERRY)
        self.rb_dmz.pack(side="left", padx=5)
        self.rb_int = ctk.CTkRadioButton(type_row, text="INT (internet_INT, gs_dc_int)", 
                                          variable=self.zone_type, value="INT", 
                                          font=ctk.CTkFont(size=11), fg_color=BRAND_BERRY)
        self.rb_int.pack(side="left", padx=15)
        
        env_row = ctk.CTkFrame(inner, fg_color="transparent")
        env_row.pack(fill="x", pady=(5, 0))
        self.lbl_env = ctk.CTkLabel(env_row, text="환경:" if get_lang() == "ko" else "Environment:", 
                                     font=ctk.CTkFont(size=11), width=80)
        self.lbl_env.pack(side="left")
        
        self.env_prd = ctk.CTkCheckBox(env_row, text="prd (운영)" if get_lang() == "ko" else "prd (Prod)", 
                                        font=ctk.CTkFont(size=11), fg_color=BRAND_BERRY)
        self.env_prd.select()
        self.env_prd.pack(side="left", padx=5)
        self.env_dev = ctk.CTkCheckBox(env_row, text="dev (개발)" if get_lang() == "ko" else "dev (Dev)", 
                                        font=ctk.CTkFont(size=11), fg_color=BRAND_BERRY)
        self.env_dev.pack(side="left", padx=10)
        self.env_stg = ctk.CTkCheckBox(env_row, text="stg (스테이징)" if get_lang() == "ko" else "stg (Stg)", 
                                        font=ctk.CTkFont(size=11), fg_color=BRAND_BERRY)
        self.env_stg.pack(side="left", padx=10)
    
    def _build_info_section(self):
        frame = ctk.CTkFrame(self, corner_radius=8)
        frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        info_ko = """💡 생성 버튼 클릭 시 섹션 위치를 묻습니다.
• SmartConsole에서 Cleanup 룰 번호 확인
• 삽입할 위치의 룰 번호 입력 (예: Cleanup이 #61이면 61)
• Inbound 생성 후 Outbound 위치 재확인"""
        info_en = """💡 You will be asked for section position when clicking Generate.
• Check Cleanup rule number in SmartConsole
• Enter rule number for insertion (e.g. 61 if Cleanup is #61)
• After Inbound, you'll be asked for Outbound position"""
        
        self.info_label = ctk.CTkLabel(frame, text=info_ko if get_lang() == "ko" else info_en,
                                        font=ctk.CTkFont(size=11), text_color="#B0B0B0", justify="left")
        self.info_label.pack(padx=15, pady=10, anchor="w")
    
    def _build_button_section(self):
        frame = ctk.CTkFrame(self, corner_radius=8)
        frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(5, 10))
        inner = ctk.CTkFrame(frame, fg_color="transparent")
        inner.pack(padx=15, pady=10)
        
        self.generate_btn = IconButton(inner, "▶ 생성" if get_lang() == "ko" else "▶ Generate", 
                                        self._start_generate, "success", 80)
        self.generate_btn.pack(side="left", padx=5)
        self.generate_btn.configure(state="disabled")
        
        self.preview_btn = IconButton(inner, "미리보기" if get_lang() == "ko" else "Preview", 
                                       self._preview, "secondary", 80)
        self.preview_btn.pack(side="left", padx=5)
    
    def refresh_lang(self):
        lang = get_lang()
        self.lbl_title.configure(text="Zone 정책 생성" if lang == "ko" else "Zone Policy Generator")
        self.lbl_pkg.configure(text="패키지:" if lang == "ko" else "Package:")
        self.btn_verify.configure(text="확인" if lang == "ko" else "Verify")
        self.lbl_zone.configure(text="Zone 설정" if lang == "ko" else "Zone Settings")
        self.lbl_base.configure(text="기본 이름:" if lang == "ko" else "Base Name:")
        self.base_name_entry.configure(placeholder_text="예: CCS, APP" if lang == "ko" else "e.g. CCS, APP")
        self.lbl_type.configure(text="Zone 타입:" if lang == "ko" else "Zone Type:")
        self.lbl_env.configure(text="환경:" if lang == "ko" else "Environment:")
        self.env_prd.configure(text="prd (운영)" if lang == "ko" else "prd (Prod)")
        self.env_dev.configure(text="dev (개발)" if lang == "ko" else "dev (Dev)")
        self.env_stg.configure(text="stg (스테이징)" if lang == "ko" else "stg (Stg)")
        
        info_ko = """💡 생성 버튼 클릭 시 섹션 위치를 묻습니다.
• SmartConsole에서 Cleanup 룰 번호 확인
• 삽입할 위치의 룰 번호 입력 (예: Cleanup이 #61이면 61)
• Inbound 생성 후 Outbound 위치 재확인"""
        info_en = """💡 You will be asked for section position when clicking Generate.
• Check Cleanup rule number in SmartConsole
• Enter rule number for insertion (e.g. 61 if Cleanup is #61)
• After Inbound, you'll be asked for Outbound position"""
        self.info_label.configure(text=info_ko if lang == "ko" else info_en)
        
        self.generate_btn.configure(text="▶ 생성" if lang == "ko" else "▶ Generate")
        self.preview_btn.configure(text="미리보기" if lang == "ko" else "Preview")
    
    def set_generate_enabled(self, enabled):
        self.generate_btn.configure(state="normal" if enabled else "disabled")
    
    def _get_environments(self):
        return [e for e, c in [("prd", self.env_prd), ("dev", self.env_dev), ("stg", self.env_stg)] if c.get()]
    
    def _get_source_zones(self):
        return ["internet_DMZ", "gs_dc_dmz"] if self.zone_type.get() == "DMZ" else ["internet_INT", "gs_dc_int"]
    
    def _verify_package(self):
        lang = get_lang()
        if not self.app.connected:
            messagebox.showwarning("경고" if lang == "ko" else "Warning", 
                                   "먼저 서버에 연결하세요" if lang == "ko" else "Connect first")
            return
        name = self.package_entry.get().strip()
        if not name:
            messagebox.showwarning("경고" if lang == "ko" else "Warning", 
                                   "패키지명 입력" if lang == "ko" else "Enter package")
            return
        
        self.app.log(f"확인 중: {name}..." if lang == "ko" else f"Checking: {name}...", "STEP")
        r = self.app.api.show_package(name)
        if "uid" in r:
            self.app.log(f"'{name}' 확인됨!" if lang == "ko" else f"'{name}' OK!", "SUCCESS")
            messagebox.showinfo("확인" if lang == "ko" else "OK", f"'{name}' OK")
        else:
            self.app.log(f"없음: {r.get('message')}" if lang == "ko" else f"Not found: {r.get('message')}", "ERROR")
            messagebox.showerror("오류" if lang == "ko" else "Error", f"'{name}' not found")
    
    def _preview(self):
        lang = get_lang()
        base, envs = self.base_name_entry.get().strip(), self._get_environments()
        if not base:
            messagebox.showwarning("경고" if lang == "ko" else "Warning", 
                                   "기본 이름 입력" if lang == "ko" else "Enter base name")
            return
        if not envs:
            messagebox.showwarning("경고" if lang == "ko" else "Warning", 
                                   "환경 선택" if lang == "ko" else "Select env")
            return
        
        zt, src = self.zone_type.get(), self._get_source_zones()
        txt = f"=== {'미리보기' if lang == 'ko' else 'Preview'} ===\n"
        txt += f"{'기본' if lang == 'ko' else 'Base'}: {base}\n"
        txt += f"{'타입' if lang == 'ko' else 'Type'}: {zt}\n"
        txt += f"{'환경' if lang == 'ko' else 'Env'}: {envs}\n"
        txt += f"{'소스' if lang == 'ko' else 'Source'}: {src}\n\n"
        
        txt += f"=== Zone ===\n"
        for e in envs:
            txt += f"  {base.lower()}_{zt.lower()}_{e}\n"
        
        txt += f"\n=== {base}_Inbound ===\n"
        for e in envs:
            txt += f"  {src[0]} → {base.lower()}_{zt.lower()}_{e}\n"
        for e in envs:
            txt += f"  {src[1]} → {base.lower()}_{zt.lower()}_{e}\n"
        for e in envs:
            txt += f"  Any(Neg) → {base.lower()}_{zt.lower()}_{e}\n"
        
        txt += f"\n=== {base}_Outbound ===\n"
        for e in envs:
            txt += f"  {base.lower()}_{zt.lower()}_{e} → {src[0]}\n"
        for e in envs:
            txt += f"  {base.lower()}_{zt.lower()}_{e} → {src[1]}\n"
        for e in envs:
            txt += f"  {base.lower()}_{zt.lower()}_{e} → Any(Neg)\n"
        
        win = ctk.CTkToplevel(self)
        win.title("미리보기" if lang == "ko" else "Preview")
        win.geometry("500x500")
        win.after(100, lambda: (win.lift(), win.focus_force()))
        t = ctk.CTkTextbox(win, font=ctk.CTkFont(family="Consolas", size=11))
        t.pack(fill="both", expand=True, padx=10, pady=10)
        t.insert("1.0", txt)
        t.configure(state="disabled")
    
    def _start_generate(self):
        lang = get_lang()
        if self.app.is_running:
            return
        if not self.app.connected:
            messagebox.showwarning("경고" if lang == "ko" else "Warning", "연결 필요" if lang == "ko" else "Connect first")
            return
        
        base, envs = self.base_name_entry.get().strip(), self._get_environments()
        if not base:
            messagebox.showwarning("경고" if lang == "ko" else "Warning", "기본 이름 입력" if lang == "ko" else "Enter base name")
            return
        if not envs:
            messagebox.showwarning("경고" if lang == "ko" else "Warning", "환경 선택" if lang == "ko" else "Select env")
            return
        
        d = PositionDialog(self, "Inbound 위치" if lang == "ko" else "Inbound Position", 
                           "룰 번호 입력 (빈칸: 맨 아래)" if lang == "ko" else "Rule number (empty: bottom)")
        self.wait_window(d)
        if d.result is None:
            return
        
        if not messagebox.askyesno("확인" if lang == "ko" else "Confirm",
            f"정책 생성?\n\n기본: {base}\n타입: {self.zone_type.get()}\n환경: {envs}" if lang == "ko" else 
            f"Generate?\n\nBase: {base}\nType: {self.zone_type.get()}\nEnv: {envs}"):
            return
        
        self.app.is_running = True
        threading.Thread(target=self._run_generate, args=(base, envs, d.result), daemon=True).start()
    
    def _run_generate(self, base, envs, in_pos):
        lang = get_lang()
        try:
            zt, pkg, src = self.zone_type.get(), self.package_entry.get().strip(), self._get_source_zones()
            
            self.app.log("=" * 40, "INFO")
            self.app.log("정책 생성 시작" if lang == "ko" else "Starting", "STEP")
            self.app.log(f"패키지: {pkg}" if lang == "ko" else f"Package: {pkg}", "STEP")
            
            r = self.app.api.show_package(pkg)
            if "uid" not in r:
                self.app.log("패키지 없음!" if lang == "ko" else "Package not found!", "ERROR")
                return
            
            layers = r.get("access-layers", [])
            layer = layers[0].get("uid") if layers else f"{pkg} Network"
            self.app.log(f"레이어: {layer}" if lang == "ko" else f"Layer: {layer}", "INFO")
            
            self.app.log("Zone 생성 중..." if lang == "ko" else "Creating zones...", "STEP")
            for z in src:
                if "uid" not in self.app.api.show_security_zone(z):
                    if "uid" in self.app.api.add_security_zone(z):
                        self.app.log(f"  ✓ {z}", "SUCCESS")
                else:
                    self.app.log(f"  - {z} 존재" if lang == "ko" else f"  - {z} exists", "WARNING")
            
            for e in envs:
                z = f"{base.lower()}_{zt.lower()}_{e}"
                if "uid" not in self.app.api.show_security_zone(z):
                    if "uid" in self.app.api.add_security_zone(z):
                        self.app.log(f"  ✓ {z}", "SUCCESS")
                else:
                    self.app.log(f"  - {z} 존재" if lang == "ko" else f"  - {z} exists", "WARNING")
            
            sec_in = f"{base}_Inbound"
            self.app.log(f"섹션: {sec_in}" if lang == "ko" else f"Section: {sec_in}", "STEP")
            sec_in_result = self.app.api.add_access_section(layer, sec_in, in_pos)
            if "uid" in sec_in_result:
                self.app.log(f"  ✓ 섹션 생성됨" if lang == "ko" else f"  ✓ Section created", "SUCCESS")
            else:
                # Check if section already exists
                if "already exists" in sec_in_result.get("message", "").lower() or "Object already exists" in sec_in_result.get("message", ""):
                    self.app.log(f"  → 기존 섹션 사용" if lang == "ko" else f"  → Using existing section", "WARNING")
                else:
                    self.app.log(f"  ✗ 섹션 생성 실패: {sec_in_result.get('message', 'Error')}" if lang == "ko" else f"  ✗ Section failed: {sec_in_result.get('message', 'Error')}", "ERROR")
                    return
            
            self.app.log("Inbound 룰..." if lang == "ko" else "Inbound rules...", "STEP")
            
            # 룰 생성 - 섹션 이름으로 position.below 사용
            for e in envs:
                dst, inline_name = f"{base.lower()}_{zt.lower()}_{e}", f"any_to_{base.lower()}_{zt.lower()}_{e}"
                inline_uid = self._create_layer(inline_name)
                r = self.app.api.add_access_rule(layer, sec_in, "Any", dst, inline_uid)
                if "uid" in r:
                    self.app.api.set_rule_negate_source(r["uid"], layer, src)
                    self.app.log(f"  ✓ Any(Neg)→{dst}", "SUCCESS")
                else:
                    self.app.log(f"  ✗ Any(Neg)→{dst}: {r.get('message', 'Error')}", "ERROR")
            
            for e in envs:
                dst, inline_name = f"{base.lower()}_{zt.lower()}_{e}", f"{src[1]}_to_{base.lower()}_{zt.lower()}_{e}"
                inline_uid = self._create_layer(inline_name)
                r = self.app.api.add_access_rule(layer, sec_in, src[1], dst, inline_uid)
                if "uid" in r:
                    self.app.log(f"  ✓ {src[1]}→{dst}", "SUCCESS")
                else:
                    self.app.log(f"  ✗ {src[1]}→{dst}: {r.get('message', 'Error')}", "ERROR")
            
            for e in envs:
                dst, inline_name = f"{base.lower()}_{zt.lower()}_{e}", f"{src[0].split('_')[0]}_to_{base.lower()}_{zt.lower()}_{e}"
                inline_uid = self._create_layer(inline_name)
                r = self.app.api.add_access_rule(layer, sec_in, src[0], dst, inline_uid)
                if "uid" in r:
                    self.app.log(f"  ✓ {src[0]}→{dst}", "SUCCESS")
                else:
                    self.app.log(f"  ✗ {src[0]}→{dst}: {r.get('message', 'Error')}", "ERROR")
            
            self.app.log("Inbound 완료!" if lang == "ko" else "Inbound done!", "SUCCESS")
            
            self._evt1 = threading.Event()
            self.after(0, self._ask_pub1)
            self._evt1.wait()
            if self._pub1:
                self.app.log("게시 중..." if lang == "ko" else "Publishing...", "STEP")
                if "task-id" in self.app.api.publish():
                    self.app.log("게시 완료!" if lang == "ko" else "Published!", "SUCCESS")
            
            self._evt2 = threading.Event()
            self.after(0, self._ask_out_pos)
            self._evt2.wait()
            if self._out_pos is None:
                self.app.log("Outbound 취소" if lang == "ko" else "Outbound cancelled", "WARNING")
                return
            
            sec_out = f"{base}_Outbound"
            self.app.log(f"섹션: {sec_out}" if lang == "ko" else f"Section: {sec_out}", "STEP")
            sec_out_result = self.app.api.add_access_section(layer, sec_out, self._out_pos)
            if "uid" in sec_out_result:
                self.app.log(f"  ✓ 섹션 생성됨" if lang == "ko" else f"  ✓ Section created", "SUCCESS")
            else:
                if "already exists" in sec_out_result.get("message", "").lower() or "Object already exists" in sec_out_result.get("message", ""):
                    self.app.log(f"  → 기존 섹션 사용" if lang == "ko" else f"  → Using existing section", "WARNING")
                else:
                    self.app.log(f"  ✗ 섹션 생성 실패: {sec_out_result.get('message', 'Error')}" if lang == "ko" else f"  ✗ Section failed: {sec_out_result.get('message', 'Error')}", "ERROR")
                    return
            
            self.app.log("Outbound 룰..." if lang == "ko" else "Outbound rules...", "STEP")
            
            for e in envs:
                s, inline_name = f"{base.lower()}_{zt.lower()}_{e}", f"{base.lower()}_{zt.lower()}_{e}_to_any"
                inline_uid = self._create_layer(inline_name)
                r = self.app.api.add_access_rule(layer, sec_out, s, "Any", inline_uid)
                if "uid" in r:
                    self.app.api.set_rule_negate_destination(r["uid"], layer, src)
                    self.app.log(f"  ✓ {s}→Any(Neg)", "SUCCESS")
                else:
                    self.app.log(f"  ✗ {s}→Any(Neg): {r.get('message', 'Error')}", "ERROR")
            
            for e in envs:
                s, inline_name = f"{base.lower()}_{zt.lower()}_{e}", f"{base.lower()}_{zt.lower()}_{e}_to_{src[1]}"
                inline_uid = self._create_layer(inline_name)
                r = self.app.api.add_access_rule(layer, sec_out, s, src[1], inline_uid)
                if "uid" in r:
                    self.app.log(f"  ✓ {s}→{src[1]}", "SUCCESS")
                else:
                    self.app.log(f"  ✗ {s}→{src[1]}: {r.get('message', 'Error')}", "ERROR")
            
            for e in envs:
                s, inline_name = f"{base.lower()}_{zt.lower()}_{e}", f"{base.lower()}_{zt.lower()}_{e}_to_{src[0].split('_')[0]}"
                inline_uid = self._create_layer(inline_name)
                r = self.app.api.add_access_rule(layer, sec_out, s, src[0], inline_uid)
                if "uid" in r:
                    self.app.log(f"  ✓ {s}→{src[0]}", "SUCCESS")
                else:
                    self.app.log(f"  ✗ {s}→{src[0]}: {r.get('message', 'Error')}", "ERROR")
            
            self.app.log("Outbound 완료!" if lang == "ko" else "Outbound done!", "SUCCESS")
            
            self._evt3 = threading.Event()
            self.after(0, self._ask_pub2)
            self._evt3.wait()
            if self._pub2:
                self.app.log("게시 중..." if lang == "ko" else "Publishing...", "STEP")
                if "task-id" in self.app.api.publish():
                    self.app.log("게시 완료!" if lang == "ko" else "Published!", "SUCCESS")
            
            self.app.log("=" * 40, "INFO")
            self.app.log("정책 생성 완료!" if lang == "ko" else "Complete!", "SUCCESS")
            self.after(0, lambda: messagebox.showinfo("완료" if lang == "ko" else "Done", 
                                                       "정책 생성 완료!" if lang == "ko" else "Policy created!"))
            
        except Exception as e:
            self.app.log(f"오류: {e}" if lang == "ko" else f"Error: {e}", "ERROR")
        finally:
            self.app.is_running = False
    
    def _create_layer(self, name):
        """Create inline layer and return UID"""
        check = self.app.api.show_access_layer(name)
        if "uid" in check:
            return check["uid"]
        
        result = self.app.api.add_access_layer(name)
        if "uid" in result:
            self.app.api.set_cleanup_rule(name)
            self.app.api.set_access_layer(name)
            return result["uid"]
        else:
            self.app.log(f"  → Layer 생성 실패: {name} - {result.get('message', 'Error')}", "ERROR")
        return name  # fallback to name
    
    def _find_section_uid(self, layer, section_name):
        """Find existing section UID by name"""
        try:
            result = self.app.api.show_access_rulebase(layer)
            if "rulebase" in result:
                for item in result["rulebase"]:
                    if item.get("type") == "access-section" and item.get("name") == section_name:
                        return item.get("uid")
        except:
            pass
        return None
    
    def _ask_pub1(self):
        lang = get_lang()
        self._pub1 = messagebox.askyesno("게시" if lang == "ko" else "Publish", 
                                          "Inbound 게시?" if lang == "ko" else "Publish Inbound?")
        self._evt1.set()
    
    def _ask_out_pos(self):
        lang = get_lang()
        d = PositionDialog(self, "Outbound 위치" if lang == "ko" else "Outbound Position",
                           "룰 번호 (빈칸: 맨 아래)" if lang == "ko" else "Rule number (empty: bottom)")
        self.wait_window(d)
        self._out_pos = d.result
        self._evt2.set()
    
    def _ask_pub2(self):
        lang = get_lang()
        self._pub2 = messagebox.askyesno("게시" if lang == "ko" else "Publish", 
                                          "Outbound 게시?" if lang == "ko" else "Publish Outbound?")
        self._evt3.set()
