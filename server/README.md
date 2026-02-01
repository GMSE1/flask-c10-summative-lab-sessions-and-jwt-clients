# 💪 Workout Tracker API

A secure Flask REST API for tracking personal workouts with session-based authentication.

## 📋 Description

This API provides a complete backend for a workout tracking application. Users can:
- Register and authenticate securely with password hashing (bcrypt)
- Create, read, update, and delete their personal workouts
- View paginated workout history
- Maintain secure sessions with isolation between users

Built with Flask, SQLAlchemy, and Flask-RESTful following REST best practices.

---

## 🚀 Installation

### Prerequisites
- Python 3.14
- pipenv

### Setup Steps

1. **Clone the repository**
```bash
   git clone <your-repo-url>
   cd <repo-name>/server
```

2. **Install dependencies**
```bash
   pipenv install
   pipenv shell
```

3. **Initialize the database**
```bash
   flask db init
   flask db migrate -m "initial migration"
   flask db upgrade
```

4. **Seed the database (optional)**
```bash
   python seed.py
```
   This creates 3 demo users (user1, user2, user3) with password: `password123`

---

## ▶️ Running the Application
```bash
python app.py
```

The API will run on `http://localhost:5555`

---

## 📡 API Endpoints

### Authentication Endpoints

#### POST `/signup`
Register a new user and auto-login.

**Request Body:**
```json
{
  "username": "string",
  "password": "string",
  "password_confirmation": "string"
}
```

**Success Response (201):**
```json
{
  "id": 1,
  "username": "string"
}
```

**Error Response (422):**
```json
{
  "error": "Username already exists"
}
```

---

#### POST `/login`
Authenticate an existing user.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Success Response (200):**
```json
{
  "id": 1,
  "username": "string"
}
```

**Error Response (401):**
```json
{
  "error": "Invalid username or password"
}
```

---

#### GET `/check_session`
Check if user session is active (for auto-login on page refresh).

**Success Response (200):**
```json
{
  "id": 1,
  "username": "string"
}
```

**Not Logged In (401):**
```json
{}
```

---

#### DELETE `/logout`
End user session.

**Success Response (204):**
Empty response

**Error Response (401):**
```json
{
  "error": "Not logged in"
}
```

---

### Workout Endpoints

**Note:** All workout endpoints require authentication. Users can only access their own workouts.

#### GET `/workouts`
Get paginated list of current user's workouts.

**Query Parameters:**
- `page` (optional, default: 1) - Page number
- `per_page` (optional, default: 10) - Results per page

**Example:**
```
GET /workouts?page=1&per_page=5
```

**Success Response (200):**
```json
{
  "page": 1,
  "per_page": 5,
  "total": 23,
  "total_pages": 5,
  "workouts": [
    {
      "id": 1,
      "exercise": "Bench Press",
      "sets": 4,
      "reps": 10,
      "duration": 30,
      "notes": "Felt strong today",
      "date": "2026-01-31T19:00:00",
      "user_id": 1
    }
  ]
}
```

**Error Response (401):**
```json
{
  "error": "Unauthorized"
}
```

---

#### POST `/workouts`
Create a new workout for current user.

**Request Body:**
```json
{
  "exercise": "string (required)",
  "sets": "integer (required, min: 1)",
  "reps": "integer (required, min: 1)",
  "duration": "integer (optional, minutes)",
  "notes": "string (optional)"
}
```

**Success Response (201):**
```json
{
  "id": 1,
  "exercise": "Bench Press",
  "sets": 4,
  "reps": 10,
  "duration": 30,
  "notes": "Felt strong today",
  "date": "2026-01-31T19:00:00",
  "user_id": 1
}
```

**Error Responses:**
- 401: Not authenticated
- 422: Validation error (e.g., "Sets must be at least 1")

---

#### GET `/workouts/<id>`
Get a specific workout (only if it belongs to current user).

**Success Response (200):**
```json
{
  "id": 1,
  "exercise": "Bench Press",
  "sets": 4,
  "reps": 10,
  "duration": 30,
  "notes": "Felt strong today",
  "date": "2026-01-31T19:00:00",
  "user_id": 1
}
```

**Error Responses:**
- 401: Not authenticated
- 404: Workout not found or doesn't belong to user

---

#### PATCH `/workouts/<id>`
Update a specific workout (only if it belongs to current user).

**Request Body:** (all fields optional)
```json
{
  "exercise": "string",
  "sets": "integer",
  "reps": "integer",
  "duration": "integer",
  "notes": "string"
}
```

**Success Response (200):**
```json
{
  "id": 1,
  "exercise": "Bench Press",
  "sets": 5,
  "reps": 12,
  "duration": 35,
  "notes": "Increased weight!",
  "date": "2026-01-31T19:00:00",
  "user_id": 1
}
```

**Error Responses:**
- 401: Not authenticated
- 404: Workout not found or doesn't belong to user
- 422: Validation error

---

#### DELETE `/workouts/<id>`
Delete a specific workout (only if it belongs to current user).

**Success Response (204):**
Empty response

**Error Responses:**
- 401: Not authenticated
- 404: Workout not found or doesn't belong to user

---

## 🔒 Security Features

- **Password Hashing:** All passwords are hashed using bcrypt before storage
- **Session-Based Auth:** Secure session cookies manage user state
- **User Isolation:** Users can only access their own workout data
- **Input Validation:** All user inputs are validated before database operations
- **CORS Configuration:** Cross-origin requests properly configured

---

## 🗃️ Database Models

### User
- `id` - Primary key
- `username` - Unique, required
- `_password_hash` - Bcrypt hashed password
- `workouts` - One-to-many relationship with Workout

### Workout
- `id` - Primary key
- `exercise` - Required, workout name
- `sets` - Required, minimum 1
- `reps` - Required, minimum 1
- `duration` - Optional, in minutes
- `notes` - Optional, additional details
- `date` - Auto-generated timestamp
- `user_id` - Foreign key to User

---

## 🧪 Testing with cURL

### Login
```bash
curl -X POST http://localhost:5555/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "password123"}' \
  -c cookies.txt
```

### Get Workouts
```bash
curl "http://localhost:5555/workouts?page=1&per_page=5" \
  -b cookies.txt
```

### Create Workout
```bash
curl -X POST "http://localhost:5555/workouts" \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"exercise": "Squats", "sets": 5, "reps": 8, "duration": 25}'
```

---

## 👥 Author

Greg Marshall - Flatiron School Student

---

## 📄 License

This project is part of the Flatiron School curriculum.
