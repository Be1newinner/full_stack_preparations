### ✅ **Topic 4: MongoDB Integration with Motor — Clean, Async, Scalable**

---

### 🎯 **Goal**:
- Use MongoDB asynchronously (FAANG-standard: non-blocking I/O)
- Maintain a clean architecture
- Set up dependency injection for DB
- Prepare for testing, scaling, and microservices

---

### ⚙️ **Library: Motor (Async MongoDB Driver)**

```bash
pip install motor
```

---

### 📁 Project Layout (Feature-Based + MongoDB):

```
app/
├── main.py
├── core/
│   └── config.py              ← Mongo URI from env
├── db/
│   ├── mongo.py               ← DB client, dependency function
│   └── collections.py         ← Collection references
├── api/
│   └── user/
│       ├── router.py
│       ├── schemas.py
│       └── service.py
```

---

## 🧩 Step-by-Step Breakdown

---

### 1. **MongoDB Connection Setup (`mongo.py`)**

```python
# app/db/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.MONGO_DB_NAME]

# Dependency function
def get_database(request: Request):
    return db
```

---

### 2. **Configuration (`config.py`)**

```python
# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "myapp"

    class Config:
        env_file = ".env"

settings = Settings()
```

✅ This allows us to use `.env` for deployment and keep secrets safe.

---

### 3. **Collection Access (`collections.py`)**

```python
# app/db/collections.py
from app.db.mongo import db

user_collection = db["users"]
product_collection = db["products"]
```

---

### 4. **Schemas for MongoDB IDs (`schemas.py`)**

MongoDB uses `ObjectId`, so you’ll need to validate it.

```python
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class UserBase(BaseModel):
    name: str
    email: str

class UserDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
```

---

### 5. **CRUD with Motor (`service.py`)**

```python
# app/api/user/service.py
from app.db.mongo import get_database
from app.api.user.schemas import UserDB, UserBase
from fastapi import Depends
from bson import ObjectId

async def create_user(user: UserBase, db = Depends(get_database)):
    user_dict = user.dict()
    result = await db["users"].insert_one(user_dict)
    user_dict["_id"] = result.inserted_id
    return UserDB(**user_dict)

async def get_user(user_id: str, db = Depends(get_database)):
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    return UserDB(**user) if user else None
```

---

### 6. **Router Layer (`router.py`)**

```python
# app/api/user/router.py
from fastapi import APIRouter, Depends, HTTPException
from app.api.user.schemas import UserBase, UserDB
from app.api.user.service import create_user, get_user

router = APIRouter()

@router.post("/", response_model=UserDB)
async def create(user: UserBase):
    return await create_user(user)

@router.get("/{user_id}", response_model=UserDB)
async def read(user_id: str):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

### 7. **Include Router in `main.py`**

```python
from fastapi import FastAPI
from app.api.user.router import router as user_router

app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["Users"])
```

## 🧠 **Bonus Teaching Points Explained with Examples**

---

### ✅ 1. **Use `ObjectId` Properly to Prevent Bugs**

---

MongoDB uses `_id` as a special field of type `ObjectId`. But FastAPI and Pydantic don't understand `ObjectId` by default — and this leads to bugs like:

- Invalid response serialization  
- Broken lookups (`find_one({"_id": user_id})` silently fails)

---

#### 🛠️ Fix: Custom `PyObjectId` for Pydantic

```python
from bson import ObjectId
from pydantic import BaseModel, Field

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class UserDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: str

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
```

💡 **Teach this to avoid 500s** in serialization, and to ensure `_id` shows as `id` in the response.

---

### ✅ 2. **Wrap Mongo Calls in `service.py` (Service Layer)**

---

🔥 FAANG-Level Pattern = **Separate business logic from routing**.

**❌ Don’t do this (in router):**

```python
@router.post("/")
async def create_user(user: UserBase):
    await db["users"].insert_one(user.dict())
    ...
```

**✅ Do this (in service.py):**

```python
# service.py
async def create_user(user: UserBase, db):
    result = await db["users"].insert_one(user.dict())
    return str(result.inserted_id)
```

```python
# router.py
@router.post("/")
async def create(user: UserBase, db=Depends(get_database)):
    return await create_user(user, db)
```

💡 **Why teach this?**  
- Keeps router clean and focused on HTTP handling  
- Services are reusable (can use in CLI, cron jobs, tests, etc.)  
- Makes **unit testing easier** (just mock `db`)

---

### ✅ 3. **Inject DB into Services with `Depends()`**

---

This is **FastAPI’s Dependency Injection system** — clean, scalable, and testable.

```python
# db/mongo.py
def get_database():
    return db
```

```python
# router.py
@router.post("/")
async def create_user(user: UserBase, db=Depends(get_database)):
    return await user_service.create_user(user, db)
```

💡 **Why teach this?**  
- Promotes **loose coupling**  
- You can easily **swap DB** in tests, microservices, or during refactors  
- It's how real-world DI works in NestJS, Spring Boot, etc.

---

### ✅ 4. **Return `UserDB` with `response_model` to Sanitize Response**

---

Returning full Mongo docs can leak internal fields (e.g., `hashed_password`, `internal_flags`, etc.)

FastAPI solves this with `response_model`.

```python
@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)
    return user
```

With `response_model=UserOut`, only safe fields are returned.

```python
# schemas.py
class UserOut(BaseModel):
    id: str
    name: str
    email: str
```

💡 **Why teach this?**  
- Enforces clean, minimal APIs  
- Reduces payload size  
- Protects sensitive info in prod

---

### ✅ 5. **Teach Why `async` I/O Matters for Scale**

---

MongoDB supports async via `motor`, and **FastAPI is async-first**.

---

#### ❌ Blocking call (not scalable):
```python
def get_users():
    users = db["users"].find()  # This blocks event loop!
```

#### ✅ Non-blocking, async call:
```python
async def get_users():
    users = []
    async for user in db["users"].find():
        users.append(user)
    return users
```

---

### 🔥 What to Explain to Students:

- **Async I/O = Non-blocking** — multiple requests handled concurrently
- Ideal for I/O-bound workloads like **DB, APIs, files, queues**
- If your service makes DB/API calls, you must use `async` to scale efficiently
- Blocking code in async frameworks causes performance bottlenecks

---

### ⚡ Pro Tip for Teaching:

Use a diagram like this:

```
[ Request 1 ] -- (awaiting DB) → Free to serve...
[ Request 2 ] -- (awaiting MongoDB) → Free to serve...
[ Request 3 ] -- → Now serving!
```

⛔ If blocking: All requests are stuck waiting 🐌  
✅ If async: FastAPI serves more requests concurrently ⚡