from fastapi import APIRouter
from datetime import datetime, timedelta
from typing import Dict, Any
from app.utils.sefaria import sefaria_api
from app.utils.hebrew_date import hebrew_date_calculator
from app.utils.astronomy import astronomy_calculator
from app.utils.visualizations import moon_visualizer, tide_visualizer, sefirot_visualizer

router = APIRouter()

@router.get("/weekly-parsha")
async def get_weekly_parsha() -> Dict[str, Any]:
    """
    Get the current weekly parsha with comprehensive spiritual insights
    """
    current_date = datetime.now()
    
    # Get Hebrew date information
    hebrew_date = hebrew_date_calculator.get_hebrew_date(current_date)
    
    # Get parsha information from Sefaria
    parsha_info = sefaria_api.get_parsha(current_date)
    parsha_name = parsha_info.get("parsha", "")
    
    # Get all related texts
    related_texts = sefaria_api.get_related_texts(f"Torah.{parsha_name}")
    
    # Get astronomical data
    astronomical_data = astronomy_calculator.get_astronomical_data(
        current_date,
        latitude=31.7683,  # Jerusalem coordinates
        longitude=35.2137
    )
    
    # Get visualizations
    moon_visual = astronomy_calculator.get_moon_visual(
        astronomical_data["moon"]["phase"]["percentage"],
        astronomical_data["moon"]["phase"]["name"]
    )
    
    tide_visual = astronomy_calculator.get_tide_visual({
        "high_tide": astronomical_data["astronomical_events"].get("high_tide", 0),
        "low_tide": astronomical_data["astronomical_events"].get("low_tide", 0)
    })
    
    # Get Sefirot visualization if text mentions sefirot
    highlighted_sefirot = []
    if related_texts:
        text = related_texts.get("rashi", {}).get("text", "")
        if "keter" in text.lower(): highlighted_sefirot.append("Keter")
        if "chochmah" in text.lower(): highlighted_sefirot.append("Chochmah")
        if "binah" in text.lower(): highlighted_sefirot.append("Binah")
        if "chesed" in text.lower(): highlighted_sefirot.append("Chesed")
        if "gevurah" in text.lower(): highlighted_sefirot.append("Gevurah")
        if "tiferet" in text.lower(): highlighted_sefirot.append("Tiferet")
        if "netzach" in text.lower(): highlighted_sefirot.append("Netzach")
        if "hod" in text.lower(): highlighted_sefirot.append("Hod")
        if "yesod" in text.lower(): highlighted_sefirot.append("Yesod")
        if "malchut" in text.lower(): highlighted_sefirot.append("Malchut")
    
    sefirot_visual = sefirot_visualizer.create_sefirot_tree(highlighted_sefirot)
    
    parsha_data = {
        "parsha_name": parsha_name,
        "hebrew_date": hebrew_date,
        "english_date": current_date.strftime("%Y-%m-%d"),
        "parsha_text": related_texts.get("rashi", {}).get("text", ""),
        "related_texts": related_texts,
        "astronomical_data": astronomical_data,
        "visualizations": {
            "moon": moon_visual,
            "tide": tide_visual,
            "sefirot": sefirot_visual
        },
        "spiritual_significance": {
            "omer_day": hebrew_date.get("omer_day"),
            "is_holiday": hebrew_date.get("is_holiday"),
            "moon_phase": astronomical_data["moon"].get("phase", {}).get("name"),
            "current_mazal": astronomical_data["moon"].get("constellation"),
            "zodiac_positions": astronomical_data["zodiac_positions"],
            "prayer_times": astronomical_data["prayer_times"],
            "astronomical_events": astronomical_data["astronomical_events"]
        }
    }
    """
    Get the current weekly parsha with comprehensive spiritual insights
    """
    current_date = datetime.now()
    
    # Get Hebrew date information
    hebrew_date = hebrew_date_calculator.get_hebrew_date(current_date)
    
    # Get parsha information from Sefaria
    parsha_info = sefaria_api.get_parsha(current_date)
    parsha_name = parsha_info.get("parsha", "")
    
    # Get all related texts
    related_texts = sefaria_api.get_related_texts(f"Torah.{parsha_name}")
    
    # Get astronomical data
    astronomical_data = astronomy_calculator.get_astronomical_data(
        current_date,
        latitude=31.7683,  # Jerusalem coordinates
        longitude=35.2137
    )
    
    parsha_data = {
        "parsha_name": parsha_name,
        "hebrew_date": hebrew_date,
        "english_date": current_date.strftime("%Y-%m-%d"),
        "parsha_text": related_texts.get("rashi", {}).get("text", ""),
        "related_texts": related_texts,
        "astronomical_data": astronomical_data,
        "spiritual_significance": {
            "omer_day": hebrew_date.get("omer_day"),
            "is_holiday": hebrew_date.get("is_holiday"),
            "moon_phase": astronomical_data["moon"].get("phase", {}).get("name"),
            "current_mazal": astronomical_data["moon"].get("constellation"),
            "zodiac_positions": astronomical_data["zodiac_positions"],
            "prayer_times": astronomical_data["prayer_times"],
            "astronomical_events": astronomical_data["astronomical_events"]
        }
    }
    
    # Add error handling
    if "error" in parsha_info:
        parsha_data["error"] = parsha_info["error"]
    if "error" in hebrew_date:
        parsha_data["error"] = hebrew_date["error"]
    if "error" in astronomical_data:
        parsha_data["error"] = astronomical_data["error"]
    
    return parsha_data

@router.get("/astronomy/{date}")
async def get_astronomy_data(date: str, latitude: float = 31.7683, longitude: float = 35.2137) -> Dict[str, Any]:
    """
    Get astronomical data for a specific date and location
    """
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        return astronomy_calculator.get_astronomical_data(date_obj, latitude, longitude)
    except ValueError:
        return {"error": "Invalid date format. Please use YYYY-MM-DD"}

@router.get("/hebrew-date/{date}")
async def get_hebrew_date(date: str) -> Dict[str, Any]:
    """
    Get Hebrew date information for a specific date
    """
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        return hebrew_date_calculator.get_hebrew_date(date_obj)
    except ValueError:
        return {"error": "Invalid date format. Please use YYYY-MM-DD"}

def get_hebrew_date(date):
    """Get Hebrew date for a given Gregorian date"""
    try:
        hebrew_date = HebrewDate.from_gregorian(date.year, date.month, date.day)
        return {
            "day": hebrew_date.day,
            "month": hebrew_date.month,
            "year": hebrew_date.year,
            "month_name": hebrew_date.month_name,
            "year_name": hebrew_date.year_name,
            "is_holiday": hebrew_date.is_holiday,
            "omer_day": hebrew_date.omer_day
        }
    except Exception as e:
        return {"error": str(e)}

def get_current_parsha(date):
    """Calculate the current parsha based on the Hebrew date"""
    hebrew_date = HebrewDate.from_gregorian(date.year, date.month, date.day)
    
    # Calculate based on Hebrew date
    # This is a simplified calculation - in production use a proper Hebrew calendar
    # For now, we'll just cycle through the parshiyot
    year_start = datetime(date.year, 9, 1)  # Approximate Rosh Hashanah
    weeks = (date - year_start).days // 7
    return PARSHA_CYCLE[weeks % len(PARSHA_CYCLE)]

def get_sefaria_text(ref: str, language: str = "en"):
    """Get text from Sefaria v3 API"""
    base_url = "https://api.sefaria.org/v3/texts"
    params = {
        "ref": ref,
        "version": "English - Metsudah Linear Bible",
        "context": True
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Process the text
        text = data.get('text', [])
        text = "\n".join(text) if isinstance(text, list) else text
        
        return {
            "text": text,
            "source": "Metsudah Linear Bible",
            "language": language,
            "hebrew_text": data.get('hebrew', [])
        }
    except requests.RequestException as e:
        return {
            "error": str(e),
            "text": "Error fetching text from Sefaria"
        }

def get_kabbalistic_texts(parsha_name: str):
    """Get Kabbalistic texts from Sefaria"""
    return {
        "zohar": get_sefaria_text(f"Zohar.{parsha_name}"),
        "baal_shem_tov": get_sefaria_text(f"Baal Shem Tov.{parsha_name}"),
        "ari": get_sefaria_text(f"Ari.{parsha_name}"),
        "tanya": get_sefaria_text(f"Tanya.{parsha_name}")
    }

def get_mazalot(date):
    """Get current mazalot (constellations) based on date"""
    observer = ephem.Observer()
    observer.date = date.strftime('%Y/%m/%d')
    
    # Calculate positions
    sun = Sun()
    moon = Moon()
    
    sun.compute(observer)
    moon.compute(observer)
    
    return {
        "sun": {
            "position": sun.alt,
            "constellation": get_constellation(sun.alt)
        },
        "moon": {
            "position": moon.alt,
            "phase": moon.phase,
            "constellation": get_constellation(moon.alt)
        }
    }

def get_constellation(position):
    """Get the zodiac constellation based on position"""
    # This is a simplified implementation
    # In production, use proper astronomical calculations
    constellations = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return constellations[int(position) % len(constellations)]

def get_chassidic_insights(parsha_name: str):
    """Get Chassidic insights"""
    return [
        {
            "title": "Chassidic Perspective",
            "content": "Placeholder for Chassidic insights",
            "source": "Chabad.org"
        },
        {
            "title": "Tanya Insights",
            "content": "Placeholder for Tanya insights",
            "source": "Tanya Online"
        }
    ]

def get_kabbalistic_insights(parsha_name: str):
    """Get Kabbalistic insights"""
    return [
        {
            "title": "Zohar Insights",
            "content": "Placeholder for Zohar insights",
            "source": "Zohar Online"
        },
        {
            "title": "Ari Insights",
            "content": "Placeholder for Ari insights",
            "source": "Ari Institute"
        }
    ]

router = APIRouter()

@router.get("/weekly-parsha")
async def get_weekly_parsha() -> Dict[str, Any]:
    """
    Get the current weekly parsha with comprehensive spiritual insights
    """
    current_date = datetime.now()
    
    # Get parsha information from Sefaria
    parsha_info = sefaria_api.get_parsha(current_date)
    parsha_name = parsha_info.get("parsha", "")
    
    # Get all related texts
    related_texts = sefaria_api.get_related_texts(f"Torah.{parsha_name}")
    
    # Get Hebrew date
    hebrew_date = {
        "day": current_date.day,
        "month": current_date.month,
        "year": current_date.year,
        "month_name": "",  # TODO: Implement proper Hebrew month name
        "year_name": "",   # TODO: Implement proper Hebrew year name
        "is_holiday": False,
        "omer_day": None
    }
    
    # Get astronomical data
    mazalot = {
        "sun": {
            "position": None,
            "constellation": ""  # TODO: Implement proper constellation calculation
        },
        "moon": {
            "position": None,
            "phase": None,
            "constellation": ""  # TODO: Implement proper constellation calculation
        }
    }
    
    parsha_data = {
        "parsha_name": parsha_name,
        "hebrew_date": hebrew_date,
        "english_date": current_date.strftime("%Y-%m-%d"),
        "parsha_text": related_texts.get("rashi", {}).get("text", ""),
        "related_texts": related_texts,
        "astronomical_data": mazalot,
        "spiritual_significance": {
            "omer_day": hebrew_date.get("omer_day"),
            "is_holiday": hebrew_date.get("is_holiday"),
            "moon_phase": mazalot["moon"].get("phase"),
            "current_mazal": mazalot["moon"].get("constellation")
        }
    }
    
    # Add error handling
    if "error" in parsha_info:
        parsha_data["error"] = parsha_info["error"]
    
    return parsha_data

@router.get("/astronomy")
async def get_astronomy_data() -> Dict[str, Any]:
    """
    Get current astronomical data relevant to Jewish observance
    """
    current_date = datetime.now()
    
    # Add actual astronomical calculations
    # This would require integration with an astronomy API
    
    astronomy_data = {
        "date": current_date.strftime("%Y-%m-%d"),
        "moon_phase": "New Moon",  # Placeholder
        "moon_age": 0,  # Placeholder
        "mazalot": "Taurus",  # Placeholder
        "astronomical_events": []
    }
    return astronomy_data
