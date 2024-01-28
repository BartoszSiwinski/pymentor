from typing import Optional, Callable

from participants import Mentor, Mentee


TYPE_FOR_FUNCTION_CHECKING_MATCHING_CONDITION = Callable[[Mentor, Mentee], bool]


def get_competency_overlap_checker(
        min_interest_priority_level: Optional[int] = None
) -> TYPE_FOR_FUNCTION_CHECKING_MATCHING_CONDITION:
    def condition_function(mentor: Mentor, mentee: Mentee) -> bool:
        for mentee_interest in mentee.interests:
            if (
                    min_interest_priority_level is None
                    and mentee_interest in mentor.expertise
            ) or (
                    min_interest_priority_level is not None
                    and mentee_interest in mentor.expertise
                    and mentee.interests[mentee_interest] <= min_interest_priority_level
                    and mentor.expertise[mentee_interest] <= min_interest_priority_level
            ):
                return True
        return False

    return condition_function


def check_mentor_has_no_less_experience_than_mentee(
    mentor: Mentor,
    mentee: Mentee
) -> bool:
    return mentor.person.years_of_experience >= mentee.person.years_of_experience


def check_mentor_and_mentee_are_not_from_the_same_business_unit(
    mentor: Mentor,
    mentee: Mentee
) -> bool:
    return mentor.person.business_unit != mentee.person.business_unit


def check_mentor_and_mentee_are_not_the_same_person(
    mentor: Mentor,
    mentee: Mentee
) -> bool:
    return mentor.person != mentee.person


def are_mentor_and_mentee_a_match_under_conditions(
    mentor: Mentor,
    mentee: Mentee,
    conditions: list[TYPE_FOR_FUNCTION_CHECKING_MATCHING_CONDITION]
):
    return all([condition_check(mentor, mentee) for condition_check in conditions])
