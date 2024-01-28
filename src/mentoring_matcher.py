from matching import match_mentors_and_mentees
from participants import Mentee, Mentor
from matching_conditions import TYPE_FOR_FUNCTION_CHECKING_MATCHING_CONDITION


class MentoringMatcher:

    def __init__(self, mentors: list[Mentor], mentees: list[Mentee]):
        self.unassigned_mentors = mentors
        self.unassigned_mentees = mentees
        self.assigned_mentors = []
        self.assigned_mentees = []
        self.matched_pairs = []

    def match_unassigned(
        self,
        matching_conditions: list[TYPE_FOR_FUNCTION_CHECKING_MATCHING_CONDITION]
    ) -> list[tuple[Mentor, Mentee]]:
        new_matches = match_mentors_and_mentees(
            self.unassigned_mentors,
            self.unassigned_mentees,
            matching_conditions
        )

        self.matched_pairs.extend(new_matches)

        self.assigned_mentors.extend([x[0] for x in new_matches])
        self.unassigned_mentors = [
            x for x in self.unassigned_mentors
            if x not in self.assigned_mentors
        ]

        self.assigned_mentees.extend([x[1] for x in new_matches])
        self.unassigned_mentees = [
            x for x in self.unassigned_mentees
            if x not in self.assigned_mentees
        ]

        return new_matches
