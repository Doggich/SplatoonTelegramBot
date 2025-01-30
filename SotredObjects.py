from typing import Any, List, Dict, Iterator, Tuple, Optional


class Link:
    def __init__(self) -> None:
        self.box: List[Any] = []

    def add(self, object_: Any) -> None:
        self.box.append(object_)

    def remove(self, index: int) -> None:
        self.box.pop(index)

    def get(self) -> List[Any]:
        return self.box

    def all(self) -> List[Any]:
        return self.box

    def __str__(self) -> str:
        return ", ".join(str(box) for box in self.box)

    def __len__(self) -> int:
        return len(self.box)

    def __getitem__(self, index: int) -> Any:
        return self.box[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self.box[index] = value

    def __delitem__(self, index: int) -> None:
        del self.box[index]

    def __iter__(self) -> Iterator[Any]:
        return iter(self.box)


class Box:
    def __init__(self, rows_names: Optional[List[str]] = None, values: Optional[List[Any]] = None) -> None:
        if rows_names is None or values is None:
            self.rows_names: List[str] = []
            self.values: List[Any] = []
            self.box: Dict[str, Any] = {}
        else:
            self.rows_names = rows_names
            self.values = values
            self.box = {key: value for key, value in zip(self.rows_names, self.values)}

    def call(self) -> Dict[str, Any]:
        return self.box

    def add(self, row_name: str, value: Any) -> None:
        self.box[row_name] = value

    def clear(self) -> None:
        self.rows_names = []
        self.values = []
        self.box = {}

    def __str__(self) -> str:
        return ", ".join(f"{key}: {value}" for key, value in self.box.items())

    def __getitem__(self, key: str) -> Any:
        return self.box[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.box[key] = value

    def __delitem__(self, key: str) -> None:
        del self.box[key]

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        return iter(self.box.items())
