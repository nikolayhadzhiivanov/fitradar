import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from .base import BaseScraper
from ..normalizer import normalize_product

class SilaBgScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            store_code="silabg",
            store_name="Сила БГ",
            base_url="https://www.silabg.com"
        )

    def parse_product_card(self, card_elem) -> Dict[str, Any]:
        """
        Parses a single product card element from SilaBG HTML structure.
        """
        title_elem = card_elem.select_one("a.product-title, .title, h3, .name")
        title = title_elem.get_text(strip=True) if title_elem else "Неизвестен продукт"

        link = title_elem.get("href") if title_elem and title_elem.has_attr("href") else "#"
        if link and not link.startswith("http"):
            link = f"{self.base_url}{link}"

        price_elem = card_elem.select_one(".price, .current-price, .promo-price, span.price")
        price_val = 0.0
        if price_elem:
            p_text = price_elem.get_text(strip=True).replace("лв", "").replace("BGN", "").replace(",", ".").strip()
            nums = re.findall(r'\d+(?:\.\d+)?', p_text)
            if nums:
                price_val = float(nums[0])

        old_price_elem = card_elem.select_one(".old-price, del, .crossed")
        old_price_val = None
        if old_price_elem:
            op_text = old_price_elem.get_text(strip=True).replace("лв", "").replace("BGN", "").replace(",", ".").strip()
            nums = re.findall(r'\d+(?:\.\d+)?', op_text)
            if nums:
                old_price_val = float(nums[0])

        img_elem = card_elem.select_one("img")
        img_url = img_elem.get("src") if img_elem and img_elem.has_attr("src") else ""

        return {
            "store_code": self.store_code,
            "raw_title": title,
            "price_bgn": price_val,
            "old_price_bgn": old_price_val,
            "product_url": link,
            "image_url": img_url
        }

    def parse(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".product-card, .item, .product-item, .box-product")
        results = []
        for c in cards:
            raw = self.parse_product_card(c)
            if raw["price_bgn"] > 0:
                results.append(normalize_product(raw))
        return results

    def run(self) -> List[Dict[str, Any]]:
        target_url = f"{self.base_url}/bg/category/proteini.html"
        try:
            html = self.fetch_page(target_url)
            return self.parse(html)
        except Exception as e:
            print(f"[{self.store_name}] Live scrape note: {e}")
            return []
