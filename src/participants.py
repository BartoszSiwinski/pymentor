from dataclasses import dataclass


@dataclass
class Person:
    fullname: str
    email_address: str
    years_of_experience: int
    business_unit: str

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
    sub_id: int

    def __hash__(self) -> int:
        return hash(f"mentor_{self.person.email_address}_{self.sub_id}")
