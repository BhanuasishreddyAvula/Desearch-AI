"""Service container dependency providers placeholder for business services."""

from app.core.container import Container, container


def get_services_container() -> Container:
    """Dependency provider for business services container (placeholder)."""
    return container
