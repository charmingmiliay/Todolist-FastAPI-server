from app.domain.list import List

def init_lists() -> list[list]:
    return [
        List(1, "아침밥 먹기", 1, "Yet", "아침밥을 먹으면 힘이 생깁니다."),
        List(2, "양치하기", 1, "Yet", "양치는 필수입니다."),
        List(3, "새 옷으로 갈아입기", 1, "Done", "예쁘게 꼬까옷을 입어봅시다"),
        List(4, "이번주 올출하기", 2, "Yet", "병가가 3개 남았으므로, 결석을 그만해야합니다."),
        List(5, "장보기", 3, "Done", "아버지께서 마늘, 파, 라면을 사오라고 시키심"),
    ]

class ListRepository:
    def __init__(self):
        self._lists: dict[int, List] = {}

        self._next_code = 6

        for list in init_lists():
            self.save(list)

    def find_all(self) -> list[List]:
        return list(self._lists.values())

    def find_by_code(self, list_code: int) -> List | None:
        return self._lists.get(list_code)

    def save(self, list: List) -> List:
        if list.list_code == 0:
            list.list_code = self._next_code
            self._next_code += 1

        self._lists[list.list_code] = list

        return list
