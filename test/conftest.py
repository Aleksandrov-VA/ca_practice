import pytest
from app.events.domain.entities import Event
from app.events.infrastructure.inmemory_event_repository import InMemoryEventRepository

@pytest.fixture
def valid_event():
    """фикстура предоставляющая валидный объект события"""
    return Event.create(
        title       = 'заголовок тестового события',
        description = 'описание тестового события',
        start_at    = '2024-07-01T15:30:00',
        end_at      = '2024-07-01T16:30:00'
    )

@pytest.fixture(scope="function")
def inmemory_repo():
    """фикстура предоставляющая валидный объект хранимого в памяти репозитория"""
    return InMemoryEventRepository()
