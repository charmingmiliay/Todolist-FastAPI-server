from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class ListNotFoundError(Exception):
    def __init__(self, list_code: int):
        super().__init__(f"해당 메뉴가 존재하지 않습니다. list_code={list_code}")
        self.list_code = list_code

class AiRequestError(Exception):
    pass

def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(ListNotFoundError)
    def handle_list_not_found(request: Request, e: ListNotFoundError):
        return JSONResponse(
            status_code= 404,
            content={
                "code": "ERROR_CODE_00001",
                "description": "조회실패",
                "detail": str(e),
            },
        )

        @app.exception_handler(AiRequestError)
        def handle_ai_request_error(request:Request, e: AiRequestError):
            return JSONResponse(
                status_code = 502,
                content={
                    "code": "ERROR_CODE_00011",
                    "description": "AI 응답실패",
                    "detail": str(e),
                },
            )
