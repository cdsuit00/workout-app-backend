# Workout Application Backend

A Flask SQLAlchemy backend for a workout tracking application.

## Features

- User management
- Workout creation and tracking
- Exercise database
- Set tracking and progress monitoring
- RESTful API endpoints

## Installation

1. Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd workout-app-backend

2. Install dependencies using Pipenv:
    pipenv install
    pipenv shell

3. Initialize the database:
    python server/seed.py

4. Run the application:
    python server/app.py

##

The server will run on http://localhost:5555

API Endpoints
Endpoints will be documented here as they are implemented.

Database Schema
The application uses SQLite with the following main tables:

Users

Workouts

Exercises

WorkoutExercises

Sets

## Development

To run migrations:
flask db init
flask db migrate
flask db upgrade