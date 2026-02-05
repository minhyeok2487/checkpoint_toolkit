"""
CheckPoint Management Toolkit - 설정
"""

# CheckPoint 브랜드 컬러
BRAND_BERRY = "#ee0c5d"
BRAND_BERRY_DARK = "#b70d4e"
BRAND_PURPLE = "#741984"
BRAND_GRAVITAS = "#41273c"

# 상태 컬러
SUCCESS = "#00d26a"
WARNING = "#ffaa00"
ERROR = "#ff4757"

# 앱 설정
APP_GEOMETRY = "1400x800"
APP_MIN_SIZE = (1200, 700)

def get_object_types(lang="ko"):
    """언어별 오브젝트 타입"""
    if lang == "en":
        return {
            "host": {
                "columns": ["Name", "IP Address", "Description"],
                "api_columns": ["name", "ip-address", "comments"],
                "format": "Name, IP Address, Description",
                "template": [["name", "ip-address", "comments"], ["server-01", "10.0.1.10", "Example"]]
            },
            "network": {
                "columns": ["Name", "Subnet", "Mask", "Description"],
                "api_columns": ["name", "subnet", "mask-length", "comments"],
                "format": "Name, Subnet, Mask, Description",
                "template": [["name", "subnet", "mask-length", "comments"], ["net-web", "10.0.1.0", "24", "Web server"]]
            },
            "group": {
                "columns": ["Name", "Members", "Description"],
                "api_columns": ["name", "members", "comments"],
                "format": "Name, Members(;sep), Description",
                "template": [["name", "members", "comments"], ["grp-web", "srv1;srv2", "Group"]]
            },
            "service-tcp": {
                "columns": ["Name", "Port", "Description"],
                "api_columns": ["name", "port", "comments"],
                "format": "Name, Port, Description",
                "template": [["name", "port", "comments"], ["svc-http", "80", "HTTP"]]
            },
            "service-udp": {
                "columns": ["Name", "Port", "Description"],
                "api_columns": ["name", "port", "comments"],
                "format": "Name, Port, Description",
                "template": [["name", "port", "comments"], ["svc-dns", "53", "DNS"]]
            },
            "address-range": {
                "columns": ["Name", "Start IP", "End IP", "Description"],
                "api_columns": ["name", "ip-address-first", "ip-address-last", "comments"],
                "format": "Name, Start IP, End IP, Description",
                "template": [["name", "ip-address-first", "ip-address-last", "comments"], ["range", "10.0.10.100", "10.0.10.200", "DHCP"]]
            },
            "application-site": {
                "columns": ["Name", "URL List", "Category", "Description"],
                "api_columns": ["name", "url-list", "primary-category", "description"],
                "format": "Name*, URL List*(;sep), Category, Description",
                "template": [["name", "url-list", "primary-category", "description"], ["blocked", "malware.com;phish.net", "", "Blocked sites"]]
            },
            "dns-domain": {
                "columns": ["Domain", "FQDN Only", "Description"],
                "api_columns": ["name", "fqdn-only", "comments"],
                "format": "Domain(.example.com), FQDN Only(true/false), Description",
                "template": [["name", "fqdn-only", "comments"],
                             [".naver.com", "true", "Naver (exact domain only)"],
                             [".google.com", "false", "Google (includes subdomains)"]]
            }
        }
    else:
        return {
            "host": {
                "columns": ["이름", "IP주소", "설명"],
                "api_columns": ["name", "ip-address", "comments"],
                "format": "이름, IP주소, 설명",
                "template": [["name", "ip-address", "comments"], ["server-01", "10.0.1.10", "예시"]]
            },
            "network": {
                "columns": ["이름", "서브넷", "마스크", "설명"],
                "api_columns": ["name", "subnet", "mask-length", "comments"],
                "format": "이름, 서브넷, 마스크, 설명",
                "template": [["name", "subnet", "mask-length", "comments"], ["net-web", "10.0.1.0", "24", "웹서버"]]
            },
            "group": {
                "columns": ["이름", "멤버", "설명"],
                "api_columns": ["name", "members", "comments"],
                "format": "이름, 멤버(;구분), 설명",
                "template": [["name", "members", "comments"], ["grp-web", "srv1;srv2", "그룹"]]
            },
            "service-tcp": {
                "columns": ["이름", "포트", "설명"],
                "api_columns": ["name", "port", "comments"],
                "format": "이름, 포트, 설명",
                "template": [["name", "port", "comments"], ["svc-http", "80", "HTTP"]]
            },
            "service-udp": {
                "columns": ["이름", "포트", "설명"],
                "api_columns": ["name", "port", "comments"],
                "format": "이름, 포트, 설명",
                "template": [["name", "port", "comments"], ["svc-dns", "53", "DNS"]]
            },
            "address-range": {
                "columns": ["이름", "시작IP", "종료IP", "설명"],
                "api_columns": ["name", "ip-address-first", "ip-address-last", "comments"],
                "format": "이름, 시작IP, 종료IP, 설명",
                "template": [["name", "ip-address-first", "ip-address-last", "comments"], ["range", "10.0.10.100", "10.0.10.200", "DHCP"]]
            },
            "application-site": {
                "columns": ["이름", "URL목록", "카테고리", "설명"],
                "api_columns": ["name", "url-list", "primary-category", "description"],
                "format": "이름*, URL목록*(;구분), 카테고리, 설명",
                "template": [["name", "url-list", "primary-category", "description"], ["blocked", "malware.com;phish.net", "", "차단사이트"]]
            },
            "dns-domain": {
                "columns": ["도메인", "FQDN전용", "설명"],
                "api_columns": ["name", "fqdn-only", "comments"],
                "format": "도메인(.example.com), FQDN전용(true/false), 설명",
                "template": [["name", "fqdn-only", "comments"],
                             [".naver.com", "true", "네이버 (정확히 이 도메인만)"],
                             [".google.com", "false", "구글 (하위도메인 포함)"]]
            }
        }
