# CheckPoint Management Toolkit v3.5 (Stable) 인수인계 분석서

> **작성일:** 2026-02-05  
> **작성자:** 남기완 (보안팀)  
> **대상:** 후임 인프라/보안 엔지니어  
> **버전:** v3.5-stable (CustomTkinter 기반)

---

## 1. 개요

### 1.1 도구 목적
CheckPoint 방화벽 Management API를 활용하여 오브젝트 및 정책을 대량으로 생성하는 GUI 자동화 도구입니다. 현대오토에버 보안팀의 CheckPoint 운영 업무 효율화를 위해 자체 개발되었습니다.

### 1.2 핵심 기능 (3개 탭)

| 탭 | 기능 | 설명 |
|---|------|------|
| 📦 대량 등록 (ImportTab) | 오브젝트 벌크 생성 | Host, Network, Group, Service 등 7종 오브젝트를 CSV로 대량 등록 |
| 📋 벌크 정책 (PolicyTab) | Access Rule 대량 생성 | CSV 기반 Access Rule을 지정 레이어/위치에 벌크 삽입 |
| 🔐 Zone 정책 (ZonePolicyTab) | Zone 아키텍처 자동 구축 | Zone 오브젝트, Inline Layer, Section, Zone-to-Zone 룰 자동 생성 |

### 1.3 실행 환경
- **Python:** 3.8 이상
- **의존성:** `customtkinter>=5.2.0`, `requests>=2.28.0`
- **OS:** Windows (VDI 환경 사용, 듀얼모니터 DPI 대응)
- **대상 장비:** CheckPoint R82.x Management Server
- **통신:** REST API (`https://<mgmt>:443/web_api`)

---

## 2. 아키텍처

### 2.1 디렉토리 구조
```
checkpoint_toolkit_v3.5-stable/
├── main.py                  # 앱 진입점 + 메인 윈도우 (App 클래스)
├── config.py                # 브랜드 컬러, 앱 설정, 오브젝트 타입 정의
├── lang.py                  # 한/영 다국어 번역 테이블
├── widgets.py               # 공용 위젯 (버튼, 로그패널, 다이얼로그)
├── api/
│   ├── __init__.py          # CheckPointAPI re-export
│   └── management_api.py   # Management API 클라이언트 (REST)
├── tabs/
│   ├── __init__.py          # ImportTab (대량 등록)
│   ├── policy_tab.py        # PolicyTab (벌크 정책)
│   └── zone_policy_tab.py   # ZonePolicyTab (Zone 정책)
├── build.bat                # PyInstaller EXE 빌드 스크립트
├── requirements.txt         # pip 의존성
└── README.md                # 사용 설명서
```

### 2.2 코드 규모
| 파일 | 라인 수 | 역할 |
|------|---------|------|
| main.py | 411 | 메인 윈도우, 연결관리, 페이지 라우팅 |
| config.py | 111 | 설정값, 오브젝트 타입 스키마 |
| lang.py | 297 | 한/영 번역 사전 |
| widgets.py | 192 | IconButton, LogPanel, RowDialog, PositionDialog |
| api/management_api.py | 136 | CheckPoint REST API 래퍼 |
| tabs/__init__.py | 342 | ImportTab (오브젝트 대량 등록) |
| tabs/policy_tab.py | 542 | PolicyTab (Access Rule 벌크 생성) |
| tabs/zone_policy_tab.py | 469 | ZonePolicyTab (Zone 정책 자동화) |
| **합계** | **2,507** | |

### 2.3 모듈 의존성 흐름
```
main.py (App)
  ├── config.py          ← 설정값
  ├── lang.py            ← 다국어
  ├── widgets.py         ← UI 컴포넌트
  ├── api/               ← CheckPoint API 통신
  │   └── management_api.py (CheckPointAPI)
  └── tabs/              ← 기능 탭
      ├── __init__.py    (ImportTab)
      ├── policy_tab.py  (PolicyTab)
      └── zone_policy_tab.py (ZonePolicyTab)
```

---

## 3. 핵심 모듈 분석

### 3.1 `api/management_api.py` - CheckPointAPI 클래스

CheckPoint Management Server와 REST API 통신을 담당합니다. 모든 API 호출은 `_call()` 메서드를 통해 수행됩니다.

**인증 흐름:**
1. `login(user, password, domain)` → SID 발급 → `self.sid` 저장
2. 이후 모든 요청에 `X-chkp-sid` 헤더로 SID 전송
3. 작업 완료 후 `publish()` → `logout()`

**지원 API 목록:**

| 카테고리 | 메서드 | CheckPoint API |
|----------|--------|----------------|
| 인증 | `login()`, `logout()` | login, logout |
| 세션 | `publish()`, `discard()` | publish, discard |
| 오브젝트 | `add_host()`, `add_network()`, `add_group()` | add-host, add-network, add-group |
| 서비스 | `add_service_tcp()`, `add_service_udp()` | add-service-tcp, add-service-udp |
| 범위/앱 | `add_address_range()`, `add_application_site()` | add-address-range, add-application-site |
| Zone | `show/add_security_zone()` | show/add-security-zone |
| 레이어 | `show/add/set_access_layer()` | show/add/set-access-layer |
| 정책 | `add_access_section()`, `add_access_rule()` | add-access-section, add-access-rule |
| Negate | `set_rule_negate_source/destination()` | set-access-rule (negate 옵션) |

**주의사항:**
- `verify=False`: 자체서명 인증서 환경 (운영 환경 기본)
- `timeout=30`: API 응답 대기 30초
- `ignore-warnings: True`: 대부분의 API 호출에 포함 (중복 경고 무시)

### 3.2 `tabs/__init__.py` - ImportTab (대량 등록)

CSV 파일 또는 수동 입력으로 오브젝트를 대량 등록합니다.

**지원 오브젝트 7종:**
- host, network, group, service-tcp, service-udp, address-range, application-site

**작업 플로우:**
1. 오브젝트 타입 선택 (라디오 버튼)
2. CSV 로드 또는 수동 행 추가
3. 테이블에서 데이터 확인/편집
4. `▶ 등록` 클릭 → 백그라운드 스레드에서 순차 API 호출
5. 각 행마다 `add-{type}` API 호출, 결과 로그 출력
6. 완료 후 Publish 여부 확인

**CSV 형식 (예: host)**
```csv
name,ip-address,comments
server-01,10.0.1.10,웹서버
server-02,10.0.1.11,DB서버
```

**특이사항:**
- Group의 members는 세미콜론(`;`) 구분자 사용
- Application-site의 url-list도 세미콜론 구분자
- 오브젝트 존재 시 `set-{type}`으로 업데이트 시도

### 3.3 `tabs/policy_tab.py` - PolicyTab (벌크 정책)

Access Rule을 CSV로 대량 생성합니다.

**CSV 컬럼 (7개):**
```
name, source, destination, service, action, track, comments
```

**특징:**
- 패키지 → 레이어 검증 후 룰 생성 가능
- 삽입 위치 지정: 룰 번호 또는 맨 아래(bottom)
- Source/Destination/Service에 세미콜론(`;`)으로 다중 값 지정 가능
- Action: Accept, Drop, Ask, Inform
- Track: Log, None, Alert, Mail, SNMP, UserDefined

**작업 플로우:**
1. 패키지명 입력 → `Verify` (show-package로 검증)
2. 레이어 선택 (Inline Layer 포함)
3. CSV 로드 또는 수동 입력
4. 삽입 위치 지정 (Position Dialog)
5. 순차 `add-access-rule` 호출
6. Publish

### 3.4 `tabs/zone_policy_tab.py` - ZonePolicyTab (Zone 정책)

현대오토에버 Zone 아키텍처 기반으로 정책 골격을 자동 생성합니다.

**Zone 네이밍 규칙:**
```
{base_name}_{zone_type}_{environment}
예: ccs_dmz_prd, app_int_dev
```

**Zone 타입별 Source Zone:**
| 타입 | Source Zone 1 | Source Zone 2 |
|------|--------------|--------------|
| DMZ | internet_DMZ | gs_dc_dmz |
| INT | internet_INT | gs_dc_int |

**자동 생성 항목:**

1. **Zone 오브젝트**: Source Zone 2개 + Destination Zone (환경별)
2. **Inline Layer**: Zone 조합별로 FW + App Control + URL Filtering 활성화
3. **Section Title**: `{base}_Inbound`, `{base}_Outbound`
4. **Inbound 룰** (역순 생성 - position.below 특성):
   - `internet_DMZ → zone` (Apply Layer)
   - `gs_dc_dmz → zone` (Apply Layer)
   - `Any(Negate) → zone` (Apply Layer)
5. **Outbound 룰** (역순 생성):
   - `zone → internet_DMZ` (Apply Layer)
   - `zone → gs_dc_dmz` (Apply Layer)
   - `zone → Any(Negate)` (Apply Layer)
6. **Cleanup Rule**: 각 Inline Layer 하단에 Drop + Log

**Inbound/Outbound 분리 Publish:**
- Inbound 룰 생성 → Publish 여부 확인 → Outbound 위치 재지정 → Outbound 룰 생성 → Publish
- 이유: Inbound 생성 후 룰 번호가 변경되므로 Outbound 위치를 다시 확인해야 함

### 3.5 `main.py` - App 클래스

**주요 기능:**
- DPI 스케일링 처리 (듀얼모니터 VDI 환경 대응)
- CustomTkinter 자동 DPI 비활성화 (`CTK_SCALING=1.0`)
- 연결 설정 JSON 저장/복원 (`connection_settings.json`)
- 다크/라이트 테마 전환
- 한/영 언어 전환 (런타임)
- 사이드바 페이지 라우팅 (3개 탭)
- 로그 파일 자동 생성 (`cp_YYYYMMDD_HHMMSS.log`)

**연결 관리:**
- 연결 시 `connect_btn` 비활성, `disconnect_btn` 활성
- 각 탭의 실행 버튼 연결 상태에 따라 활성/비활성 제어
- 종료 시 실행 중인 작업 확인 → 연결 해제 → 창 닫기

---

## 4. 운영 가이드

### 4.1 설치 및 실행

**방법 1: Python 직접 실행**
```bash
pip install customtkinter requests
python main.py
```

**방법 2: EXE 빌드**
```bash
build.bat
# 결과: dist/CheckPointToolkit.exe
```

### 4.2 최초 사용

1. 서버 IP, 포트(443), 사용자명, 비밀번호 입력
2. MDS 환경인 경우 도메인(CMA) 입력
3. `연결` 클릭 → 상태 표시등 녹색 확인
4. 원하는 탭 선택 후 작업 수행

### 4.3 자주 사용하는 시나리오

**시나리오 1: 신규 고객 오브젝트 등록**
1. `📦 대량 등록` 탭
2. 오브젝트 타입 선택 (예: host)
3. CSV 로드 또는 수동 입력
4. `▶ 등록` → Publish

**시나리오 2: 신규 Zone 구축 (현대오토에버)**
1. `🔐 Zone 정책` 탭
2. 패키지명 입력 → `확인`
3. 기본 이름(예: CCS), Zone 타입(DMZ/INT), 환경(prd/dev/stg) 설정
4. `미리보기`로 생성될 항목 확인
5. `▶ 생성` → Inbound 위치 입력 → 생성 → Publish
6. SmartConsole에서 Outbound 위치 확인 → 입력 → 생성 → Publish

**시나리오 3: 정책 룰 대량 추가**
1. `📋 벌크 정책` 탭
2. 패키지 검증 → 레이어 선택
3. CSV 로드 (name, source, destination, service, action, track, comments)
4. 삽입 위치 지정 → `▶ 생성` → Publish

### 4.4 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| 로그인 실패 | 인증서 문제 또는 잘못된 자격증명 | 서버 IP, 계정 확인. API 포트(443) 방화벽 허용 확인 |
| 오브젝트 생성 실패 | 이름 중복 또는 잘못된 형식 | 로그에서 에러 메시지 확인. 이름 규칙 준수 |
| Zone 정책 위치 오류 | 룰 번호 변경 | SmartConsole에서 현재 Cleanup 룰 번호 재확인 |
| Publish 실패 | 다른 세션에서 잠금 | SmartConsole에서 다른 세션 discard 후 재시도 |
| GUI 스케일링 이상 | DPI 설정 충돌 | `CTK_SCALING` 환경변수 조정, 또는 디스플레이 배율 100% 설정 |
| MDS 도메인 접속 불가 | 도메인명 오류 | 정확한 CMA 이름 입력 (대소문자 구분) |

---

## 5. 관련 스크립트

이 GUI 도구 외에 CLI 전용 쉘 스크립트도 운영 중입니다.

| 스크립트 | 용도 | 실행 환경 |
|---------|------|----------|
| `checkpoint_bulk_object.sh` | 오브젝트 벌크 생성 (mgmt_cli) | Management Server 직접 |
| `checkpoint_policy_generator.sh` | Zone 정책 자동 생성 (mgmt_cli) | Management Server 직접 |
| `checkpoint_bulk_import.sh` | 오브젝트 벌크 생성 (curl/REST) | 원격 Linux |

**CLI vs GUI 선택 기준:**
- Management Server SSH 접근 가능 → 쉘 스크립트 (mgmt_cli 직접, 더 빠름)
- VDI/원격 PC에서만 작업 → GUI 도구 (REST API, 편의성)

---

## 6. 버전 히스토리 및 실험 버전

### 6.1 Stable vs Experimental

| 항목 | v3.5-stable | v3.5/v3.8-experimental |
|------|-------------|----------------------|
| 프레임워크 | CustomTkinter | PyQt6 |
| 안정성 | 검증 완료 ✅ | 실험 중 ⚠️ |
| DPI 대응 | 수동 설정 필요 | 네이티브 지원 |
| VDI 호환 | 일부 제한 | 개선됨 |
| Zone 정책 | 안정 | 크래시 수정 완료 |

### 6.2 PyQt6 전환 배경
- CustomTkinter의 VDI 듀얼모니터 DPI 스케일링 문제
- CustomTkinter의 느린 렌더링 (대량 데이터 테이블)
- PyQt6의 네이티브 DPI 지원 및 성능 이점

### 6.3 향후 권장사항
1. **운영에는 v3.5-stable 사용** (검증 완료)
2. PyQt6 실험 버전은 추가 테스트 후 전환 검토
3. Zone 정책 생성 시 반드시 `미리보기`로 확인 후 실행
4. 중요 작업 전 SmartConsole에서 백업 권장

---

## 7. CheckPoint API 참고

### 7.1 API 기본 흐름
```
login → [작업들] → publish → logout
```

### 7.2 세션 관리 주의사항
- 동시 세션 수 제한 (기본 100개)
- publish하지 않으면 변경사항 임시 저장 상태 유지
- discard로 임시 변경사항 취소 가능
- 세션 타임아웃: 기본 600초 (10분)

### 7.3 API 문서 위치
- SmartConsole → Help → Management API Reference
- `https://<mgmt>/api_docs`

---

## 8. 연락처 및 참고자료

- **CheckPoint 기술지원:** TAC (Technical Assistance Center)
- **내부 Wiki:** [보안팀 Confluence 페이지 참조]
- **소스 저장소:** git.namgun.or.kr (자체 Git 서버)
