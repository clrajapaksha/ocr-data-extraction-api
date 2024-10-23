from typing import Optional, List
from fastapi import HTTPException


class ValidateUploadFileSizeMiddleware:
    """Content size limiting middleware for ASGI applications

    Args:
      app (ASGI application): ASGI application
      max_content_size (optional): the maximum content size allowed in bytes, None for no limit
    """

    def __init__(self, app, max_content_size: Optional[int] = None):
        self.app = app
        self.max_content_size = max_content_size

    def receive_wrapper(self, receive):
        received = 0

        async def inner():
            nonlocal received
            message = await receive()
            if message["type"] != "http.request" or self.max_content_size is None:
                return message
            body_len = len(message.get("body", b""))
            received += body_len

            if received > self.max_content_size:
                raise HTTPException(detail="File is too big", status_code=413)

            return message

        return inner

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        wrapper = self.receive_wrapper(receive)
        await self.app(scope, wrapper, send)