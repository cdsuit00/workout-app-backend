from marshmallow import Schema, fields, validate, validates, ValidationError

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(load_default=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # Schema validations
    @validates('category')
    def validate_category(self, value):
        valid_categories = ['cardio', 'strength', 'flexibility', 'balance', 'core']
        if value.lower() not in valid_categories:
            raise ValidationError(f"Category must be one of: {', '.join(valid_categories)}")
    
    @validates('name')
    def validate_name_uniqueness(self, value):
        # Remove database dependency for now - we'll handle this in routes
        pass

# Create schema instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)