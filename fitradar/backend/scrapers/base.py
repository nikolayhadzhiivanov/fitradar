import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "bg,en-US;q=0.9,en;q=0.8",
}

class BaseScraper:
    def __init__(self, store_code: str, store_name: str, base_url: str):
        self.store_code = store_code
        self.store_name = store_name
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def fetch_page(self, url: str, timeout: int = 8) -> str:
        response = self.session.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text

    def parse(self, html: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("Subclasses must implement parse()")

    def run(self) -> List[Dict[str, Any]]:
        raise NotImplementedError("Subclasses must implement run()")
