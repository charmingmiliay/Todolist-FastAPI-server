from dataclasses import dataclass

@dataclass
class List:
    # 할 일 번호(PK)
    list_code: int

    # 할 일 제목
    list_title: str

    # 할 일의 카테고리 (1. 의식주, 2. 학원(공부), 3. 심부름)
    list_category: int

    # 할 일의 완료 여부
    list_status: str

    # 할 일의 내용(필수는 아님)
    list_column: str | None = None
