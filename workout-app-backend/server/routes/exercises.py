from flask import Blueprint, request, jsonify
from extensions import db
from models import Exercise, Workout, WorkoutExercise
from schemas.exercise_schema import exercise_schema, exercises_schema
from schemas.workout_schema import workout_schema

exercise_bp = Blueprint('exercises', __name__)

# GET /exercises - List all exercises
@exercise_bp.route('', methods=['GET'])
def get_exercises():
    try:
        exercises = Exercise.query.all()
        # Use dump() instead of jsonify()
        return jsonify(exercises_schema.dump(exercises)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /exercises/<id> - Show an exercise and associated workouts
@exercise_bp.route('/<int:id>', methods=['GET'])
def get_exercise(id):
    try:
        exercise = Exercise.query.get_or_404(id)
        
        # Get workouts that include this exercise
        workout_exercises = WorkoutExercise.query.filter_by(exercise_id=id).all()
        workouts_with_details = []
        
        for we in workout_exercises:
            workout = Workout.query.get(we.workout_id)
            workout_data = workout_schema.dump(workout)
            workouts_with_details.append({
                **workout_data,
                "reps": we.reps,
                "sets": we.sets,
                "duration_seconds": we.duration_seconds
            })
        
        exercise_data = exercise_schema.dump(exercise)
        exercise_data['workouts'] = workouts_with_details
        exercise_data['total_workouts'] = len(workouts_with_details)
        
        return jsonify(exercise_data), 200
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
        
        # Use dump() instead of jsonify()
        return jsonify(exercise_schema.dump(exercise)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# PUT /exercises/<id> - Update an exercise
@exercise_bp.route('/<int:id>', methods=['PUT'])
def update_exercise(id):
    try:
        exercise = Exercise.query.get_or_404(id)
        data = request.get_json()
        
        # Check for uniqueness (excluding current exercise)
        name = data.get('name')
        if name and Exercise.query.filter(Exercise.name.ilike(name), Exercise.id != id).first():
            return jsonify({"error": "Exercise with this name already exists"}), 400
        
        # Validate and update
        exercise_data = exercise_schema.load(data, partial=True)
        
        for key, value in exercise_data.items():
            setattr(exercise, key, value)
        
        db.session.commit()
        
        # Use dump() instead of jsonify()
        return jsonify(exercise_schema.dump(exercise)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# DELETE /exercises/<id> - Delete an exercise and associated workout exercises
@exercise_bp.route('/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    try:
        exercise = Exercise.query.get_or_404(id)
        
        # Delete associated workout exercises
        WorkoutExercise.query.filter_by(exercise_id=id).delete()
        
        db.session.delete(exercise)
        db.session.commit()
        
        return jsonify({"message": "Exercise and associated workout data deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400