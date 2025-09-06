import pandas as pd


def adjust_duration(df: pd.DataFrame, target_duration: int) -> pd.DataFrame:
    total_duration = df['time_limit'].sum()

    while total_duration > target_duration and not df.empty:
        question_to_remove = df.loc[df['time_limit'].idxmax()]
        df = df.drop(question_to_remove.name)
        total_duration -= question_to_remove['time_limit']

    return df
