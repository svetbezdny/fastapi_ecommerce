from uuid import uuid4

from fastapi import Request, Response, status
from loguru import logger
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class LogMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        log_id = str(uuid4())
        request = Request(scope)
        path = request.url.path

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                status_code = message["status"]

                with logger.contextualize(log_id=log_id):
                    if status_code in [401, 402, 403, 404]:
                        logger.warning(f"Request to {path} failed")
                    else:
                        logger.info("Successfully accessed " + path)
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            with logger.contextualize(log_id=log_id):
                logger.error(f"Request to {path} failed: {e}")
                response = Response(
                    content={"success": False},
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    media_type="application/json",
                )
                await response(scope, receive, send)
