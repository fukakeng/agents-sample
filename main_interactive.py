import asyncio

from agents import run_demo_loop

from agent_getter import get_triage_agent


async def main():
    model = "gpt-4o-mini"
    triage_agent = get_triage_agent(model)
    
    for handoff in triage_agent.handoffs:
        handoff.handoffs = [triage_agent]
    
    await run_demo_loop(triage_agent)
    

if __name__ == "__main__":
    asyncio.run(main())
