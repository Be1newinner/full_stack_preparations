## 📂 **Topic 8: File Uploads (Images, PDFs) with FastAPI + MongoDB**

---

## 🧠 Why This Matters at FAANG-Level

| Concern | Why It Matters |
|--------|----------------|
| 🚀 File Upload Support | Modern apps often need profile pics, product images, resumes, etc. |
| 🧱 Storage Strategy | Needs clear separation of metadata (DB) and actual files (FS or cloud) |
| 🔐 Security | Sanitize file names, MIME type checking, size limits |
| 📈 Scalability | Recommend S3/GCS for large-scale systems |

---

## 🧭 Strategy Options

| Option | Best For | Notes |
|--------|----------|-------|
| 🗃 Store on Filesystem | Dev/small-scale apps | Store file path in MongoDB |
| ☁️ Store on S3/Bucket | Production-scale | Store file URL + metadata in MongoDB |
| 🧠 Store in MongoDB (GridFS) | Large files, no cloud | Not ideal for web apps, but good for ML workloads |

---

## ✅ Basic Upload Example: Filesystem Upload

---

### 📁 Folder Structure

```
📂app
 ┣ 📂uploads
 ┣ 📄main.py
 ┗ 📂routers
    ┗ 📄upload.py
```

---

### 🧪 Code: Basic Upload Endpoint

```python
# routers/upload.py
from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
import os
from uuid import uuid4

router = APIRouter()
UPLOAD_DIR = "uploads"

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate type
    if file.content_type not in ["image/png", "image/jpeg", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Create safe filename
    ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid4().hex}.{ext}"

    # Save to disk
    filepath = os.path.join(UPLOAD_DIR, unique_filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": unique_filename, "path": filepath}
```

---

### ✅ Save Metadata in MongoDB

```python
# services/upload_service.py
from datetime import datetime

async def save_file_metadata(db, filename: str, content_type: str, uploader_id: str):
    return await db["uploads"].insert_one({
        "filename": filename,
        "content_type": content_type,
        "uploaded_by": uploader_id,
        "created_at": datetime.utcnow()
    })
```

---

## 🔒 Security Considerations

| 🔍 Concern | ✅ Solution |
|-----------|-------------|
| Invalid file types | Check `file.content_type` |
| Large files | Use `File(..., max_length=10_000_000)` or nginx limits |
| XSS in filenames | Sanitize / UUID filenames |
| Path traversal | Never use user filenames as-is |

---

## 🚀 Bonus: Upload to Amazon S3 (Production-Grade)

```bash
pip install boto3 python-multipart
```

```python
# services/s3.py
import boto3
from uuid import uuid4

s3 = boto3.client("s3")

async def upload_to_s3(file: UploadFile, bucket: str):
    filename = f"{uuid4().hex}.{file.filename.split('.')[-1]}"
    s3.upload_fileobj(file.file, bucket, filename)
    file_url = f"https://{bucket}.s3.amazonaws.com/{filename}"
    return file_url
```

---

### 🧪 Test with Swagger UI

Upload a file via Swagger `/upload`, verify the metadata is saved, file exists, and accessible URL is returned.

---

## ✅ Best Practices Summary

| Best Practice | Description |
|---------------|-------------|
| 🧱 Store file metadata in Mongo | Store URL, MIME type, uploaded_by, etc. |
| 🔐 Validate file MIME + extension | To prevent malicious uploads |
| 🗃 Organize uploads by feature | e.g. `/uploads/users/`, `/uploads/products/` |
| ☁️ Use S3 for scalability | Better for large/production apps |
| 🧼 Sanitize file names | Use UUIDs instead of raw names |

---

## 🎯 Bonus Project Ideas (YouTube Material)

| Idea | Description |
|------|-------------|
| 📸 Avatar Upload | Image validation, resizing with Pillow |
| 📄 Resume Upload | Upload PDF for job boards |
| 🛒 Product Images | Multiple image support per product |
| 🧠 GridFS Example | For storing PDFs inside Mongo |
