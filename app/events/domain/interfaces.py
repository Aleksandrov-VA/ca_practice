from abc import ABC, abstractmethod
from uuid import UUID
from app.events.domain.entities import Event

class EventRepository(ABC):
    """ интерфейс репозитория для хранения (объектов) события """

    @abstractmethod
    async def create_event_in_repo(self, event: Event) -> None:
        """ метод для создания записи в репозитории
            параметры: event - объект события для сохранения в репозитории
        """
        pass

    @abstractmethod
    async def update_event_in_repo(self, event: Event, **fields) -> None:
        """ метод для обновления записи в репозитории (редактирование события)
            параметры: event - обновляемое событие
                       fields - список значений для обновления полей существующей записи
        """
        pass

    @abstractmethod
    async def delete_event_in_repo(self, event_id: UUID) -> None:
        """ метод для удаления записи в репозитории (удаление события)
            параметры: event_id - идентификатор удаляемой записи
        """
        pass

    @abstractmethod
    def get_event_by_id(self, event_id: UUID) -> Event | None:
        pass