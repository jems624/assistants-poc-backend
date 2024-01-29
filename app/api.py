import openai

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.settings import settings
from app.schemas import MessageRequest

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
async def list_messages(thread_id: str):
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
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
        instructions="Limit your response to 500 characters or less. All your reponses must be in rhyme.",
    )
    return run

@app.get("/threads/{thread_id}/runs/{run_id}", tags=["Runs"])
async def get_run(thread_id: str, run_id: str):
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )
    return run