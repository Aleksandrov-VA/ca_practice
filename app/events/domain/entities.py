from uuid import UUID, uuid4
from dataclasses import dataclass, field
from typing import Self
from app.events.domain.value_object import TimePeriod

@dataclass
class Event:
    title: str
    description: str
    period: TimePeriod
    id: UUID = field(default_factory = uuid4)

    @classmethod
    def create(cls, title: str, description: str, start_at: str, end_at: str) -> Self:
        period = TimePeriod.create(start_at, end_at)
        return cls(title = title, description = description, period = period)

    def update(self, **update_kwargs) -> Self:

        new_start_at = update_kwargs.pop('start_at', self.period.start_at.isoformat())
        new_end_at   = update_kwargs.pop('end_at',   self.period.end_at.isoformat())

        self.period = TimePeriod.create(new_start_at, new_end_at)

        for key, value in update_kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def to_dict(self):
            return {
            'id' : str(self.id),
            'title' : self.title,
            'description' : self.description,
            'start_at': self.period.start_at.isoformat(),
            'end_at' : self.period.end_at.isoformat()
        }

    @classmethod
    def restore_from_dict(cls, event_dict: dict) -> Self:
        try:
            period = TimePeriod.create(event_dict['start_at'], event_dict['end_at'])

            return cls(
                id = UUID(event_dict['id']),
                title = event_dict['title'],
                description = event_dict['description'],
                period = period
            )
        except KeyError as exc:
            raise ValueError(f'отсутствует обязательное поле {exc}')
        except ValueError as exc:
            raise ValueError(f'ошибка валидации: {exc}')


    def __eq__(self, other):
        if not isinstance(self, Event):
            return False
        return (
            self.id == other.id and
            self.title  == other.title and
            self.period == other.period and
            self.description == other.description)

    def __str__(self):
        return (f'\n'
                f'title: \t\t\t {self.title} \n'
                f'description: \t {self.description} \n'
                f'start_at: \t\t {self.period.start_at} \n'
                f'end_at: \t\t {self.period.end_at} \n'
                f'event_id: \t\t {self.id}')
