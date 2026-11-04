from app.core.exceptions import ListNotFoundError
from app.domain.list import List
from app.repositories.list_repository import ListRepository
from app.schemas.list import ListcreateRequest, ListReaponse

class ListService:
    def __init__(self, repository: ListRepository):
        self.repository = repository

    def find_lists(self) -> list[ListReaponse]:
        lists = self.repository.find_all()

        return [ListReaponse.from_list(list) for list in lists]

    def find_list(self, list_code: int) -> ListReaponse:
        list = self.repository.find_by_code(list_code)

        if list is None:
            raise ListNotFoundError(list_code)

        return ListReaponse.from_list(list)

    def register_list(self, request: ListcreateRequest) -> ListReaponse:
        list = List(
            list_code = 0,
            list_title=request.list_title,
            list_category=request.list_category,
            list_status=request.list_status,
            list_column=request.list_column,
        )

        saved = self.repository.save(list)

        return ListReaponse.from_list(saved)
