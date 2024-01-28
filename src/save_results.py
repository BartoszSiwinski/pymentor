import os

import pandas as pd

from src.participants import Mentee, Mentor


def _append_data_to_excel(
        excel_file_path: str,
        excel_sheet_name: str,
        df: pd.DataFrame
):
    excel_file_exists = os.path.isfile(excel_file_path)

    with pd.ExcelWriter(
            excel_file_path,
            engine='openpyxl',
            mode='a' if excel_file_exists else 'w',
            if_sheet_exists='replace' if excel_file_exists else None
    ) as writer:
        df.to_excel(writer, excel_sheet_name, index=False, engine='openpyxl')


def save_mentors_to_excel(
        excel_file_path: str,
        excel_sheet_name: str,
        assigned_mentors: list[Mentor],
        unassigned_mentors: list[Mentor]
):
    df = pd.DataFrame(
        [
            {
                "email_address": mentor.person.email_address,
                "fullname": mentor.person.fullname,
                "years_of_experience": mentor.person.years_of_experience,
                "business_unit": mentor.person.business_unit,
                "assigned": mentor in assigned_mentors,
                "expertise": list(mentor.expertise.keys()),
                "sub_id": mentor.sub_id
            } for mentor in assigned_mentors + unassigned_mentors
        ]
    )
    _append_data_to_excel(excel_file_path, excel_sheet_name, df)


def save_mentees_to_excel(
        excel_file_path: str,
        excel_sheet_name: str,
        assigned_mentees: list[Mentee],
        unassigned_mentees: list[Mentee]
):
    df = pd.DataFrame(
        [
            {
                "email_address": mentee.person.email_address,
                "fullname": mentee.person.fullname,
                "years_of_experience": mentee.person.years_of_experience,
                "business_unit": mentee.person.business_unit,
                "assigned": mentee in assigned_mentees,
                "interests": list(mentee.interests.keys())
            } for mentee in assigned_mentees + unassigned_mentees
        ]
    )
    _append_data_to_excel(excel_file_path, excel_sheet_name, df)


def save_mentorship_pairs_excel(
        excel_file_path: str,
        excel_sheet_name: str,
        pairs: list[tuple[Mentor, Mentee]]
):
    df = pd.DataFrame(
        [
            {
                "email_address_mentor": mentor.person.email_address,
                "fullname_mentor": mentor.person.fullname,
                "mentor_expertise": list(mentor.expertise.keys()),
                "email_address_mentee": mentee.person.email_address,
                "fullname_mentee": mentee.person.fullname,
                "mentee_interests": list(mentee.interests.keys())
            } for mentor, mentee in pairs
        ]
    )
    _append_data_to_excel(excel_file_path, excel_sheet_name, df)
