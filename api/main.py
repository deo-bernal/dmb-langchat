"""DMB LangChat API — LangChain + durable Convex memory."""

from __future__ import annotations

import logging
import os
import warnings
from typing import Literal

from convex import ConvexClient
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

warnings.filterwarnings("ignore")
os.environ.setdefault("GRPC_VERBOSITY", "ERROR")
os.environ.setdefault("GLOG_minloglevel", "2")
logging.getLogger("google").setLevel(logging.ERROR)

load_dotenv()

CONVEX_URL = (os.getenv("CONVEX_URL") or "").strip()
GOOGLE_API_KEY = (os.getenv("GOOGLE_API_KEY") or "").strip()
OPENAI_API_KEY = (os.getenv("OPENAI_API_KEY") or "").strip()
GEMINI_MODEL = (os.getenv("GEMINI_MODEL") or "gemini-2.0-flash").strip()
OPENAI_MODEL = (os.getenv("OPENAI_MODEL") or "gpt-4o-mini").strip()
CORS_ORIGINS = [
    o.strip()
    for o in (
        os.getenv("CORS_ORIGINS")
        or "http://localhost:5173,http://localhost:4173,https://www.dmbwebsolutions.com,https://dmbwebsolutions.com"
    ).split(",")
    if o.strip()
]
SYSTEM_PROMPT = (
    "You are DMB LangChat, a friendly assistant for DMB Web Solutions. "
    "You remember earlier turns in this thread. Be concise and practical."
)
HISTORY_LIMIT = 40
MODEL_PROVIDER = (
    "gemini"
    if GOOGLE_API_KEY
    else ("openai" if OPENAI_API_KEY else "demo-echo")
)
ACTIVE_MODEL = (
    GEMINI_MODEL
    if MODEL_PROVIDER == "gemini"
    else (OPENAI_MODEL if MODEL_PROVIDER == "openai" else "demo-echo")
)

app = FastAPI(title="DMB LangChat API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def require_convex() -> ConvexClient:
    if not CONVEX_URL or "YOUR_DEPLOYMENT" in CONVEX_URL:
        raise HTTPException(status_code=503, detail="CONVEX_URL is not configured.")
    return ConvexClient(CONVEX_URL)


def require_model() -> BaseChatModel | None:
    if GOOGLE_API_KEY:
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            temperature=0.7,
            google_api_key=GOOGLE_API_KEY,
        )
    if OPENAI_API_KEY:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=0.7,
            api_key=OPENAI_API_KEY,
        )
    return None


def demo_echo_reply(message: str, history_len: int) -> str:
    """Offline fallback so durable Convex memory can be demonstrated without an LLM key."""
    return (
        f"[demo-echo] I stored your message in Convex and can see {history_len} turn(s) "
        f"in this thread (including this one). You said: {message[:240]}"
    )


class ChatRequest(BaseModel):
    sessionId: str = Field(min_length=8, max_length=128)
    threadId: str | None = None
    message: str = Field(min_length=1, max_length=4000)


class ChatResponse(BaseModel):
    threadId: str
    reply: str
    role: Literal["ai"] = "ai"


class CreateThreadRequest(BaseModel):
    sessionId: str = Field(min_length=8, max_length=128)
    title: str | None = None


@app.get("/health")
def health():
    return {
        "ok": True,
        "convexConfigured": bool(CONVEX_URL and "YOUR_DEPLOYMENT" not in CONVEX_URL),
        "modelConfigured": True,
        "modelProvider": MODEL_PROVIDER,
        "model": ACTIVE_MODEL,
    }


@app.post("/threads")
def create_thread(body: CreateThreadRequest):
    client = require_convex()
    thread_id = client.mutation(
        "threads:create",
        {"sessionId": body.sessionId, "title": body.title or "New chat"},
    )
    return {"threadId": thread_id}


@app.post("/chat", response_model=ChatResponse)
def chat(body: ChatRequest):
    client = require_convex()
    model = require_model()

    thread_id = body.threadId
    if not thread_id:
        thread_id = client.mutation(
            "threads:create",
            {"sessionId": body.sessionId, "title": "New chat"},
        )

    thread = client.query("threads:get", {"threadId": thread_id})
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found.")
    if thread.get("sessionId") != body.sessionId:
        raise HTTPException(status_code=403, detail="Thread does not belong to this session.")

    client.mutation(
        "messages:append",
        {"threadId": thread_id, "role": "human", "content": body.message},
    )

    history_rows = client.query("messages:listByThread", {"threadId": thread_id}) or []
    history_rows = history_rows[-HISTORY_LIMIT:]

    if model is None:
        reply_text = demo_echo_reply(body.message, len(history_rows))
    else:
        lc_messages: list = [SystemMessage(content=SYSTEM_PROMPT)]
        for row in history_rows:
            role = row.get("role")
            content = row.get("content") or ""
            if role == "human":
                lc_messages.append(HumanMessage(content=content))
            elif role == "ai":
                lc_messages.append(AIMessage(content=content))
            elif role == "system":
                lc_messages.append(SystemMessage(content=content))

        try:
            reply = (model | StrOutputParser()).invoke(lc_messages)
        except Exception as exc:  # noqa: BLE001 — surface model errors to client
            raise HTTPException(status_code=502, detail=f"Model error: {exc}") from exc
        reply_text = str(reply).strip() or "(empty reply)"

    client.mutation(
        "messages:append",
        {"threadId": thread_id, "role": "ai", "content": reply_text},
    )
    return ChatResponse(threadId=str(thread_id), reply=reply_text)
