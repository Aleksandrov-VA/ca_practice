import pytest
from app.events.domain.entities import Event

def test_event_create_valid_data(valid_event):
    """ проверка создание объекта события с корректными данными """
    assert valid_event.title       == 'заголовок тестового события'
    assert valid_event.description == 'описание тестового события'
    assert valid_event.period.start_at.isoformat() == '2024-07-01T15:30:00'
    assert valid_event.period.end_at.isoformat()   == '2024-07-01T16:30:00'

@pytest.mark.parametrize('update_kwargs', [
        {'title' : 'новый заголовок события'},
        {'description' : 'новое описание события'},
        {'title': 'повторная смена заголовка', 'description' : 'повторная правка описания события'}
    ],
    ids = [
        'update_title',
        'update_description',
        'update_all_attributes'
    ])
def test_event_update_valid_attributes(valid_event, update_kwargs):
    """ параметризованный тест:
        проверка обновления события с корректными данными
        (обновление заголовка события, описания события, обновление обоих параметров) """

    valid_event_id = valid_event.id
    updated_event  = valid_event.update(**update_kwargs)

    assert updated_event is valid_event
    assert valid_event.id == valid_event_id

    for key, value in update_kwargs.items():
        assert getattr(valid_event, key) == value

@pytest.mark.parametrize('update_kwargs', [
        {'start_at' : '2004-06-30T09:15:00'},
        {'end_at'   : '2024-07-02T09:15:00'},
        {'start_at' : '2024-06-30T09:15:00', 'end_at' : '2024-07-15T09:15:00'},
    ],
    ids = [
        'update_time_period.start_at',
        'update_time_period.end_at',
        'update_time_period_all'
    ])

def test_event_update_valid_time_period(valid_event, update_kwargs):
    """ параметризованный тест:
        проверка обновления события с корректными данными
        (обновление временных меток начала события, завершения события, обновление обоих параметров) """

    expected_start_time = update_kwargs.get('start_at', valid_event.period.start_at.isoformat())
    expected_end_time   = update_kwargs.get('end_at',   valid_event.period.end_at.isoformat())

    valid_event_id = valid_event.id
    updated_event  = valid_event.update(**update_kwargs)

    assert updated_event is valid_event
    assert valid_event.id == valid_event_id

    assert updated_event.period.start_at.isoformat() == expected_start_time
    assert updated_event.period.end_at.isoformat()   == expected_end_time

@pytest.mark.parametrize('create_kwargs, expected_error', [
        ({'start_at' : '2024-16-30T09:15:00', 'end_at' : '2024-06-30T09:45:00'}, 'Некорректный формат метки начала события'),
        ({'start_at' : '2024-11-30T09:15:00', 'end_at' : '_024-11-30T09:45:00'}, 'Некорректный формат метки завершения события'),
        ({'start_at' : '2024-06-30T09:15:00', 'end_at' : '2024-06-30T08:45:00'}, 'Начало события не может быть позже его окончания.'),
        ({'start_at' : '2024-11-30T09:15:00', 'end_at' : '2024-11-30T09:15:00'}, 'Событие не может иметь нулевую продолжительность.')
    ],
    ids = [
        'invalid start date format',
        'invalid end date format',
        'start date after end date',
        'zero duration event'
    ])

def test_event_create_with_invalid_time_period(create_kwargs, expected_error):
    """ параметризованный тест:
        проверка валидации временных меток при обновлении события """

    title       = 'title_test_event_create_with_invalid_time_period'
    description = 'description_test_event_create_with_invalid_time_period'
    start_at = create_kwargs['start_at']
    end_at   = create_kwargs['end_at']

    with pytest.raises(ValueError) as exc:
        Event.create(title = title, description = description, start_at = start_at, end_at = end_at)
    assert expected_error == str(exc.value)

@pytest.mark.parametrize('update_kwargs, expected_error', [
        ({'start_at' : '2024-16-30T09:15:00', 'end_at' : '2024-06-30T09:45:00'}, 'Некорректный формат метки начала события'),
        ({'start_at' : '2024-11-30T09:15:00', 'end_at' :  '024-11-30T09:45:00'}, 'Некорректный формат метки завершения события'),
        ({'start_at' : '2024-06-30T09:15:00', 'end_at' : '2024-06-30T08:45:00'}, 'Начало события не может быть позже его окончания.'),
        ({'start_at' : '2024-11-30T09:15:00', 'end_at' : '2024-11-30T09:15:00'}, 'Событие не может иметь нулевую продолжительность.')
    ],
    ids = [
        'invalid start date format',
        'invalid end date format',
        'start date after end date',
        'zero duration event'
    ])
def test_event_update_with_invalid_time_period(valid_event, update_kwargs, expected_error):
    """ параметризованный тест:
        проверка валидации временных меток при обновлении события """

    with pytest.raises(ValueError) as exc:
        valid_event.update(**update_kwargs)
    assert expected_error == str(exc.value)

def test_event_round_serialization(valid_event):
    event_to_dict = valid_event.to_dict()
    restored_event = Event.restore_from_dict(event_to_dict)
    assert restored_event == valid_event

