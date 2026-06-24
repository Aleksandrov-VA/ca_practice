from typing import Dict
from uuid import UUID
from app.events.domain.entities import Event
from app.events.domain.interfaces import EventRepository

class InMemoryEventRepository(EventRepository):
    """ реализация интерфейса репозитория для хранения представлений объектов события
        для сохранения использован словарь events: dict[UUID, event.to_dict()] = {}
    """
    def __init__(self):
        self.events : Dict[UUID, dict] = {}

    async def create_event_in_repo(self, event: Event) -> None:
        """ метод для создания записи в репозитории
            параметры: event - объект события для сохранения в репозитории
         """
        if event.id in self.events:
            raise ValueError(f'событие event.id = {event.id} уже существует в репозитории, повторная запись запрещена')
        self.events[event.id] = event.to_dict()
        return None

    async def update_event_in_repo(self, event: Event, **update_kwargs) -> None:
        """ метод для обновления записи в репозитории (редактирование события)
            параметры: event - обновляемое событие
                       update_kwargs - список значений для обновления полей существующей записи
        """
        if event.id not in self.events:
            raise ValueError(f'событие event.id = {event.id} не найдено в репозитории')
        updated_event_in_repo = event.update(**update_kwargs)
        self.events[event.id] = updated_event_in_repo.to_dict()
        return None

    async def delete_event_in_repo(self, event_id: UUID) -> None:
        """ метод для удаления записи в репозитории (удаление события)
            параметры: event - удаляемое событие
        """
        if  event_id not in self.events:
            return None
        self.events.pop(event_id)
        return None

    async def get_event_by_id(self, event_id: UUID) -> Event | None:
        """ метод для извлечения записи из репозитория (получение события)
            параметры: event_id - идентификатор извлекаемой записи
        """
        if event_id  not in self.events:
            return None
        event = Event.restore_from_dict(self.events[event_id])
        return event