from agents import GuardrailFunctionOutput, function_tool, input_guardrail
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


@input_guardrail
def guardrail_input(context, agent, input: str) -> GuardrailFunctionOutput:
    """入力に対するガードレールを適用する"""
    return GuardrailFunctionOutput(
        output_info="不適切な入力です。",
        tripwire_triggered=(input == "不適切な入力"),
    )