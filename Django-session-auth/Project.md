# Django REST Framework Session Authentication with CSRF and Custom User Model

This project demonstrates how to implement **Session Authentication** in Django REST Framework using a **Custom User Model** with **CSRF token protection**.  
It includes:
- Registration, Login, Logout APIs
- Protected view (only for authenticated users)
- "Check session" API to detect logged-in state
- HTML + JavaScript frontend with professional API calls

---

## **Project Flow**
1. **User visits the site** → frontend calls `/api/me/` to check session.
2. If session is valid → dashboard is shown immediately.
3. If not logged in → login/register form is displayed.
4. **Login**:  
   - Frontend gets CSRF token from `/api/csrf/`.
   - Sends POST request with credentials to `/api/login/`.
   - Django creates a session (`sessionid` cookie) and stores user login state.
5. **Protected View**:
   - Browser sends session cookie automatically.
   - Backend authenticates using `SessionAuthentication`.
6. **Logout**:
   - Frontend sends POST request to `/api/logout/` with CSRF token.
   - Django deletes session data.

---

## **Backend Setup**

### 1️⃣ Install dependencies
