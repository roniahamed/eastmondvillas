# Accounts — Admin & Auth API Reference

A developer-friendly, code-backed reference for the `accounts` app endpoints that the frontend will call. This document covers admin user management endpoints implemented in the app plus the auth/registration endpoints exposed by `dj-rest-auth` and `dj-rest-auth.registration` at the paths configured in `accounts/urls.py`.

Base path
- The routes below are shown with a base prefix of `/api/` (the project mounts APIs under that prefix in many setups). If your deployment mounts the `accounts.urls` at a different prefix, replace `/api/` with the actual base.
- The `accounts` app registers these subpaths (see `accounts/urls.py`):
  - `auth/` -> `dj_rest_auth.urls`
  - `registration/` -> `dj_rest_auth.registration.urls`
  - `auth/users/<pk>/` -> account delete view
  - `admin/users/` and `admin/users/<pk>/` -> admin user management views

Authentication
- Supported: session cookie or token-based (depends on project config). Frontend commonly uses JWT or Bearer token with header:
  Authorization: Bearer <access_token>

- Common 401 response when credentials are missing or invalid:
  Status: 401 Unauthorized
  Body:
  {
    "detail": "Authentication credentials were not provided."
  }

Error format notes
- Validation errors from DRF serializers are returned with field keys and messages. Example shapes you may see:
  - Field error (single): { "email": ["A user with that email already exists."] }
  - Field error (string): { "email": "A user with that email already exists." }
  - Non-field error: { "non_field_errors": ["Some error"] }
- Permission denied: 403 Forbidden
  { "detail": "You do not have permission to perform this action." }
- Not found: 404 Not Found
  { "detail": "Not found." }

---

## 1) Admin: List users
- Endpoint: GET /api/admin/users/
- Permission: Admin only (permission class: `IsAdmin`) — user must have `role == 'admin'` or `is_staff == True`.
- Query params: pagination or filtering may be provided by project-level DRF settings; this view returns the full queryset ordered by `-date_joined` by default.

Request example
- Headers:
  Authorization: Bearer <ADMIN_TOKEN>

Response (200 OK)
[
  {
    "id": 12,
    "email": "alice@example.com",
    "name": "Alice Smith",
    "role": "manager",
    "permission": "read_write",
    "phone": "+441234567890",
    "address": "123 Example St",
    "is_verified": false,
    "is_active": true,
    "is_staff": false
  },
  { /* more users */ }
]

Errors
- 401 Unauthorized: missing/invalid credentials
- 403 Forbidden: authenticated but not admin/staff

---

## 2) Admin: Create a user
- Endpoint: POST /api/admin/users/
- Permission: Admin only (`IsAdmin`)
- Content-Type: application/json
- Important: For creation the `AdminUserSerializer` enforces these required fields: `email`, `name`, `phone`, `role`, `permission`, `password`.

Request body (JSON) — required fields for create
{
  "email": "new.user@example.com",
  "name": "New User",
  "phone": "+441234567899",
  "role": "agent",
  "permission": "read_write",
  "password": "StrongP@ssw0rd",
  "address": "Optional address",
  "is_active": true,
  "is_staff": false
}

Example curl (using Bearer token)
```bash
curl -X POST "https://your.api.host/api/admin/users/" \
  -H "Authorization: Bearer <ADMIN_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"email":"new.user@example.com","name":"New User","phone":"+441234567899","role":"agent","permission":"read_write","password":"StrongP@ssw0rd"}'
```

Success response (201 Created)
Status: 201
Body:
{
  "id": 42,
  "email": "new.user@example.com",
  "name": "New User",
  "role": "agent",
  "permission": "read_write",
  "phone": "+441234567899",
  "address": "Optional address",
  "is_verified": false,
  "is_active": true,
  "is_staff": false
}

Validation errors (400 Bad Request)
- Missing required fields (example):
Status: 400
Body:
{
  "email": "This field is required.",
  "name": "This field is required.",
  "phone": "This field is required.",
  "role": "This field is required.",
  "permission": "This field is required.",
  "password": "This field is required."
}

- Duplicate email (example):
Status: 400
Body:
{
  "email": ["A user with that email already exists."]
}

Permission errors
- 403 Forbidden if non-admin attempts this request.

Notes
- The serializer uses `create_user` from the model manager so the password is properly hashed. The API will never return the `password` field.

---

## 3) Admin: Retrieve a single user
- Endpoint: GET /api/admin/users/{id}/
- Permission: Admin only (`IsAdmin`)

Request example
- GET /api/admin/users/42/
- Headers: Authorization: Bearer <ADMIN_TOKEN>

Response (200 OK)
{
  "id": 42,
  "email": "new.user@example.com",
  "name": "New User",
  "role": "agent",
  "permission": "read_write",
  "phone": "+441234567899",
  "address": "Optional address",
  "is_verified": false,
  "is_active": true,
  "is_staff": false
}

Errors
- 404 Not Found if id does not exist
- 403 Forbidden if non-admin

---

## 4) Admin: Update a user
- Endpoint (full update): PUT /api/admin/users/{id}/
- Endpoint (partial update): PATCH /api/admin/users/{id}/
- Permission: Admin only (`IsAdmin`)
- Behavior: `password` is optional on update; if provided it will be used to set the new password via `set_password`.

Request (PATCH) example — change name and phone only
PATCH /api/admin/users/42/
{
  "name": "Updated Name",
  "phone": "+441234567900"
}

Success response (200 OK) — updated user object (same fields as above)

Validation error examples (400)
- Duplicate email when changing email to one already used by another user
  {
    "email": ["A user with that email already exists."]
  }

---

## 5) Admin: Delete a user
- Endpoint: DELETE /api/admin/users/{id}/
- Permission: Admin only (`IsAdmin`)
- Response: 204 No Content on success

Notes: This Delete uses DRF's `RetrieveUpdateDestroyAPIView` and will attempt to delete the user object from the DB. If the delete operation raises a DB OperationalError due to related constraints, admin may instead use the special anonymize fallback (see next endpoint) though that fallback is implemented on `DELETE /api/auth/users/{id}/`.

Errors
- 404 Not Found if user doesn't exist
- 403 Forbidden if not admin/staff

---

## 6) Auth-path: Delete user (special-case)
- Endpoint: DELETE /api/auth/users/{id}/
- Permission: Requires authentication. The view logic permits deletion if the requester is:
  - staff (is_staff == True) OR
  - role == 'admin' OR
  - deleting their own account (requester.pk == target.pk)
- Response on success: 204 No Content

Behavior details (implemented in `UserDeleteView`)
- If the authenticated user is permitted, the view attempts to `target.delete()`.
- If the DB raises an OperationalError during delete (e.g., cascade constraints or DB-level locks), the view falls back to anonymize the user:
  - `email` -> `deleted_user_<pk>@example.invalid`
  - `name` -> `[deleted]`
  - `is_active` -> False
  - The view then saves the user and returns 204.

Example success responses
- Deletion: Status 204 No Content (empty body)

Permission error (403)
Status: 403 Forbidden
Body:
{
  "detail": "You do not have permission to perform this action."
}

---

## 7) Registration & Auth endpoints (provided by dj-rest-auth)
The `accounts` app includes the `dj_rest_auth` and `dj_rest_auth.registration` URL sets at the paths `auth/` and `registration/` respectively. Common endpoints available (subject to project configuration) include:

Auth (under `/api/auth/`):
- POST /api/auth/login/ — login with credentials (returns user/session/token depending on config)
  Request: { "email": "...", "password": "..." }
  Success: 200 OK (body depends on dj-rest-auth settings; typically returns user details and possibly token)
- POST /api/auth/logout/ — logout (server-side session/token invalidation)
- GET /api/auth/user/ — get currently authenticated user (uses `CustomUserDetailsSerializer` in this project)
  Response sample:
  {
    "pk": 12,
    "id": 12,
    "email": "alice@example.com",
    "name": "Alice Smith",
    "role": "manager",
    "permission": "read_write",
    "is_verified": false,
    "phone": "+441234567890",
    "address": "123 Example St",
    "date_joined": "2025-01-01T12:00:00Z",
    "is_active": true,
    "is_staff": false
  }
- Password change/reset endpoints (typical paths):
  - POST /api/auth/password/change/
  - POST /api/auth/password/reset/
  - POST /api/auth/password/reset/confirm/

Registration (under `/api/registration/`):
- POST /api/registration/ — register a new user
  The project provides `CustomRegisterSerializer` which requires `email` and `name`, and optionally `phone`.

Registration request example
POST /api/registration/
{
  "email": "new.user@example.com",
  "name": "New User",
  "phone": "+441234567899",
  "password1": "StrongP@ssw0rd",
  "password2": "StrongP@ssw0rd"
}

Notes about registration
- `CustomRegisterSerializer` removes `username` and intentionally prevents clients from assigning `role` or `permission` during registration. Roles/permissions must be assigned by an admin via the admin endpoints.
- The serializer also validates that an email already verified via `allauth` will be rejected.
- Response shape after successful registration depends on `dj-rest-auth` settings (it may return the user object, user + token, or trigger an email verification flow).

Common registration errors (400)
- Password mismatch
  { "password2": ["The two password fields didn't match."] }
- Email already exists
  { "email": ["This email is already in use."] }

---

## Frontend integration checklist (quick)
- Always send authentication credentials (Authorization header or cookies) with admin requests.
- For create user: include required fields in the body: `email`, `name`, `phone`, `role`, `permission`, `password`.
- For update: `password` is optional. Only include it when changing a password.
- For delete via `/api/auth/users/{id}/`: expect 204 on success; if you see the user still in lists, the backend may have anonymized instead of deleting due to DB constraints.
- Handle error responses:
  - 400: show field-specific validation errors
  - 401: redirect to login
  - 403: show 'insufficient permissions' UI
  - 404: show 'not found'

---

## Examples (fetch) — create user (admin)
Example using fetch with Bearer token (replace host and token):
```js
fetch('https://your.api.host/api/admin/users/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer <ADMIN_TOKEN>'
  },
  body: JSON.stringify({
    email: 'new.user@example.com',
    name: 'New User',
    phone: '+441234567899',
    role: 'agent',
    permission: 'read_write',
    password: 'StrongP@ssw0rd'
  })
})
.then(res => {
  if (!res.ok) return res.json().then(err => Promise.reject(err));
  return res.json();
})
.then(data => console.log('created', data))
.catch(err => console.error('error', err));
```

---

## Backend notes / assumptions (for maintainers)
- The `AdminUserSerializer` enforces required fields on create: `email`, `name`, `phone`, `role`, `permission`, `password`.
- The delete fallback (anonymization) is implemented only on `DELETE /api/auth/users/{id}/`. The admin `DELETE /api/admin/users/{id}/` uses the default DRF destroy from `RetrieveUpdateDestroyAPIView` and may surface DB errors instead of anonymizing.

If you want, I can:
- Add concrete curl examples for every endpoint in this doc.
- Generate Postman / OpenAPI snippets for automatic import in the frontend team.
- Add integration test examples (pytest/django) for the admin endpoints.

-- end
