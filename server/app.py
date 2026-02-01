from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import app, db, api
from models import User, Workout

# Auth Routes

class Signup(Resource):
    def post(self):
        data = request.get_json()
        
        # Validate password confirmation
        if data.get('password') != data.get('password_confirmation'):
            return {'error': 'Passwords do not match'}, 422
        
        try:
            user = User(username=data.get('username'))
            user.password_hash = data.get('password')
            
            db.session.add(user)
            db.session.commit()
            
            session['user_id'] = user.id
            
            return {'id': user.id, 'username': user.username}, 201
            
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Username already exists'}, 422
        except ValueError as e:
            db.session.rollback()
            return {'error': str(e)}, 422

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return {'id': user.id, 'username': user.username}, 200
        
        return {'error': 'Invalid username or password'}, 401

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            return {'id': user.id, 'username': user.username}, 200
        
        return {}, 401

class Logout(Resource):
    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        
        return {'error': 'Not logged in'}, 401

# Workout Routes

class WorkoutIndex(Resource):
    def get(self):
        # Check if user is logged in
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Query only user's workouts with pagination
        pagination = Workout.query.filter_by(user_id=user_id).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Format workouts
        workouts = [{
            'id': w.id,
            'exercise': w.exercise,
            'sets': w.sets,
            'reps': w.reps,
            'duration': w.duration,
            'notes': w.notes,
            'date': w.date.isoformat(),
            'user_id': w.user_id
        } for w in pagination.items]
        
        return {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'total_pages': pagination.pages,
            'workouts': workouts
        }, 200
    
    def post(self):
        # Check if user is logged in
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        
        data = request.get_json()
        
        try:
            workout = Workout(
                exercise=data.get('exercise'),
                sets=data.get('sets'),
                reps=data.get('reps'),
                duration=data.get('duration'),
                notes=data.get('notes'),
                user_id=user_id  # Associate with logged-in user
            )
            
            db.session.add(workout)
            db.session.commit()
            
            return {
                'id': workout.id,
                'exercise': workout.exercise,
                'sets': workout.sets,
                'reps': workout.reps,
                'duration': workout.duration,
                'notes': workout.notes,
                'date': workout.date.isoformat(),
                'user_id': workout.user_id
            }, 201
            
        except ValueError as e:
            db.session.rollback()
            return {'error': str(e)}, 422

class WorkoutDetail(Resource):
    def get(self, id):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        
        # Find workout and ensure it belongs to user
        workout = Workout.query.filter_by(id=id, user_id=user_id).first()
        
        if not workout:
            return {'error': 'Workout not found'}, 404
        
        return {
            'id': workout.id,
            'exercise': workout.exercise,
            'sets': workout.sets,
            'reps': workout.reps,
            'duration': workout.duration,
            'notes': workout.notes,
            'date': workout.date.isoformat(),
            'user_id': workout.user_id
        }, 200
    
    def patch(self, id):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        
        # Find workout and ensure it belongs to user
        workout = Workout.query.filter_by(id=id, user_id=user_id).first()
        
        if not workout:
            return {'error': 'Workout not found'}, 404
        
        data = request.get_json()
        
        try:
            if 'exercise' in data:
                workout.exercise = data['exercise']
            if 'sets' in data:
                workout.sets = data['sets']
            if 'reps' in data:
                workout.reps = data['reps']
            if 'duration' in data:
                workout.duration = data['duration']
            if 'notes' in data:
                workout.notes = data['notes']
            
            db.session.commit()
            
            return {
                'id': workout.id,
                'exercise': workout.exercise,
                'sets': workout.sets,
                'reps': workout.reps,
                'duration': workout.duration,
                'notes': workout.notes,
                'date': workout.date.isoformat(),
                'user_id': workout.user_id
            }, 200
            
        except ValueError as e:
            db.session.rollback()
            return {'error': str(e)}, 422
    
    def delete(self, id):
        user_id = session.get('user_id')
        if not user_id:
            return {'error': 'Unauthorized'}, 401
        
        # Find workout and ensure it belongs to user
        workout = Workout.query.filter_by(id=id, user_id=user_id).first()
        
        if not workout:
            return {'error': 'Workout not found'}, 404
        
        db.session.delete(workout)
        db.session.commit()
        
        return {}, 204

# Register routes
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Logout, '/logout')
api.add_resource(WorkoutIndex, '/workouts')
api.add_resource(WorkoutDetail, '/workouts/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
