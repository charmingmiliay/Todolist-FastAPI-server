from openai.types.responses import response
from anyio import NoEventLoopError
import asyncio
import time

import openai

from app.core.config import Settings
from app.core.exceptions import AiRequestError

class OpenAiLlmClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.model = settings.openai_model

        if settings.openai_api_key is None:
            raise ValueError("OpenAI_API_KEY가 없어 OpenAI 클라이언트를 만들 수 없습니다.")

        api_key = settings.openai_api_key.get_secret_value()

        self._client = openai.OpenAI(
            api_key=api_key,
            timeout=settings.openai_timeout_seconds,
            max_retries=1,
        )

        self._async_client = openai.AsyncOpenAI(
            api_key=api_key,
            timeout=settings.openai_timeout_seconds,
            max_retries=1,
        )

    def ask(self, instructions: str, question: str) -> str:
        start = time.perf_counter()

        try:
            response = self._client.responses.create(
                model=self.settings.openai_model,
                instructions=instructions,
                input=question,
                max_output_tokens=self.settings.openai_max_output_tokens,
                reasoning={"effort": self.settings.openai_reasoning_effort},
                store=False,
            )
        except openai.OpenAIError as e:
            raise to_ai_request_error(e) from e

        print_usage("ask_async", response, start)

        return response.output_text

    async def ask_async(self, instructions: str, question: str) -> str:
        start = time.perf_counter()

        try:
            response = await self._async_client.responses.create(
                model=self.settings.openai_model,
                instructions=instructions,
                input=question,
                max_output_tokens=self.settings.openai_max_output_tokens,
                reasoning={"effort": self.settings.openai_reasoning_effort},
                store=False,
            )
        except openai.OpenAIError as e:
            raise to_ai_request_error(e) from e

        print_usage("ask_async", response, start)

        return response.output_text

    async def close(self) -> None:
        self._client.close()
        await self._async_client.close()

def print_usage(method: str, response, start: float) -> None:
    elapsed_ms = int((time.perf_counter() - start) * 1000)

    usage = response.usage

    if usage is not None:
        print(f"[OpenAiLlmClient.{method}] model={response.model}, "
            f"입력 토큰={usage.input_tokens}, 출력 토큰={usage.output_tokens}, {elapsed_ms}ms")

def to_ai_request_error(e: openai.OpenAIError) -> AiRequestError:
    if isinstance(e, openai.AuthenticationError):
        return AiRequestError("OpenAI API 키가 올바르지 않습니다. OPENAI_API_KEY를 확인하세요.")

    if isinstance(e, openai.RateLimitError):
        return AiRequestError("OpenAI 요청 한도를 넘었거나 충전 잔액이 부족합니다.")

    if isinstance(e, openai.APITimeoutError):
        return AiRequestError("OpenAI 응답이 제한 시간 안에 오지 않았습니다.")

    if isinstance(e, openai.APIConnectionError):
        return AiRequestError("OpenAI 서버에 연결할 수 없습니다.")

    return AiRequestError(f"OpenAI 호출 실패 : {e}")

class FakeLlmClient:
    def __init__(self, settings: Settings):
        self.delay_seconds = settings.fake_llm_delay_seconds
        self.model = "fake-llm"

    def ask(self, instructions: str, question: str) -> str:
        time.sleep(self.delay_seconds)
        return f"(가짜 응답) '{question}'에 대한 응답입니다. {self.delay_seconds}초 기다렸습니다."

    async def ask_async(self, instructions: str, question: str) -> str:
        await asyncio.sleep(self.delay_seconds)
        return f"(가짜 응답) '{question}'에 대한 응답입니다. {self.delay_seconds}초 기다렸습니다."

    async def close(self) -> None:
        pass

LlmClient = OpenAiLlmClient | FakeLlmClient
