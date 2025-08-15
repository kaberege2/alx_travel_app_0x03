# 🧭 ALX Travel App - Milestone 3: Listings, Bookings & Payments API

This milestone extends the Travel App with **payment initiation** for bookings and **automated confirmation emails** using Celery.

## 🚀 Project Overview

In this stage, we:

- Built CRUD API endpoints for **Listings** and **Bookings**.
- Added **payment initiation endpoint** for bookings.
- Integrated **Celery** to send booking confirmation emails asynchronously.
- Used `ModelViewSet` for RESTful API endpoints.
- Integrated Swagger (drf-yasg) for auto-generated API documentation.

---

## 🧱 Tech Stack

- Python 3.x
- Django 5.2.3
- Django REST Framework 3.16.0
- drf-yasg 1.21.10 (Swagger for API docs)
- django-environ
- PyMySQL
- Celery + Redis (for background tasks)

---

## 🧑‍💻 Custom User Model

We use a custom user model with roles:

- `guest`
- `host`
- `admin`

Users authenticate via email and have UUID primary keys.

---

## 🏠 Models Summary

### 📍 Listing

| Field         | Type      | Description            |
| ------------- | --------- | ---------------------- |
| property_id   | UUIDField | Unique property ID     |
| host          | FK(User)  | Host of the listing    |
| name          | CharField | Property name          |
| description   | TextField | Description            |
| location      | CharField | Location string        |
| pricepernight | Decimal   | Cost per night         |
| created_at    | DateTime  | Auto timestamp         |
| updated_at    | DateTime  | Auto updated timestamp |

### 📆 Booking

| Field       | Type        | Description                    |
| ----------- | ----------- | ------------------------------ |
| booking_id  | UUIDField   | Unique booking ID              |
| property    | FK(Listing) | Property booked                |
| user        | FK(User)    | Guest who made booking         |
| start_date  | DateField   | Booking start date             |
| end_date    | DateField   | Booking end date               |
| total_price | Decimal     | Total cost                     |
| status      | Choice      | pending / confirmed / canceled |
| created_at  | DateTime    | Auto timestamp                 |

---

## 🧩 API Endpoints

Base URL: `/api/`

### ✅ Listings Endpoints

| Method | Endpoint          | Description                 |
| ------ | ----------------- | --------------------------- |
| GET    | `/listings/`      | List all listings           |
| POST   | `/listings/`      | Create new listing          |
| GET    | `/listings/{id}/` | Retrieve a specific listing |
| PUT    | `/listings/{id}/` | Update listing              |
| DELETE | `/listings/{id}/` | Delete listing              |

### ✅ Bookings Endpoints

| Method | Endpoint                   | Description                  |
| ------ | -------------------------- | ---------------------------- |
| GET    | `/bookings/`               | List all bookings            |
| POST   | `/bookings/`               | Create new booking           |
| GET    | `/bookings/{id}/`          | Retrieve a booking           |
| PUT    | `/bookings/{id}/`          | Update booking               |
| DELETE | `/bookings/{id}/`          | Delete booking               |
| POST   | `/bookings/{id}/initiate/` | Initiate payment for booking |

---

## 💳 Payment & Email Flow

1. **Initiate Payment**

   - Send a `POST` request to `/bookings/{id}/initiate/`.
   - The system verifies booking details and prepares the payment process.

2. **On Successful Payment**

   - Booking status is updated to **confirmed**.
   - A **confirmation email** is sent to the user asynchronously using **Celery**.

3. **Email Sending**

   - Celery worker sends the email in the background.
   - Redis is used as the message broker.

---

## 📑 API Documentation

Visit:
🔗 [`/swagger/`](http://localhost:8000/swagger/) — Swagger UI
🔗 [`/redoc/`](http://localhost:8000/redoc/) — ReDoc UI

---

## 🔌 How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/kaberege2/alx_travel_app_0x01.git
   cd alx_travel_app
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up `.env` file:

   ```env
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=mysql://user:password@localhost:3306/travelapp
   CELERY_BROKER_URL=redis://localhost:6379/0
   ```

4. Run migrations:

   ```bash
   python manage.py migrate
   ```

5. Start Redis (in another terminal):

   ```bash
   redis-server
   ```

6. Start Celery worker:

   ```bash
   celery -A alx_travel_app worker --loglevel=info
   ```

7. Start development server:

   ```bash
   python manage.py runserver
   ```

---

## 🧪 Testing the API

Use **Postman**, **Insomnia**, or **Swagger UI** to:

- Create listings and bookings
- Initiate a payment for a booking
- Receive booking confirmation emails

---

## 📂 Project Structure

```
alx_travel_app/
├── bookings/
│   ├── models.py
│   ├── views.py
│   ├── tasks.py
│   ├── urls.py
│   └── serializers.py
├── listings/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
├── users/
│   ├── models.py
│   └── managers.py
├── settings.py
└── README.md
```
