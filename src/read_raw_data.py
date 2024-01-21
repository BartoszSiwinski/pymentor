import json
import pandas as pd

from utilities import get_key_for_value

FILE_PATH = '../mentoring_raw_data.xlsx'


def get_interests_map():
    with open('../refs/interests_map.json') as file:
        return json.load(file)


INTERESTS_MAP = get_interests_map()


def get_processed_data_for_mentoring_program(input_excel_file_path: str):
    df = pd.read_excel(input_excel_file_path)
    df = select_relevant_columns(df)
    # 1st row contains some metadata irrelavant for the mentoring program
    df = drop_first_row(df)
    df = rename_columns(df)
    df = consolidate_mentee_interests(df)
    df = consolidate_mentor_interests(df)
    df = process_experience_range_column_values(df)
    df = process_role_column_values(df)

    df.to_json('../data_from_excel.json', indent=4, orient='records')

    return df


def select_relevant_columns(df: pd.DataFrame):
    all_columns: list[str] = df.columns

    columns_with_interests = [
        column_name
        for column_name in all_columns
        if column_name.startswith(("Q6_", "Q70_", "Q71_", "Q72_", "Q73_"))
    ]
    columns_with_personal_data = [
        'Full Name',
        'E-mail Address',
        'Q40',  # business unit
        'Q21',  # years of experience
        'Q22',  # 'Mentor' or 'Mentee' or 'Both - Mentor and Mentee'
        'Q23'   # ERG
    ]

    relevant_columns = columns_with_personal_data
    relevant_columns.extend(columns_with_interests)
    relevant_df = df[relevant_columns]

    return relevant_df


def drop_first_row(df):
    return df.iloc[1:, :]


def rename_columns(df: pd.DataFrame):
    df = df.rename(
        columns={
            "Full Name": "fullname",
            "E-mail Address": "email_address",
            "Q40": "business_unit",
            "Q21": "years_of_experience",
            "Q22": "role",
            "Q23": "employee_resource_group"
        }
    )
    return df


def consolidate_interests(
        df: pd.DataFrame,
        consolidate_interests_column_name: str,
        columns_to_consolidate: list[str]
):
    def apply_function(row):
        return {
            get_key_for_value(INTERESTS_MAP, column): row[column]
            for column in columns_to_consolidate
            if pd.notna(row[column])
        }
    df[consolidate_interests_column_name] = df.apply(apply_function, axis=1)
    df = df.drop(columns=columns_to_consolidate)
    return df


def consolidate_mentee_interests(df: pd.DataFrame):
    mentee_interests_columns = [
        column for column in df.columns if column.startswith('Q6_')
    ]

    return consolidate_interests(
        df,
        'mentee_interests',
        mentee_interests_columns)


def consolidate_mentor_interests(df: pd.DataFrame):
    mentee_interests_columns = [
        column for column in df.columns
        if column.startswith(("Q70_", "Q71_", "Q72_", "Q73_"))
    ]

    return consolidate_interests(
        df,
        'mentor_interests',
        mentee_interests_columns
    )


def process_experience_range_column_values(df: pd.DataFrame):
    df["years_of_experience"] = df["years_of_experience"].replace(
        {
            "1-5 Years": 0,
            "5-10 Years": 1,
            "10-15 Years": 2,
            "15-20 Years": 3,
            "20+ Years": 4,
        }
    )
    return df


def process_role_column_values(df: pd.DataFrame):
    df["role"] = df["role"].replace(
        {
            "Mentor": "mentor",
            "Mentee": "mentee",
            "Both - Mentor and Mentee": "both",
        }
    )
    return df


print(get_processed_data_for_mentoring_program(FILE_PATH))
print(get_processed_data_for_mentoring_program(FILE_PATH).iloc[0])
