from agents import Agent, WebSearchTool

from function_tools import fetch_city_id, fetch_weather


__movie_agent = Agent(
    name="Movie critic", 
    instructions="あなたは映画評論家です。キーワードに合う映画のおすすめを3つ教えてください", 
)

__weather_agent = Agent(
        name="weather agent",
        instructions="""
        あなたは天気情報を提供するエージェントです。指定された地域のidをツールを使って特定し、その地域の天気情報を取得して提供してください。
        地域がツールでうまく特定できなかった場合は、WEB検索して天気を調べて提供してください。
        回答は必ず全ての調査が終了してから行ってください。
        """,
        tools=[fetch_city_id, fetch_weather, WebSearchTool()],
    )


def _get_movie_agent(model: str) -> Agent:
    __movie_agent.model = model
    return __movie_agent


def _get_weather_agent(model: str) -> Agent:
    __weather_agent.model = model
    return __weather_agent


def get_triage_agent(model: str) -> Agent:
    return Agent(
        name="Triage Agent",
        instructions="質問内容に応じて、適切なエージェントへハンドオフしてください。",
        handoffs=[_get_movie_agent(model), _get_weather_agent(model)],
    )