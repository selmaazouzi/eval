import pandas as pd
from typing import Any, Dict


def filter_by_column(df: pd.DataFrame, column: str, value: Any) -> pd.DataFrame:
    return df[df[column] == value] if value else df


def filter_code_questions(df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
    if not params.get('questionCode'):
        return pd.DataFrame()

    code_params = params['questionCode']
    language = code_params.get('programmingLanguage')
    num_code_questions = code_params.get('questionCodeCount', 0)
    print(f"num_code_questions: {num_code_questions}")

    code_questions = df[
        (df['question_type'] == 'code') &
        (df['tags'].str.contains(language, case=False, na=False))
        ]

    return code_questions.sample(n=min(num_code_questions, len(code_questions)))
