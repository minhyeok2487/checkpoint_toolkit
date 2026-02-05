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
        return self._call("add-access-rule", {"layer": layer, "position": "bottom", "name": "Cleanup Rule", "action": "Drop", "track": {"type": "Log"}, "ignore-warnings": True})
    
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
