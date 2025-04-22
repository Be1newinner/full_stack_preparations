### ✅ **Topic 3: Path Parameters, Query Parameters, and Request Body with Pydantic**

This topic teaches how to build real APIs with user input, validations, and data modeling — the **core skill** for backend engineers.

---

#### 🎯 **Goals:**
- Understand how FastAPI handles:
  - Path parameters (e.g., `/users/{id}`)
  - Query parameters (e.g., `/search?q=fastapi`)
  - Request body using Pydantic models

---

#### 📘 **What to Teach:**

1. **Path Parameters:**
   ```python
   @app.get("/users/{user_id}")
   def get_user(user_id: int):
       return {"user_id": user_id}
   ```

2. **Query Parameters:**
   ```python
   @app.get("/search")
   def search(q: str = None, limit: int = 10):
       return {"query": q, "limit": limit}
   ```

3. **Request Body with Pydantic:**
   ```python
   from pydantic import BaseModel

   class UserCreate(BaseModel):
       name: str
       email: str
       age: int

   @app.post("/users")
   def create_user(user: UserCreate):
       return user.dict()
   ```

4. **Mixing All Together (FAANG-style endpoint):**
   ```python
   @app.post("/products/{product_id}")
   def update_product(product_id: str, q: str = None, product: ProductSchema = Body(...)):
       return {"product_id": product_id, "query": q, "payload": product}
   ```

## ✅ Extra Notes (FAANG-level Best Practices for Parameters and Body)

---

### 1. **`Body(..., embed=True)` → Controlling Payload Shape**

By default, FastAPI expects the full payload to match the Pydantic model directly.

But sometimes, you want the payload **nested under a key** — for example:

```json
{
  "user": {
    "name": "Vijay",
    "email": "vijay@example.com",
    "age": 30
  }
}
```

To accept this nested structure, use:

```python
from fastapi import Body
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users")
def create_user(user: UserCreate = Body(..., embed=True)):
    return user
```

💡 **Why teach this?**  
It gives you **flexibility** in API design — matching frontend/client expectations easily.

---

### 2. **Using `Query(...)` for Validations on Query Params**

This is where FastAPI shines with auto-validations 🔥

Example:

```python
from fastapi import Query

@app.get("/items")
def get_items(
    q: str = Query(..., min_length=3, max_length=50, regex="^fast.*"),
    limit: int = Query(10, ge=1, le=100)
):
    return {"q": q, "limit": limit}
```

🔍 **What this does:**
- `q` must start with `"fast"` and be 3-50 chars long.
- `limit` must be between 1 and 100.

🚀 These validations are **automatic**, and FastAPI generates clear errors like:
```json
{
  "detail": [
    {
      "loc": ["query", "q"],
      "msg": "string does not match regex",
      "type": "value_error.str.regex"
    }
  ]
}
```

💡 **Why teach this?**  
It enforces **API contracts** like a pro and protects against bad requests.

---

### 3. **`response_model=YourModel` to Sanitize Output**

Suppose your DB object contains sensitive info (e.g., hashed password), but you only want to return `id`, `name`, `email`.

Example:

```python
from pydantic import BaseModel

class UserDB(BaseModel):
    id: str
    name: str
    email: str
    hashed_password: str

class UserOut(BaseModel):
    id: str
    name: str
    email: str

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: str):
    # Pretend this comes from DB
    user = UserDB(
        id="abc123",
        name="Vijay",
        email="vijay@example.com",
        hashed_password="s3cret"
    )
    return user
```

🧼 FastAPI will **automatically strip** `hashed_password` in the response:
```json
{
  "id": "abc123",
  "name": "Vijay",
  "email": "vijay@example.com"
}
```

💡 **Why teach this?**  
It enforces **clean API responses** and protects data from leaks.