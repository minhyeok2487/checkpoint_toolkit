"""
CheckPoint Management API Client
"""

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CheckPointAPI:
    def __init__(self, server: str, port: int = 443):
        self.server = server
        self.port = port
        self.base_url = f"https://{server}:{port}/web_api"
        self.sid = None
    
    def _call(self, endpoint: str, payload: dict = None) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.sid:
            headers["X-chkp-sid"] = self.sid
        try:
            r = requests.post(f"{self.base_url}/{endpoint}", json=payload or {}, headers=headers, verify=False, timeout=30)
            return r.json()
        except Exception as e:
            return {"message": str(e)}
    
    def login(self, user: str, password: str, domain: str = None) -> dict:
        payload = {"user": user, "password": password}
        if domain:
            payload["domain"] = domain
        result = self._call("login", payload)
        if "sid" in result:
            self.sid = result["sid"]
        return result
    
    def logout(self) -> dict:
        result = self._call("logout")
        self.sid = None
        return result
    
    def publish(self) -> dict:
        return self._call("publish")
    
    def discard(self) -> dict:
        return self._call("discard")
    
    def show_object(self, obj_type: str, name: str) -> dict:
        return self._call(f"show-{obj_type}", {"name": name})
    
    def add_host(self, name: str, ip: str, comments: str = "") -> dict:
        return self._call("add-host", {"name": name, "ip-address": ip, "comments": comments, "ignore-warnings": True})
    
    def set_host(self, name: str, ip: str, comments: str = "") -> dict:
        return self._call("set-host", {"name": name, "ip-address": ip, "comments": comments, "ignore-warnings": True})
    
    def add_network(self, name: str, subnet: str, mask: int, comments: str = "") -> dict:
        return self._call("add-network", {"name": name, "subnet": subnet, "mask-length": mask, "comments": comments, "ignore-warnings": True})
    
    def set_network(self, name: str, subnet: str, mask: int, comments: str = "") -> dict:
        return self._call("set-network", {"name": name, "subnet": subnet, "mask-length": mask, "comments": comments, "ignore-warnings": True})
    
    def add_group(self, name: str, members: list, comments: str = "") -> dict:
        payload = {"name": name, "comments": comments, "ignore-warnings": True}
        if members:
            payload["members"] = members
        return self._call("add-group", payload)
    
    def add_service_tcp(self, name: str, port: str, comments: str = "") -> dict:
        return self._call("add-service-tcp", {"name": name, "port": port, "comments": comments, "ignore-warnings": True})
    
    def add_service_udp(self, name: str, port: str, comments: str = "") -> dict:
        return self._call("add-service-udp", {"name": name, "port": port, "comments": comments, "ignore-warnings": True})
    
    def add_address_range(self, name: str, first: str, last: str, comments: str = "") -> dict:
        return self._call("add-address-range", {"name": name, "ip-address-first": first, "ip-address-last": last, "comments": comments, "ignore-warnings": True})
    
    def add_application_site(self, name: str, urls: list, category: str = "", description: str = "") -> dict:
        payload = {"name": name, "url-list": urls}
        payload["primary-category"] = category if category else "Custom_Application_Site"
        if description:
            payload["description"] = description
        return self._call("add-application-site", payload)
    
    def show_package(self, name: str) -> dict:
        return self._call("show-package", {"name": name})
    
    def show_security_zone(self, name: str) -> dict:
        return self._call("show-security-zone", {"name": name})
    
    def add_security_zone(self, name: str) -> dict:
        return self._call("add-security-zone", {"name": name, "ignore-warnings": True})
    
    def show_access_layer(self, name: str) -> dict:
        return self._call("show-access-layer", {"name": name})
    
    def show_access_rulebase(self, layer: str) -> dict:
        return self._call("show-access-rulebase", {"name": layer, "limit": 500})
    
    def add_access_layer(self, name: str) -> dict:
        return self._call("add-access-layer", {"name": name, "add-default-rule": False, "ignore-warnings": True})
    
    def set_access_layer(self, name: str) -> dict:
        return self._call("set-access-layer", {"name": name, "applications-and-url-filtering": True, "content-awareness": True, "ignore-warnings": True})
    
    def set_cleanup_rule(self, layer: str) -> dict:
        return self._call("add-access-rule", {
            "layer": layer,
            "position": "bottom",
            "name": "Cleanup Rule",
            "source": "Any",
            "destination": "Any",
            "service": "Any",
            "action": "Drop",
            "track": {"type": "Log"},
            "ignore-warnings": True
        })
    
    def add_access_section(self, layer: str, name: str, position: str = "") -> dict:
        """Create section at specified position"""
        payload = {"layer": layer, "name": name, "ignore-warnings": True}
        if position:
            payload["position"] = position
        else:
            payload["position"] = "bottom"
        return self._call("add-access-section", payload)
    
    def add_access_rule(self, layer: str, section_name: str, source: str, destination: str, inline_layer: str) -> dict:
        """Add rule below section (using section name)"""
        return self._call("add-access-rule", {
            "layer": layer,
            "position": {"below": section_name},
            "name": f"{source}_to_{destination}",
            "source": source,
            "destination": destination,
            "service": "Any",
            "action": "Apply Layer",
            "inline-layer": inline_layer,
            "track": {"type": "Log"},
            "ignore-warnings": True
        })
    
    def set_rule_negate_source(self, uid: str, layer: str, zones: list) -> dict:
        return self._call("set-access-rule", {"uid": uid, "layer": layer, "source": zones, "source-negate": True, "ignore-warnings": True})
    
    def set_rule_negate_destination(self, uid: str, layer: str, zones: list) -> dict:
        return self._call("set-access-rule", {"uid": uid, "layer": layer, "destination": zones, "destination-negate": True, "ignore-warnings": True})

    def add_dns_domain(self, name: str, is_sub_domain: bool = False, comments: str = "") -> dict:
        return self._call("add-dns-domain", {"name": name, "is-sub-domain": is_sub_domain, "comments": comments, "ignore-warnings": True})

    def set_dns_domain(self, name: str, is_sub_domain: bool = False, comments: str = "") -> dict:
        return self._call("set-dns-domain", {"name": name, "is-sub-domain": is_sub_domain, "comments": comments, "ignore-warnings": True})

    def show_objects(self, obj_type: str, limit: int = 500, offset: int = 0) -> dict:
        """범용 오브젝트 목록 조회 (단일 페이지)"""
        return self._call(f"show-{obj_type}s", {
            "limit": limit,
            "offset": offset,
            "details-level": "standard"
        })

    def show_all_objects(self, obj_type: str, progress_callback=None, user_defined_only=True) -> dict:
        """전체 오브젝트 목록 조회 (페이징 처리)"""
        all_objects = []
        offset = 0
        limit = 500
        total = None

        while True:
            result = self.show_objects(obj_type, limit, offset)
            if "objects" not in result:
                return result  # 오류 반환

            # 사용자 정의 오브젝트만 필터링
            if user_defined_only:
                filtered = [obj for obj in result["objects"]
                           if obj.get("domain", {}).get("name") == "SMC User"]
                all_objects.extend(filtered)
            else:
                all_objects.extend(result["objects"])

            total = result.get("total", len(all_objects))

            if progress_callback:
                progress_callback(offset + len(result["objects"]), total)

            if offset + limit >= total:
                break
            offset += limit

        return {"objects": all_objects, "total": len(all_objects)}

    def show_all_access_rules(self, layer: str, progress_callback=None) -> dict:
        """전체 Access Rule 목록 조회 (페이징 처리, 섹션 정보 포함)"""
        all_items = []  # 섹션과 룰 모두 포함
        objects_dict = {}  # UID -> name 매핑
        offset = 0
        limit = 500

        while True:
            result = self._call("show-access-rulebase", {
                "name": layer,
                "limit": limit,
                "offset": offset,
                "details-level": "standard",
                "use-object-dictionary": True
            })

            if "rulebase" not in result:
                return result

            # objects-dictionary에서 UID -> name 매핑 구축
            for obj in result.get("objects-dictionary", []):
                uid = obj.get("uid", "")
                name = obj.get("name", uid)
                if uid:
                    objects_dict[uid] = name

            # 섹션과 룰 순서대로 추출
            for item in result.get("rulebase", []):
                if item.get("type") == "access-rule":
                    item["_item_type"] = "Rule"
                    all_items.append(item)
                elif item.get("type") == "access-section":
                    # 섹션 추가
                    section_item = {
                        "_item_type": "Section",
                        "name": item.get("name", ""),
                        "uid": item.get("uid", "")
                    }
                    all_items.append(section_item)
                    # 섹션 내부 룰도 추출
                    for rule in item.get("rulebase", []):
                        if rule.get("type") == "access-rule":
                            rule["_item_type"] = "Rule"
                            rule["_section"] = item.get("name", "")
                            all_items.append(rule)

            total = result.get("total", len(all_items))
            if progress_callback:
                progress_callback(offset + limit, total)

            if offset + limit >= total:
                break
            offset += limit

        return {"items": all_items, "total": len(all_items), "objects_dict": objects_dict}
