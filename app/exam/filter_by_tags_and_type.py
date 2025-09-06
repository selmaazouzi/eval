import pandas as pd
from typing import Any, Dict, List
import math

def distribute_questions_by_difficulty(df: pd.DataFrame, num_questions: int, difficulty: str) -> pd.DataFrame:
   
    if df.empty or num_questions <= 0:
        return pd.DataFrame()
    
    if difficulty == 'EASY':
        num_easy = math.ceil(num_questions * 0.75)
        num_medium = num_questions - num_easy
        
        easy_questions = df[df['difficulty'] == 'EASY']
        medium_questions = df[df['difficulty'] == 'MEDIUM']
        
        if len(easy_questions) < num_easy or len(medium_questions) < num_medium:
            total_available = len(easy_questions) + len(medium_questions)
            
            if total_available < num_questions:
                return pd.concat([easy_questions, medium_questions])
            else:
                ratio = len(easy_questions) / total_available
                num_easy = min(math.ceil(num_questions * ratio), len(easy_questions))
                num_medium = min(num_questions - num_easy, len(medium_questions))
        
        selected_easy = easy_questions.sample(n=num_easy) if num_easy > 0 else pd.DataFrame()
        selected_medium = medium_questions.sample(n=num_medium) if num_medium > 0 else pd.DataFrame()
        
        result = pd.concat([selected_easy, selected_medium])
        return result
    
    elif difficulty == 'MEDIUM':
        num_medium = math.ceil(num_questions * 0.75)
        num_hard = num_questions - num_medium
        
        medium_questions = df[df['difficulty'] == 'MEDIUM']
        hard_questions = df[df['difficulty'] == 'HARD']
        
        if len(medium_questions) < num_medium or len(hard_questions) < num_hard:
            total_available = len(medium_questions) + len(hard_questions)
            
            if total_available < num_questions:
                return pd.concat([medium_questions, hard_questions])
            else:
                ratio = len(medium_questions) / total_available
                num_medium = min(math.ceil(num_questions * ratio), len(medium_questions))
                num_hard = min(num_questions - num_medium, len(hard_questions))
        
        selected_medium = medium_questions.sample(n=num_medium) if num_medium > 0 else pd.DataFrame()
        selected_hard = hard_questions.sample(n=num_hard) if num_hard > 0 else pd.DataFrame()
        
        result = pd.concat([selected_medium, selected_hard])
        return result
    
    elif difficulty == 'HARD':
        hard_questions = df[df['difficulty'] == 'HARD']
        result = hard_questions.sample(n=min(num_questions, len(hard_questions)))
        return result
    
    return pd.DataFrame()

def filter_by_tag_and_type(df: pd.DataFrame, generate_exam: List[Dict[str, Any]], difficulty: str) -> pd.DataFrame:
    
    all_selected_questions = []
    working_df = df.copy()
    
    # Process each tag group separately
    for group in generate_exam:
        tag_set = group['tag']  # Single tag set for this group
        question_choice = group['questionChoice']
        free_question = group['freeQuestion']
        
        
        # Filter for current tag only
        tag_filtered = working_df[working_df['tags'].apply(
            lambda x: any(tag.lower() in [t.strip().lower() for t in x.split(',')] 
                        for tag in tag_set)
        )]
        
        
        # Handle choice questions for this tag
        if question_choice > 0:
            choice_questions = tag_filtered[tag_filtered['question_type'] == 'choice']
            
            selected_choice = distribute_questions_by_difficulty(
                choice_questions,
                question_choice,
                difficulty
            )
            
            if not selected_choice.empty:
                all_selected_questions.append(selected_choice)
                working_df = working_df.drop(selected_choice.index)
        
        # Handle free form questions for this tag
        if free_question > 0:
            free_form_questions = tag_filtered[tag_filtered['question_type'] == 'free_form']
            
            selected_free = distribute_questions_by_difficulty(
                free_form_questions,
                free_question,
                difficulty
            )
            
            if not selected_free.empty:
                all_selected_questions.append(selected_free)
                working_df = working_df.drop(selected_free.index)
    
    if not all_selected_questions:
        return pd.DataFrame()
    
    result = pd.concat(all_selected_questions)
    
    return result
   