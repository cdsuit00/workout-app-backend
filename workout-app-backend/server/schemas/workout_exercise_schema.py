from marshmallow import Schema, fields, validate, validates, ValidationError, validates_schema

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(validate=validate.Range(min=1, max=1000))
    sets = fields.Int(validate=validate.Range(min=1, max=100))
    duration_seconds = fields.Int(validate=validate.Range(min=1, max=36000))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Schema validations
    @validates('reps')
    def validate_reps_positive(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Reps must be positive if provided")
    
    @validates('sets')
    def validate_sets_positive(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Sets must be positive if provided")
    
    @validates('duration_seconds')
    def validate_duration_positive(self, value):
        if value is not None and value <= 0:
            raise ValidationError("Duration must be positive if provided")
    
    @validates_schema
    def validate_has_reps_sets_or_duration(self, data, **kwargs):
        reps = data.get('reps')
        sets = data.get('sets')
        duration = data.get('duration_seconds')
        
        has_reps_sets = reps is not None and sets is not None
        has_duration = duration is not None
        
        if not (has_reps_sets or has_duration):
            raise ValidationError("Must provide either reps/sets or duration_seconds")
        
        if has_reps_sets and has_duration:
            raise ValidationError("Cannot provide both reps/sets and duration_seconds")

# Create schema instances
workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)