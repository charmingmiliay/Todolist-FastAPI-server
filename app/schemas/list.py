from typing import Literal

from pydantic import Field

from app.domain.list import List
from app.schemas.base import CamelModel

class ListcreateRequest(CamelModel):
    list_title: str = Field(min_length=2, max_length=30)
    list_category: int = Field(ge=1)
    list_status: Literal["Done", "Yet"] = "Yet"
    list_column: str | None = Field(default=None, max_length=300)

class ListReaponse(CamelModel):
    list_title: str
    list_category: int
    list_status: str
    list_column: str | None

    @classmethod
    def from_list(cls, list: List) -> ListReaponse:

        return cls(
            list_title = list.list_title,
            list_category = list.list_category,
            list_status = list.list_status,
            list_column = list.list_column
        )


# [구경해보기]
# ---------------------------------------------------------------------
# [요청 DTO와 응답 DTO를 나누는 이유]
#
# MenuCreateRequest에는 menu_code가 없고, MenuResponse에는 있다.
# 메뉴 번호는 리소스를 생성할 때 서버(MenuRepository)가 정하는 값이라 클라이언트가 보낼 필요가 없고,
# 반대로 정상적으로 생성되었다면 응답에는 있어야 하기 때문이다.
# DTO 하나로 생성 요청과 응답에 모두 사용해버리면 '요청에서는 무시되는 필드'가 생겨나고,
# /docs 화면의 요청 예시에도 menuCode가 나타나 헷갈린다.
# Spring 프로젝트에서 MenuRequest와 MenuResponse를 나눴던 것과 같은 이유다.
# ---------------------------------------------------------------------
