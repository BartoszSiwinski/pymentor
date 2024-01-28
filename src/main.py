from read_raw_data import get_processed_data_for_mentoring_program
from mentoring_matcher import MentoringMatcher
from participants import get_mentors_and_mentees
from save_results import save_mentors_to_excel, save_mentees_to_excel, save_mentorship_pairs_excel
import matching_conditions


# Data to change
RAW_DATA_EXCEL_FILE_PATH = 'mentoring_raw_data.xlsx'
RESULTS_FILE_PATH = '../results.xlsx'


def main():
    participants = get_processed_data_for_mentoring_program(
        RAW_DATA_EXCEL_FILE_PATH,
        save_to_json=True
    )
    mentors, mentees = get_mentors_and_mentees(participants)

    mentoring_matcher = MentoringMatcher(mentors, mentees)

    conditions_for_first_round = [
        matching_conditions.check_mentor_and_mentee_are_not_from_the_same_business_unit,
        matching_conditions.check_mentor_has_no_less_experience_than_mentee,
        matching_conditions.get_competency_overlap_checker(1),
        matching_conditions.check_mentor_and_mentee_are_not_the_same_person,
    ]
    mentoring_matcher.match_unassigned(conditions_for_first_round)

    conditions_for_second_round = [
        matching_conditions.check_mentor_and_mentee_are_not_from_the_same_business_unit,
        matching_conditions.check_mentor_has_no_less_experience_than_mentee,
        matching_conditions.get_competency_overlap_checker(2),
        matching_conditions.check_mentor_and_mentee_are_not_the_same_person,
    ]
    mentoring_matcher.match_unassigned(conditions_for_second_round)

    conditions_for_third_round = [
        matching_conditions.get_competency_overlap_checker(),
        matching_conditions.check_mentor_and_mentee_are_not_the_same_person,
    ]
    mentoring_matcher.match_unassigned(conditions_for_third_round)

    save_mentors_to_excel(
        RESULTS_FILE_PATH,
        'all_mentors',
        mentoring_matcher.assigned_mentors,
        mentoring_matcher.unassigned_mentors
    )
    save_mentees_to_excel(
        RESULTS_FILE_PATH,
        'all_mentees',
        mentoring_matcher.assigned_mentees,
        mentoring_matcher.unassigned_mentees
    )
    save_mentorship_pairs_excel(
        RESULTS_FILE_PATH,
        'mentoring_pairs',
        mentoring_matcher.matched_pairs
    )


if __name__ == '__main__':
    main()
