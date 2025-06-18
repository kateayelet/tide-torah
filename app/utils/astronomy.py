from datetime import datetime
from typing import Dict, Any
from ephem import *
from pytz import timezone
from astral import LocationInfo
from astral.sun import sun
import os
from dotenv import load_dotenv
from cachetools import TTLCache
from functools import lru_cache
from app.utils.visualizations import moon_visualizer, tide_visualizer

load_dotenv()

class AstronomyCalculator:
    def __init__(self):
        self.cache = TTLCache(maxsize=int(os.getenv('CACHE_MAX_SIZE', 1000)), ttl=int(os.getenv('CACHE_TTL', 3600)))
        self.israel_tz = timezone('Asia/Jerusalem')
        self.location = LocationInfo("Jerusalem", "Israel")

    def get_moon_visual(self, phase: float, phase_name: str) -> Dict[str, Any]:
        """
        Get a visual representation of the moon phase
        """
        return moon_visualizer.create_moon_visual(phase, phase_name)

    def get_tide_visual(self, tide_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a visual representation of tide patterns
        """
        return tide_visualizer.create_tide_visual(tide_data)

    def get_astronomical_data(self, date: datetime, latitude: float = 31.7683, longitude: float = 35.2137) -> Dict[str, Any]:
        """
        Get comprehensive astronomical data for a given date and location
        """
        # Check cache first
        cache_key = f"{date.strftime('%Y-%m-%d')}_{latitude}_{longitude}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Convert to Israel time
            date = date.astimezone(self.israel_tz)
            
            # Set up observer
            observer = Observer()
            observer.lat = str(latitude)
            observer.lon = str(longitude)
            observer.date = date.strftime('%Y/%m/%d')

            # Calculate moon data
            moon = Moon()
            moon.compute(observer)
            moon_phase = self._calculate_moon_phase(moon.phase)
            
            # Calculate sun data
            sun = Sun()
            sun.compute(observer)
            
            # Calculate zodiac positions
            zodiac_positions = self._calculate_zodiac_positions(date)
            
            # Calculate prayer times
            prayer_times = self._calculate_prayer_times(date, latitude, longitude)
            
            result = {
                "date": date.strftime("%Y-%m-%d"),
                "moon": {
                    "phase": moon_phase,
                    "position": moon.alt,
                    "constellation": self._get_mazal(moon.alt)
                },
                "sun": {
                    "position": sun.alt,
                    "constellation": self._get_mazal(sun.alt)
                },
                "zodiac_positions": zodiac_positions,
                "prayer_times": prayer_times,
                "astronomical_events": self._get_astronomical_events(date)
            }
            
            # Cache the result
            self.cache[cache_key] = result
            return result
            
        except Exception as e:
            return {"error": str(e)}

    def _calculate_moon_phase(self, phase: float) -> Dict[str, Any]:
        """
        Calculate detailed moon phase information
        """
        phases = [
            "New Moon", "Waxing Crescent", "First Quarter",
            "Waxing Gibbous", "Full Moon", "Waning Gibbous",
            "Last Quarter", "Waning Crescent"
        ]
        
        phase_index = int((phase / 100) * 8)
        return {
            "name": phases[phase_index],
            "percentage": phase,
            "age": self._calculate_moon_age()
        }

    def _calculate_moon_age(self) -> float:
        """
        Calculate moon's age in days
        """
        new_moon = Moon()
        new_moon.compute_new_moon()
        return (datetime.now() - new_moon.date).days

    def _calculate_zodiac_positions(self, date: datetime) -> Dict[str, Dict[str, Any]]:
        """
        Calculate positions of all planets in zodiac
        """
        planets = {
            "sun": Sun(),
            "moon": Moon(),
            "mercury": Mercury(),
            "venus": Venus(),
            "mars": Mars(),
            "jupiter": Jupiter(),
            "saturn": Saturn()
        }
        
        positions = {}
        for name, planet in planets.items():
            planet.compute(date)
            positions[name] = {
                "constellation": self._get_mazal(planet.alt),
                "degree": planet.alt,
                "sign": self._get_zodiac_sign(planet.alt)
            }
        return positions

    def _get_mazal(self, position: float) -> str:
        """
        Get the mazal (constellation) for a given position
        """
        # Simplified calculation - in production use proper ephemeris
        mazalot = [
            "Aries", "Taurus", "Gemini", "Cancer",
            "Leo", "Virgo", "Libra", "Scorpio",
            "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        return mazalot[int(position) % len(mazalot)]

    def _get_zodiac_sign(self, position: float) -> str:
        """
        Get the zodiac sign for a given position
        """
        # Simplified calculation - in production use proper ephemeris
        signs = [
            "Aries", "Taurus", "Gemini", "Cancer",
            "Leo", "Virgo", "Libra", "Scorpio",
            "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        return signs[int(position) % len(signs)]

    def _calculate_prayer_times(self, date: datetime, latitude: float, longitude: float) -> Dict[str, str]:
        """
        Calculate prayer times for the given location
        """
        s = sun(self.location.observer, date=date)
        return {
            "alos": s.dawn().strftime("%H:%M"),
            "sunrise": s.sunrise().strftime("%H:%M"),
            "talit": s.sunrise().strftime("%H:%M"),
            "shacharit": s.sunrise().strftime("%H:%M"),
            "mincha_gedola": s.sunset().strftime("%H:%M"),
            "mincha_ketana": s.sunset().strftime("%H:%M"),
            "plag_hamincha": s.sunset().strftime("%H:%M"),
            "sunset": s.sunset().strftime("%H:%M"),
            "tzeit_hakochavim": s.dusk().strftime("%H:%M")
        }

    def _get_astronomical_events(self, date: datetime) -> list:
        """
        Get astronomical events for the date
        """
        events = []
        
        # Check for lunar eclipses
        if self._is_lunar_eclipse(date):
            events.append({
                "type": "lunar_eclipse",
                "time": date.strftime("%H:%M"),
                "description": "Lunar eclipse visible"
            })
            
        # Check for solar eclipses
        if self._is_solar_eclipse(date):
            events.append({
                "type": "solar_eclipse",
                "time": date.strftime("%H:%M"),
                "description": "Solar eclipse visible"
            })
            
        return events

    def _is_lunar_eclipse(self, date: datetime) -> bool:
        """
        Check if there's a lunar eclipse on the date
        """
        # Simplified check - in production use proper ephemeris
        return False  # Implement proper calculation

    def _is_solar_eclipse(self, date: datetime) -> bool:
        """
        Check if there's a solar eclipse on the date
        """
        # Simplified check - in production use proper ephemeris
        return False  # Implement proper calculation

# Create a singleton instance
astronomy_calculator = AstronomyCalculator()
