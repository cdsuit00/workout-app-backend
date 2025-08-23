from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

### Start of Exercise model ###

class Exercise(BaseModel):
    __tablename__ = 'exercises'
    
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', cascade='all, delete-orphan')
    
    # Validations
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Exercise name cannot be empty")
        if len(name) > 100:
            raise ValueError("Exercise name cannot exceed 100 characters")
        return name.strip()
    
    @validates('category')
    def validate_category(self, key, category):
        valid_categories = ['cardio', 'strength', 'flexibility', 'balance', 'core']
        if category.lower() not in valid_categories:
            raise ValueError(f"Category must be one of: {', '.join(valid_categories)}")
        return category.lower()
    
    def __repr__(self):
        return f'<Exercise {self.name} ({self.category})>'
    
### Start of Workout model ###

class Workout(BaseModel):
    __tablename__ = 'workouts'
    
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', backref='workout', cascade='all, delete-orphan')
    
    # Validations
    @validates('date')
    def validate_date(self, key, date):
        if not date:
            raise ValueError("Workout date is required")
        if isinstance(date, str):
            # Try to convert string to date if needed
            from datetime import datetime
            try:
                date = datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format")
        
        if date > datetime.utcnow().date():
            raise ValueError("Workout date cannot be in the future")
        return date
    
    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Duration must be a positive integer")
        if duration > 360:  # 6 hours max
            raise ValueError("Duration cannot exceed 360 minutes (6 hours)")
        return duration
    
    @validates('notes')
    def validate_notes(self, key, notes):
        if notes and len(notes) > 1000:
            raise ValueError("Notes cannot exceed 1000 characters")
        return notes
    
    def __repr__(self):
        return f'<Workout {self.date} ({self.duration_minutes} minutes)>'