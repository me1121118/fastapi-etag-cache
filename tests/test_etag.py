import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from fastapi_etag_cache import ETagMiddleware

@pytest.fixture
def app():
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(ETagMiddleware)

    @fastapi_app.get("/items")
    async def get_items():
        return {"items": [1, 2, 3]}

    return fastapi_app

@pytest.mark.asyncio
async def test_etag_header_generation(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # First request: 200 with ETag header
        r1 = await client.get("/items")
        assert r1.status_code == 200
        assert "ETag" in r1.headers
        etag = r1.headers["ETag"]

        # Second request with matching If-None-Match: Returns 304 Not Modified
        r2 = await client.get("/items", headers={"If-None-Match": etag})
        assert r2.status_code == 304
        assert r2.text == "" # Zero body payload transferred!
