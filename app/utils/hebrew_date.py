from datetime import datetime
from typing import Dict, Any
from hebrewcal import HebrewDate
from pytz import timezone
from dateutil import parser
from cachetools import TTLCache
import os
from dotenv import load_dotenv

load_dotenv()

class HebrewDateCalculator:
    def __init__(self):
        self.cache = TTLCache(maxsize=int(os.getenv('CACHE_MAX_SIZE', 1000)), ttl=int(os.getenv('CACHE_TTL', 3600)))
        self.israel_tz = timezone('Asia/Jerusalem')

    def get_hebrew_date(self, date: datetime) -> Dict[str, Any]:
        """
        Get complete Hebrew date information for a given date
        """
        # Check cache first
        cache_key = date.strftime("%Y-%m-%d")
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Convert to Israel time
            date = date.astimezone(self.israel_tz)
            
            # Get Hebrew date
            hebrew_date = HebrewDate.from_gregorian(date.year, date.month, date.day)
            
            # Calculate Omer day
            omer_day = self._calculate_omer_day(date)
            
            # Check for holidays
            is_holiday = self._is_holiday(date)
            
            # Get zodiac information
            zodiac = self._get_zodiac(date)
            
            result = {
                "gregorian_date": date.strftime("%Y-%m-%d"),
                "hebrew_day": hebrew_date.day,
                "hebrew_month": hebrew_date.month,
                "hebrew_year": hebrew_date.year,
                "hebrew_month_name": hebrew_date.month_name,
                "hebrew_year_name": hebrew_date.year_name,
                "is_holiday": is_holiday,
                "omer_day": omer_day,
                "zodiac_sign": zodiac,
                "day_of_week": hebrew_date.day_of_week,
                "parsha": self._get_parsha(date)
            }
            
            # Cache the result
            self.cache[cache_key] = result
            return result
            
        except Exception as e:
            return {"error": str(e)}

    def _calculate_omer_day(self, date: datetime) -> int:
        """
        Calculate the current day of the Omer
        """
        # Omer starts from the second night of Pesach
        pesach_start = datetime(date.year, 4, 15)
        days = (date - pesach_start).days
        return days + 1 if 0 <= days < 49 else None

    def _is_holiday(self, date: datetime) -> bool:
        """
        Check if the date is a Jewish holiday
        """
        hebrew_date = HebrewDate.from_gregorian(date.year, date.month, date.day)
        return hebrew_date.is_holiday

    def _get_zodiac(self, date: datetime) -> str:
        """
        Get the zodiac sign for the date
        """
        # Convert to Julian day
        jd = (date - datetime(1, 1, 1)).days + 1721425
        
        # Calculate zodiac position
        zodiac_start = (jd - 1) % 12
        zodiac_signs = [
            "Aries", "Taurus", "Gemini", "Cancer",
            "Leo", "Virgo", "Libra", "Scorpio",
            "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        return zodiac_signs[zodiac_start]

    def _get_parsha(self, date: datetime) -> str:
        """
        Get the weekly parsha for the date
        """
        hebrew_date = HebrewDate.from_gregorian(date.year, date.month, date.day)
        return hebrew_date.parsha

# Create a singleton instance
hebrew_date_calculator = HebrewDateCalculator()
