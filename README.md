## 📌 About the Project

`alx_travel_app` is the backend foundation for a travel listing platform. This milestone focuses on initializing the Django project, setting up MySQL as the backend database, and integrating Swagger for automatic API documentation. The project structure follows industry-standard best practices, making it scalable, secure, and team-friendly.

---

## 🎯 Learning Objectives

By completing this milestone, you will:

- ✅ Bootstrap a Django project with modular, production-ready configurations.
- ✅ Use `django-environ` to manage environment variables securely.
- ✅ Integrate **Swagger (drf-yasg)** for automated API documentation.
- ✅ Set up **CORS** headers to allow cross-origin requests.
- ✅ Configure **MySQL** as the main database engine.
- ✅ Follow Git version control practices for collaborative development.

---

## ⚙️ Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/xxxxxxxxxx/alx_travel_app.git
cd alx_travel_app
```

````

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory:

```ini
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

# MySQL Database Settings
DB_NAME=alxtravel
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 5. Run Initial Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🛠️ Technologies Used

- **Django** – Web framework
- **Django REST Framework** – API development
- **drf-yasg** – Swagger API documentation
- **django-environ** – Environment variable management
- **django-cors-headers** – CORS handling
- **MySQL** – Relational database
- **Celery & RabbitMQ** – (Installed for future use)
````
