from sqlalchemy.orm import DeclarativeBase


class BaseDomainModel(DeclarativeBase):
    """
    Base class for all domain models.

    This is the root of the domain model hierarchy. All domain models should
    inherit from this class. It provides common functionality and serves as a
    marker for domain entities.
    """
    __abstract__ = True  # Mark this class as abstract for SQLAlchemy