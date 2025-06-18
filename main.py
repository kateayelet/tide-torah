from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
from astral.sun import sun
from astral import LocationInfo
import pytz

app = FastAPI(title="Jewish Spiritual Companion")

class PrayerTimes(BaseModel):
    sunrise: str
    sunset: str
    shacharit: str
    mincha: str
    maariv: str
    tefillin: str

class WeeklyParsha(BaseModel):
    parsha_name: str
    hebrew_name: str
    reading_date: str
    chassidic_insight: str
    kabbalistic_perspective: str

class AstronomicalData(BaseModel):
    moon_phase: str
    tide: str
    mazalot: str

@app.get("/prayer-times/{latitude}/{longitude}", response_model=PrayerTimes)
async def get_prayer_times(latitude: float, longitude: float):
    """Calculate daily prayer times based on location"""
    location = LocationInfo("", "", "Israel", "Asia/Jerusalem")
    location.latitude = latitude
    location.longitude = longitude
    
    s = sun(location.observer, date=datetime.now())
    
    return PrayerTimes(
        sunrise=s.sunrise().strftime("%H:%M"),
        sunset=s.sunset().strftime("%H:%M"),
        shacharit="08:00",  # Adjust based on sunrise
        mincha="16:00",     # Adjust based on sunset
        maariv="19:00",     # Adjust based on sunset
        tefillin="08:00"    # Time for putting on tefillin
    )

@app.get("/weekly-parsha", response_model=WeeklyParsha)
async def get_weekly_parsha():
    """Get the current week's parsha with insights"""
    # Calculate current week's parsha
    current_date = datetime.now()
    
    # This is a simplified example - in a real app you'd have a more sophisticated
    # parsha calculation based on the Hebrew calendar
    parsha_data = {
        "parsha_name": "Korach",
        "hebrew_name": "קרח",
        "reading_date": current_date.strftime("%Y-%m-%d"),
        "chassidic_insight": "The parsha of Korach teaches about the importance of unity and the dangers of divisiveness.",
        "kabbalistic_perspective": "Korach represents the challenge of ego and the need to align with divine will."
    }
    
    return WeeklyParsha(**parsha_data)

@app.get("/astronomical-data", response_model=AstronomicalData)
async def get_astronomical_data():
    """Get astronomical data including moon phase and mazalot"""
    # This is a placeholder - in a real app you'd integrate with an astronomy API
    return AstronomicalData(
        moon_phase="Waxing Gibbous",
        tide="High",
        mazalot="Gemini"
    )

@app.get("/practical-reminders")
async def get_practical_reminders():
    """Get practical reminders for the day/week"""
    current_date = datetime.now()
    
    # Example reminders
    reminders = {
        "today": [
            "Prepare challah for Shabbat" if current_date.weekday() == 4 else None,
            "Hydrate well today as we approach Tisha B'Av" if current_date.month == 7 else None
        ],
        "this_week": [
            "Plan your Shabbat menu",
            "Review this week's parsha"
        ]
    }
    
    return {
        "reminders": {k: [r for r in v if r] for k, v in reminders.items()}
    }
