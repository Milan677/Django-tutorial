# 🌐 Google OAuth2 Django Authentication

A simple **Google Login integration** using Django REST Framework (DRF) for the backend and the **Google Identity Services API** for the frontend.  
This project demonstrates how to authenticate users via Google, verify tokens on the backend, and issue JWTs for secure access to protected APIs.

---

## 🚀 Project Overview

This project implements a **Google Sign-In** flow where users can log in using their Google account.  
The workflow consists of:
1. **Frontend (HTML/JS)** → Handles Google sign-in and sends the ID token to the backend.
2. **Backend (Django)** → Verifies the Google ID token, creates or fetches the user, and issues JWT tokens.
3. **Authenticated APIs** → Use JWT access tokens to fetch user-specific data securely.

---

## 🧩 Frontend Flow

### 🔹 Overview

The frontend uses **Google Identity Services** to authenticate users and retrieve an ID token.  
This token is then sent to the Django backend for verification and JWT generation.

### 🔹 Steps

1. Google Sign-In button is loaded using:
   ```html
   <script src="https://accounts.google.com/gsi/client" async defer></script>
   ```
2. On login, Google returns a credential (ID Token).
3. The frontend sends this token to /api/google-login/.
4. The backend verifies the token and returns access + refresh tokens.
5. The frontend uses the access token to call /api/user-info/.

 | Tool                         | Purpose                                           |
| ---------------------------- | ------------------------------------------------- |
| **Google Identity Services** | Render Google login button and handle OAuth2 flow |
| **Fetch API**                | Communicate with backend endpoints                |
| **Local Django server**      | Backend logic and token verification              |

## ⚙️ Backend Flow
### 🔹 Overview

The backend uses Django REST Framework with Simple JWT for token management.
It includes:

- Token verification using google-auth

- User creation or retrieval

- JWT token issuance

- Protected endpoints with authentication

🔹 Flow Diagram

```html
Frontend → [Google Login Button]
       ↓
Google → returns ID Token
       ↓
Frontend → sends token to /api/google-login/
       ↓
Django → verifies token via google.oauth2.id_token
       ↓
Django → creates or fetches user
       ↓
Django → returns JWT tokens (access + refresh)
       ↓
Frontend → stores access token
       ↓
Frontend → uses token for /api/user-info/
```

## 🧱 Dependencies & Setup
### 🔹 Python Dependencies

| Package                         | Purpose                      |
| ------------------------------- | ---------------------------- |
| `Django`                        | Backend framework            |
| `djangorestframework`           | API framework                |
| `djangorestframework-simplejwt` | JWT authentication           |
| `google-auth`                   | Verify Google ID tokens      |
| `google-auth-oauthlib`          | OAuth helper tools           |
| `django-cors-headers`           | Handle cross-origin requests |

### 🔹 Installation Commands

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install django djangorestframework djangorestframework-simplejwt google-auth google-auth-oauthlib django-cors-headers

```
## 💡 Notes

- Your Google Client ID must match between frontend and backend.
- If you encounter CORS issues, verify django-cors-headers configuration.
-Tokens are JWT-based, so you can use them with any API that requires authentication.

### 🧰 Tech Stack

| Layer             | Technology                                 |
| ----------------- | ------------------------------------------ |
| **Frontend**      | HTML, JavaScript, Google Identity Services |
| **Backend**       | Django, DRF, JWT (SimpleJWT), Google Auth  |
| **Database**      | SQLite (default)                           |
| **Auth Protocol** | OAuth2 via Google ID Token Verification    |

### 👨‍💻 Author

Kamlesh Das
(📧 daskamlesh677@gmail.com)


