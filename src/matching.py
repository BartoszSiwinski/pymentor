import json

import networkx as nx

from src.data_classes import Mentee, Mentor, Person


def get_list_of_participants() -> list[dict[str, [str, int]]]:
    with open('data.json') as f:
        data = json.load(f)
    return data


def have_mentorship_overlap(
        mentor: Mentor,
        mentee: Mentee,
        min_interest_priority_level: int = 999
) -> bool:
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
            full_name=participant["full_name"],
            email_address=participant["email_address"]
        )

        if participant["role"] not in {'mentor', 'mentee', 'both'}:
            raise ValueError(
                f"Incorrect entity type. Should be 'mentor' or 'mentee', but"
                f" is '${participant['role']}'"
            )

        if participant["role"] in {'mentee', 'both'}:
            mentees.append(
                Mentee(person, set(participant["subjects"]))
            )
        if participant["role"] in {'mentor', 'both'}:
            # for capacity_id in range(participant["capacity"]):
            mentors.append(Mentor(person, set(participant["subjects"])))

    return mentors, mentees


def get_mentor_mentee_pairs(
        mentors: list[Mentor],
        mentees: list[Mentee],
        min_engagement_level: int = 0
) -> list[tuple[Mentor, Mentee]]:
    graph = nx.Graph()

    graph.add_nodes_from(mentors)
    graph.add_nodes_from(mentees)

    for mentor in mentors:
        for mentee in mentees:
            if (
                mentor.person.years_of_experience >= mentee.person.years_of_experience
                and mentor.person.region != mentee.person.region
                and have_mentorship_overlap(mentor, mentee, min_engagement_level)
                and mentor.person != mentee.person
            ):
                graph.add_edge(mentor, mentee)

    results: list[tuple[Mentor, Mentee]] = list(
        filter(
            lambda x: isinstance(x[0], Mentor),
            nx.bipartite.maximum_matching(graph, top_nodes=mentors).items()
        )
    )

    return results
