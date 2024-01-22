from pydantic import BaseModel
from typing import Self, cast


class Pill(BaseModel):
    name: str
    comment_permalink: str
    from_user: str
    date: int
    amount: int

    @classmethod
    def from_data(cls, pill: dict[str, str | int | float]) -> Self:
        return cls(
            name=cast(str, pill["name"]),
            comment_permalink=cast(str, pill["commentID"]),
            from_user=cast(str, pill["fromUser"]),
            date=int(pill["date"]),
            amount=cast(int, pill.get("amount", 1)),
        )
