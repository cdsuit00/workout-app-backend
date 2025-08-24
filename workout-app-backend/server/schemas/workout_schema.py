from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=360))
    notes = fields.Str(validate=validate.Length(max=1000))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Schema validations
    @validates('date')
    def validate_date_not_future(self, value):
        if value > date.today():
            raise ValidationError("Workout date cannot be in the future")
    
    @validates('duration_minutes')
    def validate_duration_positive(self, value):
        if value <= 0:
            raise ValidationError("Duration must be a positive integer")

# Create schema instances
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)