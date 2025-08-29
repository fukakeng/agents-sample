import asyncio

from agents import InputGuardrailTripwireTriggered, Runner

from agent_getter import get_triage_agent
from user_info import UserInfo


async def main():
    model = "gpt-5-mini"
    triage_agent = get_triage_agent(model)

    result = await Runner.run(triage_agent, "明日の東京の天気を教えてください。")
    print(result.final_output)

    print("--------------------------------------------------")

    result = await Runner.run(triage_agent, "明日の箱根町の天気を教えてください。")
    print(result.final_output)

    print("--------------------------------------------------")
    
    user_info = UserInfo(area="横浜")
    result = await Runner.run(triage_agent, "明日の天気を教えてください。", context=user_info)
    print(result.final_output)

    print("--------------------------------------------------")

    result = await Runner.run(triage_agent, "SFアクション映画について教えてください。")
    print(result.final_output)

    print("--------------------------------------------------")

    try:
        result = await Runner.run(triage_agent, "不適切な入力")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print(f"ガードレール作動：{e.guardrail_result.output.output_info}")


if __name__ == "__main__":
    asyncio.run(main())
