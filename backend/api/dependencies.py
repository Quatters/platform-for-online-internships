from backend.settings import LimitOffsetParams


class ListPageParams(LimitOffsetParams):
    search: str | None
    # later would be great to include filters here
