from __future__ import annotations


class AppError(Exception):
    """Base exception class for all application errors"""


class NotFoundError(AppError):
    """Raised when domain entity is not found"""


class ValidationError(AppError):
    """Raised on domain-level validation failures"""


class UnauthorizedError(AppError):
    """Raised on authorization / authentification failures"""


class DomainError(Exception):
    """Base class for all explicit domain/application errors."""


class ValidationError(DomainError):
    """Raised when input data is invalid at the use-case level."""


class NotFoundError(DomainError):
    """Raised when a referenced entity does not exist."""


class PermissionDeniedError(DomainError):
    """Raised when the caller is not allowed to perform the action."""


class ConflictError(DomainError):
    """Raised on uniqueness/state conflicts."""