# 🚀 Quick Import Guide

## What You Have

- **1 Collection**: `eastmondvilla-collection.json` (33 endpoints)
- **1 Environment**: `eastmondvilla-environment.json` (All user roles)

---

## Import in 60 Seconds

### Step 1: Import Collection
```
1. Open Postman
2. Click "Import" button (top-left)
3. Drag & drop "eastmondvilla-collection.json"
4. Click "Import"
```

### Step 2: Import Environment
```
1. Click "Environments" icon (left sidebar)
2. Click "Import"
3. Select "eastmondvilla-environment.json"
4. Click "Import"
```

### Step 3: Test It
```
1. Select "Eastmond Villa - All Users Environment" (top-right dropdown)
2. Open "Authentication" folder
3. Click "Login" request
4. Click "Send" button
5. ✅ See access token in response
6. ✅ Check "Test Results" tab shows green checkmarks
```

---

## Switch Users

Edit these 2 variables in environment:

| User Type | Email | Password |
|-----------|-------|----------|
| Admin | admin@eastmondvilla.com | admin123 |
| Manager | manager1@eastmondvilla.com | manager123 |
| Agent | agent1@eastmondvilla.com | agent123 |
| Customer | customer1@example.com | customer123 |

**How to switch:**
1. Click eye icon (top-right)
2. Change `current_user_email`
3. Change `current_user_password`
4. Login again

---

## Test Workflows

### Customer Flow
```
Login → List Properties → Check Availability → Create Booking
```

### Admin Flow
```
Login → Create Property → Upload Image → List All Users
```

### Manager Flow
```
Login → List Bookings → Update Status → Approve Booking
```

---

## Troubleshooting

**Problem:** 401 Unauthorized
- ✅ Login first
- ✅ Check environment is selected

**Problem:** Variables not saving
- ✅ Environment must be selected (top-right)
- ✅ Check Test Results tab for green checks

**Problem:** Server connection failed
- ✅ Start Django: `python manage.py runserver 8888`
- ✅ Check `base_url` in environment

---

## What's Included

✅ **33 API Endpoints**
✅ **4 User Roles** (Admin, Manager, Agent, Customer)
✅ **Automated Token Management**
✅ **Auto-Save IDs** (property_id, booking_id)
✅ **Request Chaining**
✅ **Permission Testing**

---

## Next Steps

1. ✅ Import files
2. ✅ Select environment
3. ✅ Login
4. ✅ Start testing!

**Total time:** ~60 seconds 🎉

See `POSTMAN_README.md` for detailed documentation.
