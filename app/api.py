import json
import openai

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from inspect import iscoroutinefunction
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput

from app import tools
from app.settings import settings
from app.schemas import MessageRequest
from app.tools import download_webpage

# from app.routers import chat

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = openai.Client(api_key=settings.openai_api_key)

@app.post("/threads", tags=["Threads"])
async def create_thread():
    thread = client.beta.threads.create()
    return thread


@app.get("/threads/{thread_id}/messages", tags=["Messages"])
async def list_messages(thread_id: str, limit: int=10):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
        limit=limit
    )
    return messages

@app.post("/threads/{thread_id}/messages", tags=["Messages"])
async def create_message(thread_id: str, body: MessageRequest):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=body.message
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=settings.openai_assistant_id,
        instructions="Limit your response to 2000 characters or less. Provide links to any sources you used for your response.",
    )
    return {'run': run, 'message': message}

@app.get("/threads/{thread_id}/runs/{run_id}", tags=["Runs"])
async def get_run(thread_id: str, run_id: str):
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )

    # If run is pending action, run the action
    if run.required_action and run.required_action.type == 'submit_tool_outputs':
        tool_outputs = []
        for tool_call in run.required_action.submit_tool_outputs.tool_calls:
            if tool_call.type == 'function':
                # Get function from module by name
                function = getattr(tools, tool_call.function.name)
                if function:
                    # Run function with arguments
                    args = json.loads(tool_call.function.arguments)
                    if iscoroutinefunction(function):
                        output = await function(**args)
                    else:
                        output = function(**args)
                    tool_outputs.append(ToolOutput(
                        tool_call_id=tool_call.id,
                        output=output
                    ))

                # if tool_call.function.name == 'download_webpage':
                #     args = json.loads(tool_call.function.arguments)
                #     html = download_webpage(**args)
                #     tool_outputs.append({
                #         "tool_call_id": tool_call.id,
                #         "output": html
                #     })
        
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )

    return run