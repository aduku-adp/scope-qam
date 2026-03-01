#!/usr/bin/env python3
"""FastAPI entrypoint for local execution and WSGI/ASGI import."""

import os

import uvicorn

from application import make_app  # application definition

is_local_runtime = bool((__name__ == "__main__") or os.environ.get("LOCAL_TEST"))

# In pytest, tests patch and build dedicated app instances.
if os.environ.get("TEST_ENV", "0") != "1":  # pragma: no cover
    app = make_app(is_local_runtime=is_local_runtime)

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)  # nosec
