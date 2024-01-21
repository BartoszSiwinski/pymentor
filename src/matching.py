from typing import Optional

import networkx as nx

from src.data_classes import Mentee, Mentor, Person


def have_mentorship_overlap(
        mentor: Mentor,
        mentee: Mentee,
        min_interest_priority_level: Optional[int] = None
) -> bool:
    if min_interest_priority_level is None:
        min_interest_priority_level = 999

    for interest in mentee.interests:
        if (
                mentee.interests[interest] <= min_interest_priority_level
                and interest in mentor.expertise
                and mentor.expertise[interest] <= min_interest_priority_level
        ):
            return True
    return False


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
            mentors.append(Mentor(person, participant["mentor_expertise"]))

    return mentors, mentees


def get_mentor_mentee_pairs(
        mentors: list[Mentor],
        mentees: list[Mentee],
        min_engagement_level: Optional[int] = None
) -> list[tuple[Mentor, Mentee]]:
    graph = nx.Graph()

    graph.add_nodes_from(mentors)
    graph.add_nodes_from(mentees)

    for mentor in mentors:
        for mentee in mentees:
            if (
                # mentor.person.years_of_experience >= mentee.person.years_of_experience and
                # mentor.person.business_unit != mentee.person.business_unit and
                have_mentorship_overlap(mentor, mentee, min_engagement_level) and
                mentor.person != mentee.person
            ):
                graph.add_edge(mentor, mentee)

    results: list[tuple[Mentor, Mentee]] = list(
        filter(
            lambda x: isinstance(x[0], Mentor),
            nx.bipartite.maximum_matching(graph, top_nodes=mentors).items()
        )
    )

    return results
