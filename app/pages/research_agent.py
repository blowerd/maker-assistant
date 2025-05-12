import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)

load_dotenv(override=True)  # If you want to explicitly override the environment variable in code regardless of what’s in the terminal

# Ensure your OpenAI key is available
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def load_prompt(filepath):
    with open(filepath, 'r') as f:
        return f.read()

class DIYProjectOutput(BaseModel):
    is_DIY_project: bool
    reasoning: str

guardrail_agent = Agent( 
    name="Guardrail check",
    instructions="Check to see if the user is asking about how to create an object, tools to create an object, or possible project ideas.",
    output_type=DIYProjectOutput,
)

@input_guardrail
async def diy_guardrail( 
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=not result.final_output.is_DIY_project,
    )

# Define your agent
task_generator = Agent(
    name="Workshop Research Assistant",
    instructions=load_prompt('./app/prompts/workshop_assistant.txt'),
    input_guardrails=[diy_guardrail],
)

# Async wrapper for running the agent
async def generate_tasks(goal):
    try:
        result = await Runner.run(task_generator, goal)
        return result.final_output
    except InputGuardrailTripwireTriggered:
        return "I am designed to help you with DIY and workshop knowledge. I'd love to help you answer a question related to those topics!"

# Streamlit UI
st.set_page_config(page_title="AI Workshop Warrior", layout="centered")
st.title("🛠️ Workshop Research Agent")
st.write("Helping weekend warriors with their workshop projects.")

user_goal = st.text_area("Enter your query", placeholder="e.g. How would I build a bookshelf out of white pine?")

if st.button("Generate Tasks"):
    if user_goal.strip() == "":
        st.warning("Please enter a query.")
    else:
        with st.spinner("Finding you some information..."):
            tasks = asyncio.run(generate_tasks(user_goal))
            st.success("Here's your requested information!:")
            st.markdown(f"```text\n{tasks}\n```")