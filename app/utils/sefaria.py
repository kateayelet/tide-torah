import requests
from typing import Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from cachetools import TTLCache
from functools import lru_cache

load_dotenv()

class SefariaAPI:
    def __init__(self):
        self.base_url = "https://api.sefaria.org/v3"
        self.api_key = os.getenv("SEFARIA_API_KEY")
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else None
        }
        self.text_cache = TTLCache(maxsize=int(os.getenv('CACHE_MAX_SIZE', 1000)), ttl=int(os.getenv('CACHE_TTL', 3600)))
        self.parsha_cache = TTLCache(maxsize=int(os.getenv('CACHE_MAX_SIZE', 1000)), ttl=int(os.getenv('CACHE_TTL', 3600)))

    @lru_cache(maxsize=128)
    def get_text(self, ref: str, version: str = "English - Metsudah Linear Bible") -> Dict[str, Any]:
        """
        Get text from Sefaria by reference with caching
        """
        cache_key = f"{ref}_{version}"
        if cache_key in self.text_cache:
            return self.text_cache[cache_key]

        url = f"{self.base_url}/texts"
        params = {
            "ref": ref,
            "version": version,
            "context": True
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            result = response.json()
            self.text_cache[cache_key] = result
            return result
        except requests.RequestException as e:
            return {"error": str(e)}

    @lru_cache(maxsize=32)
    def get_parsha(self, date: datetime) -> Dict[str, Any]:
        """
        Get the parsha for a given date with caching
        """
        cache_key = date.strftime("%Y-%m-%d")
        if cache_key in self.parsha_cache:
            return self.parsha_cache[cache_key]

        url = f"{self.base_url}/calendar"
        params = {
            "date": date.strftime("%Y-%m-%d"),
            "type": "parsha"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            result = response.json()
            self.parsha_cache[cache_key] = result
            return result
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_text(self, ref: str, version: str = "English - Metsudah Linear Bible") -> Dict[str, Any]:
        """
        Get text from Sefaria by reference
        """
        url = f"{self.base_url}/texts"
        params = {
            "ref": ref,
            "version": version,
            "context": True
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_parsha(self, date: datetime) -> Dict[str, Any]:
        """
        Get the parsha for a given date
        """
        url = f"{self.base_url}/calendar"
        params = {
            "date": date.strftime("%Y-%m-%d"),
            "type": "parsha"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    def get_kabbalistic_texts(self, ref: str) -> Dict[str, Any]:
        """
        Get Kabbalistic texts related to a reference
        """
        texts = {}
        kabbalistic_sources = [
            "Zohar",
            "Tanya",
            "Baal Shem Tov",
            "Ari"
        ]
        
        for source in kabbalistic_sources:
            text_ref = f"{source}.{ref}"
            texts[source.lower()] = self.get_text(text_ref)
        
        return texts

    def get_chassidic_texts(self, ref: str) -> Dict[str, Any]:
        """
        Get Chassidic texts related to a reference
        """
        texts = {}
        chassidic_sources = [
            "Chabad.org",
            "Tanya",
            "Chassidic Insights"
        ]
        
        for source in chassidic_sources:
            text_ref = f"{source}.{ref}"
            texts[source.lower()] = self.get_text(text_ref)
        
        return texts

    def get_related_texts(self, ref: str) -> Dict[str, Any]:
        """
        Get all related texts for a reference
        """
        return {
            "rashi": self.get_text(f"Rashi on {ref}"),
            "midrash": self.get_text(f"Midrash Rabbah.{ref}"),
            "gemara": self.get_text(f"Gemara.{ref}"),
            "kabbalistic": self.get_kabbalistic_texts(ref),
            "chassidic": self.get_chassidic_texts(ref)
        }

# Create a singleton instance
sefaria_api = SefariaAPI()
