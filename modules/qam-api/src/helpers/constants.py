"""Generic constants."""

import os
import textwrap

# API designation
API_VERSION = "0.1"
API_VERSION_PATH = "v1"
API_TITLE = "QAM API Service"
API_DESCRIPTION = textwrap.dedent(
    """
    This service manages the QAM companies.
    """
)

# Database configuration
PG_HOST = os.environ.get("PG_HOST", "localhost")
PG_PORT = int(os.environ.get("PG_PORT", "5432"))
PG_USER = os.environ.get("PG_USER", "postgres")
PG_PASSWORD = os.environ.get("PG_PASSWORD", "postgres")
PG_DATABASE = os.environ.get("DB_NAME", "qam_db")
