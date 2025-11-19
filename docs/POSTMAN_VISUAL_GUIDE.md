# 🎯 Postman Collection - Visual Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                   EASTMOND VILLA API                             │
│                  Complete Postman Collection                     │
└─────────────────────────────────────────────────────────────────┘

📦 FILES TO IMPORT
═══════════════════════════════════════════════════════════════════

  1️⃣  eastmondvilla-collection.json      (33 endpoints)
  2️⃣  eastmondvilla-environment.json     (All user roles)


👥 USER ROLES IN ENVIRONMENT
═══════════════════════════════════════════════════════════════════

  🔴 ADMIN        admin@eastmondvilla.com      / admin123
     └─ Full system access, user management

  🟡 MANAGER      manager1@eastmondvilla.com   / manager123
     └─ Manage properties & bookings

  🟢 AGENT        agent1@eastmondvilla.com     / agent123
     └─ Update properties, upload media

  🔵 CUSTOMER     customer1@example.com        / customer123
     └─ Create bookings, view properties


📋 API ENDPOINTS (33 TOTAL)
═══════════════════════════════════════════════════════════════════

  🔐 AUTHENTICATION (5)
     ├─ Register New User
     ├─ Login (auto-saves token) ⭐
     ├─ Get Current User
     ├─ Refresh Token
     └─ Logout

  👑 ADMIN - USER MANAGEMENT (5)
     ├─ List All Users
     ├─ Get User Details
     ├─ Create User
     ├─ Update User
     └─ Delete User

  🏡 PROPERTIES (8)
     ├─ List All Properties (Public) ⭐
     ├─ Search Properties (Public)
     ├─ Get Property Details (Public)
     ├─ Create Property (Admin/Manager)
     ├─ Update Property
     ├─ Delete Property (Admin)
     ├─ Get Property Media
     └─ Check Availability ⭐

  📅 BOOKINGS (7)
     ├─ List My Bookings
     ├─ Create Booking ⭐
     ├─ Get Booking Details
     ├─ Update Booking
     ├─ Update Status (Admin/Manager)
     ├─ Cancel Booking
     └─ Delete Booking (Admin)

  🎬 MEDIA MANAGEMENT (5)
     ├─ Upload Property Image
     ├─ Upload Property Video
     ├─ Add Virtual Tour URL
     ├─ Update Media
     └─ Delete Media

  ⭐ = Most commonly used endpoints


🔄 HOW TO SWITCH USERS
═══════════════════════════════════════════════════════════════════

  Step 1: Click 👁️ eye icon (top-right in Postman)
  
  Step 2: Edit these 2 variables:
  
    ┌─────────────────────────────────────────────────────┐
    │ current_user_email    │  admin@eastmondvilla.com   │
    │ current_user_password │  admin123                  │
    └─────────────────────────────────────────────────────┘
  
  Step 3: Run Login request again
  
  Step 4: ✅ Access token auto-saved!


🚀 QUICK START WORKFLOW
═══════════════════════════════════════════════════════════════════

  FOR CUSTOMERS:
  ──────────────────────────────────────────────────────────────
    1. Login as Customer
    2. List All Properties → saves property_id
    3. Check Availability
    4. Create Booking → uses saved property_id
    5. Get Booking Details
  
  
  FOR MANAGERS:
  ──────────────────────────────────────────────────────────────
    1. Login as Manager
    2. Create Property → saves property_id
    3. Upload Property Image → uses saved property_id
    4. List Bookings
    5. Update Booking Status (approve/confirm)
  
  
  FOR ADMINS:
  ──────────────────────────────────────────────────────────────
    1. Login as Admin
    2. List All Users → saves target_user_id
    3. Create User (new agent/manager)
    4. Update User Role
    5. Full access to all endpoints


🎨 AUTO-SAVED VARIABLES
═══════════════════════════════════════════════════════════════════

  After Login:
    ✅ access_token      (Used for all authenticated requests)
    ✅ refresh_token     (For refreshing expired token)
    ✅ user_id           (Current user ID)
    ✅ user_role         (admin/manager/agent/customer)
    ✅ user_permission   (only_view/read_write/full_access)
  
  After Listing Properties:
    ✅ property_id       (First property ID)
    ✅ property_slug     (Property slug)
  
  After Creating Booking:
    ✅ booking_id        (Created booking ID)
  
  After Uploading Media:
    ✅ media_id          (Uploaded media ID)


🎯 PERMISSION MATRIX
═══════════════════════════════════════════════════════════════════

  Action                    Customer  Agent  Manager  Admin
  ───────────────────────────────────────────────────────────
  View Properties              ✅      ✅      ✅      ✅
  Create Booking               ✅      ✅      ✅      ✅
  Update Property              ❌      ✅      ✅      ✅
  Create Property              ❌      ❌      ✅      ✅
  Delete Property              ❌      ❌      ❌      ✅
  Approve Bookings             ❌      ❌      ✅      ✅
  Manage Users                 ❌      ❌      ❌      ✅


⚡ 60-SECOND IMPORT
═══════════════════════════════════════════════════════════════════

  1. Open Postman
     
  2. Import Collection
     → Click "Import" button
     → Select "eastmondvilla-collection.json"
     → Click "Import"
     
  3. Import Environment
     → Click "Environments" icon (left sidebar)
     → Click "Import"
     → Select "eastmondvilla-environment.json"
     → Click "Import"
     
  4. Select Environment
     → Click dropdown (top-right)
     → Select "Eastmond Villa - All Users Environment"
     
  5. Test Login
     → Open "Authentication" folder
     → Click "Login" request
     → Click "Send"
     → ✅ See green checkmarks in Test Results
     
  6. Start Testing!
     → All endpoints ready to use
     → Tokens auto-saved
     → IDs auto-captured


🆘 TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════

  Problem: 401 Unauthorized
  ────────────────────────────────────────────────────────────
    ✅ Run Login request first
    ✅ Check environment is selected (top-right)
    ✅ Verify access_token is saved (click eye icon)
  
  
  Problem: 403 Forbidden
  ────────────────────────────────────────────────────────────
    ✅ User role doesn't have permission
    ✅ Check permission matrix above
    ✅ Try logging in as Admin or Manager
  
  
  Problem: Variables not saving
  ────────────────────────────────────────────────────────────
    ✅ Ensure environment is selected
    ✅ Check Test Results tab shows green checks
    ✅ View Console (bottom) for debug logs
  
  
  Problem: Server connection failed
  ────────────────────────────────────────────────────────────
    ✅ Start Django server:
       python manage.py runserver 8888
    ✅ Check base_url in environment (http://localhost:8888)


📚 DOCUMENTATION
═══════════════════════════════════════════════════════════════════

  📄 POSTMAN_README.md
     → Full documentation with workflows and examples
  
  📄 POSTMAN_QUICK_IMPORT.md
     → 60-second import guide
  
  📄 POSTMAN_FILES_SUMMARY.md
     → Overview and statistics
  
  📄 This file (visual guide)
     → Quick reference


✅ SUMMARY
═══════════════════════════════════════════════════════════════════

  Files:         2 (1 collection + 1 environment)
  Endpoints:     33 (all features covered)
  User Roles:    4 (admin, manager, agent, customer)
  Setup Time:    60 seconds
  Status:        ✅ Ready to import!


┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  🎉 Import the 2 files and start testing immediately! 🚀       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```
