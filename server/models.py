from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from config import db, bcrypt
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    
    # Relationship: User has many workouts
    workouts = db.relationship('Workout', backref='user', cascade='all, delete-orphan')
    
    # Password hashing
    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    
    def __repr__(self):
        return f'<User {self.username}>'

class Workout(db.Model):
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer)  # in minutes
    notes = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Validations
    @validates('exercise')
    def validate_exercise(self, key, exercise):
        if not exercise or len(exercise.strip()) == 0:
            raise ValueError("Exercise name is required")
        return exercise
    
    @validates('sets')
    def validate_sets(self, key, sets):
        if sets < 1:
            raise ValueError("Sets must be at least 1")
        return sets
    
    @validates('reps')
    def validate_reps(self, key, reps):
        if reps < 1:
            raise ValueError("Reps must be at least 1")
        return reps
    
    def __repr__(self):
        return f'<Workout {self.exercise}>'
