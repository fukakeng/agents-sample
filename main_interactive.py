import asyncio

import httpx
from agents import Agent, Runner, function_tool, run_demo_loop


async def main():
    model = "gpt-4o-mini"

    movie_agent = Agent(
        name="Movie critic", 
        instructions="あなたは映画評論家です。キーワードに合う映画のおすすめを3つ教えてください", 
        model=model
    )
    weather_agent = Agent(
        name="weather agent",
        instructions="あなたは天気情報を提供するエージェントです。対応外の地域の場合は非対応であることを伝えて終了してください。",
        model=model,
        tools=[fetch_weather],
    )
    triage_agent = Agent(
        name="Triage Agent",
        instructions="質問内容に応じて、適切なエージェントへハンドオフしてください。",
        handoffs=[movie_agent, weather_agent],
        model=model,
    )
    movie_agent.handoffs = [triage_agent]
    weather_agent.handoffs = [triage_agent]

    await run_demo_loop(triage_agent)


@function_tool
def fetch_weather(city: str) -> str:
    """東京または埼玉の天気を取得する"""
    # https://weather.tsukumijima.net/primary_area.xml
    city_dict = {
        '東京': '130010',
        '埼玉': '110010'
    }
    city_id = city_dict.get(city)
    if not city_id:
        return "東京と埼玉の天気情報のみ取得可能です。"
    
    with httpx.Client() as client:
        response = client.get(f"https://weather.tsukumijima.net/api/forecast/city/{city_id}")
        return response.text
    

if __name__ == "__main__":
    asyncio.run(main())
