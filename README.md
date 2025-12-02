# 🏝️ Eastmond Villa - Luxury Property Management System

A comprehensive Django REST API for managing luxury villa rentals and property sales, featuring role-based access control, booking management, Google Calendar integration, and advanced analytics.

🌐 **Live Website:** [https://www.eastmondvillas.com/](https://www.eastmondvillas.com/)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Deployment](#-deployment)

---

## ✨ Features

### 🔐 Authentication & Authorization
- JWT-based authentication (Simple JWT + dj-rest-auth)
- Role-based access control (Admin, Manager, Agent, Customer)
- Granular permissions (only_view, download, full_access)
- User registration, login, password reset


### 🏡 Property Management
- CRUD operations for luxury properties
- Multiple property types (rent/sale)
- Status workflow (draft → pending_review → published → archived/sold)
- Rich property data: amenities, location, pricing, staff details
- Image gallery management (general + bedroom images)
- Agent assignment to properties
- Property download tracking
- Advanced search, filtering, and ordering

### 📅 Booking System
- Complete booking lifecycle management
- Status transitions (pending → approved → rejected → completed → cancelled)
- Date conflict validation
- Real-time availability checking
- Monthly booking reports for agents
- Automatic analytics updates

### ⭐ Reviews & Favorites
- Customer reviews with rating system
- Multi-image review support
- Property favorites/wishlist
- Review moderation

### 📊 Analytics & Reporting
- Daily analytics tracking
- Property download metrics
- Booking statistics by date range
- Agent performance summaries
- Dashboard overview (properties, reviews, users)

### 🔔 Notifications & Announcements
- System notifications
- Announcement broadcasting
- Activity log tracking with audit trail

### 👥 User Management
- Admin panel for user CRUD
- Agent listing and summary
- Property assignment to agents
- User profile updates
- Role and permission management

### 📱 Additional Features
- Contact form submissions
- Resource library
- Activity logging (django-auditlog)
- CORS support for frontend integration
- OpenAPI/Swagger documentation (drf-spectacular)

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 5.2.7 + Django REST Framework 3.16.1
- **Database:** PostgreSQL (via psycopg 3.2.13)
- **Authentication:** dj-rest-auth 7.0.1 + Simple JWT 5.5.1
- **API Documentation:** drf-spectacular 0.29.0
- **Admin Interface:** django-unfold 0.69.0 (modern admin UI)

### Integrations
- **Google Calendar API:** Booking availability management
- **Redis:** Caching and WebSocket backend
- **Channels:** WebSocket support with Daphne

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL 14+
- Redis (for channels/caching)

### Installation

1. **Clone repository**
   ```bash
   git clone https://github.com/roniahamed/eastmondvillas.git
   cd eastmondvilla
   ```

2. **Create virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   
   Create `.env` file:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   DB_NAME=eastmondvilla_db
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   
   REDIS_URL=redis://localhost:6379
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py populate_villas  # Optional: sample data
   ```

6. **Run Server**
   ```bash
   python manage.py runserver 8888
   ```

7. **Access**
   - API: http://localhost:8888/api/
   - Admin: http://localhost:8888/admin/
   - Swagger: http://localhost:8888/swagger/

---

## 📚 API Documentation

### Base URLs

- **Local Development:** `http://localhost:8888/api`
- **Production (Live):** `https://api.eastmondvillas.com/api`

### Core Endpoints

**Authentication**
- `POST /registration/` - Register user
- `POST /auth/login/` - Login (JWT tokens)
- `GET /auth/user/` - Current user
- `POST /auth/token/refresh/` - Refresh token

**Properties**
- `GET /villas/properties/` - List properties
- `POST /villas/properties/` - Create property
- `GET /villas/properties/{id}/` - Property details
- `GET /villas/properties/{id}/availability/` - Check availability

**Bookings**
- `GET /villas/bookings/` - List bookings
- `POST /villas/bookings/` - Create booking
- `PATCH /villas/bookings/{id}/` - Update status

**Reviews & Favorites**
- `GET /villas/reviews/` - List reviews
- `POST /villas/reviews/` - Create review
- `POST /villas/favorites/toggle/` - Toggle favorite

**Admin**
- `GET /admin/users/` - List users
- `GET /agents/` - List agents
- `GET /villas/dashboard/` - Dashboard stats
- `GET /villas/analytics/` - Analytics

**Other**
- `GET /notifications/list/` - Notifications
- `GET /announcements/announcement/` - Announcements
- `POST /list_vila/contect/` - Contact form
- `GET /resources/` - Resources
- `GET /activity-log/list/` - Activity log

For complete documentation:
- **[API_INTEGRATION_GUIDE.md](docs/API_INTEGRATION_GUIDE.md)** - Detailed guide
- **[Postman Collection](docs/Eastmond%20Villa%20API.postman_collection.json)** - Import to Postman
- **[Environment File](docs/eastmondvilla-environment.json)** - Postman environment

---

## 📁 Project Structure

```
eastmondvilla/
├── accounts/          # User authentication
├── villas/            # Properties & bookings
├── announcements/     # System announcements
├── notifications/     # User notifications
├── resources/         # Resource library
├── activityLog/       # Audit trail
├── list_vila/         # Contact forms
├── docs/              # API documentation
├── media/             # Uploaded files
├── static/            # Static files
└── requirements.txt
```

---

## ⚙️ Configuration

### User Roles
| Role | Permission | Access |
|------|------------|--------|
| Admin | full_access | Full system access |
| Manager | full_access | Property & booking management |
| Agent | only_view | Assigned properties (if full_access) |
| Customer | only_view | View properties, create bookings |

### Status Workflows
- **Property:** draft → pending_review → published → archived/sold
- **Booking:** pending → approved/rejected → completed/cancelled

---

## 🚢 Deployment

### Production (Live Site)
The application is currently deployed and accessible at:
- **Website:** https://www.eastmondvillas.com/
- **API:** https://api.eastmondvillas.com/
- **API Docs:** https://api.eastmondvillas.com/swagger/

### Production Setup Checklist
1. Set `DEBUG=False`
2. Configure PostgreSQL (managed service)
3. Setup Redis (ElastiCache/Redis Labs)
4. Configure Google Calendar API
5. Collect static files: `python manage.py collectstatic`
6. Use Daphne/Gunicorn + Nginx
7. Setup SSL (Let's Encrypt)
8. Configure CORS for frontend domain
9. Set secure environment variables

### Docker
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 📞 Contact

- **Developer:** Roni Ahamed
- **Repository:** [github.com/roniahamed/eastmondvillas](https://github.com/roniahamed/eastmondvillas)

---

**Version:** 3.1.0 | **Updated:** December 3, 2025 | **Live:** [eastmondvillas.com](https://www.eastmondvillas.com/)
