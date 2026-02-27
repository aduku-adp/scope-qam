#!/usr/bin/env python3
"""Main to define a FastAPI application for GKE, GCR, or GCF.

Please do not modify this file, or at your own risk.
"""
import os

import uvicorn

from application import make_app  # application definition

is_local_runtime = bool((__name__ == "__main__") or os.environ.get("LOCAL_TEST"))

# In pytest, we use a test app instead
if os.environ.get("TEST_ENV", "0") != "1":  # pragma: no cover
    app = make_app(is_local_runtime=is_local_runtime)

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run("main:app", host="0.0.0.0", port=8008, reload=True)  # nosec
