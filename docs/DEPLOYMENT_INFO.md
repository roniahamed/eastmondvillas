# 🚀 Eastmond Villa Deployment Information

## Live Production Site

**Website:** [https://www.eastmondvillas.com/](https://www.eastmondvillas.com/)

### API Endpoints

- **Base API URL:** `https://api.eastmondvillas.com/api`
- **API Documentation:** `https://api.eastmondvillas.com/swagger/`

---

## Environment Configuration

### Local Development
```env
API_BASE_URL=http://localhost:8888/api
DEBUG=True
```

### Production
```env
API_BASE_URL=https://api.eastmondvillas.com/api
DEBUG=False
ALLOWED_HOSTS=www.eastmondvillas.com,eastmondvillas.com
```

---

## Quick Start Integration

### JavaScript/React
```javascript
// .env file
REACT_APP_API_URL=https://api.eastmondvillas.com/api

// In your code
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8888/api';
```

### Python
```python
import os
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8888/api')
# Production: https://www.eastmondvillas.com/api
```

### cURL
```bash
# Replace localhost with production URL
curl https://api.eastmondvillas.com/api/villas/properties/
```

---

## Postman Setup

### Import Collection
1. Open Postman
2. Import: `docs/Eastmond Villa API.postman_collection.json`
3. Import Environment: `docs/eastmondvilla-environment.json`

### Configure for Production
In your Postman environment, set:
```json
{
  "base_url": "https://api.eastmondvillas.com/api"
}
```

---

## Testing the Live API

### Check API Health
```bash
curl https://api.eastmondvillas.com/api/
```

### Get Properties (Public)
```bash
curl https://api.eastmondvillas.com/api/villas/properties/
```

### Login
```bash
curl -X POST https://api.eastmondvillas.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
```

---

## Documentation Files Updated

✅ **Postman Collection** - `docs/Eastmond Villa API.postman_collection.json`
- Updated description with live URL
- All endpoints tested and validated

✅ **API Integration Guide** - `docs/API_INTEGRATION_GUIDE.md`
- Updated version to 2.1 (Production Ready)
- Added both local and production base URLs
- Updated code examples with environment variable support
- Updated footer with live site link

✅ **README.md** - Project documentation
- Added live website link at the top
- Updated base URLs section with both environments
- Enhanced deployment section with production details
- Updated version to 3.1.0

---

## Features Available on Live Site

### ✅ Fully Functional
- User registration and authentication (JWT)
- Property browsing and search
- Booking creation and management
- Review system with image uploads
- Favorites/wishlist
- Admin panel with Unfold UI
- Google Calendar integration
- Real-time availability checking
- Analytics dashboard
- Agent management
- Notifications and announcements

### 🔒 Authentication
- JWT tokens (access + refresh)
- Role-based access control (Admin, Manager, Agent, Customer)
- Granular permissions (only_view, download, full_access)

### 📊 API Documentation
- Interactive Swagger UI
- ReDoc documentation
- OpenAPI 3.0 schema
- Postman collection

---

## Support & Contact

- **Issues:** Report on GitHub repository
- **Email:** support@eastmondvilla.com
- **Developer:** Roni Ahamed
- **Repository:** [github.com/roniahamed/eastmondvillas](https://github.com/roniahamed/eastmondvillas)

---

**Last Updated:** December 3, 2025  
**Version:** 3.1.0  
**Status:** ✅ Live & Operational
