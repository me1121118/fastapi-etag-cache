"""
fastapi-etag-cache: Automatic ETag calculation and HTTP 304 Not Modified middleware for FastAPI.
Drastically saves network bandwidth and speeds up repeat API requests.
"""

import hashlib
from typing import Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class ETagMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware that calculates SHA-1 ETags on GET responses.
    If the client sends a matching 'If-None-Match' header, returns HTTP 304 Not Modified.

    Usage:
        app.add_middleware(ETagMiddleware)
    """
    def __init__(self, app, weak: bool = True):
        super().__init__(app)
        self.weak = weak

    async def dispatch(self, request: Request, call_next) -> Response:
        # Only process safe GET and HEAD requests
        if request.method not in ("GET", "HEAD"):
            return await call_next(request)

        response = await call_next(request)

        # Only apply to successful 200 responses
        if response.status_code != 200:
            return response

        # Read response body
        body = [section async for section in response.body_iterator]
        full_body = b"".join(body)

        # Generate SHA-1 hash of body
        digest = hashlib.sha1(full_body).hexdigest()
        etag = f'W/"{digest}"' if self.weak else f'"{digest}"'

        # Check client's If-None-Match header
        client_etag = request.headers.get("If-None-Match")
        if client_etag and (client_etag == etag or client_etag == f'"{digest}"' or client_etag == "*"):
            return Response(status_code=304, headers={"ETag": etag})

        # Return original response with ETag header
        new_headers = dict(response.headers)
        new_headers["ETag"] = etag

        return Response(
            content=full_body,
            status_code=response.status_code,
            headers=new_headers,
            media_type=response.media_type
        )
