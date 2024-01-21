from dataclasses import dataclass
from typing import Optional


@dataclass
class Person:
    full_name: str
    email_address: str
    years_of_experience: Optional[int] = None
    region: Optional[str] = None

    def __hash__(self) -> int:
        return hash(self.email_address)


@dataclass
class Mentee:
    person: Person
    interests: dict[str:int]

    def __hash__(self) -> int:
        return hash(f"mentee_{self.person.email_address}")


@dataclass
class Mentor:
    person: Person
    expertise: dict[str:int]
    # added for future possibility of having one person
    # mentoring multiple mentees
    mentor_sub_id: int = 0

    def __hash__(self) -> int:
        return hash(f"mentor_{self.person.email_address}_{self.mentor_sub_id}")
