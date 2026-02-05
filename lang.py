"""
CheckPoint Management Toolkit - 다국어 지원
"""

LANG = {
    "ko": {
        # 앱
        "app_title": "CheckPoint 관리 도구 v3.7",
        "app_subtitle": "현대오토에버 보안팀",
        
        # 헤더
        "server": "서버:",
        "port": "포트:",
        "user": "사용자:",
        "password": "비밀번호:",
        "domain": "도메인:",
        "domain_hint": "선택사항",
        "connect": "연결",
        "disconnect": "해제",
        "connected": "연결됨",
        "disconnected": "연결 안됨",
        "connecting": "연결 중...",
        
        # 사이드바
        "menu": "메뉴",
        "menu_import": "📦 대량 등록",
        "menu_policy": "📋 벌크 정책",
        "menu_zone": "🔐 Zone 정책",
        "menu_gaia": "🖥️ GAIA 관리",
        
        # 대량 등록 탭
        "object_type": "오브젝트 타입",
        "format": "형식:",
        "load_csv": "CSV 불러오기",
        "add": "+ 추가",
        "edit": "편집",
        "delete": "삭제",
        "save_csv": "CSV 저장",
        "template": "템플릿",
        "file": "파일:",
        "update_existing": "기존 오브젝트 업데이트",
        "test_mode": "테스트 모드",
        "auto_publish": "자동 게시",
        "row_count": "행:",
        "start_import": "▶ 등록 시작",
        
        # 벌크 정책 탭
        "policy_package": "정책 패키지",
        "package": "패키지:",
        "verify": "확인",
        "bulk_policy": "벌크 정책 생성",
        "policy_format": "형식: 섹션, 룰이름, 소스, 목적지, 서비스, 액션(Accept/Drop/inline), 트랙, 인라인레이어, 소스부정(;구분), 목적지부정(;구분), 위치, 설명",
        "auto_create_zones": "Zone 자동 생성",
        "auto_create_layers": "Layer 자동 생성",
        "msg_verify_package_first": "먼저 패키지를 확인하세요",
        "msg_confirm_generate_policy": "{count}개 정책을 생성하시겠습니까?",
        "log_creating_rules": "룰 생성 중...",
        "generate": "▶ 생성",
        
        # 로그 패널
        "log_title": "📋 실시간 로그",
        "clear": "지우기",
        "ready": "준비",
        
        # 다이얼로그
        "warning": "경고",
        "error": "오류",
        "confirm": "확인",
        "complete": "완료",
        "yes": "예",
        "no": "아니오",
        "save": "저장",
        "cancel": "취소",
        "close": "닫기",
        "add_row": "행 추가",
        "edit_row": "행 편집",
        "position": "위치:",
        "position_hint": "예: 61",
        "multi_value_hint": "※ 여러 값은 세미콜론(;)으로 구분",
        
        # 메시지
        "msg_fill_required": "필수 항목을 모두 입력하세요",
        "msg_connect_first": "먼저 서버에 연결하세요",
        "msg_no_data": "등록할 데이터가 없습니다",
        "msg_no_save_data": "저장할 데이터가 없습니다",
        "msg_select_row_edit": "편집할 행을 선택하세요",
        "msg_select_row_delete": "삭제할 행을 선택하세요",
        "msg_confirm_delete": "선택한 행을 삭제하시겠습니까?",
        "msg_confirm_exit": "연결을 해제하고 종료하시겠습니까?",
        "msg_task_running": "작업이 진행 중입니다.",
        "msg_enter_package": "패키지 이름을 입력하세요",
        "msg_package_exists": "패키지 '{name}'이(가) 존재합니다",
        "msg_package_not_found": "패키지 '{name}'을(를) 찾을 수 없습니다",
        "msg_confirm_generate": "정책을 생성하시겠습니까?\n\n기본: {base}\n타입: {type}\n환경: {envs}",
        "msg_policy_complete": "정책 생성이 완료되었습니다!",
        "msg_saved": "저장됨: {path}",
        "msg_template_created": "템플릿: {path}",
        "msg_rows_loaded": "{count}개 행 로드됨",
        
        # 로그 메시지
        "log_connecting": "{server}:{port}에 연결 중...",
        "log_connected": "연결 성공!",
        "log_disconnected": "연결 해제됨",
        "log_failed": "실패: {msg}",
        "log_import_start": "{type} 등록 시작...",
        "log_importing": "등록 중 {current}/{total}: {name}",
        "log_created": "  ✓ 생성됨: {name}",
        "log_updated": "  ✓ 업데이트됨: {name}",
        "log_skipped": "  - 건너뜀: {name}",
        "log_failed_item": "  ✗ 실패: {name} - {error}",
        "log_complete": "완료! 성공:{success} 건너뜀:{skip} 실패:{fail}",
        "log_publishing": "게시 중...",
        "log_published": "게시 완료!",
        "log_publish_failed": "게시 실패: {msg}",
        "log_import_complete": "등록 완료",
        "log_test_mode": "[테스트 모드]",
        "log_checking": "확인 중: {name}...",
        "log_package_confirmed": "패키지 '{name}' 확인됨!",
        "log_not_found": "찾을 수 없음: {msg}",
        "log_policy_start": "정책 생성 시작",
        "log_creating_zones": "Zone 생성 중...",
        "log_zone_created": "  ✓ {name}",
        "log_zone_failed": "  ✗ {name}",
        "log_section": "섹션: {name}",
        "log_policy_complete": "정책 생성 완료!",
        "log_error": "오류: {msg}",
        
        # 컬럼
        "col_name": "이름",
        "col_ip": "IP주소",
        "col_desc": "설명",
        "col_subnet": "서브넷",
        "col_mask": "마스크",
        "col_members": "멤버",
        "col_port": "포트",
        "col_start_ip": "시작IP",
        "col_end_ip": "종료IP",
        "col_urls": "URL목록",
        "col_category": "카테고리",

        # Export 기능
        "fetch_server": "서버에서 불러오기",
        "msg_fetching_start": "오브젝트 조회 중...",
        "msg_fetching": "불러오는 중... {current}/{total}",
        "msg_fetched": "{count}개 오브젝트 불러옴",
    },
    
    "en": {
        # App
        "app_title": "CheckPoint Management Tool v3.7",
        "app_subtitle": "Bulk Object & Policy Manager",
        
        # Header
        "server": "Server:",
        "port": "Port:",
        "user": "User:",
        "password": "Password:",
        "domain": "Domain:",
        "domain_hint": "Optional",
        "connect": "Connect",
        "disconnect": "Disconnect",
        "connected": "Connected",
        "disconnected": "Disconnected",
        "connecting": "Connecting...",
        
        # Sidebar
        "menu": "Menu",
        "menu_import": "📦 Bulk Import",
        "menu_policy": "📋 Bulk Policy",
        "menu_zone": "🔐 Zone Policy",
        "menu_gaia": "🖥️ GAIA Mgmt",
        
        # Import Tab
        "object_type": "Object Type",
        "format": "Format:",
        "load_csv": "Load CSV",
        "add": "+ Add",
        "edit": "Edit",
        "delete": "Delete",
        "save_csv": "Save CSV",
        "template": "Template",
        "file": "File:",
        "update_existing": "Update existing objects",
        "test_mode": "Test mode",
        "auto_publish": "Auto publish",
        "row_count": "Rows:",
        "start_import": "▶ Start Import",
        
        # Policy Tab
        "policy_package": "Policy Package",
        "package": "Package:",
        "verify": "Verify",
        "bulk_policy": "Bulk Policy Generator",
        "policy_format": "Format: Section, RuleName, Source, Destination, Service, Action(Accept/Drop/inline), Track, InlineLayer, NegateSrc(;sep), NegateDst(;sep), Position, Comments",
        "auto_create_zones": "Auto create zones",
        "auto_create_layers": "Auto create layers",
        "msg_verify_package_first": "Please verify package first",
        "msg_confirm_generate_policy": "Generate {count} policies?",
        "log_creating_rules": "Creating rules...",
        "generate": "▶ Generate",
        
        # Log Panel
        "log_title": "📋 Real-time Log",
        "clear": "Clear",
        "ready": "Ready",
        
        # Dialogs
        "warning": "Warning",
        "error": "Error",
        "confirm": "Confirm",
        "complete": "Complete",
        "yes": "Yes",
        "no": "No",
        "save": "Save",
        "cancel": "Cancel",
        "close": "Close",
        "add_row": "Add Row",
        "edit_row": "Edit Row",
        "position": "Position:",
        "position_hint": "e.g. 61",
        "multi_value_hint": "※ Multiple values separated by semicolon(;)",
        
        # Messages
        "msg_fill_required": "Please fill in all required fields",
        "msg_connect_first": "Please connect to server first",
        "msg_no_data": "No data to import",
        "msg_no_save_data": "No data to save",
        "msg_select_row_edit": "Please select a row to edit",
        "msg_select_row_delete": "Please select a row to delete",
        "msg_confirm_delete": "Delete selected row?",
        "msg_confirm_exit": "Disconnect and exit?",
        "msg_task_running": "Task is running.",
        "msg_enter_package": "Please enter package name",
        "msg_package_exists": "Package '{name}' exists",
        "msg_package_not_found": "Package '{name}' not found",
        "msg_policy_complete": "Policy generation complete!",
        "msg_saved": "Saved: {path}",
        "msg_template_created": "Template: {path}",
        "msg_rows_loaded": "{count} rows loaded",
        
        # Log messages
        "log_connecting": "Connecting to {server}:{port}...",
        "log_connected": "Connected!",
        "log_disconnected": "Disconnected",
        "log_failed": "Failed: {msg}",
        "log_import_start": "Starting {type} import...",
        "log_importing": "Importing {current}/{total}: {name}",
        "log_created": "  ✓ Created: {name}",
        "log_updated": "  ✓ Updated: {name}",
        "log_skipped": "  - Skipped: {name}",
        "log_failed_item": "  ✗ Failed: {name} - {error}",
        "log_complete": "Done! Success:{success} Skipped:{skip} Failed:{fail}",
        "log_publishing": "Publishing...",
        "log_published": "Published!",
        "log_publish_failed": "Publish failed: {msg}",
        "log_import_complete": "Import complete",
        "log_test_mode": "[TEST MODE]",
        "log_checking": "Checking: {name}...",
        "log_package_confirmed": "Package '{name}' confirmed!",
        "log_not_found": "Not found: {msg}",
        "log_policy_start": "Policy generation started",
        "log_creating_zones": "Creating zones...",
        "log_zone_created": "  ✓ {name}",
        "log_zone_failed": "  ✗ {name}",
        "log_section": "Section: {name}",
        "log_policy_complete": "Policy generation complete!",
        "log_error": "Error: {msg}",
        
        # Columns
        "col_name": "Name",
        "col_ip": "IP Address",
        "col_desc": "Description",
        "col_subnet": "Subnet",
        "col_mask": "Mask",
        "col_members": "Members",
        "col_port": "Port",
        "col_start_ip": "Start IP",
        "col_end_ip": "End IP",
        "col_urls": "URL List",
        "col_category": "Category",

        # Export feature
        "fetch_server": "Fetch from Server",
        "msg_fetching_start": "Fetching objects...",
        "msg_fetching": "Fetching... {current}/{total}",
        "msg_fetched": "{count} objects fetched",
    }
}

# 현재 언어
_current_lang = "ko"

def get_lang():
    return _current_lang

def set_lang(lang: str):
    global _current_lang
    if lang in LANG:
        _current_lang = lang

def t(key: str, **kwargs) -> str:
    """번역 텍스트 반환"""
    text = LANG.get(_current_lang, LANG["ko"]).get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except:
            return text
    return text
