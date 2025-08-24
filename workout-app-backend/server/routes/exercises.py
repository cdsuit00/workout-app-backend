from flask import Blueprint, request, jsonify
from extensions import db
from models import Exercise, Workout, WorkoutExercise
from schemas.exercise_schema import exercise_schema, exercises_schema

exercise_bp = Blueprint('exercises', __name__)

# GET /exercises - List all exercises
@exercise_bp.route('', methods=['GET'])
def get_exercises():
    try:
        exercises = Exercise.query.all()
        return exercises_schema.jsonify(exercises), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /exercises/<id> - Show an exercise and associated workouts
@exercise_bp.route('/<int:id>', methods=['GET'])
def get_exercise(id):
    try:
        exercise = Exercise.query.get_or_404(id)
        return exercise_schema.jsonify(exercise), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# POST /exercises - Create an exercise
@exercise_bp.route('', methods=['POST'])
def create_exercise():
    try:
        data = request.get_json()
        
        # Check for uniqueness before schema validation
        name = data.get('name')
        if name and Exercise.query.filter(Exercise.name.ilike(name)).first():
            return jsonify({"error": "Exercise with this name already exists"}), 400
        
        # Validate and deserialize input
        exercise_data = exercise_schema.load(data)
        exercise = Exercise(**exercise_data)
        db.session.add(exercise)
        db.session.commit()
        return exercise_schema.jsonify(exercise), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# DELETE /exercises/<id> - Delete an exercise
@exercise_bp.route('/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    try:
        exercise = Exercise.query.get_or_404(id)
        db.session.delete(exercise)
        db.session.commit()
        return jsonify({"message": "Exercise deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400