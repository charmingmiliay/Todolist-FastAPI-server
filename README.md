# Todolist FastAPI Server

FastAPI로 만든 할 일 목록 API입니다. 할 일을 등록하고 조회할 수 있으며, 일정과 관련된 질문에 답하는 AI API도 제공합니다.

## 주요 기능

- 할 일 전체 조회, 번호로 단일 조회, 새 할 일 등록
- OpenAI API를 이용한 일정 관련 질의응답
- 동기(`def`)와 비동기(`async def`) AI 엔드포인트 비교
- API 키 없이 동작하는 가짜 LLM 모드
- FastAPI의 Swagger UI를 통한 API 확인 및 테스트

> **데이터 저장 방식:** 할 일은 서버 프로세스의 메모리에 저장됩니다. 서버를 재시작하면 새로 등록한 할 일은 사라지고 초기 예시 5개로 돌아갑니다. 현재 데이터베이스 연동, 수정, 삭제 기능은 없습니다.

## 기술 스택

- Python 3.14 이상
- FastAPI, Pydantic, pydantic-settings
- OpenAI Python SDK (AI 응답)
- uv (의존성 관리)

현재 코드에서는 LangChain을 사용하지 않습니다. AI 기능은 OpenAI SDK의 Responses API를 직접 호출합니다.

## 실행 방법

Python 3.14 이상과 [uv](https://docs.astral.sh/uv/getting-started/installation/)를 설치한 뒤 다음 명령을 실행합니다.

```bash
git clone https://github.com/charmingmiliay/Todolist-FastAPI-server.git
cd Todolist-FastAPI-server
uv sync
```

프로젝트 루트의 `.env.example`을 `.env`로 복사하고 필요에 따라 값을 수정합니다. API 키가 없어도 가짜 LLM으로 AI API를 시험할 수 있습니다.

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

서버를 시작합니다.

```bash
uv run uvicorn app.main:app --reload
```

- API 문서: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## 환경 변수

주요 설정은 `.env.example`에 정리되어 있습니다.

| 변수 | 설명 |
| --- | --- |
| `OPENAI_API_KEY` | 실제 OpenAI 응답에 사용할 API 키. 없으면 가짜 LLM을 사용합니다. |
| `OPENAI_MODEL` | 실제 OpenAI 요청에 사용할 모델 이름 |
| `OPENAI_REASONING_EFFORT` | 추론 수준 |
| `OPENAI_MAX_OUTPUT_TOKENS` | AI 응답의 최대 출력 토큰 수 |
| `OPENAI_TIMEOUT_SECONDS` | OpenAI 응답 대기 시간(초) |
| `FAKE_LLM` | `true`이면 API 키가 있어도 가짜 LLM을 사용합니다. |
| `FAKE_LLM_DELAY_SECONDS` | 가짜 LLM의 응답 지연 시간(초) |
| `THREAD_POOL_SIZE` | 동기 핸들러 실험을 위한 스레드 풀 크기(선택 사항) |

실제 OpenAI 응답을 사용하려면 `OPENAI_API_KEY`를 환경 변수 또는 `.env`에 설정하고 `FAKE_LLM=false`로 둡니다. API 키나 `.env` 파일은 Git에 커밋하지 마세요.

## API

### 할 일 목록

| 메서드 | 경로 | 기능 |
| --- | --- | --- |
| `GET` | `/api/lists` | 전체 할 일 조회 |
| `GET` | `/api/lists/{list_code}` | 번호로 할 일 하나 조회 |
| `POST` | `/api/lists` | 할 일 등록 (`201 Created`) |

할 일 등록 요청 예시:

```json
{
  "listTitle": "운동하기",
  "listCategory": 1,
  "listStatus": "Yet",
  "listColumn": "저녁에 30분 걷기"
}
```

`listTitle`은 2~30자, `listCategory`는 1 이상의 정수입니다. `listStatus`는 `Yet` 또는 `Done`이며 생략하면 `Yet`입니다. `listColumn`은 선택 사항으로 최대 300자입니다. 코드에 정의된 카테고리 예시는 `1` 의식주, `2` 학원·공부, `3` 심부름입니다. 요청과 응답의 필드 이름은 `camelCase`를 사용합니다.

등록 응답 예시:

```json
{
  "listTitle": "운동하기",
  "listCategory": 1,
  "listStatus": "Yet",
  "listColumn": "저녁에 30분 걷기"
}
```

현재 응답에는 생성된 `listCode`가 포함되지 않습니다. 존재하지 않는 번호를 조회하면 `404`가 반환됩니다.

### AI 질의응답

| 메서드 | 경로 | 기능 |
| --- | --- | --- |
| `POST` | `/api/ai/ask/sync` | 동기 방식으로 질문 |
| `POST` | `/api/ai/ask/async` | 비동기 방식으로 질문 |

두 엔드포인트의 요청·응답 형식은 같습니다.

요청 예시:

```json
{
  "question": "오늘 할 일을 어떻게 정리하면 좋을까요?"
}
```

응답 형식:

```json
{
  "answer": "질문에 대한 응답",
  "model": "fake-llm"
}
```

`question`은 1~500자입니다. 가짜 LLM을 사용하면 `model`은 `fake-llm`이며 실제 OpenAI 응답의 내용은 모델과 질문에 따라 달라집니다.

## 프로젝트 구조

```text
app/
├── main.py                 # FastAPI 앱 및 시작·종료 처리
├── routers/                # 할 일 및 AI API 경로
├── schemas/                # 요청·응답 모델
├── services/               # 비즈니스 로직
├── repositories/           # 메모리 기반 할 일 저장소
├── clients/                # 실제·가짜 LLM 클라이언트
├── core/                   # 환경 설정 및 예외 처리
└── domain/                 # 할 일 데이터 모델
```
