from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Question(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    tags = db.Column(db.String(200), nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    help_description = db.Column(db.Text)
    statement = db.Column(db.Text)
    keycloak_group_id = db.Column(db.String(50), nullable=True)  # Added this field


    def to_dict(self):
        return {
            'id': str(self.id),
            'question_type': self.question_type,
            'category': self.category,
            'difficulty': self.difficulty,
            'tags': self.tags,
            'time_limit': self.time_limit,
            'active': self.active,
            'help_description': self.help_description,
            'keycloak_group_id': self.keycloak_group_id  # Added this field
        }

    @classmethod
    def get_active_questions(cls):
        return cls.query.filter_by(active=True).all()

    @classmethod
    def clear_all(cls):
        cls.query.delete()
        db.session.commit()
