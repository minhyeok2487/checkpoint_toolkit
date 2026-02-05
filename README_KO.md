# CheckPoint Toolkit v3.6 (Stable)

**현대오토에버 보안팀 전용 CheckPoint 방화벽 관리 도구**

CheckPoint Management API 및 GAIA API를 활용하여 오브젝트, 정책, Gateway OS를 관리할 수 있는 Windows GUI 애플리케이션입니다.

---

## 📋 목차

1. [주요 기능](#주요-기능)
2. [시스템 요구사항](#시스템-요구사항)
3. [설치 방법](#설치-방법)
4. [시작하기](#시작하기)
5. [기능별 상세 사용법](#기능별-상세-사용법)
   - [대량 등록 (Bulk Import)](#1-대량-등록-bulk-import)
   - [벌크 정책 (Bulk Policy)](#2-벌크-정책-bulk-policy)
   - [Zone 정책 (Zone Policy)](#3-zone-정책-zone-policy)
   - [GAIA 관리 (GAIA Management)](#4-gaia-관리-gaia-management)
6. [CSV 파일 형식](#csv-파일-형식)
7. [문제 해결](#문제-해결)
8. [버전 히스토리](#버전-히스토리)

---

## 주요 기능

### 📦 대량 등록 (Bulk Import)
- CSV 파일을 통한 오브젝트 대량 등록
- 지원 오브젝트 타입: Host, Network, Range, Group
- 실시간 진행 상황 모니터링
- 테스트 모드 지원 (실제 등록 없이 검증)

### 📋 벌크 정책 (Bulk Policy)
- CSV 파일을 통한 Access Rule 대량 생성
- 다중 소스/목적지/서비스 지원 (세미콜론 구분)
- 섹션 자동 생성
- 누락된 오브젝트 자동 생성 (그룹)

### 🔐 Zone 정책 (Zone Policy)
- 현대오토에버 전용 Zone 기반 정책 자동 생성

### 🖥️ GAIA 관리 (GAIA Management)
- Gateway OS 레벨 원격 관리
- 인터페이스 조회/설정
- 라우팅 테이블 관리
- DNS/NTP 설정
- 스크립트 실행 (Expert 모드)
- 시스템 정보 조회
- DMZ/INT 타입 지원
- 환경별 자동 생성 (prd/dev/stg)
- Inbound/Outbound 룰 자동 구성
- Inline Layer 자동 생성

---

## 시스템 요구사항

- **운영체제**: Windows 10/11 (64-bit)
- **CheckPoint 버전**: R80.10 이상 (Management API 지원)
- **네트워크**: CheckPoint Management Server 접근 가능
- **Python**: 3.8 이상 (소스 실행 시)

---

## 설치 방법

### 방법 1: 실행 파일 사용 (권장)

1. `checkpoint_toolkit.exe` 파일을 원하는 폴더에 복사
2. 더블클릭하여 실행

### 방법 2: Python 소스 실행

```bash
# 1. 필요 패키지 설치
pip install customtkinter requests

# 2. 실행
python main.py
```

### 방법 3: 직접 빌드

```bash
# build.bat 실행 또는
pyinstaller --onefile --windowed --name checkpoint_toolkit main.py
```

---

## 시작하기

### 1. 프로그램 실행

프로그램을 실행하면 아래와 같은 화면이 나타납니다:

```
┌─────────────────────────────────────────────────────────┐
│  CheckPoint Toolkit v3.4         [☀️/🌙] [🇰🇷/🇺🇸]      │
├─────────────────────────────────────────────────────────┤
│  서버: [________________] 포트: [443]                    │
│  사용자: [____________] 비밀번호: [********]             │
│  도메인: [____________] (선택)                           │
│                                    [🔗 연결] [🔓 해제]   │
├─────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────────────────┐ ┌───────────────┐ │
│ │ 📦 대량등록│ │                      │ │  로그 패널    │ │
│ │ 📋 벌크정책│ │      작업 영역        │ │               │ │
│ │ 🔐 Zone정책│ │                      │ │               │ │
│ └──────────┘ └──────────────────────┘ └───────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 2. 서버 연결

1. **서버 주소** 입력 (예: `192.168.1.100` 또는 `mgmt.example.com`)
2. **포트** 입력 (기본값: `443`)
3. **사용자명** 입력 (CheckPoint 관리자 계정)
4. **비밀번호** 입력
5. **도메인** 입력 (MDS 환경에서만 필요, 단일 SMS는 비워둠)
6. **[🔗 연결]** 버튼 클릭

> 💡 연결 정보는 자동 저장되어 다음 실행 시 자동 입력됩니다.

### 3. 테마 및 언어 변경

- **☀️/🌙 버튼**: 라이트/다크 테마 전환
- **🇰🇷/🇺🇸 버튼**: 한국어/영어 전환

---

## 기능별 상세 사용법

### 1. 대량 등록 (Bulk Import)

CSV 파일을 통해 Host, Network, Range, Group 오브젝트를 대량으로 등록합니다.

#### 사용 방법

1. 좌측 메뉴에서 **[📦 대량 등록]** 클릭
2. **[CSV 불러오기]** 버튼으로 CSV 파일 선택
3. 테이블에서 데이터 확인 및 편집
4. 옵션 설정:
   - ☑️ **테스트 모드**: 실제 등록 없이 검증만 수행
   - ☑️ **자동 게시**: 등록 완료 후 자동으로 Publish
5. **[▶ 실행]** 버튼 클릭

#### CSV 형식

```csv
type,name,ip,subnet,range_start,range_end,members,color,comments
host,web-server-01,192.168.1.10,,,,,blue,웹 서버 1
host,web-server-02,192.168.1.11,,,,,blue,웹 서버 2
network,internal-net,,192.168.0.0,255.255.0.0,,,green,내부 네트워크
range,dhcp-pool,,,192.168.100.1,192.168.100.254,,yellow,DHCP 풀
group,web-servers,,,,,web-server-01;web-server-02,red,웹 서버 그룹
```

| 컬럼 | 필수 | 설명 |
|------|:----:|------|
| type | ✅ | `host`, `network`, `range`, `group` 중 하나 |
| name | ✅ | 오브젝트 이름 (고유해야 함) |
| ip | △ | IP 주소 (host: 필수, network: 네트워크 주소) |
| subnet | △ | 서브넷 마스크 (network만 해당) |
| range_start | △ | 범위 시작 IP (range만 해당) |
| range_end | △ | 범위 종료 IP (range만 해당) |
| members | △ | 그룹 멤버 (세미콜론으로 구분, group만 해당) |
| color | - | 색상 (blue, green, red, yellow 등) |
| comments | - | 설명 |

---

### 2. 벌크 정책 (Bulk Policy)

CSV 파일을 통해 Access Rule을 대량으로 생성합니다.

#### 사전 준비 (중요!)

⚠️ **룰 생성 전에 반드시 확인하세요:**

1. **오브젝트 먼저 등록**: 소스/목적지에 사용할 오브젝트는 **대량 등록 탭에서 먼저 등록**하세요!
   - 또는 "오브젝트 자동생성" 옵션을 사용하면 빈 그룹으로 자동 생성됩니다.
   
2. **서비스 이름 정확히 일치**: 서비스는 CheckPoint에 **기존 등록된 이름과 정확히 일치**해야 합니다!
   - 기본 제공: `http`, `https`, `ssh`, `telnet`, `ftp`, `Any` 등
   - 사용자 정의 서비스는 SmartConsole에서 **먼저 생성** 후 **동일한 이름** 사용
   - **서비스는 자동 생성되지 않습니다!**
   - 대소문자 구분에 주의하세요 (예: `MSSQL` ≠ `mssql`)

#### 사용 방법

1. 좌측 메뉴에서 **[📋 벌크 정책]** 클릭
2. **패키지 이름** 입력 (예: `Standard`)
3. **레이어 이름** 입력 (비워두면 자동 감지)
4. **[확인]** 버튼으로 패키지 존재 확인
5. **[CSV 불러오기]** 버튼으로 CSV 파일 선택
6. 옵션 설정:
   - ☑️ **오브젝트 자동생성**: 없는 오브젝트를 빈 그룹으로 생성
   - ☑️ **테스트 모드**: 실제 생성 없이 검증만 수행
   - ☑️ **자동 게시**: 완료 후 자동 Publish
7. **[▶ 정책 생성]** 버튼 클릭
8. **삽입 위치** 입력 (룰 번호 또는 빈칸으로 맨 아래)

#### CSV 형식

```csv
name,source,destination,service,action,track,comments
allow-web,web-servers,app-servers,http;https,Accept,Log,웹 트래픽 허용
allow-db,app-servers,db-servers,MSSQL,Accept,Log,DB 접근 허용
deny-all,Any,db-servers,Any,Drop,Log,나머지 차단
```

| 컬럼 | 필수 | 설명 |
|------|:----:|------|
| name | ✅ | 룰 이름 |
| source | ✅ | 소스 오브젝트 (세미콜론으로 다중 입력 가능) |
| destination | ✅ | 목적지 오브젝트 (세미콜론으로 다중 입력 가능) |
| service | ✅ | 서비스 (세미콜론으로 다중 입력 가능) |
| action | ✅ | `Accept`, `Drop`, `Reject` 중 하나 |
| track | - | `Log`, `None`, `Detailed Log`, `Extended Log` |
| comments | - | 룰 설명 |

#### 다중 값 입력 예시

```csv
name,source,destination,service,action,track,comments
multi-rule,src1;src2;src3,dst1;dst2,http;https;ssh,Accept,Log,다중 소스/목적지/서비스
```

---

### 3. Zone 정책 (Zone Policy)

현대오토에버 전용 Zone 기반 정책을 자동으로 생성합니다.

#### 사용 방법

1. 좌측 메뉴에서 **[🔐 Zone 정책]** 클릭
2. **패키지 이름** 입력 (예: `Standard`)
3. **[확인]** 버튼으로 패키지 존재 확인
4. Zone 설정:
   - **기본 이름**: 시스템 이름 (예: `CCS`, `APP`, `WEB`)
   - **Zone 타입**: `DMZ` 또는 `INT` 선택
   - **환경**: `prd`, `dev`, `stg` 중 선택 (복수 선택 가능)
5. **[미리보기]** 버튼으로 생성될 정책 확인
6. **[▶ 생성]** 버튼 클릭
7. **Inbound 위치** 입력 (Cleanup Rule 번호)
8. Inbound 생성 후 **게시 여부** 선택
9. **Outbound 위치** 입력
10. Outbound 생성 후 **게시 여부** 선택

#### 생성되는 구조

**예: 기본 이름 = `CCS`, 타입 = `DMZ`, 환경 = `prd`, `dev`**

```
생성되는 Security Zone:
├── internet_DMZ (소스 Zone)
├── gs_dc_dmz (소스 Zone)
├── ccs_dmz_prd (대상 Zone)
└── ccs_dmz_dev (대상 Zone)

CCS_Inbound 섹션:
├── internet_DMZ → ccs_dmz_prd (Inline Layer: internet_to_ccs_dmz_prd)
├── internet_DMZ → ccs_dmz_dev (Inline Layer: internet_to_ccs_dmz_dev)
├── gs_dc_dmz → ccs_dmz_prd (Inline Layer: gs_dc_dmz_to_ccs_dmz_prd)
├── gs_dc_dmz → ccs_dmz_dev (Inline Layer: gs_dc_dmz_to_ccs_dmz_dev)
├── Any(Neg) → ccs_dmz_prd (Inline Layer: any_to_ccs_dmz_prd)
└── Any(Neg) → ccs_dmz_dev (Inline Layer: any_to_ccs_dmz_dev)

CCS_Outbound 섹션:
├── ccs_dmz_prd → internet_DMZ (Inline Layer: ccs_dmz_prd_to_internet)
├── ccs_dmz_dev → internet_DMZ (Inline Layer: ccs_dmz_dev_to_internet)
├── ccs_dmz_prd → gs_dc_dmz (Inline Layer: ccs_dmz_prd_to_gs_dc_dmz)
├── ccs_dmz_dev → gs_dc_dmz (Inline Layer: ccs_dmz_dev_to_gs_dc_dmz)
├── ccs_dmz_prd → Any(Neg) (Inline Layer: ccs_dmz_prd_to_any)
└── ccs_dmz_dev → Any(Neg) (Inline Layer: ccs_dmz_dev_to_any)
```

#### Zone 타입별 소스 Zone

| 타입 | 소스 Zone 1 | 소스 Zone 2 |
|:----:|-------------|-------------|
| DMZ | internet_DMZ | gs_dc_dmz |
| INT | internet_INT | gs_dc_int |

---

## CSV 파일 형식

### 파일 인코딩

- **UTF-8** 인코딩 사용 권장
- Excel에서 저장 시: "CSV UTF-8 (쉼표로 분리)" 선택

### 템플릿 다운로드

각 기능의 **[템플릿]** 버튼을 클릭하면 샘플 CSV 파일이 생성됩니다.

### Excel에서 CSV 만들기

1. Excel에서 데이터 작성
2. **파일 → 다른 이름으로 저장**
3. 파일 형식: **CSV UTF-8 (쉼표로 분리) (*.csv)** 선택
4. 저장

---

## 문제 해결

### 연결 오류

| 오류 메시지 | 원인 | 해결 방법 |
|-------------|------|-----------|
| Connection refused | 서버 접근 불가 | 네트워크 확인, 방화벽 포트 확인 |
| Authentication failed | 인증 실패 | 사용자명/비밀번호 확인 |
| SSL Error | 인증서 오류 | 무시됨 (자체 서명 인증서 허용) |
| Domain not found | 도메인 오류 | 도메인 이름 확인 (MDS 환경) |

### 오브젝트 등록 오류

| 오류 메시지 | 원인 | 해결 방법 |
|-------------|------|-----------|
| Object already exists | 중복 이름 | 다른 이름 사용 또는 기존 삭제 |
| Invalid IP address | IP 형식 오류 | IP 주소 형식 확인 |
| Invalid subnet mask | 서브넷 오류 | 서브넷 마스크 형식 확인 |

### 정책 생성 오류

| 오류 메시지 | 원인 | 해결 방법 |
|-------------|------|-----------|
| Package not found | 패키지 없음 | 패키지 이름 확인 |
| Layer not found | 레이어 없음 | 레이어 이름 확인 |
| Service not found | 서비스 없음 | CheckPoint에 서비스 등록 필요 |
| Object not found | 오브젝트 없음 | 오브젝트 자동생성 옵션 사용 |

### 게시 오류

| 오류 메시지 | 원인 | 해결 방법 |
|-------------|------|-----------|
| Publish failed | 게시 실패 | 충돌 확인, SmartConsole에서 수동 게시 |
| Session locked | 세션 잠김 | 다른 세션 종료 후 재시도 |

---

## 버전 히스토리

### v3.6 (2026-01-23) - Stable
- 🎉 **GAIA API 지원 추가** (Gateway OS 관리)
- ✨ GAIA 관리 탭 추가
- ✨ 시스템 정보 조회 (호스트명, 버전, Uptime)
- ✨ 인터페이스 관리 (Physical, Bond, VLAN)
- ✨ 라우팅 관리 (Static Route 추가/삭제)
- ✨ DNS/NTP 설정
- ✨ Expert 모드 스크립트 실행
- 🔧 Management API와 GAIA API 완전 분리 구조

### v3.4 (2026-01-23)
- 🎉 **Zone 정책 생성 로직 안정화**
- 🔧 섹션 이름 기반 `position.below` 사용 (쉘 스크립트와 동일)
- 🔧 섹션 UID 대신 섹션 이름으로 룰 위치 지정
- 🔧 Track 타입 Log로 통일
- 🔧 Application Site 기본 카테고리 자동 지정 (`Custom_Application_Site`)
- 📋 CSV 파일 mgmt_cli batch 모드 호환

### v3.3 (2026-01-22)
- ✨ 벌크 정책 생성 기능 추가 (CSV 기반)
- ✨ Zone 정책 탭 분리
- 🔧 로그 패널 폰트 크기 증가 (10pt → 12pt)
- 🔧 로그 패널 너비 증가 (320 → 400)

### v3.2 (2026-01-22)
- ✨ 다크/라이트 테마 토글 추가
- ✨ 한국어/영어 언어 토글 추가
- 🔧 테마 설정 저장 기능

### v3.1 (2026-01-22)
- ✨ 사이드바 네비게이션 추가
- ✨ 모듈화 리팩토링 (7개 파일 분리)
- 🔧 레이아웃 최적화

### v3.0 (2026-01-22)
- ✨ CustomTkinter 기반 현대적 UI
- ✨ 현대오토에버 브랜드 컬러 적용

### v2.x (2026-01-22)
- CSV 편집 기능
- Zone 정책 생성 기능
- 버그 수정

### v1.0 (2026-01-22)
- 최초 버전
- 대량 오브젝트 등록 기능

---

## mgmt_cli Batch 모드 호환

본 툴의 오브젝트 CSV 파일은 CheckPoint `mgmt_cli` batch 모드와 호환됩니다.

### 사용법

```bash
# 로그인
mgmt_cli login user admin password *** > session.txt

# Host 등록
mgmt_cli -s session.txt add host --batch hosts.csv

# Network 등록
mgmt_cli -s session.txt add network --batch networks.csv

# Service-TCP 등록
mgmt_cli -s session.txt add service-tcp --batch services.csv

# Access Rule 등록
mgmt_cli -s session.txt add access-rule --batch policy.csv

# Publish
mgmt_cli -s session.txt publish

# 로그아웃
mgmt_cli -s session.txt logout
```

### Policy CSV 형식 (mgmt_cli용)

| 컬럼 | 설명 | 예시 | 비고 |
|:----:|------|------|------|
| layer | 정책 패키지 레이어 | test Network | 패키지명 + " Network" |
| position | 룰 위치 | top, bottom | 또는 above/below + 섹션명 |
| name | 룰 이름 | web-to-db | 고유해야 함 |
| source | 출발지 | web-server, Any | 다중: source.1, source.2 |
| destination | 목적지 | db-server, Any | 다중: destination.1, destination.2 |
| service | 서비스 | https, Any | 다중: service.1, service.2 |
| action | 동작 | Accept, Drop | |
| track.type | 로깅 | Log, None | |
| comments | 설명 | 웹 트래픽 | 선택 |

### 다중 값 입력 (mgmt_cli)

```csv
layer,position,name,source.1,source.2,destination,service.1,service.2,action,track.type
test Network,bottom,multi-rule,host-1,host-2,db-server,https,ssh,Accept,Log
```

> ⚠️ **주의**: GUI 툴은 세미콜론(`;`) 구분, mgmt_cli는 인덱스(`.1`, `.2`) 방식

---

## 지원 및 문의

현대오토에버 보안팀

---

## 라이선스

이 소프트웨어는 현대오토에버 내부용으로 개발되었습니다.
