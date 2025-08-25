import asyncio

import httpx
from agents import Agent, Runner, WebSearchTool, function_tool


async def main():
    model = "gpt-5-mini"

    movie_agent = Agent(
        name="Movie critic", 
        instructions="あなたは映画評論家です。キーワードに合う映画のおすすめを3つ教えてください", 
        model=model
    )
    weather_agent = Agent(
        name="Weather agent",
        instructions="""
        あなたは天気情報を提供するエージェントです。指定された地域のidをツールを使って特定し、その地域の天気情報を取得して提供してください。
        地域がツールでうまく特定できなかった場合は、WEB検索して天気を調べて提供してください。
        回答は必ず全ての調査が終了してから行ってください。
        """,
        model=model,
        tools=[fetch_city_id, fetch_weather, WebSearchTool()],
    )
    triage_agent = Agent(
        name="Triage Agent",
        instructions="質問内容に応じて、適切なエージェントへハンドオフしてください。",
        handoffs=[movie_agent, weather_agent],
        model=model,
    )

    result = await Runner.run(triage_agent, "明日の東京の天気を教えてください。")
    print(result.final_output)

    print("--------------------------------------------------")

    result = await Runner.run(triage_agent, "明日の箱根町の天気を教えてください。")
    print(result.final_output)

    print("--------------------------------------------------")

    result = await Runner.run(triage_agent, "SFアクション映画について教えてください。")
    print(result.final_output)


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
    

if __name__ == "__main__":
    asyncio.run(main())
