# CheckPoint Management Tool v3.8 (Stable)

CSV 기반 CheckPoint 오브젝트 및 정책 대량 관리 도구 + GAIA Gateway OS 관리

## 🚀 실행

```bash
pip install -r requirements.txt
python main.py
```

## 📁 구조

```
checkpoint_toolkit/
├── main.py              # 메인 앱
├── config.py            # 설정
├── lang.py              # 다국어 (한/영)
├── api.py               # CheckPoint Management API
├── gaia_api.py          # CheckPoint GAIA API (Gateway OS)
├── widgets.py           # UI 위젯
├── tabs/
│   ├── __init__.py      # 대량 오브젝트 등록
│   ├── policy_tab.py    # 벌크 정책 생성
│   ├── zone_policy_tab.py # Zone 정책 생성
│   └── gaia_tab.py      # GAIA Gateway 관리
├── requirements.txt
└── build.bat            # EXE 빌드
```

## 🎨 기능

### 대량 오브젝트 등록
CSV 파일로 오브젝트 일괄 등록:
- Host, Network, Group
- Service-TCP, Service-UDP
- Address-Range, Application-Site (URL)

### 벌크 정책 생성
CSV 파일로 Access Rule 일괄 생성:
- Section 자동 생성
- Zone 자동 생성
- Inline Layer 자동 생성
- Negate 룰 지원

### GAIA Gateway 관리 (NEW!)
Gateway OS 원격 관리:
- 시스템 정보 조회 (호스트명, 버전, Uptime)
- 인터페이스 관리 (Physical, Bond, VLAN)
- 라우팅 관리 (Static Route)
- DNS/NTP 설정
- Expert 모드 스크립트 실행

### 기타
- 🌙/☀️ 다크/라이트 모드
- 🌐 한국어/영어 전환
- 설정 자동 저장

## 📋 정책 CSV 포맷

| 컬럼 | 설명 | 예시 |
|------|------|------|
| section | 섹션 이름 | Web_Inbound |
| rule_name | 룰 이름 | internet_to_web |
| source | 소스 Zone/오브젝트 | internet_zone |
| destination | 목적지 Zone/오브젝트 | web_zone |
| service | 서비스 | HTTPS, Any |
| action | 액션 | Accept, Drop, inline |
| track | 로깅 | Log, None |
| inline_layer | 인라인 레이어 이름 | internet_to_web_layer |
| negate_src | 소스 부정 (;구분) | zone1;zone2 |
| negate_dst | 목적지 부정 (;구분) | zone1;zone2 |
| position | 위치 | top, bottom, 61 |
| comments | 설명 | Internet to Web |

### 예시 CSV
```csv
section,rule_name,source,destination,service,action,track,inline_layer,negate_src,negate_dst,position,comments
Web_Inbound,internet_to_web,internet_zone,web_zone,HTTPS,inline,Log,internet_to_web_layer,,,top,Internet to Web
Web_Inbound,any_to_web_deny,Any,web_zone,Any,Drop,Log,,internet_zone;dc_zone,,,Deny others
Web_Outbound,web_to_internet,web_zone,internet_zone,HTTPS,inline,Log,web_to_internet_layer,,,top,Web to Internet
```

## ⚙️ 빌드

```cmd
build.bat
```

→ `dist/CheckPointToolkit.exe` 생성

## 📝 지원 환경

- Python 3.10+
- CheckPoint R81.x Management Server
- Windows / macOS / Linux
