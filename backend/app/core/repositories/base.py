"""Base generic repository interface definition."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")


class BaseRepository(ABC, Generic[T, ID]):
    """Abstract generic base repository interface for CRUD operations."""

    @abstractmethod
    def create(self, entity: T) -> T:
        """Create and store a new entity."""
        ...

    @abstractmethod
    def get_by_id(self, id_val: ID) -> T | None:
        """Retrieve an entity by identifier."""
        ...

    @abstractmethod
    def list_all(self) -> list[T]:
        """Retrieve all stored entities."""
        ...

    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an existing entity."""
        ...

    @abstractmethod
    def delete(self, id_val: ID) -> bool:
        """Delete an entity by identifier."""
        ...
