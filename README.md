# Workout Application Backend

A comprehensive Flask SQLAlchemy backend API for tracking workouts, exercises, and fitness progress. This application provides a RESTful API for managing workout routines, exercise catalog, and tracking sets/reps.

## Features

 - Exercise Management: Create, read, update, and delete exercises
 - Workout Tracking: Log workouts with duration, date, and notes
 - Workout-Exercise Relationships: Associate exercises with workouts including sets, reps, and duration
 - Data Validation: Comprehensive server-side validation with Marshmallow schemas
 - RESTful API: Clean, consistent API endpoints following REST conventions
 - SQLite Database: Lightweight database with proper relationships and constraints

## Installation

    Prerequisites
    Python 3.8+
    Pipenv (recommended) or pip/virtualenv

1. Clone the repository:
    git clone git@github.com:cdsuit00/workout-app-backend.git
    cd workout-app-backend

2. Install dependencies using Pipenv:
    pipenv install
    pipenv shell

3. Initialize the database:
    python server/seed.py

4. Run the application:
    python server/app.py
   
The server will run on http://localhost:5555

## Dependencies
    Production
      Flask==2.2.2
      Flask-Migrate==3.1.0
      Flask-SQLAlchemy==3.0.3
      Marshmallow==3.20.1
      Werkzeug==2.2.2
    
    Development
      ipdb==0.13.9
      requests==*

## API Endpoints
    Exercises
      GET /exercises - List all exercises
      GET /exercises/<id> - Get exercise details with workout history
      POST /exercises - Create a new exercise
      PUT /exercises/<id> - Update an exercise
      DELETE /exercises/<id> - Delete an exercise and associated data
    
    Workouts
      GET /workouts - List all workouts
      GET /workouts/<id> - Get workout details with exercise information
      POST /workouts - Create a new workout
      DELETE /workouts/<id> - Delete a workout and associated exercises
    
    Workout Exercises
      POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Add exercise to workout
      PUT /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Update exercise in workout
      DELETE /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises - Remove exercise from workout

## Database Schema
    Models
      Exercise: id, name, category, equipment_needed, created_at, updated_at
      Workout: id, date, duration_minutes, notes, created_at, updated_at
      WorkoutExercise: id, workout_id, exercise_id, reps, sets, duration_seconds, created_at, updated_at
    
    Relationships
      Workout ↔ WorkoutExercise (one-to-many)
      Exercise ↔ WorkoutExercise (one-to-many)
      Workout ↔ Exercise (many-to-many through WorkoutExercise)
    
    Constraints & Validations
      Table Constraints: Positive value checks, unique workout-exercise combinations, required field logic
      Model Validations: Date validation, category validation, length checks, uniqueness constraints
      Schema Validations: Comprehensive input validation with Marshmallow
