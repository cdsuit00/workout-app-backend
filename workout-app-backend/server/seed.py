#!/usr/bin/env python3

import sys
import os
from datetime import datetime, date as date_type

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app  # Now this should work
from extensions import db  # Remove relative import
from models import Exercise, Workout, WorkoutExercise  # Remove relative import
def seed_database():
    app = create_app()
    
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        
        print("Creating sample exercises...")
        # Create sample exercises
        exercises = [
            Exercise(
                name="Push-ups",
                category="strength",
                equipment_needed=False
            ),
            Exercise(
                name="Running",
                category="cardio",
                equipment_needed=False
            ),
            Exercise(
                name="Dumbbell Curls",
                category="strength",
                equipment_needed=True
            ),
            Exercise(
                name="Yoga",
                category="flexibility",
                equipment_needed=False
            ),
            Exercise(
                name="Plank",
                category="core",
                equipment_needed=False
            )
        ]
        
        for exercise in exercises:
            db.session.add(exercise)
        db.session.commit()
        print(f"Created {len(exercises)} exercises")
        
        print("Creating sample workouts...")
        # Create sample workouts - use date_type instead of date
        workouts = [
            Workout(
                date=date_type(2024, 1, 15),  # Use date_type instead of date
                duration_minutes=45,
                notes="Morning workout session"
            ),
            Workout(
                date=date_type(2024, 1, 16),  # Use date_type instead of date
                duration_minutes=30,
                notes="Evening cardio"
            )
        ]
        
        for workout in workouts:
            db.session.add(workout)
        db.session.commit()
        print(f"Created {len(workouts)} workouts")
        
        print("Creating workout exercises...")
        # Create workout exercise associations
        workout_exercises = [
            WorkoutExercise(
                workout_id=1,
                exercise_id=1,
                reps=15,
                sets=3,
                duration_seconds=None
            ),
            WorkoutExercise(
                workout_id=1,
                exercise_id=5,
                reps=None,
                sets=None,
                duration_seconds=60
            ),
            WorkoutExercise(
                workout_id=2,
                exercise_id=2,
                reps=None,
                sets=None,
                duration_seconds=1800
            )
        ]
        
        for we in workout_exercises:
            db.session.add(we)
        db.session.commit()
        print(f"Created {len(workout_exercises)} workout exercises")
        
        print("Database seeded successfully!")
        print("Sample data created:")
        print(f"- Exercises: {Exercise.query.count()}")
        print(f"- Workouts: {Workout.query.count()}")
        print(f"- Workout Exercises: {WorkoutExercise.query.count()}")
        
        print("Testing relationships...")
        # Test the many-to-many relationships
        workout = Workout.query.get(1)
        exercise = Exercise.query.get(1)

        print(f"Workout 1 has {len(workout.exercises)} exercises")
        print(f"Exercise 1 appears in {len(exercise.workouts)} workouts")
        print(f"Workout 1 exercise names: {[ex.name for ex in workout.exercises]}")
        
        # Test convenience methods
        total_reps = exercise.get_total_reps()
        print(f"Exercise 1 total reps: {total_reps}")

        workout_count = exercise.get_workout_count()
        print(f"Exercise 1 workout count: {workout_count}")

        print("Relationship tests passed!")
        
        print("Testing validations and constraints...")
        # Test validation errors
        try:
            # Test duplicate exercise name
            duplicate_exercise = Exercise(name="Push-ups", category="strength")
            db.session.add(duplicate_exercise)
            db.session.commit()
            print("ERROR: Should have failed duplicate name validation")
        except Exception as e:
            print(f"✓ Correctly caught duplicate name error: {e}")
            db.session.rollback()

        try:
            # Test future date - use date_type instead of date
            from datetime import timedelta
            future_workout = Workout(date=date_type.today() + timedelta(days=1), duration_minutes=30)
            db.session.add(future_workout)
            db.session.commit()
            print("ERROR: Should have failed future date validation")
        except Exception as e:
            print(f"✓ Correctly caught future date error: {e}")
            db.session.rollback()

        try:
            # Test negative duration
            negative_workout = Workout(date=date_type(2024, 1, 1), duration_minutes=-5)
            db.session.add(negative_workout)
            db.session.commit()
            print("ERROR: Should have failed negative duration validation")
        except Exception as e:
            print(f"✓ Correctly caught negative duration error: {e}")
            db.session.rollback()

        print("All validation tests passed!")

if __name__ == '__main__':
    seed_database()