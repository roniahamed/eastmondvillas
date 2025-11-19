# Accounts - Admin API

This document describes the Admin-managed user endpoints and the user-delete endpoint for the Accounts app. It documents the request/response payloads, field definitions, validation rules, permissions, and example status codes.

Base URL
--

The collection uses the environment variable `{{base_url}}` — e.g. `http://localhost:8000/api`.

Authentication & Authorization
--

- Authentication: endpoints require authentication. The collection assumes Bearer JWT tokens in an `Authorization: Bearer {{access_token}}` header.
- Admin/Staff endpoints require the custom `IsAdmin` permission (admin role or staff). Ordinary authenticated users can only delete their own account via the `auth/users/<id>/` endpoint.

Endpoints overview
--

- GET /admin/users/ — List users (admin/staff only)
- POST /admin/users/ — Create user (admin/staff only)
- GET /admin/users/<id>/ — Retrieve single user (admin/staff only)
- PUT /admin/users/<id>/ — Update user (admin/staff only)
- DELETE /admin/users/<id>/ — Delete user (admin/staff only)
- DELETE /auth/users/<id>/ — Delete account (authenticated users may delete their own account; staff/admin may delete any account)

Field definitions (AdminUserSerializer)
--

Error format notes
--

- Validation errors from DRF serializers are returned with field keys and messages. Example shapes you may see:
  - Field error (single): { "email": ["A user with that email already exists."] }
  - Non-field error: { "non_field_errors": ["Some error"] }

Auth & Registration endpoints (dj-rest-auth)
--

The `accounts` app includes `dj_rest_auth` under the `auth/` prefix and `dj_rest_auth.registration` under `registration/`. Below are the common routes exposed by those packages (as mounted in `accounts/urls.py`) with example payloads and responses. Exact available routes depend on which dj-rest-auth features are enabled in project settings (simplejwt, email verification, etc.).

1) Login (obtain JWT or tokens)

- Path: POST /auth/login/
- Purpose: Authenticate and obtain access/refresh tokens. When the project uses `djangorestframework-simplejwt` with dj-rest-auth this returns `access` and `refresh` tokens.
- Request body (example):

  {
    "email": "admin@example.com",
    "password": "AdminPassword123"
  }

- Responses:
  - 200 OK (JWT):

    {
      "access": "<jwt_access_token>",
      "refresh": "<jwt_refresh_token>"
    }

  - 400 Bad Request (invalid credentials):

    {
      "detail": "Unable to log in with provided credentials."
    }

2) Logout

- Path: POST /auth/logout/
- Purpose: Logout the user. Behavior depends on token backend (may blacklist refresh token).
- Request: Authorization header required
- Response: 200 OK

  {
    "detail": "Successfully logged out."
  }

3) Current user (user details)

- Path: GET /auth/user/
- Purpose: Return the current authenticated user's details using `CustomUserDetailsSerializer`.
- Request: Authorization header required
- Response (200 OK example):

  {
    "pk": 1,
    "id": 1,
    "email": "admin@example.com",
    "name": "Admin",
    "role": "admin",
    "permission": "full_access",
    "is_verified": true,
    "phone": "+15550000000",
    "address": "HQ",
    "date_joined": "2025-01-01T00:00:00Z",
    "is_active": true,
    "is_staff": true
  }

4) Password change

- Path: POST /auth/password/change/
- Purpose: Change the logged-in user's password.
- Request body example:

  {
    "old_password": "OldPass123",
    "new_password1": "NewStrongPass123",
    "new_password2": "NewStrongPass123"
  }

- Response: 200 OK

  {
    "detail": "New password has been saved."
  }

5) Password reset (request)

- Path: POST /auth/password/reset/
- Purpose: Request a password reset email be sent to the given address.
- Request body example:

  {
    "email": "user@example.com"
  }

- Response: 200 OK

  {
    "detail": "Password reset e-mail has been sent."
  }

6) Password reset confirm (tokenized)

- Path: POST /auth/password/reset/confirm/
- Purpose: Confirm a password reset using uid/token (depends on frontend and email flow). Payload depends on the configured backend.
- Response: 200 OK on success.

7) Registration (sign up)

- Path: POST /registration/
- Purpose: Register a new user using `CustomRegisterSerializer` which allows `email`, `name`, `phone`, `password1`, `password2`. Roles and permissions are NOT accepted via regular registration and must be assigned by admins.
- Request body example:

  {
    "email": "signup@example.com",
    "name": "Signup User",
    "phone": "+15557778888",
    "password1": "SignupPass123",
    "password2": "SignupPass123"
  }

- Response (201 Created example):

  {
    "pk": 11,
    "email": "signup@example.com",
    "name": "Signup User",
    "phone": "+15557778888",
    "is_active": true
  }

8) Verify email (if enabled)

- Path: POST /registration/verify-email/
- Purpose: Verify email address using the key sent by email (if allauth/dj-rest-auth verification is enabled).
- Request body example:

  {
    "key": "<email-confirm-key>"
  }

- Response: 200 OK (body may vary depending on configuration).

Notes & assumptions
--

- The exact dj-rest-auth endpoints available and their shapes depend on how dj-rest-auth and allauth are configured in the project (simplejwt vs token auth, email verification enabled, custom serializers). The examples above match the typical simplejwt + dj-rest-auth + dj-rest-auth.registration setup and the custom serializers present in this repository.
- If you want, I can automatically add these auth/register requests to the Postman collection with Postman test scripts that store the returned `access` token into the `{{access_token}}` environment variable.

Full endpoint reference (detailed)
--

Below is a full, explicit reference for each path that `accounts/urls.py` registers. Each entry includes: path, allowed methods, required permissions, request payload (when applicable), sample responses, and notes.

1) auth/ (dj-rest-auth)
  - Registered path: `path('auth/', include('dj_rest_auth.urls'))`
  - Notes: dj-rest-auth exposes several endpoints. Which ones are active depends on settings. Typical endpoints include:

  a) POST /auth/login/
    - Purpose: Authenticate and obtain tokens (session or JWT depending on config).
    - Request body example: { "email": "user@example.com", "password": "Password123" }
    - Success: 200 OK with token payload (e.g., { "access": "...", "refresh": "..." }) or session info.
    - Errors: 400 Bad Request for invalid credentials.

  b) POST /auth/logout/
    - Purpose: Logout the current user. May accept the refresh token to blacklist it when using JWT.
    - Required: Authorization header
    - Success: 200 OK { "detail": "Successfully logged out." }

  c) GET /auth/user/
    - Purpose: Return the current authenticated user's details using `CustomUserDetailsSerializer`.
    - Required: Authorization header
    - Success: 200 OK (user object)

  d) POST /auth/password/change/
    - Purpose: Change the authenticated user's password.
    - Request: { "old_password": "...", "new_password1": "...", "new_password2": "..." }
    - Success: 200 OK { "detail": "New password has been saved." }

  e) POST /auth/password/reset/
    - Purpose: Request a password reset email be sent. Request: { "email": "user@example.com" }
    - Success: 200 OK { "detail": "Password reset e-mail has been sent." }

  f) POST /auth/password/reset/confirm/
    - Purpose: Confirm a password reset using uid/token or other scheme. Payload depends on configuration.
    - Success: 200 OK on success.

2) registration/ (dj-rest-auth.registration)
  - Registered path: `path('registration/', include('dj_rest_auth.registration.urls'))`
  - Notes: Exposes registration endpoints from dj-rest-auth/Allauth.

  a) POST /registration/
    - Purpose: Register a new user. The project uses `CustomRegisterSerializer` so accepted fields are `email`, `name`, `phone`, `password1`, `password2`.
    - Example request:

     {
      "email": "signup@example.com",
      "name": "Signup User",
      "phone": "+15557778888",
      "password1": "SignupPass123",
      "password2": "SignupPass123"
     }

    - Success: 201 Created with basic user info (pk, email, name, phone, is_active)

  b) POST /registration/verify-email/
    - Purpose: Confirm email address using a key sent in the verification email (if email verification is enabled).
    - Request: { "key": "<email-confirm-key>" }
    - Success: 200 OK (body may vary)

3) auth/users/<pk>/ (User deletion view)
  - Registered path: `path('auth/users/<int:pk>/', UserDeleteView.as_view(), name='user-delete')`
  - Methods: DELETE
  - Permissions: `IsAuthenticated` — delete is allowed if the requesting user is staff/is admin role OR if the requester is deleting their own account.
  - Success: 204 No Content
  - Failure: 403 Forbidden when attempting to delete another user's account without staff/admin permissions. Body: { "detail": "You do not have permission to perform this action." }
  - Notes: If DB constraints prevent deletion (OperationalError), the view anonymizes the target user (email changed to `deleted_user_<pk>@example.invalid`, name set to `[deleted]`, `is_active=False`) and still returns 204.

4) admin/users/ (Admin-managed users list/create)
  - Registered path: `path('admin/users/', AdminUserListCreateView.as_view(), name='admin-user-list-create')`
  - Methods: GET, POST
  - Permissions: `IsAdmin` custom permission — only staff or admin-role users should be able to access.

  a) GET /admin/users/
    - Purpose: Return a list of users, ordered by `-date_joined`.
    - Request headers: Authorization required
    - Success: 200 OK — list of user objects (AdminUserSerializer fields)

  b) POST /admin/users/
    - Purpose: Create a new user with admin-controlled fields (role, permission, is_staff, is_active)
    - Required fields (on create): `email`, `name`, `phone`, `role`, `permission`, `password`
    - Example request body:

     {
      "email": "newuser@example.com",
      "name": "New User",
      "phone": "+15550001111",
      "role": "agent",
      "permission": "only_view",
      "password": "SecretPassword123",
      "address": "Unit 5, 100 Example Street",
      "is_active": true,
      "is_staff": false
     }

    - Success: 201 Created with created user object (id, email, name, role, permission, phone, address, is_verified, is_active, is_staff)
    - Errors: 400 Bad Request for missing required fields or email uniqueness violation

5) admin/users/<pk>/ (Admin-managed user detail/update/delete)
  - Registered path: `path('admin/users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail')`
  - Methods: GET, PUT, DELETE (Retrieve, update, destroy)
  - Permissions: `IsAdmin`

  a) GET /admin/users/<pk>/
    - Purpose: Retrieve a single user's admin-serializable representation.
    - Success: 200 OK

  b) PUT /admin/users/<pk>/
    - Purpose: Update fields on the user. `password` optional; when supplied it's hashed via `set_password()`.
    - Example request body (partial/full replacement accepted by DRF generic view):

     {
      "email": "updated@example.com",
      "name": "Updated Name",
      "phone": "+15559990000",
      "role": "manager",
      "permission": "download",
      "is_staff": true
     }

    - Success: 200 OK with updated user object
    - Errors: 400 Bad Request on validation problems

  c) DELETE /admin/users/<pk>/
    - Purpose: Permanently delete a user or anonymize when DB constraints prevent deletion.
    - Success: 204 No Content
    - Errors: 403 Forbidden if caller lacks admin permission

Example status codes summary
--

- 200 OK — Successful GET / PUT / POST (when returning resource)
- 201 Created — Successful resource creation (POST /admin/users/, POST /registration/)
- 204 No Content — Successful deletion (DELETE endpoints)
- 400 Bad Request — Validation errors or bad credentials for login
- 401 Unauthorized — Missing/invalid authentication credentials
- 403 Forbidden — Permission denied (IsAdmin guard or unauthorized deletion)

Next steps I can take for you
--

- Add Postman tests that capture tokens from `/auth/login/` and store in `{{access_token}}`.
- Generate a minimal `docs/ACCOUNTS_API_QUICKSTART.md` with import steps and example flows (register -> verify -> login -> create user).
- Add request/response schema examples in JSON Schema or OpenAPI components if you'd like an OpenAPI document generated from these descriptions.

If you'd like, I'll continue and implement any of the next steps above. 


{
  "id": 10,
  "email": "updated@example.com",
  "name": "Updated Name",
  "role": "manager",
  "permission": "download",
  "phone": "+15559990000",
  "address": "Unit 5, 100 Example Street",
  "is_verified": false,
  "is_active": true,
  "is_staff": true
}

3) Admin — Delete user (successful)

Request

DELETE {{base_url}}/admin/users/10/

Response

Status: 204 No Content (empty body)

4) User — Delete own account (for non-staff)

Request

DELETE {{base_url}}/auth/users/10/

Response (success)

Status: 204 No Content

Response (unauthorized attempt to delete another user)

Status: 403 Forbidden

{
  "detail": "You do not have permission to perform this action."
}

Edge cases & notes
--

- Deletion fallback: The `UserDeleteView` attempts to `delete()` the model instance. If a DB OperationalError occurs (e.g., due to DB-level foreign-key constraints or other issues), the view anonymizes the user (changes email to `deleted_user_<pk>@example.invalid`, sets name to "[deleted]", sets `is_active=False`) and returns 204. This ensures clients cannot rely solely on existence checks to determine whether a user was permanently removed.
- Email verification: `is_verified` is managed by allauth's `EmailAddress` model; registration and email verification flows are separate from the admin-managed create endpoint.
- Password handling: passwords are write-only. Never include them in GET responses. Admins creating users must provide `password` in the create payload.

Postman / environment hints
--

- Use the provided Postman environment file `docs/postman_accounts_admin_environment.json` to set `{{base_url}}` and `{{access_token}}`.
- To automate obtaining tokens, add a login call that posts to the project's auth/login endpoint (dj-rest-auth) with `admin_email` and `admin_password` and save the returned token to `{{access_token}}`.

Quick checklist for consumers
--

1. Import `docs/postman_accounts_admin_environment.json` into Postman and set `base_url` to your server.
2. Obtain a valid access token (JWT) for an admin/staff account and set `{{access_token}}`.
3. Use the collection `docs/postman_accounts_admin_collection.json` to run the endpoints.

Change log
--

- 2025-11-12 — Initial documentation created for Admin user endpoints and fields.

Questions or edits
--

If you want: add an example login request to the collection to auto-populate `{{access_token}}`, or include sample Postman tests/assertions for each response.

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
  *** End Patch
  - Non-field error: { "non_field_errors": ["Some error"] }
