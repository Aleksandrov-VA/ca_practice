from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Self

@dataclass(frozen = True)
class TimePeriod:
    """ Value-object для представления периода времени события """
    start_at: datetime
    end_at:   datetime
    _created_by_factory: bool = False

    @classmethod
    def create(cls, start_at_str: str, end_at_str: str) -> Self:
        """ Создание объекта TimePeriod из строк в формате ISO-8601 """
        try:
            start_at = datetime.fromisoformat(start_at_str)
        except ValueError:
            raise ValueError(f'Некорректный формат метки начала события')
        try:
            end_at = datetime.fromisoformat(end_at_str)
        except ValueError:
            raise ValueError(f'Некорректный формат метки завершения события')
        return cls(start_at, end_at, _created_by_factory = True)

    def __post_init__(self):
        """ Валидация временных меток начала и окончания события"""
        if self.start_at > self.end_at:
            raise ValueError('Начало события не может быть позже его окончания.')

        if self.start_at == self.end_at:
            raise ValueError('Событие не может иметь нулевую продолжительность.')

        if not self._created_by_factory:
            raise RuntimeError('попытка прямого обращения к конструктору класса TimePeriod')


    def __eq__(self, other):
        if not isinstance(self, TimePeriod):
            return False
        return (
            self.start_at == other.start_at and
            self.end_at == other.end_at)

    def __str__(self):
        return f'{self.start_at} - {self.end_at}'