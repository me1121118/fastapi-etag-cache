# ⚡ fastapi-etag-cache

[![FastAPI](https://img.shields.io/badge/FastAPI-Supported-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![HTTP: 304 Not Modified](https://img.shields.io/badge/HTTP-304%20Not%20Modified-success.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)]()

> Automatic ETag generation and HTTP 304 Not Modified caching middleware for FastAPI.

Drastically reduces network bandwidth and accelerates mobile/web client loading times when API responses have not changed.

---

### ☕ Support My Studies / Buy Me a Coffee

Hey there! 👋 I build and open-source lightweight, focused developer tools.

If this small package reduced your server egress bandwidth, please consider supporting my college/tuition fund:
- ☕ **Buy Me a Coffee:** [buymeacoffee.com/yourname](https://www.buymeacoffee.com)
- 💖 **Ko-fi:** [ko-fi.com/yourname](https://ko-fi.com)
- ⭐ **Star this repository** to help other developers discover it!

---

## 📦 Installation

```bash
pip install git+https://github.com/me1121118/fastapi-etag-cache.git
```

---

## 🚀 Quick Example

```python
from fastapi import FastAPI
from fastapi_etag_cache import ETagMiddleware

app = FastAPI()

# Add 1 line of middleware
app.add_middleware(ETagMiddleware)

@app.get("/large-catalog")
async def get_catalog():
    # Returns 200 OK + ETag header on first request.
    # Returns 304 Not Modified (empty body) on subsequent requests if data hasn't changed!
    return {"catalog": ["product_1", "product_2"]}
```

---

## 🧪 Testing

```bash
pytest -v tests
```

---

## 📄 License

MIT License. Free for personal and commercial use.
