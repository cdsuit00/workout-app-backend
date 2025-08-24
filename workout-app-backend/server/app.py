from flask import Flask, jsonify
from extensions import db, migrate

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models to ensure they're registered with SQLAlchemy
    import models
    print("Models imported successfully")
    
    # Register blueprints
    from routes.workouts import workout_bp
    from routes.exercises import exercise_bp
    
    app.register_blueprint(workout_bp, url_prefix='/workouts')
    app.register_blueprint(exercise_bp, url_prefix='/exercises')
    
    # Health check endpoint
    @app.route('/')
    def health_check():
        return jsonify({"message": "Workout App API is running!"})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5555, debug=True)