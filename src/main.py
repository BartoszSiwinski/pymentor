
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
