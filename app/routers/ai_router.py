from openai.types.responses import response
import threading
import time

from fastapi import APIRouter

from app.dependencies import AiServiceDep
from app.schemas.ai import AskRequest, AskResponse

router = APIRouter(prefix="/api/ai", tags=["AI"])

def log(handler: str, message: str) -> None:
    now = time.strftime("%H:%M:%S")
    thread = threading.current_thread().name
    print(f"{now} [{handler}] {message} (thread: {thread})")

@router.post("/ask/sync", summary="1) def 핸들러 + 동기 클라이언트")
def ask_sync(request: AskRequest, service: AiServiceDep) -> AskResponse:
    log("sync", "요청받음")
    response = service.ask(request)
    log("sync", "요청보냄")

    return response

@router.post("/ask/async", summary="2) async def 핸들러 + 비동기 클라이언트")
async def ask_async(request: AskRequest, service: AiServiceDep) -> AskResponse:
    log("async", "요청 받음")
    response = await service.ask_async(request)
    log("sync", "요청보냄")

    return response
