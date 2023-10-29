from dataclasses import dataclass
from typing import Optional


@dataclass
class Person:
    first_name: str
    last_name: str
    email_address: str
    # years_of_experience: Optional[int] = None
    # region: Optional[str] = None


@dataclass
class Mentee:
    person: Person
    interests: set[str]

    def __hash__(self) -> int:
        return hash(f"mentee_{self.person.email_address}")


@dataclass
class Mentor:
    person: Person
    expertise: set[str]
    mentor_sub_id: int

    def __hash__(self) -> int:
        return hash(f"mentor_{self.person.email_address}_{self.mentor_sub_id}")
