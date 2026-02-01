from config import app, db
from models import User, Workout
from faker import Faker
from random import randint, choice
from datetime import datetime, timedelta

fake = Faker()

# Exercise options
exercises = [
    "Bench Press", "Squats", "Deadlifts", "Pull-ups", "Push-ups",
    "Bicep Curls", "Tricep Dips", "Lunges", "Plank", "Running",
    "Cycling", "Shoulder Press", "Leg Press", "Lat Pulldown", "Rows"
]

def seed_data():
    print("🌱 Clearing database...")
    Workout.query.delete()
    User.query.delete()
    db.session.commit()
    
    print("👤 Creating users...")
    users = []
    
    # Create 3 demo users
    for i in range(1, 4):
        user = User(username=f"user{i}")
        user.password_hash = "password123"
        users.append(user)
        db.session.add(user)
    
    db.session.commit()
    print(f"✅ Created {len(users)} users")
    
    print("💪 Creating workouts...")
    workout_count = 0
    
    # Create 5-10 workouts for each user
    for user in users:
        num_workouts = randint(5, 10)
        
        for _ in range(num_workouts):
            workout = Workout(
                exercise=choice(exercises),
                sets=randint(3, 5),
                reps=randint(8, 15),
                duration=randint(20, 60),
                notes=fake.sentence(),
                date=datetime.utcnow() - timedelta(days=randint(0, 30)),
                user_id=user.id
            )
            db.session.add(workout)
            workout_count += 1
    
    db.session.commit()
    print(f"✅ Created {workout_count} workouts")
    
    print("\n🎉 Seeding complete!")
    print("\n📋 Demo credentials:")
    print("   Username: user1, Password: password123")
    print("   Username: user2, Password: password123")
    print("   Username: user3, Password: password123")

if __name__ == '__main__':
    with app.app_context():
        seed_data()
