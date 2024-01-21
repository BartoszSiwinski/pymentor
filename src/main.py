import json

from matching import get_mentor_mentee_pairs, get_mentors_and_mentees


def get_list_of_participants(file_path) -> list[dict[str, [str, int]]]:
    with open(file_path) as f:
        data = json.load(f)
    return data


def main():
    participants = get_list_of_participants('../data_from_excel.json')
    mentors, mentees = get_mentors_and_mentees(participants)
    results = get_mentor_mentee_pairs(mentors, mentees)

    for mentor, mentee in results:
        print(mentor.person.email_address, mentor.expertise.keys())
        print(mentee.person.email_address, mentee.interests.keys())
        print()

    assigned_mentees = [x[1] for x in results]
    unassigned_mentees = [x for x in mentees if x not in assigned_mentees]
    assigned_mentors = [x[0] for x in results]
    unassigned_mentors = [x for x in mentors if x not in assigned_mentors]

    print([(mentor.person.email_address, mentor.expertise.keys()) for mentor in unassigned_mentors])
    print([(mentee.person.email_address, mentee.interests.keys()) for mentee in unassigned_mentees])


if __name__ == '__main__':
    main()
