
from app.clients.llm_client import LlmClient
from app.schemas.ai import AskRequest, AskResponse

INSTRUCTIONS = "너는 사용자의 일정을 관리하는 매니저다. 유저의 질문에 친절하게 세 문장 이내로 답변한다."

class AiService:
    def __init__(self, llm_client: LlmClient):
        self.llm_client = llm_client

    def ask(self, request: AskRequest) -> AskResponse:
        answer = self.llm_client.ask(INSTRUCTIONS, request.question)
        return AskResponse(answer=answer, model=self.llm_client.model)

    async def ask_async(self, request: AskRequest) -> AskResponse:
        answer = await self.llm_client.ask_async(INSTRUCTIONS, request.question)
        return AskResponse(answer=answer, model=self.llm_client.model)
