from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Workout, Exercise, WorkoutExercise

workout_bp = Blueprint('workouts', __name__)

# GET /workouts - List all workouts
@workout_bp.route('', methods=['GET'])
def get_workouts():
    try:
        workouts = Workout.query.all()
        # Will add serialization in next step
        return jsonify([{"id": w.id, "date": w.date.isoformat()} for w in workouts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /workouts/<id> - Show a single workout with its associated exercises
@workout_bp.route('/<int:id>', methods=['GET'])
def get_workout(id):
    try:
        workout = Workout.query.get_or_404(id)
        # Will add serialization in next step
        return jsonify({"id": workout.id, "date": workout.date.isoformat()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# POST /workouts - Create a workout
@workout_bp.route('', methods=['POST'])
def create_workout():
    try:
        data = request.get_json()
        workout = Workout(
            date=data.get('date'),
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        db.session.add(workout)
        db.session.commit()
        return jsonify({"message": "Workout created", "id": workout.id}), 201
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
# Add an exercise to a workout, including reps/sets/duration
@workout_bp.route('/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    try:
        data = request.get_json()
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return jsonify({"message": "Exercise added to workout", "id": workout_exercise.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400