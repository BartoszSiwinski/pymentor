from read_raw_data import get_processed_data_for_mentoring_program
from matching import get_mentor_mentee_pairs, get_mentors_and_mentees
from save_results import save_mentors_to_excel, save_mentees_to_excel, save_mentorship_pairs_excel


def main():
    participants = get_processed_data_for_mentoring_program(
        '../mentoring_raw_data.xlsx',
        save_to_json=True
    )

    mentors, mentees = get_mentors_and_mentees(participants)
    mentoring_pairs = get_mentor_mentee_pairs(mentors, mentees)

    assigned_mentees = [x[1] for x in mentoring_pairs]
    unassigned_mentees = [x for x in mentees if x not in assigned_mentees]
    assigned_mentors = [x[0] for x in mentoring_pairs]
    unassigned_mentors = [x for x in mentors if x not in assigned_mentors]

    save_mentors_to_excel(
        '../results.xlsx',
        'all_mentors',
        assigned_mentors, unassigned_mentors
    )
    save_mentees_to_excel(
        '../results.xlsx',
        'all_mentees',
        assigned_mentees, unassigned_mentees
    )
    save_mentorship_pairs_excel(
        '../results.xlsx',
        'mentoring_pairs',
        mentoring_pairs
    )


if __name__ == '__main__':
    main()
