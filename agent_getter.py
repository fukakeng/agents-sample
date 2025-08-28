from agents import Agent, WebSearchTool

from function_tools import fetch_city_id, fetch_weather, guardrail_input


__movie_agent = Agent(
    name="Movie critic", 
    instructions="""
    あなたは映画評論家です。キーワードに合う映画のおすすめを3つ教えてください。
    映画以外の質問は他のエージェントに任せてください
    """,
)

__weather_agent = Agent(
    name="weather agent",
    instructions="""
    あなたは天気情報を提供するエージェントです。指定された地域のidをツールを使って特定し、その地域の天気情報を取得して提供してください。
    地域がツールでうまく特定できなかった場合は、WEB検索して天気を調べて提供してください。
    回答は必ず全ての調査が終了してから行ってください。
    天気以外の質問は他のエージェントに任せてください。
    """,
    tools=[fetch_city_id, fetch_weather, WebSearchTool()],
)

__general_agent = Agent(
    name="general agent",
    instructions="""
    あなたは一般的な質問に答えるエージェントです。
    専門外の質問は他のエージェントに任せるために、回答後は必ずTriage Agentに処理を渡してください。
    """,
    tools=[WebSearchTool()],
)

def _get_movie_agent(model: str) -> Agent:
    __movie_agent.model = model
    return __movie_agent


def _get_weather_agent(model: str) -> Agent:
    __weather_agent.model = model
    return __weather_agent


def _get_general_agent(model: str) -> Agent:
    __general_agent.model = model
    return __general_agent


def get_triage_agent(model: str) -> Agent:
    return Agent(
        name="Triage Agent",
        instructions="""
        質問内容に応じて、以下のルールに従って適切なエージェントへハンドオフしてください。
        映画に関する質問 -> Movie critic
        天気に関する質問 -> Weather agent
        その他の質問 -> General agent
        """,
        model=model,
        handoffs=[_get_movie_agent(model), _get_weather_agent(model), _get_general_agent(model)],
        input_guardrails=[guardrail_input]
    )