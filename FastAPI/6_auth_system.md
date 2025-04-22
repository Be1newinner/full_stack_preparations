## ✅ **Topic 6: Auth System (Register/Login, Hash Passwords, JWT, Role-Based Access, Dependency-Based Auth)**

---

### 🧩 Step-by-Step Teaching Flow:

1. **Password Hashing with `passlib`**
2. **JWT Access Token Generation and Verification**
3. **Auth Routes — Register & Login**
4. **`get_current_user` Dependency for Securing Routes**
5. **RBAC (Role-Based Access Control) with Custom Dependencies**
6. **JWT Refresh Tokens (Bonus)**
7. **Auth Exception Handling (401, 403)**

---

## 🔐 1. Password Hashing (Never Store Plain Text!)

---

### Install `passlib`:

```bash
pip install passlib[bcrypt]
```

---

### Create Utility:

```python
# core/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

> ✅ Teach students that even bcrypt hashes **should never be logged or exposed**.

---

## 🔑 2. JWT Access Token Generation & Verification

---

### Install JWT Lib:

```bash
pip install python-jose[cryptography]
```

---

### Token Creation Utils:

```python
# core/jwt.py
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
```

---

## 🔐 3. Auth Routes — Register & Login

---

### Register

```python
@router.post("/register")
async def register(user_in: UserRegister, db=Depends(get_database)):
    hashed_pw = hash_password(user_in.password)
    user_doc = {**user_in.dict(exclude={"password"}), "hashed_password": hashed_pw}
    await db["users"].insert_one(user_doc)
    return ResponseModel(success=True, message="User created")
```

---

### Login

```python
@router.post("/login")
async def login(user_in: UserLogin, db=Depends(get_database)):
    user = await db["users"].find_one({"email": user_in.email})
    if not user or not verify_password(user_in.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["_id"]), "role": user.get("role", "user")})
    return ResponseModel(success=True, message="Login success", data={"access_token": token})
```

---

## 🧩 4. Dependency: `get_current_user()`

---

```python
# deps/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_database)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = await db["users"].find_one({"_id": ObjectId(payload["sub"])})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

---

## 🛡️ 5. Role-Based Access (RBAC)

---

### Secure Any Route by Role:

```python
def has_role(required_role: str):
    async def role_checker(current_user=Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(status_code=403, detail="Access denied")
    return role_checker
```

### Usage:

```python
@router.get("/admin-only")
async def admin_dashboard(
    current_user=Depends(get_current_user),
    _=Depends(has_role("admin"))
):
    return {"msg": "Welcome Admin!"}
```

✅ Clean  
✅ Testable  
✅ Extendable (e.g., multi-role, scope-based)

---

## 🎁 6. Bonus: Refresh Tokens (for Production-Grade Systems)

Use a separate JWT for refresh token (long expiry), store in cookies or secure storage, and rotate access tokens without login.

You can even store refresh tokens in MongoDB for **logout support**.

---

## 🚨 7. Proper Auth Exception Handling

- Use HTTP 401 for unauthenticated
- Use HTTP 403 for forbidden (authenticated but not allowed)
- Use global exception handlers as you did in Topic 5

---

## ✅ Student Summary Checklist

| Concept                   | Covered | Importance |
|---------------------------|---------|------------|
| Password Hashing          | ✅      | Critical   |
| JWT Token Flow            | ✅      | High       |
| `get_current_user` DI     | ✅      | Core       |
| Role-Based Access Control | ✅      | Production |
| Refresh Token             | ✅ (Bonus) | Optional |
| Auth Errors + StatusCode  | ✅      | Clean UX   |



## 🎁 6. Bonus: **Refresh Tokens (for Production-Grade Systems)**

---

### 🚀 Why Refresh Tokens?

Access tokens should:
- Be short-lived (e.g., 15–30 mins)
- Be stateless
- Prevent long-term hijacking

But... short expiry = constant re-login?

👉 **Solution**: Use a long-lived **Refresh Token** that can:
- Issue new access tokens
- Be rotated (invalidated if stolen)
- Allow logout functionality

---

## 🔁 Auth Flow Overview (with Refresh Tokens)

1. User logs in
2. Server returns:
   - `access_token` (short expiry)
   - `refresh_token` (long expiry)
3. `access_token` is sent in **Authorization Header**
4. `refresh_token` is stored in **HttpOnly Cookie** or **Secure Local Storage**
5. When `access_token` expires:
   - Client calls `/refresh-token`
   - Server verifies `refresh_token` and issues a new `access_token`

---

## 🧱 Implementation in FastAPI (Step-by-Step)

---

### ✅ Step 1: Update Token Utility Functions

```python
# core/jwt.py
from datetime import timedelta

ACCESS_EXPIRE_MIN = 15
REFRESH_EXPIRE_DAYS = 7

def create_tokens(data: dict):
    access_token = jwt.encode(
        {**data, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MIN)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    refresh_token = jwt.encode(
        {**data, "exp": datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return access_token, refresh_token
```

---

### ✅ Step 2: Update Login Route

```python
@router.post("/login")
async def login(user_in: UserLogin, db=Depends(get_database)):
    user = await db["users"].find_one({"email": user_in.email})
    if not user or not verify_password(user_in.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token, refresh_token = create_tokens({"sub": str(user["_id"]), "role": user["role"]})

    # Optionally store the refresh token in DB
    await db["users"].update_one({"_id": user["_id"]}, {"$set": {"refresh_token": refresh_token}})

    # Return refresh token in HttpOnly Cookie (or in body if mobile)
    response = JSONResponse(
        status_code=200,
        content={"access_token": access_token}
    )
    response.set_cookie("refresh_token", refresh_token, httponly=True, max_age=604800)
    return response
```

---

### ✅ Step 3: Refresh Token Route

```python
@router.post("/refresh-token")
async def refresh_token(request: Request, db=Depends(get_database)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    
    try:
        payload = decode_token(refresh_token)
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

    user_id = payload.get("sub")
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user or user.get("refresh_token") != refresh_token:
        raise HTTPException(status_code=403, detail="Refresh token mismatch")

    access_token, new_refresh_token = create_tokens({"sub": user_id, "role": user["role"]})

    # Optionally rotate refresh token
    await db["users"].update_one({"_id": user["_id"]}, {"$set": {"refresh_token": new_refresh_token}})

    response = JSONResponse(
        status_code=200,
        content={"access_token": access_token}
    )
    response.set_cookie("refresh_token", new_refresh_token, httponly=True, max_age=604800)
    return response
```

---

### ✅ Step 4: Logout (Invalidate Refresh Token)

```python
@router.post("/logout")
async def logout(current_user=Depends(get_current_user), db=Depends(get_database)):
    await db["users"].update_one({"_id": current_user["_id"]}, {"$unset": {"refresh_token": ""}})
    response = JSONResponse(status_code=200, content={"msg": "Logged out"})
    response.delete_cookie("refresh_token")
    return response
```

---

## 🛡️ Benefits of This Design

| Feature | Benefit |
|--------|---------|
| 🔐 Short-lived Access Token | Limits damage from stolen access tokens |
| 🔁 Long-lived Refresh Token | No frequent login UX issues |
| 🧠 Stored Refresh in DB | Enables full logout and token revocation |
| 🍪 Set as HttpOnly Cookie | Prevents XSS token theft |
| 🔄 Token Rotation | Prevents reuse of stolen refresh tokens |

---

## 🧪 Testing Advice for Students

- Use **Postman** or **Hoppscotch** with **cookie support**
- Test login ➝ wait ➝ call refresh ➝ get new access token
- Manually change refresh token in DB ➝ test failure scenario