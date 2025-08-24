from flask import Blueprint, request, jsonify
from extensions import db
from models import Workout, Exercise, WorkoutExercise
from schemas.workout_schema import workout_schema, workouts_schema
from schemas.workout_exercise_schema import workout_exercise_schema, workout_exercises_schema
from schemas.exercise_schema import exercise_schema

workout_bp = Blueprint('workouts', __name__)

# GET /workouts - List all workouts with basic info
@workout_bp.route('', methods=['GET'])
def get_workouts():
    try:
        workouts = Workout.query.all()
        # Use dump() instead of jsonify() for Marshmallow schemas
        return jsonify(workouts_schema.dump(workouts)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /workouts/<id> - Show a single workout with its associated exercises and details
@workout_bp.route('/<int:id>', methods=['GET'])
def get_workout(id):
    try:
        workout = Workout.query.get_or_404(id)
        
        # Get workout exercises with exercise details
        workout_exercises = WorkoutExercise.query.filter_by(workout_id=id).all()
        exercises_with_details = []
        
        for we in workout_exercises:
            exercise = Exercise.query.get(we.exercise_id)
            exercise_data = exercise_schema.dump(exercise)
            we_data = workout_exercise_schema.dump(we)
            exercises_with_details.append({
                **exercise_data,
                **we_data,
                "exercise_name": exercise.name  # Add exercise name for convenience
            })
        
        workout_data = workout_schema.dump(workout)
        workout_data['exercises'] = exercises_with_details
        
        return jsonify(workout_data), 200
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
        
        # Use dump() instead of jsonify()
        return jsonify(workout_schema.dump(workout)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# DELETE /workouts/<id> - Delete a workout and associated workout exercises
@workout_bp.route('/<int:id>', methods=['DELETE'])
def delete_workout(id):
    try:
        workout = Workout.query.get_or_404(id)
        
        # Delete associated workout exercises (cascade delete)
        WorkoutExercise.query.filter_by(workout_id=id).delete()
        
        db.session.delete(workout)
        db.session.commit()
        
        return jsonify({"message": "Workout and associated exercises deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
# Add an exercise to a workout, including reps/sets/duration
@workout_bp.route('/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    try:
        # Check if workout and exercise exist
        workout = Workout.query.get_or_404(workout_id)
        exercise = Exercise.query.get_or_404(exercise_id)
        
        data = request.get_json()
        data['workout_id'] = workout_id
        data['exercise_id'] = exercise_id
        
        # Check if this exercise is already in the workout
        existing = WorkoutExercise.query.filter_by(
            workout_id=workout_id, 
            exercise_id=exercise_id
        ).first()
        
        if existing:
            return jsonify({"error": "Exercise already exists in this workout"}), 400
        
        # Validate and deserialize input
        workout_exercise_data = workout_exercise_schema.load(data)
        workout_exercise = WorkoutExercise(**workout_exercise_data)
        
        db.session.add(workout_exercise)
        db.session.commit()
        
        # Use dump() instead of jsonify()
        return jsonify(workout_exercise_schema.dump(workout_exercise)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# PUT /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
# Update an exercise in a workout
@workout_bp.route('/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['PUT'])
def update_exercise_in_workout(workout_id, exercise_id):
    try:
        workout_exercise = WorkoutExercise.query.filter_by(
            workout_id=workout_id, 
            exercise_id=exercise_id
        ).first_or_404()
        
        data = request.get_json()
        
        # Validate and update
        workout_exercise_data = workout_exercise_schema.load(data, partial=True)
        
        for key, value in workout_exercise_data.items():
            setattr(workout_exercise, key, value)
        
        db.session.commit()
        
        # Use dump() instead of jsonify()
        return jsonify(workout_exercise_schema.dump(workout_exercise)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# DELETE /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
# Remove an exercise from a workout
@workout_bp.route('/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['DELETE'])
def remove_exercise_from_workout(workout_id, exercise_id):
    try:
        workout_exercise = WorkoutExercise.query.filter_by(
            workout_id=workout_id, 
            exercise_id=exercise_id
        ).first_or_404()
        
        db.session.delete(workout_exercise)
        db.session.commit()
        
        return jsonify({"message": "Exercise removed from workout"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400