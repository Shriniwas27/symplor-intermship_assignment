# Leave Management System

A comprehensive, scalable leave management system built with FastAPI, featuring both REST APIs and a web frontend with modern UI components.

## 🚀 Features

### Core Functionality
- **Employee Management**: Add, update, and manage employee profiles
- **Leave Application**: Submit leave requests with validation
- **Approval Workflow**: Approve or reject leave requests with admin controls
- **Balance Tracking**: Real-time leave balance monitoring
- **Dashboard**: Comprehensive overview with statistics and recent activities

### Technical Features
- **RESTful APIs**: Well-documented API endpoints with OpenAPI/Swagger
- **Authentication**: JWT-based secure authentication
- **Role-based Access**: Admin and employee role separation
- **Database Management**: SQLAlchemy ORM with PostgreSQL
- **Responsive UI**: Bootstrap-based responsive web interface
- **Docker Support**: Containerized deployment
- **Migration Support**: Alembic for database schema management

## 📋 Requirements

- Python 3.11+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

## 🛠️ Installation & Setup

### Option 1: Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd leave_management
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up PostgreSQL database**
```bash
# Create database
createdb leave_management
```

5. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env file with your database credentials
```

6. **Run database migrations**
```bash
alembic upgrade head
```

7. **Start the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Docker Setup (Recommended)

1. **Clone and navigate**
```bash
git clone <repository-url>
cd leave_management
```

2. **Start with Docker Compose**
```bash
docker-compose up -d
```

The application will be available at: http://localhost:8000

## 🔑 Default Credentials

- **Admin Email**: admin@company.com
- **Admin Password**: admin123

## 📚 API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login` | POST | User authentication |
| `/api/v1/employees/` | GET/POST | Employee management |
| `/api/v1/employees/{id}` | GET/PUT/DELETE | Individual employee operations |
| `/api/v1/leaves/` | GET/POST | Leave request operations |
| `/api/v1/leaves/{id}/approve` | POST | Approve leave request |
| `/api/v1/leaves/{id}/reject` | POST | Reject leave request |

### Sample API Calls

**Login**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@company.com", "password": "admin123"}'
```

**Add Employee**
```bash
curl -X POST "http://localhost:8000/api/v1/employees/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@company.com",
    "department": "Engineering",
    "joining_date": "2024-01-15"
  }'
```

**Apply for Leave**
```bash
curl -X POST "http://localhost:8000/api/v1/leaves/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "start_date": "2024-12-20",
    "end_date": "2024-12-22",
    "leave_type": "vacation",
    "reason": "Holiday vacation"
  }'
```

## 🏗️ Project Structure

```
leave_management/
├── app/
│   ├── api/                    # API layer
│   │   ├── v1/
│   │   │   ├── endpoints/      # API endpoints
│   │   │   └── api.py         # API router
│   │   └── dependencies.py    # FastAPI dependencies
│   ├── core/                  # Core configuration
│   │   ├── config.py         # Settings
│   │   └── security.py       # Authentication
│   ├── db/                    # Database layer
│   │   ├── models/           # SQLAlchemy models
│   │   ├── session.py        # Database session
│   │   └── base.py          # Base model imports
│   ├── schemas/              # Pydantic schemas
│   ├── services/             # Business logic layer
│   ├── static/               # Static files (CSS, JS)
│   ├── templates/            # HTML templates
│   └── main.py              # FastAPI application
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 🎯 Edge Cases Handled

### Date Validation
- ✅ End date must be after start date
- ✅ Cannot apply for leave before joining date
- ✅ Weekend exclusion in business days calculation

### Business Logic
- ✅ Insufficient leave balance validation
- ✅ Overlapping leave request detection
- ✅ Employee existence validation
- ✅ Active employee validation
- ✅ Admin-only operations protection

### Data Integrity
- ✅ Email uniqueness enforcement
- ✅ Proper foreign key relationships
- ✅ Status transition validation
- ✅ Concurrent request handling

## 🔄 Database Migrations

Create new migration:
```bash
alembic revision --autogenerate -m "Description"
```

Apply migrations:
```bash
alembic upgrade head
```

Downgrade:
```bash
alembic downgrade -1
```

## 🧪 Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

## 🚀 Deployment

### Heroku Deployment

1. **Create Heroku app**
```bash
heroku create your-app-name
```

2. **Set environment variables**
```bash
heroku config:set DATABASE_URL=postgresql://...
heroku config:set SECRET_KEY=your-secret-key
```

3. **Deploy**
```bash
git push heroku main
```

### Render Deployment

1. Connect GitHub repository
2. Set environment variables
3. Deploy automatically

## 📈 Scaling Considerations

### From 50 to 500+ employees:

1. **Database Optimization**
   - Database indexing on frequently queried columns
   - Connection pooling
   - Read replicas for reporting

2. **Application Scaling**
   - Horizontal scaling with load balancers
   - Caching layer (Redis)
   - Background job processing (Celery)

3. **Infrastructure**
   - Kubernetes orchestration
   - CDN for static files
   - Monitoring and logging (Prometheus, Grafana)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 |
| `DEFAULT_ADMIN_EMAIL` | Default admin email | admin@company.com |
| `DEFAULT_ADMIN_PASSWORD` | Default admin password | admin123 |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify PostgreSQL is running
   - Check DATABASE_URL in .env file

2. **Authentication Issues**
   - Verify SECRET_KEY is set
   - Check token expiration

3. **Frontend Not Loading**
   - Ensure static files are properly mounted
   - Check template directory path

### Support

For issues and questions:
- Check the documentation
- Review API responses for error details
- Enable debug mode for detailed error messages

## 🎉 Demo

- **Live Demo**: [Deploy URL will be here]
- **Admin Login**: admin@company.com / admin123
- **Sample Employee**: employee@company.com / employee123