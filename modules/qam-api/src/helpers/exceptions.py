"""API exceptions."""


class BadRequest(Exception):
    """Bad request exception."""


class InternalError(Exception):
    """Internal error exception."""


class NotFound(Exception):
    """Raised when a requested resource does not exist."""

    pass


class Conflict(Exception):
    """Raised when a request conflicts with current resource state."""

    pass
