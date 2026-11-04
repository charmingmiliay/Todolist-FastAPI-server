from fastapi import APIRouter

from app.dependencies import ListServiceDep
from app.schemas.list import ListcreateRequest, ListReaponse

router = APIRouter(
    prefix="/api/lists",
    tags=["목록"]
)

# 전체 목록 조회
@router.get("", summary="목록 전체 조회")
def find_lists(service: ListServiceDep) -> list[ListReaponse]:
    return service.find_lists()

# 단일 목록 조회
@router.get("/{list_code}", summary="목록 하나 조회")
def find_list(list_code: int, service: ListServiceDep) -> ListReaponse:
    return service.find_list(list_code)

# 목록 추가
@router.post("", status_code = 201, summary="목록 추가")
def register_list(request: ListcreateRequest, service: ListServiceDep) -> ListReaponse:
    return service.register_list(request)
