***

# Leave Management System

A comprehensive, scalable leave management application built with **FastAPI** and server-side rendered HTML templates.  
It enables employee leave tracking, approval workflows, role-based access, JWT authentication, and modern UI components.

***

## 🚀 Features

- **Employee Management:** Add, update, and manage employee profiles and details.
- **Leave Application & Approval:** Submit and approve/reject leave requests with admin controls.
- **Leave Balance Tracking:** Monitor leave quotas and balances in real time.
- **Role-Based Access:** Secure JWT authentication for Admins and Employees.
- **Web Dashboard:** Dashboard with employee statistics and recent activities.
- **Responsive UI:** Bootstrap-based design for all devices.
- **RESTful APIs:** Well-documented (OpenAPI/Swagger) endpoints.
- **Database:** Uses NeonDB (or any PostgreSQL) with SQLAlchemy ORM.
- **Docker Support:** Fully containerized for deployment on Render, AWS, etc.

***

## 📦 Project Structure

```
leave_management/
│
├── app/
│   ├── api/             # API layer
│   ├── core/            # Configuration, security
│   ├── db/              # DB models, session, alembic
│   ├── schemas/         # Data models
│   ├── services/        # Business logic
│   ├── static/          # CSS, JS, images
│   ├── templates/       # HTML templates
│   └── main.py          # FastAPI app entrypoint
│
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

***

## 🛠️ Getting Started

### 1. Clone the repository

```bash
git clone 
cd leave_management
```

### 2. Set up environment variables

Copy `.env.example` to `.env` and update values with your NeonDB/Postgres credentials:

```dotenv
DATABASE_URL=postgresql://neondb_owner:@ep-dark-breeze-a29n10xy-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
BACKEND_CORS_ORIGINS=[]
DEFAULT_ADMIN_EMAIL=admin@company.com
DEFAULT_ADMIN_PASSWORD=admin123
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database & Run Migrations

```bash
alembic upgrade head
```

### 5. Start the Application

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

***

## 🐳 Docker Deployment

### Build and Run Locally

```bash
docker build -t leave-management .
docker run -p 8000:8000 --env-file .env leave-management
```

### Deploy on Render

- Create a new **Web Service**.
- Point to your repo and Dockerfile.
- Add all environment variables in Render dashboard.
- Hit deploy!

***

## 🔑 Default Admin Credentials

- **Email:** admin@company.com
- **Password:** admin123

***

## 🧪 Testing

Run the test suite:

```bash
pytest
```

***

## 📚 API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

***

## 🎯 Key API Endpoints

| Endpoint                       | Method | Description              |
|---------------------------------|--------|--------------------------|
| `/api/v1/auth/login`            | POST   | User authentication      |
| `/api/v1/employees/`            | GET,POST| Employee CRUD           |
| `/api/v1/leaves/`               | GET,POST| Leave requests          |
| `/api/v1/leaves/{id}/approve`   | POST   | Approve leave request   |
| `/api/v1/leaves/{id}/reject`    | POST   | Reject leave request    |

***

## 🆘 Troubleshooting

- **Database Connection Error:**  
  - Check if NeonDB/Postgres is running.
  - Verify your `DATABASE_URL` in `.env`.

- **App Startup Failure:**  
  - Confirm environment variables are set on Render.
  - Review Render service logs for Python errors or tracebacks.

- **Frontend Issues:**  
  - Confirm static files and templates paths in `main.py`.

***
