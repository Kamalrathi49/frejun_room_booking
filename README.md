# Virtual Workspace Room Booking System

## Overview
A RESTful API for managing workspace room bookings, cancellations, and availability. Supports private rooms, conference rooms (for teams), and shared desks, with all real-world constraints and priorities.

---

## Features
- Book a room (private, conference, shared desk)
- Cancel a booking
- List all bookings (with user, team, and room info)
- List available rooms per slot
- Team and member management for conference bookings
- User authentication (JWT)
- All endpoints protected (except signup/login)
- Dockerized for easy setup
- Comprehensive test suite

---

## API Endpoints

### User APIs
- **POST** `/api/v1/users/auth/signup/` — User signup
- **POST** `/api/v1/users/auth/login/` — User login
- **GET/PATCH** `/api/v1/users/users/{user_uuid}/` — User detail/update

### Team APIs
- **POST** `/api/v1/bookings/teams/` — Create team
- **GET** `/api/v1/bookings/teams/` — List teams

### Member APIs
- **POST** `/api/v1/bookings/members/` — Add team member
- **GET** `/api/v1/bookings/members/` — List all members
- **GET** `/api/v1/bookings/members/?team={team_uuid}` — List members by team

### Booking APIs
- **POST** `/api/v1/bookings/` — Book a room
- **POST** `/api/v1/bookings/{booking_uuid}/cancel/` — Cancel a booking
- **GET** `/api/v1/bookings/` — List all bookings
- **GET** `/api/v1/bookings/rooms/available/` — List available rooms (optionally filter by `date` and `slot`)

---

## Booking Rules & Constraints
- 15 rooms: 8 private, 4 conference, 3 shared desks (4 users each)
- Private: 1 user per slot
- Conference: team of 3+ members per slot
- Shared desk: up to 4 users per slot, auto-filled
- Time slots: 9AM–6PM (hourly)
- No double-booking for user/team/room/slot
- Children (age < 10) included in headcount but do not occupy a seat
- Cancellations free up slots

---

## Project Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Create `.env` File
Create a `.env` file in the root directory with at least:
```
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
DJANGO_READ_DOT_ENV_FILE=True
```

### 3. Build and Run with Docker
```bash
docker-compose up --build
```
- The API will be available at `http://localhost:8000/`
- The default DB is Postgres (see `docker-compose.yml`)

### 4. Run Migrations & Create Superuser
In a new terminal:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 5. (Optional) Seed Initial Data
You can use Django admin or API endpoints to create rooms, teams, and members.

---

## Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `True` for development
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `DJANGO_READ_DOT_ENV_FILE`: Should be `True` to load `.env`

---

## Running Tests
```bash
docker-compose exec web python manage.py test
```

---

## API Authentication
- Uses JWT (SimpleJWT)
- Obtain tokens via `/api/v1/users/auth/login/`
- Pass `Authorization: Bearer <access_token>` in headers for all protected endpoints

---

## Postman Collection
A ready-to-use Postman collection is included as `room-booking.postman_collection.json` (import into Postman for all endpoints and example payloads).

---

## Assumptions & Notes
- All UUIDs must be valid and exist in the DB
- Room, team, and member creation is required before booking conference rooms
- All time slots are in `HH:MM:SS` format (e.g., `09:00:00`)
- All endpoints except signup/login require authentication

---