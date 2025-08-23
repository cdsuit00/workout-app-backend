from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions here to avoid circular imports
db = SQLAlchemy()
migrate = Migrate()