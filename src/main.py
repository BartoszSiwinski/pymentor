import json

import networkx as nx

from src.data_classes import Mentee, Mentor, Person


def get_list_of_participants() -> list[dict[str, [str, int]]]:
    with open('data.json') as f:
        data = json.load(f)
    return data


def get_mentors_and_mentees(
        participants: list[dict[str, [str, int]]]
) -> tuple[list[Mentor], list[Mentee]]:
    mentors = []
    mentees = []
    for participant in participants:
        person = Person(
            first_name=participant["first_name"],
            last_name=participant["last_name"],
            email_address=participant["email_address"]
        )
        if (participant["role"].lower() == 'mentee'
                or participant["role"].lower == 'Both - Mentor and Mentee'):
            mentees.append(
                Mentee(person, set(participant["subjects"]))
            )
        elif participant["role"] == 'mentor':
            for capacity_id in range(participant["capacity"]):
                mentors.append(
                    Mentor(person, set(participant["subjects"]), capacity_id))
        else:
            raise ValueError(
                f"Incorrect entity type. Should be 'mentor' or 'mentee', but"
                f" is '${participant['role']}'"
            )
    return mentors, mentees


def get_mentor_mentee_pairs(mentors, mentees) -> list[tuple[Mentor, Mentee]]:
    graph = nx.Graph()

    graph.add_nodes_from(mentors)
    graph.add_nodes_from(mentees)

    for mentor in mentors:
        for mentee in mentees:
            if (
                # mentor.person.years_of_experience >= mentee.person.years_of_experience
                # and mentor.person.region != mentee.person.region
                mentor.person.region != mentee.person.region
                and mentor.expertise.intersection(mentee.interests)
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


def main():
    participants = get_list_of_participants()
    mentors, mentees = get_mentors_and_mentees(participants)
    results = get_mentor_mentee_pairs(mentors, mentees)

    for mentor, mentee in results:
        print(mentor.person.email_address, mentor.expertise)
        print(mentee.person.email_address, mentee.interests)
        print()

    assigned_mentees = [x[1] for x in results]
    unassigned_mentees = [x for x in mentees if x not in assigned_mentees]
    assigned_mentors = [x[0] for x in results]
    unassigned_mentors = [x for x in mentors if x not in assigned_mentors]

    print(unassigned_mentors)
    print(unassigned_mentees)


if __name__ == '__main__':
    main()
