from agents import function_tool
import httpx


@function_tool
def fetch_city_id() -> str:
    with httpx.Client() as client:
        response = client.get("https://weather.tsukumijima.net/primary_area.xml")
        return response.text


@function_tool
def fetch_weather(city_id: str) -> str:
    """天気を取得する"""
    if not city_id:
        return "地域を特定できませんでした。"

    with httpx.Client() as client:
        response = client.get(f"https://weather.tsukumijima.net/api/forecast/city/{city_id}")
        return response.text
