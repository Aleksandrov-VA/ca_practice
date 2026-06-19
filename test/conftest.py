import pytest
from app.events.domain.entities import Event

@pytest.fixture
def valid_event():
    """валидный объект"""
    return Event.create(
        title       = 'заголовок тестового события',
        description = 'описание тестового события',
        start_at    = '2024-07-01T15:30:00',
        end_at      = '2024-07-01T16:30:00'
    )