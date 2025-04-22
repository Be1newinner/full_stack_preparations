## 🧭 **Topic 7: Pagination, Filtering, and Search in MongoDB with FastAPI**

---

## 🧠 Why This Matters at FAANG-Level:

| Feature | Reason |
|--------|--------|
| ✅ **Pagination** | Prevents overfetching, optimizes API performance |
| 🔍 **Search** | Enables full-text search for modern apps |
| 🧼 **Filtering** | Allows flexible querying on any field |
| 📦 **Cursor-based Pagination (Bonus)** | Production-level support for infinite scroll & performance on huge datasets |

---

## ✅ Step-by-Step Teaching Plan (Start with Offset Pagination)

---

### 1️⃣ Basic Pagination Params

```python
# schemas/common.py
from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)
```

---

### 2️⃣ Route with Pagination

```python
# routers/products.py
from fastapi import APIRouter, Depends
from bson import ObjectId
from utils.db import get_database
from schemas.common import PaginationParams

router = APIRouter()

@router.get("/products")
async def get_products(pagination: PaginationParams = Depends(), db=Depends(get_database)):
    skip = (pagination.page - 1) * pagination.limit
    cursor = db["products"].find().skip(skip).limit(pagination.limit)
    data = await cursor.to_list(length=pagination.limit)

    total = await db["products"].count_documents({})
    return {
        "page": pagination.page,
        "limit": pagination.limit,
        "total": total,
        "data": data
    }
```

---

### 🧪 Test Cases

| Page | Limit | Expected |
|------|-------|----------|
| `1`  | `10`  | First 10 products |
| `2`  | `5`   | 6th to 10th product |
| `100`| `20`  | Possibly empty |

---

## 🔍 Add Filters and Search Support

### 3️⃣ Add Optional Query Filters

```python
@router.get("/products")
async def get_products(
    pagination: PaginationParams = Depends(),
    category: str = None,
    search: str = None,
    db=Depends(get_database)
):
    query = {}
    if category:
        query["category"] = category
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]

    skip = (pagination.page - 1) * pagination.limit
    cursor = db["products"].find(query).skip(skip).limit(pagination.limit)
    data = await cursor.to_list(length=pagination.limit)
    total = await db["products"].count_documents(query)

    return {
        "page": pagination.page,
        "limit": pagination.limit,
        "total": total,
        "filters": {"category": category, "search": search},
        "data": data
    }
```

---

### 💎 Advanced Filtering: Price Range, In-Stock, etc.

```python
price_min: float = Query(None, ge=0)
price_max: float = Query(None, ge=0)
in_stock: bool = Query(None)

# Then add:
if price_min is not None or price_max is not None:
    query["price"] = {}
    if price_min is not None:
        query["price"]["$gte"] = price_min
    if price_max is not None:
        query["price"]["$lte"] = price_max

if in_stock is not None:
    query["in_stock"] = in_stock
```

---

## ⚙️ Bonus: Cursor-Based Pagination (Production Style)

Perfect for mobile apps and infinite scrolling (like Instagram feed).

### Replace `skip/limit` with `_id`:

```python
@router.get("/products")
async def get_products(last_id: Optional[str] = None, limit: int = 10, db=Depends(get_database)):
    query = {}
    if last_id:
        query["_id"] = {"$gt": ObjectId(last_id)}

    cursor = db["products"].find(query).sort("_id", 1).limit(limit)
    data = await cursor.to_list(length=limit)

    return {
        "next_cursor": str(data[-1]["_id"]) if data else None,
        "data": data
    }
```

---

## 📦 Best Practices

| Principle | Tip |
|----------|-----|
| 🔥 FastAPI Dependency | Use for pagination & filters |
| 📊 Total Count | Always return with paginated response |
| 🔍 Case-Insensitive Search | Use `$regex` + `$options: "i"` |
| 📈 Indexing | Add indexes on search fields (`name`, `category`) |
| ⚙️ DRY Filters | Extract filters into reusable utils for large APIs |
