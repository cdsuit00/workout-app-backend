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