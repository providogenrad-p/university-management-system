from dataclasses import dataclass

@dataclass
class Student:
    id: int | None
    name: str
    email: str