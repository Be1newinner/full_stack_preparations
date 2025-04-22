### ✅ **Topic 2: FastAPI Installation + Project Setup**

This step ensures the student can get their first FastAPI app running confidently with proper structure — essential for maintainability and scaling later.

---

#### 🎯 **Goals:**
- Set up FastAPI and Uvicorn
- Create first basic route
- Use best folder structure from Day 1 (FAANG-style)
- Understand how FastAPI runs behind the scenes with ASGI

---

#### 📦 **What to Teach:**

1. **Installation:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install fastapi uvicorn
   ```

2. **Create First App:**
   `main.py`
   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/")
   def read_root():
       return {"message": "Hello, FastAPI"}
   ```

   Run:
   ```bash
   uvicorn main:app --reload
   ```

### 3. Feature-Based FastAPI Project Structure (FAANG-style)

```
app/
├── main.py                     ← FastAPI instance, includes routers
├── api/                        ← All API routers (grouped by feature)
│   ├── user/
│   │   ├── router.py           ← All endpoints related to user
│   │   ├── schemas.py          ← Pydantic models for validation
│   │   ├── service.py          ← Business logic (create_user, auth, etc.)
│   │   └── dependencies.py     ← Auth middleware, user injection
│   └── product/
│       ├── router.py
│       ├── schemas.py
│       ├── service.py
│       └── dependencies.py
├── core/                       ← App settings, configs, middlewares
│   ├── config.py
│   └── auth.py
├── db/                         ← DB connection, models, migrations
│   ├── base.py                 ← SQLAlchemy Base
│   ├── models/
│   │   ├── user.py
│   │   └── product.py
│   └── session.py              ← DB session creator
├── utils/                      ← Helper utils, reusable tools
│   └── security.py             ← password hash, token utils
└── tests/                      ← Unit & integration tests (pytest)
    ├── user/
    └── product/
```

---

### ✅ Why Feature-Based Is Better for FAANG-Level Backend:

| Traditional | Feature-Based |
|------------|----------------|
| Models, routes, services separated globally | All related logic grouped together |
| Harder to scale or isolate features | Easy to convert each feature into a microservice |
| Tight coupling, scattered logic | Encapsulated, testable, replaceable |