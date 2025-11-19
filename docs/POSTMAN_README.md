# 📦 Eastmond Villa - Postman Collection

## 🎯 Overview

Complete Postman collection for the Eastmond Villa API with support for **all user roles** in a single environment file.

## 📂 Files

### Collection
- **`eastmondvilla-collection.json`** - Complete API collection (33 endpoints)

### Environment  
- **`eastmondvilla-environment.json`** - Unified environment with all user roles

---

## 🚀 Quick Start (3 Steps)

### Step 1: Import Collection
1. Open Postman
2. Click **Import** button
3. Select `eastmondvilla-collection.json`
4. Click **Import**

### Step 2: Import Environment
1. Click **Environments** icon (left sidebar)
2. Click **Import**
3. Select `eastmondvilla-environment.json`
4. Click **Import**

### Step 3: Select Environment & Login
1. Select **"Eastmond Villa - All Users Environment"** from dropdown (top-right)
2. Open **Authentication** folder
3. Click **Login** request
4. Click **Send**
5. ✅ Access token saved automatically!

---

## 👥 User Roles & Credentials

The environment includes credentials for **all user roles**:

| Role | Email | Password | Permission | Access Level |
|------|-------|----------|------------|--------------|
| **Admin** | admin@eastmondvilla.com | admin123 | full_access | Full system access |
| **Manager** | manager1@eastmondvilla.com | manager123 | full_access | Manage properties & bookings |
| **Agent** | agent1@eastmondvilla.com | agent123 | read_write | View & update properties |
| **Customer** | customer1@example.com | customer123 | only_view | Create bookings, view properties |

---

## 🔄 Switching Between Users

### Method 1: Change Environment Variables (Recommended)
1. Click **Environment Quick Look** (eye icon, top-right)
2. Edit `current_user_email` and `current_user_password`
3. Click **Login** request again

**Examples:**

**Login as Admin:**
```
current_user_email = admin@eastmondvilla.com
current_user_password = admin123
```

**Login as Customer:**
```
current_user_email = customer1@example.com
current_user_password = customer123
```

---

## 📋 API Endpoints (33 Total)

### 🔐 Authentication (5 endpoints)
- ✅ Register New User
- ✅ Login (auto-saves token)
- ✅ Get Current User
- ✅ Refresh Token
- ✅ Logout

### 👑 Admin - User Management (5 endpoints)
- ✅ List All Users
- ✅ Get User Details
- ✅ Create User (Admin)
- ✅ Update User (Admin)
- ✅ Delete User (Admin)

### 🏡 Properties (8 endpoints)
- ✅ List All Properties (Public)
- ✅ Search Properties (Public)
- ✅ Get Property Details (Public)
- ✅ Create Property (Admin/Manager)
- ✅ Update Property (Admin/Manager/Agent)
- ✅ Delete Property (Admin)
- ✅ Get Property Media (Public)
- ✅ Check Availability (Public)

### 📅 Bookings (7 endpoints)
- ✅ List My Bookings
- ✅ Create Booking
- ✅ Get Booking Details
- ✅ Update Booking
- ✅ Update Booking Status (Admin/Manager)
- ✅ Cancel Booking
- ✅ Delete Booking (Admin)

### 🎬 Media Management (5 endpoints)
- ✅ Upload Property Image
- ✅ Upload Property Video
- ✅ Add Virtual Tour URL
- ✅ Update Media
- ✅ Delete Media

---

## 🎯 Permission Matrix

| Action | Customer | Agent | Manager | Admin |
|--------|----------|-------|---------|-------|
| View Properties | ✅ | ✅ | ✅ | ✅ |
| Create Booking | ✅ | ✅ | ✅ | ✅ |
| View Own Bookings | ✅ | ✅ | ✅ | ✅ |
| View All Bookings | ❌ | ❌ | ✅ | ✅ |
| Update Property | ❌ | ✅ | ✅ | ✅ |
| Create Property | ❌ | ❌ | ✅ | ✅ |
| Delete Property | ❌ | ❌ | ❌ | ✅ |
| Approve Bookings | ❌ | ❌ | ✅ | ✅ |
| Manage Users | ❌ | ❌ | ❌ | ✅ |
| Upload Media | ❌ | ✅ | ✅ | ✅ |

---

## 🔥 Common Workflows

### Workflow 1: Create a Booking (Customer)
```
1. Login as Customer
2. List All Properties → Auto-saves property_id
3. Check Availability → Verify dates available
4. Create Booking → Uses saved property_id
5. Get Booking Details → View confirmation
```

### Workflow 2: Manage Properties (Admin)
```
1. Login as Admin
2. Create Property → Auto-saves property_id
3. Upload Property Image → Uses saved property_id
4. List All Properties → View new property
```

---

## 🆘 Troubleshooting

### Problem: "401 Unauthorized"
**Solutions:**
1. ✅ Run **Login** request first
2. ✅ Check environment is selected (top-right dropdown)
3. ✅ Verify `access_token` is saved (Eye icon → view variables)

### Problem: "403 Forbidden"
**Solution:**
- ✅ Check user role has permission for this action
- ✅ Review permission matrix above
- ✅ Try logging in as Admin or Manager

### Problem: Variables not saving
**Solutions:**
1. ✅ Ensure environment is selected
2. ✅ Check Test Results tab shows green checkmarks
3. ✅ View Console (bottom) for debug logs

---

## ✅ Summary

**Files:**
- ✅ `eastmondvilla-collection.json` - Complete API (33 endpoints)
- ✅ `eastmondvilla-environment.json` - All users in one environment

**Features:**
- ✅ All user roles (admin, manager, agent, customer)
- ✅ Easy role switching
- ✅ Automated token management
- ✅ Request chaining with auto-saved IDs
- ✅ Permission-based access control

**Ready to import and start testing!** 🚀
