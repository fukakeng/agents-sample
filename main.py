import asyncio

import httpx
from agents import Agent, Runner, function_tool


async def main():
    movie_agent = Agent(
        name="Movie critic", 
        instructions="あなたは映画評論家です。キーワードに合う映画のおすすめを3つ教えてください", 
        model="gpt-5-mini"
    )
    whether_agent = Agent(
        name="Whether agent",
        instructions="あなたは天気情報を提供するエージェントです。対応外の地域の場合は非対応であることを伝えて終了してください。",
        model="gpt-5-mini",
        tools=[fetch_whether],
    )
    triage_agent = Agent(
        name="Triage Agent",
        instructions="質問内容に応じて、適切なエージェントへハンドオフしてください。",
        handoffs=[movie_agent, whether_agent],
        model="gpt-5-mini",
    )

    result = await Runner.run(triage_agent, "東京の天気を教えてください。")
    print(result.final_output)

    print("--------------------------------------------------")

    result = await Runner.run(triage_agent, "千葉の天気を教えてください。")
    print(result.final_output)

    print("--------------------------------------------------")

    result = await Runner.run(triage_agent, "SFアクション映画について教えてください。")
    print(result.final_output)


@function_tool
def fetch_whether(city: str) -> str:
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
