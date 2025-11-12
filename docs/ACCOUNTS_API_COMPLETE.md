# Accounts API Specification v1.0

**Base URL**: `http://localhost:8000/api/`  
**Version**: 1.0  
**Last Updated**: November 12, 2025

---

## Table of Contents

1. [Authentication](#authentication)
2. [Registration & Login](#2-registration--login)
3. [User Management (Public)](#3-user-management-public)
4. [Admin User Management](#4-admin-user-management)
5. [Account Management](#5-account-management)
6. [Data Types](#6-data-types)
7. [Error Codes](#7-error-codes)

---

## Authentication

### Overview
The API uses JWT (JSON Web Token) authentication provided by `djangorestframework-simplejwt` and `dj-rest-auth`.

### Authentication Header
```
Authorization: Bearer <access_token>
```

### Token Lifetime
- **Access Token**: 60 minutes
- **Refresh Token**: 7 days

### Roles
- `customer` - Customer (default role for new registrations)
- `agent` - Agent (can be assigned by admin)
- `manager` - Manager (can be assigned by admin)
- `admin` - Administrator (full access)

### Permissions
- `only_view` - Read-only access (default)
- `download` - Can download resources
- `full_access` - Full system access

---

## 2. Registration & Login

### POST `/api/registration/`

Register a new user account.

**Authentication**: None required

#### Request

**Headers**:
```http
Content-Type: application/json
```

**Body**:
```json
{
  "email": "string (valid email, required)",
  "name": "string (max 255 chars, required)",
  "phone": "string (max 15 chars, optional)",
  "password1": "string (required)",
  "password2": "string (must match password1, required)"
}
```

#### Field Constraints

| Field | Type | Constraints | Required |
|-------|------|-------------|----------|
| email | string | Valid email, unique | Yes |
| name | string | Max 255 characters | Yes |
| phone | string | Max 15 characters | No |
| password1 | string | Min 8 chars, not too common | Yes |
| password2 | string | Must match password1 | Yes |

#### Response

**Success (201 Created)**:
```json
{
  "pk": 1,
  "email": "newuser@example.com",
  "name": "New User",
  "phone": "+15557778888",
  "is_active": true
}
```

**Error (400 Bad Request)**:
```json
{
  "email": ["This email address is already verified."],
  "password1": ["This password is too common."],
  "password2": ["The two password fields didn't match."]
}
```

#### Side Effects
1. Creates new User with role `customer` and permission `only_view`
2. Sets `is_active=True`
3. Does NOT set `is_verified=True` (requires email verification)
4. Does NOT set `is_staff=True` (only admins can assign)

#### Example

**Request**:
```bash
curl -X POST http://localhost:8000/api/registration/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "name": "John Doe",
    "phone": "+15551234567",
    "password1": "SecurePass123!",
    "password2": "SecurePass123!"
  }'
```

**Response**:
```json
{
  "pk": 5,
  "email": "john@example.com",
  "name": "John Doe",
  "phone": "+15551234567",
  "is_active": true
}
```

---

### POST `/api/auth/login/`

Authenticate and receive JWT tokens.

**Authentication**: None required

#### Request

**Headers**:
```http
Content-Type: application/json
```

**Body**:
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

#### Response

**Success (200 OK)**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "pk": 1,
    "id": 1,
    "email": "john@example.com",
    "name": "John Doe",
    "role": "customer",
    "permission": "only_view",
    "is_verified": false,
    "phone": "+15551234567",
    "address": null,
    "date_joined": "2025-11-12T10:30:00Z",
    "is_active": true,
    "is_staff": false
  }
}
```

**Error (400 Bad Request)**:
```json
{
  "non_field_errors": ["Unable to log in with provided credentials."]
}
```

**Error (401 Unauthorized)** - Inactive Account:
```json
{
  "detail": "This account is inactive. Please Contact with support!"
}
```

#### Example

**Request**:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

**Response**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "pk": 5,
    "id": 5,
    "email": "john@example.com",
    "name": "John Doe",
    "role": "customer",
    "permission": "only_view",
    "is_verified": false,
    "phone": "+15551234567",
    "address": null,
    "date_joined": "2025-11-12T10:30:00Z",
    "is_active": true,
    "is_staff": false
  }
}
```

---

### POST `/api/auth/logout/`

Logout and blacklist refresh token.

**Authentication**: Required

#### Request

**Headers**:
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body** (optional):
```json
{
  "refresh": "string (refresh token to blacklist)"
}
```

#### Response

**Success (200 OK)**:
```json
{
  "detail": "Successfully logged out."
}
```

#### Example

**Request**:
```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json"
```

---

## 3. User Management (Public)

### GET `/api/auth/user/`

Get current authenticated user details.

**Authentication**: Required

#### Request

**Headers**:
```http
Authorization: Bearer <access_token>
```

#### Response

**Success (200 OK)**:
```json
{
  "pk": 1,
  "id": 1,
  "email": "john@example.com",
  "name": "John Doe",
  "role": "customer",
  "permission": "only_view",
  "is_verified": false,
  "phone": "+15551234567",
  "address": "123 Main St, City",
  "date_joined": "2025-11-12T10:30:00Z",
  "is_active": true,
  "is_staff": false
}
```

**Error (401 Unauthorized)**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### Example

**Request**:
```bash
curl -X GET http://localhost:8000/api/auth/user/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

### POST `/api/auth/password/change/`

Change password for authenticated user.

**Authentication**: Required

#### Request

**Headers**:
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body**:
```json
{
  "old_password": "string (required)",
  "new_password1": "string (required)",
  "new_password2": "string (must match new_password1, required)"
}
```

#### Response

**Success (200 OK)**:
```json
{
  "detail": "New password has been saved."
}
```

**Error (400 Bad Request)**:
```json
{
  "old_password": ["Wrong password."],
  "new_password2": ["The two password fields didn't match."]
}
```

#### Example

**Request**:
```bash
curl -X POST http://localhost:8000/api/auth/password/change/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "SecurePass123!",
    "new_password1": "NewSecurePass456!",
    "new_password2": "NewSecurePass456!"
  }'
```

---

### POST `/api/auth/password/reset/`

Request password reset email.

**Authentication**: None required

#### Request

**Headers**:
```http
Content-Type: application/json
```

**Body**:
```json
{
  "email": "string (required)"
}
```

#### Response

**Success (200 OK)**:
```json
{
  "detail": "Password reset e-mail has been sent."
}
```

**Note**: Returns 200 even if email doesn't exist (security best practice).

#### Example

**Request**:
```bash
curl -X POST http://localhost:8000/api/auth/password/reset/ \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}'
```

---

### POST `/api/auth/password/reset/confirm/`

Confirm password reset with token from email.

**Authentication**: None required

#### Request

**Headers**:
```http
Content-Type: application/json
```

**Body**:
```json
{
  "uid": "string (from email, required)",
  "token": "string (from email, required)",
  "new_password1": "string (required)",
  "new_password2": "string (must match new_password1, required)"
}
```

#### Response

**Success (200 OK)**:
```json
{
  "detail": "Password has been reset with the new password."
}
```

**Error (400 Bad Request)**:
```json
{
  "token": ["Invalid value"],
  "uid": ["Invalid value"]
}
```

---

### POST `/api/registration/verify-email/`

Verify email address with confirmation key.

**Authentication**: None required (if email verification is enabled)

#### Request

**Headers**:
```http
Content-Type: application/json
```

**Body**:
```json
{
  "key": "string (email confirmation key, required)"
}
```

#### Response

**Success (200 OK)**:
```json
{
  "detail": "ok"
}
```

**Error (404 Not Found)**:
```json
{
  "detail": "Not found."
}
```

---

## 4. Admin User Management

All endpoints in this section require **admin role** or **staff status**.

### GET `/api/admin/users/`

List all users (admin only).

**Authentication**: Required (Admin or Staff)

#### Request

**Headers**:
```http
Authorization: Bearer <access_token>
```

#### Response

**Success (200 OK)**:
```json
[
  {
    "id": 1,
    "email": "admin@example.com",
    "name": "Admin User",
    "role": "admin",
    "permission": "full_access",
    "phone": "+15550000000",
    "address": "HQ Office",
    "is_verified": true,
    "is_active": true,
    "is_staff": true
  },
  {
    "id": 2,
    "email": "agent@example.com",
    "name": "Agent User",
    "role": "agent",
    "permission": "download",
    "phone": "+15550001111",
    "address": null,
    "is_verified": false,
    "is_active": true,
    "is_staff": false
  }
]
```

**Error (403 Forbidden)**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### Example

**Request**:
```bash
curl -X GET http://localhost:8000/api/admin/users/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

### POST `/api/admin/users/`

Create a new user (admin only).

**Authentication**: Required (Admin or Staff)

#### Request

**Headers**:
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body**:
```json
{
  "email": "string (valid email, unique, required)",
  "name": "string (max 255 chars, required)",
  "phone": "string (max 15 chars, required)",
  "role": "string (customer|agent|manager|admin, required)",
  "permission": "string (only_view|download|full_access, required)",
  "password": "string (required)",
  "address": "string (optional)",
  "is_active": "boolean (optional, default true)",
  "is_staff": "boolean (optional, default false)"
}
```

#### Field Constraints

| Field | Type | Constraints | Required |
|-------|------|-------------|----------|
| email | string | Valid email, unique | Yes |
| name | string | Max 255 characters | Yes |
| phone | string | Max 15 characters | Yes |
| role | string | customer, agent, manager, admin | Yes |
| permission | string | only_view, download, full_access | Yes |
| password | string | Min 8 chars | Yes |
| address | string | Text field | No |
| is_active | boolean | Default: true | No |
| is_staff | boolean | Default: false | No |

#### Response

**Success (201 Created)**:
```json
{
  "id": 10,
  "email": "newagent@example.com",
  "name": "New Agent",
  "role": "agent",
  "permission": "download",
  "phone": "+15559990000",
  "address": "Regional Office",
  "is_verified": false,
  "is_active": true,
  "is_staff": false
}
```

**Error (400 Bad Request)**:
```json
{
  "email": ["A user with that email already exists."],
  "phone": ["This field is required."],
  "role": ["This field is required."]
}
```

**Error (403 Forbidden)**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### Example

**Request**:
```bash
curl -X POST http://localhost:8000/api/admin/users/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "email": "manager@example.com",
    "name": "Manager User",
    "phone": "+15558887777",
    "role": "manager",
    "permission": "full_access",
    "password": "ManagerPass123!",
    "address": "Main Office",
    "is_active": true,
    "is_staff": false
  }'
```

**Response**:
```json
{
  "id": 12,
  "email": "manager@example.com",
  "name": "Manager User",
  "role": "manager",
  "permission": "full_access",
  "phone": "+15558887777",
  "address": "Main Office",
  "is_verified": false,
  "is_active": true,
  "is_staff": false
}
```

---

### GET `/api/admin/users/<id>/`

Get details of a specific user (admin only).

**Authentication**: Required (Admin or Staff)

#### Request

**Headers**:
```http
Authorization: Bearer <access_token>
```

#### Response

**Success (200 OK)**:
```json
{
  "id": 5,
  "email": "user@example.com",
  "name": "User Name",
  "role": "customer",
  "permission": "only_view",
  "phone": "+15551234567",
  "address": "123 Street",
  "is_verified": false,
  "is_active": true,
  "is_staff": false
}
```

**Error (404 Not Found)**:
```json
{
  "detail": "Not found."
}
```

**Error (403 Forbidden)**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### Example

**Request**:
```bash
curl -X GET http://localhost:8000/api/admin/users/5/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

### PUT `/api/admin/users/<id>/`

Update a user (admin only).

**Authentication**: Required (Admin or Staff)

#### Request

**Headers**:
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body** (all fields optional for update):
```json
{
  "email": "string (valid email, unique)",
  "name": "string (max 255 chars)",
  "phone": "string (max 15 chars)",
  "role": "string (customer|agent|manager|admin)",
  "permission": "string (only_view|download|full_access)",
  "password": "string (optional, will be hashed)",
  "address": "string",
  "is_active": "boolean",
  "is_staff": "boolean"
}
```

#### Response

**Success (200 OK)**:
```json
{
  "id": 5,
  "email": "updated@example.com",
  "name": "Updated Name",
  "role": "manager",
  "permission": "download",
  "phone": "+15559990000",
  "address": "New Address",
  "is_verified": false,
  "is_active": true,
  "is_staff": true
}
```

**Error (400 Bad Request)**:
```json
{
  "email": ["A user with that email already exists."]
}
```

**Error (403 Forbidden)**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### Example

**Request**:
```bash
curl -X PUT http://localhost:8000/api/admin/users/5/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "role": "manager",
    "permission": "full_access",
    "is_staff": true
  }'
```

---

### DELETE `/api/admin/users/<id>/`

Delete a user (admin only).

**Authentication**: Required (Admin or Staff)

#### Request

**Headers**:
```http
Authorization: Bearer <access_token>
```

#### Response

**Success (204 No Content)**: Empty body

**Error (403 Forbidden)**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**Error (404 Not Found)**:
```json
{
  "detail": "Not found."
}
```

#### Side Effects
1. Attempts to delete user from database
2. If deletion fails due to DB constraints:
   - Email changed to `deleted_user_<id>@example.invalid`
   - Name set to `[deleted]`
   - `is_active` set to `False`
3. Still returns `204 No Content`

#### Example

**Request**:
```bash
curl -X DELETE http://localhost:8000/api/admin/users/5/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## 5. Account Management

### DELETE `/api/auth/users/<id>/`

Delete own account or any account (staff/admin can delete any).

**Authentication**: Required

#### Permissions
- Users can delete their **own** account
- Staff or admin role can delete **any** account

#### Request

**Headers**:
```http
Authorization: Bearer <access_token>
```

#### Response

**Success (204 No Content)**: Empty body

**Error (403 Forbidden)** - Attempting to delete another user's account:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**Error (404 Not Found)**:
```json
{
  "detail": "Not found."
}
```

#### Side Effects
Same as admin delete endpoint:
1. Attempts database deletion
2. Falls back to anonymization if constraints prevent deletion

#### Example

**Request** (user deleting own account):
```bash
curl -X DELETE http://localhost:8000/api/auth/users/5/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

**Request** (admin deleting any account):
```bash
curl -X DELETE http://localhost:8000/api/auth/users/10/ \
  -H "Authorization: Bearer <admin_access_token>"
```

---

## 6. Data Types

### Date Format
ISO 8601: `YYYY-MM-DD`

Example: `2025-11-12`

### DateTime Format
ISO 8601 with timezone: `YYYY-MM-DDTHH:MM:SSZ`

Example: `2025-11-12T10:30:00Z`

### Role Choices
- `customer` - Customer
- `agent` - Agent
- `manager` - Manager
- `admin` - Admin

### Permission Choices
- `only_view` - Only View (read-only)
- `download` - Download (can download resources)
- `full_access` - Full Access (complete system access)

### User Object Structure

```json
{
  "id": "integer (primary key)",
  "pk": "integer (alias to id)",
  "email": "string (unique email address)",
  "name": "string (user's full name)",
  "role": "string (customer|agent|manager|admin)",
  "permission": "string (only_view|download|full_access)",
  "is_verified": "boolean (email verified via allauth)",
  "phone": "string | null (phone number)",
  "address": "string | null (physical address)",
  "date_joined": "datetime (ISO 8601)",
  "is_active": "boolean (account active status)",
  "is_staff": "boolean (Django admin access)"
}
```

---

## 7. Error Codes

### HTTP Status Codes

| Code | Name | Description |
|------|------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 204 | No Content | Successful deletion |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing/invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

### Authentication Errors

**401 - Missing Credentials**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**401 - Invalid Token**:
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

**401 - Inactive Account**:
```json
{
  "detail": "This account is inactive. Please Contact with support!"
}
```

**401 - Invalid Login**:
```json
{
  "non_field_errors": ["Unable to log in with provided credentials."]
}
```

### Permission Errors

**403 - Insufficient Permissions**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**403 - Admin Required** (custom IsAdmin permission):
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Validation Errors

**400 - Field Validation**:
```json
{
  "field_name": [
    "Error message describing the validation failure"
  ],
  "another_field": [
    "Another error message"
  ]
}
```

Common validation messages:
- `"This field is required."`
- `"This field may not be blank."`
- `"A user with that email already exists."`
- `"This email address is already verified."`
- `"This password is too common."`
- `"This password is too short. It must contain at least 8 characters."`
- `"The two password fields didn't match."`
- `"Wrong password."`
- `"Enter a valid email address."`

### Resource Not Found

**404 - Not Found**:
```json
{
  "detail": "Not found."
}
```

---

## Testing

### Health Check

Test if the API is running:

```bash
curl http://localhost:8000/admin/
# Should return HTML (Django admin page)
```

### Complete Authentication Flow

```bash
# 1. Register new user
curl -X POST http://localhost:8000/api/registration/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "phone": "+15551234567",
    "password1": "TestPass123!",
    "password2": "TestPass123!"
  }'

# 2. Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'

# 3. Get user details (use access token from login response)
curl -X GET http://localhost:8000/api/auth/user/ \
  -H "Authorization: Bearer <access_token>"

# 4. Change password
curl -X POST http://localhost:8000/api/auth/password/change/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "TestPass123!",
    "new_password1": "NewTestPass456!",
    "new_password2": "NewTestPass456!"
  }'

# 5. Logout
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer <access_token>"
```

### Admin Operations (requires admin token)

```bash
# 1. Login as admin
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "AdminPass123!"
  }'

# 2. List all users
curl -X GET http://localhost:8000/api/admin/users/ \
  -H "Authorization: Bearer <admin_access_token>"

# 3. Create new user
curl -X POST http://localhost:8000/api/admin/users/ \
  -H "Authorization: Bearer <admin_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "agent@example.com",
    "name": "Agent User",
    "phone": "+15559998888",
    "role": "agent",
    "permission": "download",
    "password": "AgentPass123!",
    "is_active": true,
    "is_staff": false
  }'

# 4. Update user
curl -X PUT http://localhost:8000/api/admin/users/5/ \
  -H "Authorization: Bearer <admin_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "manager",
    "permission": "full_access"
  }'

# 5. Delete user
curl -X DELETE http://localhost:8000/api/admin/users/5/ \
  -H "Authorization: Bearer <admin_access_token>"
```

---

## Integration Notes

### Frontend Integration

1. **Store Tokens Securely**: Store access and refresh tokens in memory or secure storage (not localStorage for sensitive apps)

2. **Token Refresh**: Implement automatic token refresh before expiry:
   ```javascript
   // Token expires in 60 minutes, refresh at 55 minutes
   ```

3. **Handle 401 Errors**: Redirect to login when receiving 401 responses

4. **Role-Based UI**: Show/hide features based on user role and permission:
   ```javascript
   if (user.role === 'admin' || user.is_staff) {
     // Show admin panel
   }
   ```

### Mobile App Integration

1. Use secure storage for tokens (Keychain on iOS, Keystore on Android)
2. Implement biometric authentication for token access
3. Handle token expiry with background refresh

### Webhook/Background Integration

For server-to-server communication:
1. Create a service account with appropriate role
2. Store credentials securely in environment variables
3. Implement token refresh logic
4. Use appropriate timeouts and retry logic

---

## Rate Limiting

Currently not implemented. Consider implementing for production using:
- Django REST Framework throttling
- Nginx rate limiting
- API Gateway rate limits

---

## Versioning

Current version: **1.0**

API versioning is not currently implemented. Future versions may use:
- URL versioning (e.g., `/api/v2/`)
- Header versioning (e.g., `Accept: application/vnd.api.v2+json`)

---

## Support & Contact

For API support:
- Check the code: `/accounts/` directory
- Review tests: `/accounts/tests.py`
- Django admin: `http://localhost:8000/admin/`

---

*Accounts API Specification v1.0 - Last Updated: November 12, 2025*
