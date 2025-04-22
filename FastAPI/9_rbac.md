## 🛡️ **Topic 9: Role-Based Access Control (RBAC) in FastAPI**  
**(Production-Ready AuthZ for Admin/User/Mod Roles)**

---

### 🧠 Why FAANG-Level RBAC is Critical

| Concern | Why it Matters |
|--------|----------------|
| 🔐 Secure Resource Access | Prevent users from accessing admin-only features |
| 🏗️ Scalable Permissions | Easily manage multiple roles (admin, mod, user, etc.) |
| 📈 Enterprise Readiness | Every real-world app — SaaS, CMS, e-commerce — needs it |

---

## ✅ Step-by-Step Implementation of RBAC

---

### 1. 🏷️ Add Role Field in User Model

In `models/user_model.py` or your Pydantic schema:

```python
from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"

class UserDB(BaseModel):
    email: EmailStr
    hashed_password: str
    role: UserRole = UserRole.user  # default role
```

---

### 2. 🔐 Encode Role into JWT Token

In your auth service:

```python
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Call like this:
access_token = create_access_token({"sub": user.email, "role": user.role})
```

---

### 3. ✅ Create Dependency to Extract Role from JWT

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        user_role = payload.get("role")

        if user_email is None or user_role is None:
            raise HTTPException(status_code=403)

        return {"email": user_email, "role": user_role}
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
```

---

### 4. 🔒 Create `require_role` Decorator

```python
def require_role(required_roles: list):
    def role_checker(user = Depends(get_current_user)):
        if user["role"] not in required_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return role_checker
```

---

### 5. ✅ Use It in Any Protected Route

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/admin/dashboard")
def admin_only_endpoint(user = Depends(require_role(["admin"]))):
    return {"message": "Welcome Admin!"}

@router.get("/user/profile")
def user_profile(user = Depends(require_role(["user", "admin", "moderator"]))):
    return {"message": f"Hello {user['email']}"}
```

---

## 🧪 Example User Roles in MongoDB

```json
{
  "_id": ObjectId("..."),
  "email": "admin@example.com",
  "hashed_password": "...",
  "role": "admin"
}
```

---

## ⚙️ Optional Enhancements

| Feature | Benefit |
|--------|---------|
| 🔁 Dynamic Permissions | Use permissions stored in MongoDB, not hardcoded |
| 🛡️ Guard Routes via Middleware | Add fastapi `middleware` to log or block sensitive access |
| 📜 Audit Logs | Log role-based actions like deleting a user or changing configs |

---

## 📦 Best Practices Summary

| Best Practice | Why |
|---------------|-----|
| ✅ Role in JWT | Lightweight & secure way to transfer RBAC info |
| 🔐 Validate on Route | Keeps endpoints clean and easy to protect |
| 🧱 Enum for Roles | Avoids typos + IDE autocomplete |
| 🔁 Centralized Role Logic | Makes your app scalable and easier to test |

---

## 🎥 YouTube Video Ideas

| Video | What You'll Show |
|-------|------------------|
| 🔐 Build Role-Based Auth System | Step-by-step from JWT to route guards |
| 👥 Admin Panel with RBAC | CRUD restricted by user role |
| 💬 User + Moderator Comment App | Demo mod-only deletion/reporting |