## ✅ **Topic 5: Creating Reusable Response Models, Exception Handling, and HTTPStatus Usage (FAANG-Style)**

These are critical to **building clean, consistent APIs** that are scalable, testable, and easy for frontend teams to consume.

---

### 🔹 1. **Reusable Response Models (Standard API Response Format)**

#### ❌ Don’t just return raw data like:
```python
return {"id": user.id, "email": user.email}
```

#### ✅ Do this (Standardize the Response Format):
```python
# schemas/response.py
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")

class ResponseModel(GenericModel, Generic[DataT]):
    success: bool
    message: str
    data: Optional[DataT] = None
```

#### 🔁 Example Usage:
```python
from schemas.response import ResponseModel
from schemas.user import UserOut

@router.get("/{user_id}", response_model=ResponseModel[UserOut])
async def get_user(user_id: str, db=Depends(get_database)):
    user = await user_service.get_user_by_id(user_id, db)
    if not user:
        raise NotFoundException("User not found")
    return ResponseModel(success=True, message="User fetched", data=user)
```

> 💡 **Why teach this?**
- Consistent frontend integration
- Easily integrates with OpenAPI docs
- Frontend always expects `{ success, message, data }` — clean contract

---

### 🔹 2. **Global Exception Handling (Custom Exceptions + Middlewares)**

---

#### 🎯 Goal: **Catch all known errors globally and return proper response**

---

#### ✅ Step 1: Define Custom Exceptions
```python
# exceptions.py
class NotFoundException(Exception):
    def __init__(self, message: str = "Resource not found"):
        self.message = message
```

---

#### ✅ Step 2: Global Exception Handler
```python
# main.py or middlewares/exception_handler.py
from fastapi.responses import JSONResponse
from fastapi import Request
from exceptions import NotFoundException
from schemas.response import ResponseModel

@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content=ResponseModel(success=False, message=exc.message).dict()
    )
```

---

### 🔹 3. **Use `HTTPStatus` Enum Instead of Hardcoded Status Codes**

---

```python
from http import HTTPStatus

return JSONResponse(
    status_code=HTTPStatus.CREATED,
    content=ResponseModel(success=True, message="User created").dict()
)
```

✅ Cleaner  
✅ More readable  
✅ IDE autocompletion  
✅ Self-documented

---

### 🔁 Real-World Use Case Example (Create User Flow)

```python
from schemas.response import ResponseModel
from schemas.user import UserOut, UserIn
from http import HTTPStatus
from fastapi import APIRouter, Depends, status
from exceptions import AlreadyExistsException

@router.post("/", response_model=ResponseModel[UserOut], status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn, db=Depends(get_database)):
    existing = await db["users"].find_one({"email": user.email})
    if existing:
        raise AlreadyExistsException("User with this email already exists")

    new_user = await user_service.create_user(user, db)
    return ResponseModel(success=True, message="User created", data=new_user)
```

---

### 🧠 Summary Cheat Sheet for Students

| Feature                  | Why It Matters                             | FAANG Benefit |
|--------------------------|--------------------------------------------|----------------|
| Generic Response Model   | Consistent API contract                    | Frontend + Docs |
| Global Exception Handler | Cleaner router logic                       | Easier testing |
| Custom Exceptions        | Better error tracking                      | Logging + Alerting |
| HTTPStatus Enum          | Better readability                         | Maintainability |
| Reusable `response_model` | Secure and precise API responses           | Security ✅ |