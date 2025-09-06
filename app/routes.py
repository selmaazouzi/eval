import logging
import traceback
from flask import Blueprint, request, jsonify
from app.exam.generate_exam import generate

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

routes_bp = Blueprint('routes', __name__)

@routes_bp.post('/generate_exam')
def generate_exam_route():
    try:
        data = request.json
        logger.info("Received request data: %s", data)

        generate_exam_params = {
            'generateExam': data.get('generateExam', []),
            'questionCode': data.get('questionCode', {}),
            'difficulty': data.get('difficulty'),
            'duration': data.get('duration'),
            'category': data.get('category'),
            'userGroupId': data.get('userGroupId'),
        }

        logger.info("Parsed generate_exam_params: %s", generate_exam_params)

        result = generate(generate_exam_params)

        logger.info("Exam generation successful. Returning result with %d questions.", result.get('number_of_questions', 0))
        return jsonify(result)

    except Exception as e:
        error_message = f"Error: {str(e)}\n{traceback.format_exc()}"
        logger.error("An error occurred during exam generation:\n%s", error_message)
        return jsonify({"error": error_message}), 400

def init_routes(app):
    app.register_blueprint(routes_bp)
