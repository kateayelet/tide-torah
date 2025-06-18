from fastapi import APIRouter
from datetime import datetime, timedelta
from typing import Dict, Any

router = APIRouter()

@router.get("/shabbat-preparation")
async def get_shabbat_preparation() -> Dict[str, Any]:
    """
    Get Shabbat preparation reminders
    """
    current_date = datetime.now()
    preparation_data = {
        "date": current_date.strftime("%Y-%m-%d"),
        "challah_reminder": {
            "bake_by": (current_date + timedelta(days=1)).strftime("%Y-%m-%d"),
            "cover_reminder": True,
            "blessing_reminder": True
        },
        "candle_lighting": {
            "time": "18:00",
            "blessing_reminder": True
        },
        "practical_tips": [
            "Prepare enough food for all meals",
            "Set up Shabbat table",
            "Prepare kiddush wine and cups",
            "Check candle lighting time"
        ]
    }
    return preparation_data

@router.get("/fast-preparation")
async def get_fast_preparation(fast_name: str) -> Dict[str, Any]:
    """
    Get preparation guidelines for upcoming fasts
    """
    preparation_data = {
        "fast_name": fast_name,
        "hydration_reminder": True,
        "food_preparation": {
            "eat_heavy_meal": True,
            "time": "1-2 hours before fast"
        },
        "practical_tips": [
            "Drink plenty of water before fast",
            "Avoid salty foods before fast",
            "Plan break-fast meal",
            "Know exact fast times"
        ]
    }
    return preparation_data
