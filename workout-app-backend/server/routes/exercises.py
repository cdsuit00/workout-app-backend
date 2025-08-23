from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Exercise, Workout, WorkoutExercise

exercise_bp = Blueprint('exercises', __name__)

# GET /exercises - List all exercises
@exercise_bp.route('', methods=['GET'])
def get_exercises():
    try:
        exercises = Exercise.query.all()
        # Will add serialization in next step
        return jsonify([{"id": e.id, "name": e.name} for e in exercises]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /exercises/<id> - Show an exercise and associated workouts
@exercise_bp.route('/<int:id>', methods=['GET'])
def get_exercise(id):
    try:
        exercise = Exercise.query.get_or_404(id)
        # Will add serialization in next step
        return jsonify({"id": exercise.id, "name": exercise.name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# POST /exercises - Create an exercise
@exercise_bp.route('', methods=['POST'])
def create_exercise():
    try:
        data = request.get_json()
        exercise = Exercise(
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed', False)
        )
        db.session.add(exercise)
        db.session.commit()
        return jsonify({"message": "Exercise created", "id": exercise.id}), 201
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