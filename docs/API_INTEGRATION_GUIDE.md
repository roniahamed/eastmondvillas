# 📘 Eastmond Villa API - Complete Integration Guide

**Version:** 2.0  
**Base URL:** `http://localhost:8888/api`  
**Authentication:** JWT Bearer Token (dj-rest-auth)  
**Content-Type:** `application/json`

---

## 📑 Table of Contents

1. [Authentication](#authentication)
2. [User Management (Admin)](#user-management-admin)
3. [Properties API](#properties-api)
4. [Bookings API](#bookings-api)
5. [Media Management](#media-management)
6. [Google Calendar Integration](#google-calendar-integration)
7. [Error Handling](#error-handling)
8. [Code Examples](#code-examples)

---

## 🔐 Authentication

All authentication is handled via **dj-rest-auth** package with JWT tokens.

### User Roles & Permissions

| Role | Permission Options | Default Permission |
|------|-------------------|-------------------|
| `customer` | `only_view`, `download`, `full_access` | `only_view` |
| `agent` | `only_view`, `download`, `full_access` | `only_view` |
| `manager` | `only_view`, `download`, `full_access` | `full_access` |
| `admin` | `only_view`, `download`, `full_access` | `full_access` |

---

### 1. Register New User

**Endpoint:** `POST /api/registration/`  
**Authentication:** None (Public)  
**Description:** Register a new user account. All new users are created as `customer` with `only_view` permission.

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+1234567890",
  "password1": "SecurePass123!",
  "password2": "SecurePass123!"
}
```

**Request Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Valid email address (unique) |
| `name` | string | Yes | User's full name |
| `phone` | string | No | Phone number |
| `password1` | string | Yes | Password (min 8 chars) |
| `password2` | string | Yes | Password confirmation (must match) |

**Success Response (201 Created):**
```json
{
  "pk": 12,
  "id": 12,
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+1234567890",
  "role": "customer",
  "permission": "only_view",
  "is_active": true,
  "is_verified": false,
  "is_staff": false,
  "date_joined": "2025-11-19T10:30:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "email": ["User with this email already exists."],
  "password1": ["This password is too short."]
}
```

**Note:** Users cannot set their own role or permission during registration. Only admins can assign roles via the Admin API.

---

### 2. Login (Get Access Token)

**Endpoint:** `POST /api/auth/login/`  
**Authentication:** None (Public)  
**Description:** Authenticate user and receive JWT access and refresh tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Success Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "pk": 12,
    "id": 12,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "customer",
    "permission": "only_view",
    "is_active": true,
    "is_verified": false,
    "phone": "+1234567890",
    "address": null,
    "date_joined": "2025-11-19T10:30:00Z",
    "is_staff": false
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "non_field_errors": ["Unable to log in with provided credentials."]
}
```

**Token Usage:**
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### 3. Refresh Access Token

**Endpoint:** `POST /api/auth/token/refresh/`  
**Authentication:** None  
**Description:** Get a new access token using refresh token.

**Request Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Success Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 4. Get Current User

**Endpoint:** `GET /api/auth/user/`  
**Authentication:** Required (Bearer Token)  
**Description:** Get authenticated user's profile information.

**Request Headers:**
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200 OK):**
```json
{
  "pk": 12,
  "id": 12,
  "email": "user@example.com",
  "name": "John Doe",
  "phone": "+1234567890",
  "address": "123 Main Street",
  "role": "customer",
  "permission": "only_view",
  "is_active": true,
  "is_verified": false,
  "is_staff": false,
  "date_joined": "2025-11-19T10:30:00Z"
}
```

---

### 5. Update Current User

**Endpoint:** `PATCH /api/auth/user/`  
**Authentication:** Required (Bearer Token)  
**Description:** Update authenticated user's profile (name, phone, address only).

**Request Body:**
```json
{
  "name": "John Updated",
  "phone": "+1987654321",
  "address": "456 New Street"
}
```

**Success Response (200 OK):**
```json
{
  "pk": 12,
  "id": 12,
  "email": "user@example.com",
  "name": "John Updated",
  "phone": "+1987654321",
  "address": "456 New Street",
  "role": "customer",
  "permission": "only_view"
}
```

**Note:** Users cannot change their own role or permission. Only admins can do this via Admin API.

---

### 6. Logout

**Endpoint:** `POST /api/auth/logout/`  
**Authentication:** Required (Bearer Token)  
**Description:** Logout user (blacklist tokens).

**Success Response (200 OK):**
```json
{
  "detail": "Successfully logged out."
}
```

---

### 7. Change Password

**Endpoint:** `POST /api/auth/password/change/`  
**Authentication:** Required (Bearer Token)  
**Description:** Change authenticated user's password.

**Request Body:**
```json
{
  "old_password": "OldPass123!",
  "new_password1": "NewPass123!",
  "new_password2": "NewPass123!"
}
```

**Success Response (200 OK):**
```json
{
  "detail": "New password has been saved."
}
```

---

### 8. Password Reset (Request)

**Endpoint:** `POST /api/auth/password/reset/`  
**Authentication:** None  
**Description:** Request password reset email.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Success Response (200 OK):**
```json
{
  "detail": "Password reset e-mail has been sent."
}
```

---

### 9. Password Reset (Confirm)

**Endpoint:** `POST /api/auth/password/reset/confirm/`  
**Authentication:** None  
**Description:** Reset password using token from email.

**Request Body:**
```json
{
  "uid": "user-id-encoded",
  "token": "reset-token-from-email",
  "new_password1": "NewPassword123!",
  "new_password2": "NewPassword123!"
}
```

**Success Response (200 OK):**
```json
{
  "detail": "Password has been reset with the new password."
}
```

---

## 👑 User Management (Admin)

**Base URL:** `/api/admin/users/`  
**Required Role:** Admin (role = `admin` and is_staff = `true`)

### 1. List All Users

**Endpoint:** `GET /api/admin/users/`  
**Authentication:** Required (Admin Only)  
**Description:** Get list of all users in the system (ordered by most recent first).

**Request Headers:**
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Success Response (200 OK):**
```json
[
  {
    "id": 5,
    "email": "manager@eastmondvilla.com",
    "name": "Manager User",
    "role": "manager",
    "permission": "full_access",
    "phone": "+1234567890",
    "address": "123 Manager St",
    "is_verified": true,
    "is_active": true,
    "is_staff": false
  },
  {
    "id": 8,
    "email": "agent@eastmondvilla.com",
    "name": "Agent User",
    "role": "agent",
    "permission": "full_access",
    "phone": "+1234567891",
    "address": null,
    "is_verified": false,
    "is_active": true,
    "is_staff": false
  }
]
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 2. Get User Details

**Endpoint:** `GET /api/admin/users/{user_id}/`  
**Authentication:** Required (Admin Only)  
**Description:** Get detailed information about a specific user.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | integer | Yes | User's unique ID |

**Success Response (200 OK):**
```json
{
  "id": 5,
  "email": "manager@eastmondvilla.com",
  "name": "Manager User",
  "role": "manager",
  "permission": "full_access",
  "phone": "+1234567890",
  "address": "123 Manager St",
  "is_verified": true,
  "is_active": true,
  "is_staff": false
}
```

---

### 3. Create User (Admin)

**Endpoint:** `POST /api/admin/users/`  
**Authentication:** Required (Admin Only)  
**Description:** Create a new user with specific role and permissions.

**Request Body:**
```json
{
  "email": "newmanager@example.com",
  "name": "New Manager",
  "password": "SecurePass123!",
  "phone": "+1234567890",
  "address": "789 Office Blvd",
  "role": "manager",
  "permission": "full_access",
  "is_active": true,
  "is_staff": false
}
```

**Required Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | Valid email address (unique) |
| `name` | string | Yes | User's full name |
| `password` | string | Yes | Password (min 8 chars) |
| `phone` | string | Yes | Phone number |
| `role` | string | Yes | Role: `customer`, `agent`, `manager`, `admin` |
| `permission` | string | Yes | Permission: `only_view`, `download`, `full_access` |

**Optional Fields:**
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `address` | string | null | User's address |
| `is_active` | boolean | true | Account active status |
| `is_staff` | boolean | false | Django admin access |

**Success Response (201 Created):**
```json
{
  "id": 25,
  "email": "newmanager@example.com",
  "name": "New Manager",
  "phone": "+1234567890",
  "address": "789 Office Blvd",
  "role": "manager",
  "permission": "full_access",
  "is_verified": false,
  "is_active": true,
  "is_staff": false
}
```

**Error Response (400 Bad Request):**
```json
{
  "email": ["A user with that email already exists."],
  "phone": ["This field is required."]
}
```

---

### 4. Update User (Admin)

**Endpoint:** `PATCH /api/admin/users/{user_id}/`  
**Authentication:** Required (Admin Only)  
**Description:** Update user information, role, or permissions (partial update).

**Request Body (Example):**
```json
{
  "role": "agent",
  "permission": "download",
  "is_active": true
}
```

**Updatable Fields:**
- `email` (must be unique)
- `name`
- `phone`
- `address`
- `role`
- `permission`
- `is_active`
- `is_staff`
- `password` (if provided, will be hashed)

**Success Response (200 OK):**
```json
{
  "id": 25,
  "email": "newmanager@example.com",
  "name": "New Manager",
  "role": "agent",
  "permission": "download",
  "is_active": true
}
```

---

### 5. Delete User (Admin)

**Endpoint:** `DELETE /api/admin/users/{user_id}/`  
**Authentication:** Required (Admin Only)  
**Description:** Permanently delete a user account.

**Success Response (204 No Content):**
```
(Empty response body)
```

**Note:** If deletion fails due to foreign key constraints, the user will be anonymized (email changed, name set to "[deleted]", is_active set to false).

---

### 6. Delete User (Self or Admin)

**Endpoint:** `DELETE /api/auth/users/{user_id}/`  
**Authentication:** Required  
**Description:** Delete user account. Users can delete their own account, or admins/staff can delete any account.

**Permissions:**
- Users can delete their own account (user_id matches authenticated user)
- Users with `is_staff=true` can delete any account
- Users with `role=admin` can delete any account

**Success Response (204 No Content):**
```
(Empty response body)
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## 🏡 Properties API

**Base URL:** `/api/villas/properties/`

### Property Model Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique property ID |
| `title` | string | Property name/title |
| `slug` | string | URL-friendly slug (auto-generated) |
| `description` | text | Detailed property description |
| `price` | decimal | Base price (per night or sale price) |
| `booking_rate` | JSON | Custom booking rates: `{"booking": [{"day": 2, "price": 500}]}` |
| `listing_type` | string | `rent` or `sale` |
| `status` | string | `draft`, `pending_review`, `published`, `archived`, `sold` |
| `address` | string | Full street address |
| `city` | string | City name |
| `max_guests` | integer | Maximum guest capacity |
| `bedrooms` | integer | Number of bedrooms |
| `bathrooms` | integer | Number of bathrooms |
| `has_pool` | boolean | Has swimming pool |
| `amenities` | JSON | Property amenities: `{"wifi": true, "pool": "private"}` |
| `latitude` | decimal | GPS latitude (max 9 digits, 6 decimals) |
| `longitude` | decimal | GPS longitude (max 9 digits, 6 decimals) |
| `place_id` | string | Google Places ID |
| `seo_title` | string | SEO-optimized title |
| `seo_description` | text | SEO-optimized description |
| `signature_distinctions` | JSON array | Unique features: `["Ocean view", "Private beach"]` |
| `staff` | JSON array | Staff details: `[{"role": "chef", "name": "John"}]` |
| `calendar_link` | URL | External booking calendar link |
| `google_calendar_id` | string | Google Calendar ID for booking management |
| `assigned_agent` | integer | Agent user ID (must have role='agent') |
| `created_by` | object | User who created the property |
| `created_at` | datetime | Creation timestamp |
| `updated_at` | datetime | Last update timestamp |
| `media` | array | Array of media files (images, videos, etc.) |
| `location_coords` | object | `{"lat": 25.7907, "lng": -80.1300}` |

---

### 1. List All Properties

**Endpoint:** `GET /api/villas/properties/`  
**Authentication:** None (Public can see published properties)  
**Description:** Get list of all properties.

**Visibility Rules:**
- **Anonymous users:** Only see `published` properties
- **Customers:** Only see `published` properties
- **Agents:** See properties assigned to them
- **Managers/Admins:** See all properties

**Success Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Luxury Beach Villa",
    "slug": "luxury-beach-villa",
    "description": "Beautiful 5-bedroom villa with ocean views",
    "price": "750.00",
    "booking_rate": {
      "booking": [
        {"day": 2, "price": 500}
      ]
    },
    "listing_type": "rent",
    "status": "published",
    "address": "123 Ocean Drive",
    "city": "Miami Beach",
    "max_guests": 10,
    "bedrooms": 5,
    "bathrooms": 4,
    "has_pool": true,
    "amenities": {
      "wifi": true,
      "pool": "private",
      "parking": true
    },
    "latitude": "25.790700",
    "longitude": "-80.130000",
    "place_id": "ChIJXXXXXXXXXXX",
    "seo_title": "Luxury Beach Villa Miami - 5BR Oceanfront",
    "seo_description": "Rent our stunning luxury villa...",
    "signature_distinctions": ["Ocean View", "Private Beach Access"],
    "staff": [
      {"role": "chef", "name": "John Doe"},
      {"role": "concierge", "name": "Jane Smith"}
    ],
    "calendar_link": "https://calendar.google.com/...",
    "created_at": "2025-11-10T08:00:00Z",
    "updated_at": "2025-11-18T14:30:00Z",
    "assigned_agent": 8,
    "created_by_name": "Admin User",
    "media": [
      {
        "id": 5,
        "media_type": "image",
        "category": "media",
        "file": "/media/property_media/villa-1-main.jpg",
        "file_url": "http://localhost:8888/media/property_media/villa-1-main.jpg",
        "caption": "Main View",
        "is_primary": true,
        "order": 0
      },
      {
        "id": 6,
        "media_type": "image",
        "category": "bedroom",
        "file": "/media/property_media/villa-1-bedroom.jpg",
        "file_url": "http://localhost:8888/media/property_media/villa-1-bedroom.jpg",
        "caption": "Master Bedroom",
        "is_primary": false,
        "order": 1
      }
    ],
    "location_coords": {
      "lat": 25.7907,
      "lng": -80.13
    }
  }
]
```

---

### 2. Get Property Details

**Endpoint:** `GET /api/villas/properties/{property_id}/`  
**Authentication:** None (Public for published properties)  
**Description:** Get detailed information about a specific property.

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `property_id` | integer | Yes | Property's unique ID |

**Success Response:** Same structure as List All Properties (single object)

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

### 3. Create Property

**Endpoint:** `POST /api/villas/properties/`  
**Authentication:** Required (Admin or Manager)  
**Content-Type:** `multipart/form-data`  
**Description:** Create a new property with optional media files.

**Request Body (Form Data):**
```
title: "Luxury Beach Villa"
description: "Beautiful 5-bedroom villa with ocean views"
price: 750.00
listing_type: "rent"
status: "draft"
address: "123 Ocean Drive"
city: "Miami Beach"
max_guests: 10
bedrooms: 5
bathrooms: 4
has_pool: true
amenities: {"wifi": true, "pool": "private"}
latitude: 25.790700
longitude: -80.130000
assigned_agent: 8
media_files: [file1.jpg, file2.jpg]
media_metadata: ['{"category": "media", "caption": "Main View", "is_primary": true, "order": 0}', '{"category": "bedroom", "caption": "Master Bedroom", "order": 1}']
```

**Required Fields:**
| Field | Type | Required |
|-------|------|----------|
| `title` | string | Yes |
| `price` | decimal | Yes |
| `address` | string | Yes |
| `city` | string | Yes |
| `max_guests` | integer | Yes |
| `bedrooms` | integer | Yes |
| `bathrooms` | integer | Yes |

**Media Files (Optional):**
- `media_files`: Array of files (images, videos, PDFs)
- `media_metadata`: Array of JSON strings (one per file)
- **Important:** Number of files must match number of metadata entries

**Media Metadata Structure:**
```json
{
  "category": "media|bedroom|bathroom|exterior|other",
  "caption": "Optional description",
  "is_primary": true,
  "order": 0
}
```

**Success Response (201 Created):**
```json
{
  "id": 45,
  "title": "Luxury Beach Villa",
  "slug": "luxury-beach-villa",
  "price": "750.00",
  "status": "draft",
  "created_at": "2025-11-19T12:00:00Z",
  "created_by_name": "Admin User",
  "media": [
    {
      "id": 25,
      "media_type": "image",
      "category": "media",
      "file_url": "http://localhost:8888/media/property_media/villa-main.jpg",
      "caption": "Main View",
      "is_primary": true,
      "order": 0
    }
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Mismatch between files and metadata."
}
```

**Validation:**
- If both `latitude` and `longitude` are provided, they must be valid coordinates
- Cannot provide only one coordinate (both or neither)
- `assigned_agent` must be a user with `role='agent'`
- Media files are automatically categorized by file extension

**Google Calendar Integration:**
- Upon creation, a Google Calendar is automatically created for the property
- The `google_calendar_id` is saved to the property

---

### 4. Update Property

**Endpoint:** `PATCH /api/villas/properties/{property_id}/`  
**Authentication:** Required (Admin, Manager, or Agent with full_access)  
**Content-Type:** `application/json` or `multipart/form-data`  
**Description:** Update property information (partial update).

**Permissions:**
- **Admin/Manager:** Can update any property
- **Agent with full_access permission:** Can update properties assigned to them

**Request Body (JSON Example):**
```json
{
  "price": "800.00",
  "status": "published",
  "amenities": {
    "wifi": true,
    "pool": "private",
    "hot_tub": true
  }
}
```

**Success Response (200 OK):**
```json
{
  "id": 45,
  "title": "Luxury Beach Villa",
  "price": "800.00",
  "status": "published",
  "updated_at": "2025-11-19T12:30:00Z"
}
```

**Error Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 5. Delete Property

**Endpoint:** `DELETE /api/villas/properties/{property_id}/`  
**Authentication:** Required (Admin or Manager Only)  
**Description:** Delete a property.

**Success Response (204 No Content):**
```
(Empty response body)
```

---

### 6. Check Property Availability

**Endpoint:** `GET /api/villas/properties/{property_id}/availability/`  
**Authentication:** None (Public)  
**Description:** Get booked dates for a property from Google Calendar.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `month` | integer | No | Current month | Month (1-12) |
| `year` | integer | No | Current year | Year (e.g., 2025) |

**Request Example:**
```http
GET /api/villas/properties/1/availability/?month=12&year=2025
```

**Success Response (200 OK):**
```json
[
  {
    "start": "2025-12-24",
    "end": "2025-12-26"
  },
  {
    "start": "2025-12-31",
    "end": "2026-01-02"
  }
]
```

**Response:** Array of date ranges that are booked

**Error Response (404 Not Found):**
```json
{
  "error": "Property not found."
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Booking calendar is not configured for this property."
}
```

**Note:** This endpoint queries the property's Google Calendar to get real-time availability.

---

## 📅 Bookings API

**Base URL:** `/api/villas/bookings/`

### Booking Model Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique booking ID |
| `property` | integer | Property ID (write-only) |
| `property_details` | object | Property info (read-only) |
| `user` | integer | User ID (auto-set from authenticated user) |
| `user_details` | object | User info (read-only) |
| `email` | email | Guest's email |
| `phone` | string | Guest's phone number |
| `check_in` | date | Check-in date (YYYY-MM-DD) |
| `check_out` | date | Check-out date (YYYY-MM-DD) |
| `total_price` | decimal | Total booking price |
| `status` | string | `pending`, `approved`, `rejected`, `completed`, `cancelled` |
| `google_event_id` | string | Google Calendar event ID |
| `created_at` | datetime | Booking creation timestamp |

---

### 1. List My Bookings

**Endpoint:** `GET /api/villas/bookings/`  
**Authentication:** Required  
**Description:** Get list of bookings for authenticated user.

**Visibility Rules:**
- **Customers/Agents:** See only their own bookings
- **Managers/Admins:** See all bookings

**Success Response (200 OK):**
```json
[
  {
    "id": 123,
    "property": 1,
    "property_details": {
      "id": 1,
      "title": "Luxury Beach Villa"
    },
    "email": "user@example.com",
    "phone": "+1234567890",
    "check_in": "2025-12-15",
    "check_out": "2025-12-22",
    "total_price": "5250.00",
    "user": 12,
    "user_details": {
      "id": 12,
      "name": "John Doe",
      "email": "user@example.com"
    },
    "status": "approved",
    "google_event_id": "abc123xyz",
    "created_at": "2025-11-15T10:30:00Z"
  }
]
```

---

### 2. Get Booking Details

**Endpoint:** `GET /api/villas/bookings/{booking_id}/`  
**Authentication:** Required  
**Description:** Get detailed information about a specific booking.

**Permissions:**
- **Booking owner:** Can view their own bookings
- **Admin/Manager:** Can view any booking

**Success Response (200 OK):** Same structure as List My Bookings (single object)

**Error Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 3. Create Booking

**Endpoint:** `POST /api/villas/bookings/`  
**Authentication:** Required  
**Description:** Create a new booking for a property.

**Request Body:**
```json
{
  "property": 1,
  "email": "user@example.com",
  "phone": "+1234567890",
  "check_in": "2025-12-15",
  "check_out": "2025-12-22",
  "total_price": "5250.00"
}
```

**Required Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `property` | integer | Yes | Property ID to book |
| `email` | email | Yes | Guest's email |
| `phone` | string | Yes | Guest's phone |
| `check_in` | date | Yes | Check-in date (YYYY-MM-DD) |
| `check_out` | date | Yes | Check-out date (YYYY-MM-DD) |
| `total_price` | decimal | Yes | Total booking price |

**Validation Rules:**
- `check_out` must be after `check_in`
- `check_in` cannot be in the past
- If property has Google Calendar configured, checks for date conflicts
- Dates must not overlap with existing approved bookings

**Success Response (201 Created):**
```json
{
  "id": 125,
  "property": 1,
  "property_details": {
    "id": 1,
    "title": "Luxury Beach Villa"
  },
  "email": "user@example.com",
  "phone": "+1234567890",
  "check_in": "2025-12-15",
  "check_out": "2025-12-22",
  "total_price": "5250.00",
  "user": 12,
  "user_details": {
    "id": 12,
    "name": "John Doe",
    "email": "user@example.com"
  },
  "status": "pending",
  "google_event_id": null,
  "created_at": "2025-11-19T13:00:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "check_out": ["Check-out date must be after check-in date."],
  "check_in": ["Check-in date cannot be in the past."]
}
```

**Error Response (400 Bad Request - Date Conflict):**
```json
{
  "non_field_errors": [
    "The selected dates are not available for this property. Please choose different dates."
  ]
}
```

**Auto-Set Fields:**
- `user`: Set to authenticated user automatically
- `status`: Set to `pending` automatically

**Note:** Booking is created with status `pending`. Admin/Manager must approve it.

---

### 4. Update Booking (Change Status)

**Endpoint:** `PATCH /api/villas/bookings/{booking_id}/`  
**Authentication:** Required (Admin or Manager Only)  
**Description:** Update booking status or details.

**Request Body (Approve Booking):**
```json
{
  "status": "approved"
}
```

**Request Body (Cancel Booking):**
```json
{
  "status": "cancelled"
}
```

**Allowed Status Values:**
- `pending`: Initial status (auto-set on creation)
- `approved`: Booking confirmed (creates Google Calendar event)
- `rejected`: Booking rejected
- `completed`: Booking completed (auto or manual)
- `cancelled`: Booking cancelled (deletes Google Calendar event)

**Success Response (200 OK):**
```json
{
  "id": 125,
  "status": "approved",
  "google_event_id": "abc123xyz",
  "created_at": "2025-11-19T13:00:00Z"
}
```

**Google Calendar Integration:**
- **Status changed to `approved`:** Automatically creates event in property's Google Calendar
- **Status changed to `cancelled` or `rejected`:** Automatically deletes event from Google Calendar

**Error Response (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 5. Delete Booking

**Endpoint:** `DELETE /api/villas/bookings/{booking_id}/`  
**Authentication:** Required (Admin or Manager Only)  
**Description:** Permanently delete a booking.

**Success Response (204 No Content):**
```
(Empty response body)
```

**Note:** If the booking has a Google Calendar event, it will be automatically deleted from the calendar.

---

## 🎬 Media Management

Media files are uploaded as part of property creation or can be managed separately.

### Media Model Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique media ID |
| `media_type` | string | Auto-detected: `image`, `video`, `brochure`, `other` |
| `category` | string | User-defined: `media`, `bedroom`, `bathroom`, `exterior`, `other` |
| `file` | file | Uploaded file |
| `file_url` | string | Full URL to access the file |
| `caption` | string | Optional caption/description |
| `is_primary` | boolean | Mark as primary/cover image |
| `order` | integer | Display order (lower numbers first) |

### Media Type Detection

Files are automatically categorized by extension:
- **Images:** `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- **Videos:** `.mp4`, `.mov`, `.avi`, `.wmv`, `.mkv`
- **Brochures:** `.pdf`, `.doc`, `.docx`
- **Other:** Everything else

---

### 1. Upload Media with Property

**Endpoint:** `POST /api/villas/properties/`  
**Content-Type:** `multipart/form-data`

**Request Body:**
```
title: "Villa Name"
... (other property fields) ...
media_files: [file1.jpg, file2.jpg, video1.mp4]
media_metadata: ['{"category": "media", "caption": "Main View", "is_primary": true, "order": 0}', '{"category": "bedroom", "caption": "Bedroom", "order": 1}', '{"category": "other", "caption": "Property Tour", "order": 2}']
```

**Important Rules:**
1. Number of `media_files` must match number of `media_metadata` entries
2. Each metadata entry is a JSON string
3. Only ONE media can have `is_primary: true` (enforced at model level)
4. Lower `order` values appear first

---

### 2. Media in Property Response

When retrieving a property, media is included:

```json
{
  "id": 1,
  "title": "Property Name",
  "media": [
    {
      "id": 5,
      "media_type": "image",
      "category": "media",
      "file": "/media/property_media/villa-1-main.jpg",
      "file_url": "http://localhost:8888/media/property_media/villa-1-main.jpg",
      "caption": "Main View",
      "is_primary": true,
      "order": 0
    },
    {
      "id": 6,
      "media_type": "video",
      "category": "other",
      "file": "/media/property_media/villa-1-tour.mp4",
      "file_url": "http://localhost:8888/media/property_media/villa-1-tour.mp4",
      "caption": "Property Tour",
      "is_primary": false,
      "order": 2
    }
  ]
}
```

**Media is ordered by:**
1. `order` field (ascending)
2. `id` field (ascending) as fallback

---

## 🗓️ Google Calendar Integration

The system automatically integrates with Google Calendar for booking management.

### How It Works

1. **Property Creation:**
   - When a property is created, a dedicated Google Calendar is automatically created
   - The `google_calendar_id` is saved to the property

2. **Booking Approval:**
   - When booking status changes to `approved`, an event is created in the property's calendar
   - The `google_event_id` is saved to the booking

3. **Booking Cancellation:**
   - When booking status changes to `cancelled` or `rejected`, the event is deleted from the calendar
   - The `google_event_id` is removed from the booking

4. **Availability Check:**
   - The `/availability/` endpoint queries the property's Google Calendar
   - Returns all booked date ranges for a given month

### Availability Validation

When creating a booking, the system:
1. Checks if property has `google_calendar_id`
2. Queries Google Calendar for conflicting events
3. Validates dates are available
4. Returns error if dates conflict with existing bookings

---

## ❌ Error Handling

### HTTP Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Successful deletion |
| 400 | Bad Request | Invalid request data or validation error |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

### Error Response Format

**Validation Errors:**
```json
{
  "field_name": ["Error message for this field."],
  "another_field": ["Another error message."]
}
```

**Non-Field Errors:**
```json
{
  "non_field_errors": ["Error message that applies to the whole request."]
}
```

**Permission Errors:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**Not Found Errors:**
```json
{
  "detail": "Not found."
}
```

---

## 💻 Code Examples

### Python (Requests)

```python
import requests
from datetime import datetime, timedelta

BASE_URL = 'http://localhost:8888/api'

class EastmondVillaAPI:
    def __init__(self):
        self.base_url = BASE_URL
        self.access_token = None
        self.refresh_token = None
    
    def register(self, email, name, password, phone=''):
        """Register a new user"""
        response = requests.post(
            f'{self.base_url}/registration/',
            json={
                'email': email,
                'name': name,
                'phone': phone,
                'password1': password,
                'password2': password
            }
        )
        response.raise_for_status()
        return response.json()
    
    def login(self, email, password):
        """Login and store tokens"""
        response = requests.post(
            f'{self.base_url}/auth/login/',
            json={'email': email, 'password': password}
        )
        response.raise_for_status()
        
        data = response.json()
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        return data
    
    def _get_headers(self):
        """Get authorization headers"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def get_current_user(self):
        """Get authenticated user profile"""
        response = requests.get(
            f'{self.base_url}/auth/user/',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def get_properties(self):
        """Get all properties (public endpoint)"""
        response = requests.get(f'{self.base_url}/villas/properties/')
        response.raise_for_status()
        return response.json()
    
    def get_property(self, property_id):
        """Get property details"""
        response = requests.get(
            f'{self.base_url}/villas/properties/{property_id}/'
        )
        response.raise_for_status()
        return response.json()
    
    def check_availability(self, property_id, month=None, year=None):
        """Check property availability"""
        params = {}
        if month:
            params['month'] = month
        if year:
            params['year'] = year
            
        response = requests.get(
            f'{self.base_url}/villas/properties/{property_id}/availability/',
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def create_booking(self, property_id, email, phone, check_in, check_out, total_price):
        """Create a new booking"""
        response = requests.post(
            f'{self.base_url}/villas/bookings/',
            headers=self._get_headers(),
            json={
                'property': property_id,
                'email': email,
                'phone': phone,
                'check_in': check_in,
                'check_out': check_out,
                'total_price': total_price
            }
        )
        response.raise_for_status()
        return response.json()
    
    def get_my_bookings(self):
        """Get user's bookings"""
        response = requests.get(
            f'{self.base_url}/villas/bookings/',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def create_property(self, property_data, media_files=None):
        """Create property with optional media files"""
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        if media_files:
            # Multipart form data
            files = []
            media_metadata = []
            
            for i, (file_path, metadata) in enumerate(media_files):
                files.append(('media_files', open(file_path, 'rb')))
                import json
                media_metadata.append(json.dumps(metadata))
            
            property_data['media_metadata'] = media_metadata
            
            response = requests.post(
                f'{self.base_url}/villas/properties/',
                headers=headers,
                data=property_data,
                files=files
            )
        else:
            # JSON data only
            headers['Content-Type'] = 'application/json'
            response = requests.post(
                f'{self.base_url}/villas/properties/',
                headers=headers,
                json=property_data
            )
        
        response.raise_for_status()
        return response.json()
    
    # Admin endpoints
    def admin_list_users(self):
        """List all users (admin only)"""
        response = requests.get(
            f'{self.base_url}/admin/users/',
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()
    
    def admin_create_user(self, email, name, password, phone, role, permission):
        """Create user with role (admin only)"""
        response = requests.post(
            f'{self.base_url}/admin/users/',
            headers=self._get_headers(),
            json={
                'email': email,
                'name': name,
                'password': password,
                'phone': phone,
                'role': role,
                'permission': permission
            }
        )
        response.raise_for_status()
        return response.json()
    
    def admin_update_user(self, user_id, **updates):
        """Update user (admin only)"""
        response = requests.patch(
            f'{self.base_url}/admin/users/{user_id}/',
            headers=self._get_headers(),
            json=updates
        )
        response.raise_for_status()
        return response.json()

# Usage Example
if __name__ == '__main__':
    api = EastmondVillaAPI()
    
    # Register new customer
    user = api.register(
        email='customer@example.com',
        name='John Doe',
        password='SecurePass123!',
        phone='+1234567890'
    )
    print(f"Registered user: {user['email']}")
    
    # Login
    api.login('customer@example.com', 'SecurePass123!')
    print('Logged in successfully!')
    
    # Get current user
    current_user = api.get_current_user()
    print(f"Current user: {current_user['name']} ({current_user['role']})")
    
    # Get properties
    properties = api.get_properties()
    print(f"Found {len(properties)} properties")
    
    # Check availability
    if properties:
        property_id = properties[0]['id']
        availability = api.check_availability(property_id, month=12, year=2025)
        print(f"Booked dates: {availability}")
        
        # Create booking
        check_in = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        check_out = (datetime.now() + timedelta(days=37)).strftime('%Y-%m-%d')
        
        booking = api.create_booking(
            property_id=property_id,
            email='customer@example.com',
            phone='+1234567890',
            check_in=check_in,
            check_out=check_out,
            total_price='5250.00'
        )
        print(f"Booking created: ID {booking['id']}, Status: {booking['status']}")
    
    # Get my bookings
    my_bookings = api.get_my_bookings()
    print(f"You have {len(my_bookings)} bookings")
```

---

### JavaScript (Fetch API)

```javascript
const BASE_URL = 'http://localhost:8888/api';

class EastmondVillaAPI {
  constructor() {
    this.baseUrl = BASE_URL;
    this.accessToken = null;
    this.refreshToken = null;
  }

  async register(email, name, password, phone = '') {
    const response = await fetch(`${this.baseUrl}/registration/`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        email,
        name,
        phone,
        password1: password,
        password2: password
      })
    });
    
    if (!response.ok) {
      throw new Error(await response.text());
    }
    
    return await response.json();
  }

  async login(email, password) {
    const response = await fetch(`${this.baseUrl}/auth/login/`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email, password})
    });
    
    if (!response.ok) {
      throw new Error('Login failed');
    }
    
    const data = await response.json();
    this.accessToken = data.access_token;
    this.refreshToken = data.refresh_token;
    
    // Store in localStorage
    localStorage.setItem('accessToken', this.accessToken);
    localStorage.setItem('refreshToken', this.refreshToken);
    
    return data;
  }

  getHeaders() {
    return {
      'Authorization': `Bearer ${this.accessToken}`,
      'Content-Type': 'application/json'
    };
  }

  async getCurrentUser() {
    const response = await fetch(`${this.baseUrl}/auth/user/`, {
      headers: this.getHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Failed to get user');
    }
    
    return await response.json();
  }

  async getProperties() {
    const response = await fetch(`${this.baseUrl}/villas/properties/`);
    
    if (!response.ok) {
      throw new Error('Failed to get properties');
    }
    
    return await response.json();
  }

  async getProperty(propertyId) {
    const response = await fetch(
      `${this.baseUrl}/villas/properties/${propertyId}/`
    );
    
    if (!response.ok) {
      throw new Error('Property not found');
    }
    
    return await response.json();
  }

  async checkAvailability(propertyId, month = null, year = null) {
    let url = `${this.baseUrl}/villas/properties/${propertyId}/availability/`;
    const params = new URLSearchParams();
    
    if (month) params.append('month', month);
    if (year) params.append('year', year);
    
    if (params.toString()) {
      url += `?${params.toString()}`;
    }
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error('Failed to check availability');
    }
    
    return await response.json();
  }

  async createBooking(propertyId, email, phone, checkIn, checkOut, totalPrice) {
    const response = await fetch(`${this.baseUrl}/villas/bookings/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({
        property: propertyId,
        email,
        phone,
        check_in: checkIn,
        check_out: checkOut,
        total_price: totalPrice
      })
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(JSON.stringify(error));
    }
    
    return await response.json();
  }

  async getMyBookings() {
    const response = await fetch(`${this.baseUrl}/villas/bookings/`, {
      headers: this.getHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Failed to get bookings');
    }
    
    return await response.json();
  }

  async createProperty(propertyData, mediaFiles = []) {
    const formData = new FormData();
    
    // Add property fields
    Object.keys(propertyData).forEach(key => {
      if (typeof propertyData[key] === 'object') {
        formData.append(key, JSON.stringify(propertyData[key]));
      } else {
        formData.append(key, propertyData[key]);
      }
    });
    
    // Add media files
    mediaFiles.forEach(({file, metadata}) => {
      formData.append('media_files', file);
      formData.append('media_metadata', JSON.stringify(metadata));
    });
    
    const response = await fetch(`${this.baseUrl}/villas/properties/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.accessToken}`
      },
      body: formData
    });
    
    if (!response.ok) {
      throw new Error('Failed to create property');
    }
    
    return await response.json();
  }
}

// Usage Example
(async () => {
  const api = new EastmondVillaAPI();
  
  try {
    // Register
    await api.register(
      'customer@example.com',
      'John Doe',
      'SecurePass123!',
      '+1234567890'
    );
    console.log('Registered successfully!');
    
    // Login
    await api.login('customer@example.com', 'SecurePass123!');
    console.log('Logged in successfully!');
    
    // Get current user
    const user = await api.getCurrentUser();
    console.log('Current user:', user.name, user.role);
    
    // Get properties
    const properties = await api.getProperties();
    console.log('Found', properties.length, 'properties');
    
    // Check availability
    if (properties.length > 0) {
      const availability = await api.checkAvailability(
        properties[0].id,
        12,
        2025
      );
      console.log('Booked dates:', availability);
      
      // Create booking
      const booking = await api.createBooking(
        properties[0].id,
        'customer@example.com',
        '+1234567890',
        '2025-12-15',
        '2025-12-22',
        '5250.00'
      );
      console.log('Booking created:', booking.id);
    }
    
    // Get bookings
    const bookings = await api.getMyBookings();
    console.log('Your bookings:', bookings.length);
    
  } catch (error) {
    console.error('Error:', error.message);
  }
})();
```

---

### cURL Examples

**Register:**
```bash
curl -X POST http://localhost:8888/api/registration/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "name": "John Doe",
    "phone": "+1234567890",
    "password1": "SecurePass123!",
    "password2": "SecurePass123!"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8888/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "SecurePass123!"
  }'
```

**Get Properties:**
```bash
curl -X GET http://localhost:8888/api/villas/properties/
```

**Check Availability:**
```bash
curl -X GET "http://localhost:8888/api/villas/properties/1/availability/?month=12&year=2025"
```

**Create Booking:**
```bash
curl -X POST http://localhost:8888/api/villas/bookings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "property": 1,
    "email": "customer@example.com",
    "phone": "+1234567890",
    "check_in": "2025-12-15",
    "check_out": "2025-12-22",
    "total_price": "5250.00"
  }'
```

**Create Property with Media:**
```bash
curl -X POST http://localhost:8888/api/villas/properties/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "title=Luxury Villa" \
  -F "description=Beautiful property" \
  -F "price=750.00" \
  -F "listing_type=rent" \
  -F "address=123 Ocean Drive" \
  -F "city=Miami" \
  -F "max_guests=10" \
  -F "bedrooms=5" \
  -F "bathrooms=4" \
  -F "media_files=@/path/to/image1.jpg" \
  -F "media_files=@/path/to/image2.jpg" \
  -F 'media_metadata={"category":"media","caption":"Main View","is_primary":true,"order":0}' \
  -F 'media_metadata={"category":"bedroom","caption":"Bedroom","order":1}'
```

**Admin - List Users:**
```bash
curl -X GET http://localhost:8888/api/admin/users/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

**Admin - Create User:**
```bash
curl -X POST http://localhost:8888/api/admin/users/ \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "manager@eastmondvilla.com",
    "name": "Manager User",
    "password": "SecurePass123!",
    "phone": "+1234567890",
    "role": "manager",
    "permission": "full_access"
  }'
```

---

## 📝 Additional Notes

### Authentication Flow
1. Register user → receives user object
2. Login → receives `access_token` and `refresh_token`
3. Use `access_token` in Authorization header for protected endpoints
4. When `access_token` expires, use `/auth/token/refresh/` with `refresh_token`

### Permission Levels
- **only_view:** Read-only access
- **download:** Read + Download access
- **full_access:** Full CRUD access (create, read, update, delete)

### Role-Based Access
- **customer:** Can view published properties, create bookings
- **agent:** Can manage assigned properties (if full_access permission)
- **manager:** Can manage all properties and bookings
- **admin:** Full system access including user management

### Date Format
All dates use ISO format: `YYYY-MM-DD` (e.g., `2025-12-15`)

### Timestamps
All timestamps are in ISO 8601 format with timezone: `YYYY-MM-DDTHH:MM:SSZ`

### Media Files
- Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
- Videos: `.mp4`, `.mov`, `.avi`, `.wmv`, `.mkv`
- Documents: `.pdf`, `.doc`, `.docx`
- Upload via `multipart/form-data`
- Must include matching `media_metadata` for each file

### Google Calendar
- Automatically created for each property
- Syncs approved bookings
- Availability checked in real-time
- Events automatically deleted when bookings cancelled

---

**Last Updated:** November 19, 2025  
**API Version:** 2.0  
**Framework:** Django REST Framework + dj-rest-auth  
**Contact:** support@eastmondvilla.com
