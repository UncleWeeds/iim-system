# clients/json_server.py
import requests
from typing import List
from .base import IncidentClient, Incident

class JSONServerClient(IncidentClient):
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def list_incidents(self) -> List[Incident]:
        resp = requests.get(f"{self.base_url}/incidents")
        resp.raise_for_status()
        data = resp.json()
        return [Incident(**item) for item in data]
