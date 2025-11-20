# weather_service.py
import httpx
from typing import Dict
from config import Config

class WeatherServiceError(Exception):
    pass

class WeatherService:
    def __init__(self):
        self.api_key = Config.API_KEY
        self.base_url = Config.BASE_URL
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.timeout = Config.TIMEOUT
    
    async def get_weather(self, city: str) -> Dict:
        if not city: raise WeatherServiceError("City name cannot be empty")
        params = {"q": city, "appid": self.api_key, "units": Config.UNITS}
        return await self._make_request(self.base_url, params)

    async def get_forecast(self, city: str) -> Dict:
        if not city: raise WeatherServiceError("City name cannot be empty")
        params = {"q": city, "appid": self.api_key, "units": Config.UNITS}
        return await self._make_request(self.forecast_url, params)

    async def _make_request(self, url: str, params: Dict) -> Dict:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                if response.status_code != 200:
                    # Try to get error message from API
                    try:
                        err_msg = response.json().get('message', 'Unknown error')
                    except:
                        err_msg = f"Status {response.status_code}"
                    raise WeatherServiceError(err_msg)
                return response.json()
        except httpx.HTTPError as e:
            raise WeatherServiceError(f"Connection error: {str(e)}")
        except Exception as e:
            raise WeatherServiceError(f"An error occurred: {str(e)}")