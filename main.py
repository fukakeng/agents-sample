import asyncio

from agents import Runner

from agent_getter import get_triage_agent


async def main():
    model = "gpt-5-mini"
    triage_agent = get_triage_agent(model)

    result = await Runner.run(triage_agent, "明日の東京の天気を教えてください。")
    print(result.final_output)

    print("--------------------------------------------------")

    result = await Runner.run(triage_agent, "明日の箱根町の天気を教えてください。")
    print(result.final_output)

    print("--------------------------------------------------")

    result = await Runner.run(triage_agent, "SFアクション映画について教えてください。")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
