from contextlib import asynccontextmanager

import anyio.to_thread
from fastapi import FastAPI

from app.clients.llm_client import FakeLlmClient, OpenAiLlmClient
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.routers import list_router, ai_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    if settings.fake_llm or settings.openai_api_key is None:
        print(f"[lifespan] 가짜 LLM 클라이언틀 사용할 것이다. (FAKE_LLM={settings.fake_llm}), "
            f"키 있음={settings.openai_api_key is None}, 응답까지 {settings.fake_llm_delay_seconds}초)")
        app.state.llm_client = FakeLlmClient(settings)
    else:
        print(f"[lifespan] OpenAI 클라이언트를 사용한다. (model={settings.openai_model})")
        app.state.llm_client = OpenAiLlmClient(settings)

    if settings.thread_pool_size is not None:
        anyio.to_thread.current_default_thread_limiter().total_tokens = settings.thread_pool_size
        print(f"[lifespan] 스레드 풀 크기: {settings.thread_pool_size}개")
    yield

    llm_client = getattr(app.state, "llm_client", None)
    if llm_client is not None:
        await llm_client.close()


app = FastAPI(
    title="채림 todolist FastAPI 서버",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(list_router.router)
app.include_router(ai_router.router)
