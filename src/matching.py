import networkx as nx

from participants import Mentee, Mentor
from matching_conditions import (
    are_mentor_and_mentee_a_match_under_conditions,
    TYPE_FOR_FUNCTION_CHECKING_MATCHING_CONDITION
)


def match_mentors_and_mentees(
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
