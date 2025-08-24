#!/usr/bin/env python3

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.schemas.exercise_schema import ExerciseSchema
from server.schemas.workout_schema import WorkoutSchema
from server.schemas.workout_exercise_schema import WorkoutExerciseSchema

def test_schemas():
    print("Testing schemas without database dependencies...")
    
    exercise_schema = ExerciseSchema()
    workout_schema = WorkoutSchema()
    workout_exercise_schema = WorkoutExerciseSchema()
    
    # Test exercise schema validation
    try:
        valid_exercise = {"name": "Test Exercise", "category": "strength"}
        result = exercise_schema.load(valid_exercise)
        print("✓ Exercise schema validation passed")
        
        # Test invalid category
        try:
            invalid_exercise = {"name": "Test Exercise", "category": "invalid"}
            exercise_schema.load(invalid_exercise)
            print("✗ Exercise schema should have failed invalid category")
        except Exception as e:
            print("✓ Exercise schema correctly rejected invalid category")
            
    except Exception as e:
        print(f"✗ Exercise schema validation failed: {e}")
    
    # Test workout schema validation
    try:
        valid_workout = {"date": "2024-01-01", "duration_minutes": 30}
        result = workout_schema.load(valid_workout)
        print("✓ Workout schema validation passed")
        
        # Test negative duration
        try:
            invalid_workout = {"date": "2024-01-01", "duration_minutes": -5}
            workout_schema.load(invalid_workout)
            print("✗ Workout schema should have failed negative duration")
        except Exception as e:
            print("✓ Workout schema correctly rejected negative duration")
            
    except Exception as e:
        print(f"✗ Workout schema validation failed: {e}")
    
    print("Schema testing completed!")

if __name__ == '__main__':
    test_schemas()