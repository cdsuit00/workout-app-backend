#!/usr/bin/env python3

import sys
import os
from datetime import datetime, date as date_type

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models import Exercise, Workout, WorkoutExercise

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
        # Create sample workouts
        workouts = [
            Workout(
                date=date_type(2024, 1, 15),
                duration_minutes=45,
                notes="Morning workout session"
            ),
            Workout(
                date=date_type(2024, 1, 16),
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

if __name__ == '__main__':
    seed_database()