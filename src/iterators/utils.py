from dataclasses import dataclass, field
from itertools import batched
from typing import Iterable, TypeAlias

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = [i for i in range(0, 10)]
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData:
    def __init__(self, per_page: int = 3):
        self.per_page = per_page

    def __iter__(self):
        def generator():
            page_num = 1
            while True:
                page = request(Query(per_page=self.per_page, page=page_num))
                for item in page.results:
                    yield item
                if page.next is None:
                    break
                page_num = page.next
        return generator()


class Fibo:
    def __init__(self, n: int):
        self.n = n
        self.index = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.n:
            raise StopIteration

        value = self.a

        self.a, self.b = self.b, self.a + self.b
        self.index += 1

        return value
