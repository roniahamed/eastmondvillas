# 🎯 START HERE - Postman Import Guide

## ✅ You Need Just 2 Files

### **File 1: The Collection**
📄 `eastmondvilla-collection.json` (33 KB)
- Contains all 33 API endpoints
- Authentication, Properties, Bookings, Media, Admin

### **File 2: The Environment**
📄 `eastmondvilla-environment.json` (3.9 KB)
- Contains all 4 user roles (Admin, Manager, Agent, Customer)
- Pre-configured with credentials
- Easy switching between users

---

## 🚀 Import in 3 Steps (60 Seconds)

### Step 1: Import Collection
```
Open Postman → Import → Select "eastmondvilla-collection.json"
```

### Step 2: Import Environment
```
Environments (left sidebar) → Import → Select "eastmondvilla-environment.json"
```

### Step 3: Test It
```
Select environment (top-right) → Authentication → Login → Send
✅ See access token in response!
```

---

## 👥 All User Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@eastmondvilla.com | admin123 |
| **Manager** | manager1@eastmondvilla.com | manager123 |
| **Agent** | agent1@eastmondvilla.com | agent123 |
| **Customer** | customer1@example.com | customer123 |

### Switch Users:
1. Click eye icon (👁️) top-right
2. Change `current_user_email` and `current_user_password`
3. Login again

---

## 📋 What You Get

✅ **33 API Endpoints**
- 5 Authentication endpoints
- 5 Admin/User Management endpoints
- 8 Property endpoints (CRUD + Media)
- 7 Booking endpoints (CRUD + Status)
- 5 Media Management endpoints

✅ **4 User Roles**
- Admin (full access)
- Manager (manage properties & bookings)
- Agent (update properties, upload media)
- Customer (create bookings, view properties)

✅ **Automated Features**
- Auto-save access tokens
- Auto-capture property/booking IDs
- Request chaining support
- Test scripts for validation

---

## 🎯 Quick Test Workflow

### Test as Customer:
```
1. Login as Customer (customer1@example.com)
2. List All Properties → auto-saves property_id
3. Check Availability
4. Create Booking → uses saved property_id
5. View Booking Details
```

### Test as Admin:
```
1. Login as Admin (admin@eastmondvilla.com)
2. List All Users
3. Create Property
4. Upload Property Image
5. Manage bookings
```

---

## 📚 Need More Help?

| Read This | If You Want |
|-----------|-------------|
| `POSTMAN_QUICK_IMPORT.md` | 60-second quick start guide |
| `POSTMAN_VISUAL_GUIDE.md` | Visual ASCII reference |
| `POSTMAN_README.md` | Complete documentation with workflows |
| `POSTMAN_FILES_SUMMARY.md` | Overview and statistics |

---

## 🆘 Troubleshooting

**Problem:** 401 Unauthorized
- ✅ Run Login request first
- ✅ Check environment is selected (top-right dropdown)

**Problem:** 403 Forbidden
- ✅ User doesn't have permission for this action
- ✅ Try logging in as Admin

**Problem:** Variables not saving
- ✅ Make sure environment is selected
- ✅ Check Test Results tab for green checkmarks

---

## ✅ Checklist

- [ ] Downloaded both JSON files
- [ ] Opened Postman
- [ ] Imported collection
- [ ] Imported environment
- [ ] Selected environment
- [ ] Tested login
- [ ] Ready to test all endpoints!

---

## 🎉 That's It!

**Total Files:** 2  
**Total Setup Time:** 60 seconds  
**Total Endpoints:** 33  
**Total User Roles:** 4  

**Import the 2 files and start testing immediately!** 🚀

---

**Questions?** Read the detailed documentation in `POSTMAN_README.md`
