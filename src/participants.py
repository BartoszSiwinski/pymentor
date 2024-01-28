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


def get_mentors_and_mentees(
        participants: list[dict[str, [str, int]]]
) -> tuple[list[Mentor], list[Mentee]]:
    mentors = []
    mentees = []
    for participant in participants:
        person = Person(
            fullname=participant["fullname"],
            email_address=participant["email_address"],
            years_of_experience=participant["years_of_experience"],
            business_unit=participant["business_unit"]
        )

        if participant["role"] not in {'mentor', 'mentee', 'both'}:
            raise ValueError(
                f"Incorrect entity type. Should be 'mentor' or 'mentee', but"
                f" is '${participant['role']}'"
            )

        if participant["role"] in {'mentee', 'both'}:
            mentees.append(Mentee(person, participant["mentee_interests"]))

        if participant["role"] in {'mentor', 'both'}:
            if (
                type(participant["mentor_capacity"]) is not int
                    or participant["mentor_capacity"] < 0
            ):
                raise ValueError(
                    "Value of the field 'mentor_capacity' has to be positive integer."
                    f" Got '{participant['mentor_capacity']}' instead.")
            for i in range(participant["mentor_capacity"]):
                mentors.append(Mentor(person, participant["mentor_expertise"], i))

    return mentors, mentees
