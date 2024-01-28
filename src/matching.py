from typing import Optional

import networkx as nx

from src.participants import Mentee, Mentor, Person
from src.matching_conditions import (
    are_mentor_and_mentee_a_match_under_conditions,
    TYPE_FOR_FUNCTION_CHECKING_MATCHING_CONDITION
)


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


def get_mentor_mentee_pairs(
        mentors: list[Mentor],
        mentees: list[Mentee],
        matching_conditions: list[TYPE_FOR_FUNCTION_CHECKING_MATCHING_CONDITION]
) -> list[tuple[Mentor, Mentee]]:
    graph = nx.Graph()

    graph.add_nodes_from(mentors)
    graph.add_nodes_from(mentees)

    for mentor in mentors:
        for mentee in mentees:
            if are_mentor_and_mentee_a_match_under_conditions(mentor, mentee, matching_conditions):
                graph.add_edge(mentor, mentee)

    results: list[tuple[Mentor, Mentee]] = list(
        filter(
            lambda x: isinstance(x[0], Mentor),
            nx.bipartite.maximum_matching(graph, top_nodes=mentors).items()
        )
    )

    return results
