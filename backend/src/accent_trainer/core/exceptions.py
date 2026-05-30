class AppError(Exception):
    """Base exception class for all application errors"""


class NotFoundError(AppError):
    """Raised when domain entity is not found"""


class ValidationError(AppError):
    """Raised on domain-level validation failures"""


class UnauthorizedError(AppError):
    """Raised on authorization / authentification failures"""
