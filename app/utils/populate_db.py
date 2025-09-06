import os
from sqlalchemy.exc import SQLAlchemyError
import logging

from app import create_app, db
from app.models import Question

app = create_app()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_db():
    with app.app_context():
        try:
            # Clear existing questions
            Question.clear_all()
            
            questions = [
                Question(id='8677d48b-af18-49ca-9cb3-8245a4408df6',
                         question_type='choice', category='Backend',
                         difficulty='EASY', tags='HTML', time_limit=30),
                Question(id='2', question_type='code', category='Backend',
                         difficulty='EASY', tags='Python', time_limit=600)
            ]
            
            # Add new questions
            db.session.add_all(questions)
            db.session.commit()
            
            # Verify the insertion by querying the database
            inserted_questions = Question.query.all()
            if len(inserted_questions) == len(questions):
                logger.info("Database communication successful. Questions inserted correctly.")
                return True
            else:
                logger.warning("Database communication issue. Not all questions were inserted.")
                return False
        
        except SQLAlchemyError as e:
            logger.error(f"Database communication error: {str(e)}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    success = populate_db()
    print(f"Database population {'succeeded' if success else 'failed'}")