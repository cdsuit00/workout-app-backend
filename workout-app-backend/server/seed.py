#!/usr/bin/env python3

from app import create_app
from models import db, BaseModel

def seed_database():
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate them
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()
        
        # Import models after app context is established
        from models import User, Workout, Exercise, WorkoutExercise, Set
        
        print("Seeding database...")
        
        # Create sample users
        users = [
            User(username="john_doe", email="john@example.com"),
            User(username="jane_smith", email="jane@example.com"),
            User(username="trainer_mike", email="mike@example.com")
        ]
        
        for user in users:
            db.session.add(user)
        
        db.session.commit()
        print("Created sample users")
        
        # We'll add more seed data in subsequent steps
        
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()