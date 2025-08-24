from flask import Blueprint, request, jsonify
from extensions import db
from models import Workout, Exercise, WorkoutExercise
from schemas.workout_schema import workout_schema, workouts_schema
from schemas.workout_exercise_schema import workout_exercise_schema

workout_bp = Blueprint('workouts', __name__)

# GET /workouts - List all workouts
@workout_bp.route('', methods=['GET'])
def get_workouts():
    try:
        workouts = Workout.query.all()
        return workouts_schema.jsonify(workouts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /workouts/<id> - Show a single workout with its associated exercises
@workout_bp.route('/<int:id>', methods=['GET'])
def get_workout(id):
    try:
        workout = Workout.query.get_or_404(id)
        return workout_schema.jsonify(workout), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# POST /workouts - Create a workout
@workout_bp.route('', methods=['POST'])
def create_workout():
    try:
        data = request.get_json()
        # Validate and deserialize input
        workout_data = workout_schema.load(data)
        workout = Workout(**workout_data)
        db.session.add(workout)
        db.session.commit()
        return workout_schema.jsonify(workout), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# DELETE /workouts/<id> - Delete a workout
@workout_bp.route('/<int:id>', methods=['DELETE'])
def delete_workout(id):
    try:
        workout = Workout.query.get_or_404(id)
        db.session.delete(workout)
        db.session.commit()
        return jsonify({"message": "Workout deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
@workout_bp.route('/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    try:
        data = request.get_json()
        data['workout_id'] = workout_id
        data['exercise_id'] = exercise_id
        
        # Validate and deserialize input
        workout_exercise_data = workout_exercise_schema.load(data)
        workout_exercise = WorkoutExercise(**workout_exercise_data)
        db.session.add(workout_exercise)
        db.session.commit()
        return workout_exercise_schema.jsonify(workout_exercise), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400