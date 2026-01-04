# 🔐 Role-Based Access Control (RBAC) System

### Django + DRF + JWT + Custom Frontend

## 📌 Project Overview

This project is a custom-built Role-Based Access Control (RBAC) and Permission Management System developed using Django and Django REST Framework, with a fully decoupled frontend (HTML, CSS, JavaScript).

Unlike typical Django projects that rely on Django Admin, ViewSets, or automatic permission handling, this system implements manual, explicit permission logic at both the backend and frontend layers.

The goal of this project is to demonstrate a real-world, enterprise-grade permission system similar to what is used in SaaS platforms, LMS systems, ERP tools, and internal admin panels.

---

## 🧠 Key Concepts Demonstrated

- JWT-based authentication

- Role management using Django Groups

- Manual permission enforcement (backend + frontend)

- API-driven permission assignment

- Secure, scalable RBAC architecture

- Clear separation of concerns (Auth, Roles, Permissions, UI)

## 🛠 Tech Stack

### Backend

- Python

- Django

- Django REST Framework

- Django built-in permissions & groups

- JWT Authentication

### Frontend

- HTML

- CSS

- Vanilla JavaScript

- API-driven UI (no Django templates)

---

## 🔑 Authentication System

- Login API
``` js
POST /api/login/
```
- Uses JWT authentication

- On successful login:

     - Access token and user details are stored in localStorage

- Users are redirected based on role:

    - Admin → Admin Dashboard

    - Teacher / Student → Restricted Dashboard

## 👥 Role Management

Roles are implemented using Django Groups:

- `admin`

- `teacher`

- `student`

Each user belongs to exactly one role.
Roles act as the base layer of access control, while permissions define fine-grained access.

---

## 🔥 Permission System (Core Focus)

This project heavily focuses on manual permission management, using Django’s built-in permissions but enforcing them explicitly.

### Backend Permission Checks

Permissions are checked manually using:
``` python
request.user.has_perm("app_label.permission_codename")
```


Example:
``` python
request.user.has_perm("course.add_course")
```


No automatic permission handling is used.

---

## Permission Management Features

- API to list permissions grouped by model

- Custom UI to:

   - Display permissions model-wise

   - Assign / remove permissions for a user

   - Persist permission changes

- Changes take effect immediately

This replaces the need for Django Admin and provides a cleaner, API-driven approach.

---

## 📦 CRUD APIs With Explicit Permission Enforcement

For each model:

- Course

- Subject

- Book

### The following APIs are implemented:

- Create (``add_*``)

- Read (``view_*``)

- Update (``change_*``)

- Delete (``delete_*``)

### Important Design Choice

- ✔ Function-based views

- ✔ Explicit permission checks per action

- ❌ No ViewSets

- ❌ No automatic permissions

This ensures maximum clarity and control, making the permission flow easy to debug and explain.

---

## 🎨 Frontend Permission Enforcement (UX Layer)

The frontend enhances user experience by being permission-aware.

### Frontend Behavior

- Action buttons exist for each model and operation

- Before making an API call:

    - JWT token existence is verified

    - Permission existence is checked in localStorage

- UI feedback:

   - Success messages for allowed actions

   - Permission-denied messages for restricted actions

### ⚠️ Note:
Frontend checks are only for UX.
Backend remains the single source of truth for security.
---

## 🧑‍💼 Admin Dashboard Features

Admins can:

- View all users

- Select a specific user

- View all permissions grouped by model

- Assign or revoke permissions

- Save changes

- Immediately test permissions via UI buttons

This effectively acts as a custom RBAC admin panel, without relying on Django Admin.
---

### 🧩 What This Project Represents

This project is a custom RBAC + Permission Management System, comparable to:

- Enterprise admin dashboards

- SaaS back-office tools

- Learning Management Systems (LMS)

- ERP permission architectures

This is not a basic CRUD demo, but a real-world access control system.

---

## ✅ Design Strengths

- Manual permission checks → clear & debuggable

- Backend-enforced security → safe & reliable

- Frontend permission awareness → better UX

- JWT-based authentication → scalable

- No hidden abstractions → interview-friendly

This architecture reflects real industry practices.fresh-token handling

---

## ⚠️ Important Note: Superuser & Permissions
``` python
user = User.objects.create(**data, is_staff=True, is_superuser=True)
```


When `is_superuser=True`, the user **automatically bypasses all permission checks**.

A superuser has **full access to every action**, even if no explicit permissions are assigned.

This behavior is **built into Django** and does not require manual permission assignment.

## ⚠️ Recommendation

Do not use `is_superuser=True` for testing or demonstrating your RBAC system.

Use a regular user (`is_superuser=False`) and assign permissions explicitly to properly validate role-based access control.

Reserve the superuser account only for emergency or system-level access.

This ensures your permission system behaves as intended and accurately reflects real-world access control scenarios.
---
