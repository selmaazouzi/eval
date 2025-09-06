import pandas as pd
from app.models import Question

def load_questions(userGroupId: str = None) -> pd.DataFrame:
    
    questions = Question.query.filter_by(active=True)

    if userGroupId:
        if userGroupId == '0':
            questions = questions.filter(Question.keycloak_group_id == '0')
        else:
            questions = questions.filter(
                (Question.keycloak_group_id == '0') | 
                (Question.keycloak_group_id == userGroupId)
            )
    else:
        print("[load_questions] No user group ID provided → returning all active questions without filtering by group")

    all_questions = questions.all()

    df = pd.DataFrame([q.to_dict() for q in all_questions])
    
    return df
