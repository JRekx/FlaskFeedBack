from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

# Initialize SQLAlchemy for database operations
db = SQLAlchemy()

# Function to connect the database to the Flask app
def connect_db(app):
    db.app = app
    db.init_app(app)

# User model representing the users table in the database
class User(db.Model):
    """User model"""

    # Define the table name in the database
    __tablename__ = 'users'

    # Columns in the users table
    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True
    )
    password = db.Column(db.Text, nullable=False)  # Hashed password stored in the database
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    # Relationship with the Feedback model (one-to-many relationship)
    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    # Class method to register a new user and store their hashed password in the database
    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = cls(
            username=username,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)  # Add the new user to the session
        return user

    # Class method to authenticate a user by comparing the hashed password
    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()  # Retrieve the user from the database

        if user and bcrypt.check_password_hash(user.password, password):
            return user  # Return the user if authentication succeeds
        else:
            return None  # Return None if authentication fails

# Feedback model representing the feedback table in the database
class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey("users.username"),  # Foreign key referencing the users table
        nullable=False,
    )
