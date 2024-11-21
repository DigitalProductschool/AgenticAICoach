from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests

class AirQualityToolInput(BaseModel):
    """Input schema for AirQualityTool."""
    latitude: str = Field(..., description="Latitude of the location.")
    longitude: str = Field(..., description="Longitude of the location.")

class AirQualityTool(BaseTool):
    name: str = "Air Quality Tool"
    description: str = (
        "Get air quality data for a specific location."
    )
    args_schema: Type[BaseModel] = AirQualityToolInput

    def _run(self, latitude: str, longitude: str) -> str:
        get_api_url = f'https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&hourly=pm10,pm2_5'
        response = requests.get(get_api_url)
        response_json = response.json()
        time = response_json['hourly']['time']
        pm10 = response_json['hourly']['pm10']
        pm2_5 = response_json['hourly']['pm2_5']

        # Filter out non-null values and keep the last 4
        filtered_pm10 = [(t, p) for t, p in zip(time, pm10) if p is not None][-4:]
        filtered_pm2_5 = [(t, p) for t, p in zip(time, pm2_5) if p is not None][-4:]

        # Create dictionaries
        pm10_dict = {t: p for t, p in filtered_pm10}
        pm2_5_dict = {t: p for t, p in filtered_pm2_5}

        # Output the dictionaries
        result = {
            "pm10": pm10_dict,
            "pm2_5": pm2_5_dict
        }

        return result
    