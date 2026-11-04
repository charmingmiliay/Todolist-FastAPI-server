from typing import Annotated

from fastapi import Depends, Request

from app.clients.llm_client import LlmClient
from app.repositories.list_repository import ListRepository
from app.services.ai_service import AiService
from app.services.list_services import ListService

list_repository = ListRepository()

def get_list_repository() -> ListRepository:
    return list_repository

def get_list_service(repository: Annotated[ListRepository, Depends(get_list_repository)]) -> ListService:
    return ListService(repository)

ListServiceDep = Annotated[ListService, Depends(get_list_service)]

def get_llm_client(request: Request) -> LlmClient:
    return request.app.state.llm_client

def get_ai_service(llm_client: Annotated[LlmClient, Depends(get_llm_client)]) -> AiService:
    return AiService(llm_client)

AiServiceDep = Annotated[AiService, Depends(get_ai_service)]
