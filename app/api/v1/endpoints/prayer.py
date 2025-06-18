from fastapi import APIRouter
from datetime import datetime
from astral import LocationInfo
from astral.sun import sun
from pytz import timezone

router = APIRouter()

@router.get("/daily-schedule")
async def get_daily_prayer_schedule(latitude: float, longitude: float, date: str = None):
    """
    Get daily prayer times based on location
    """
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d")
    
    city = LocationInfo("Custom Location", "", "Asia/Jerusalem", latitude, longitude)
    s = sun(city.observer, date=date)
    
    return {
        "date": date.strftime("%Y-%m-%d"),
        "prayer_times": {
            "alos": s.dawn().strftime("%H:%M"),
            "sunrise": s.sunrise().strftime("%H:%M"),
            "talit": s.sunrise().strftime("%H:%M"),
            "shacharit": s.sunrise().strftime("%H:%M"),
            "mincha_gedola": s.sunset().strftime("%H:%M"),
            "mincha_ketana": s.sunset().strftime("%H:%M"),
            "plag_hamincha": s.sunset().strftime("%H:%M"),
            "sunset": s.sunset().strftime("%H:%M"),
            "tzeit_hakochavim": s.dusk().strftime("%H:%M"),
        }
    }

@router.get("/tefillin")
async def get_tefillin_schedule(latitude: float, longitude: float, date: str = None):
    """
    Get tefillin wearing times
    """
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d")
    
    # TODO: Add logic for Chol Hamoed, Yom Tov, etc.
    return {
        "date": date.strftime("%Y-%m-%d"),
        "tefillin_allowed": True,
        "start_time": "07:00",
        "end_time": "13:00"
    }
