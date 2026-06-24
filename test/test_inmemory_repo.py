import pytest
from uuid import UUID

@pytest.mark.asyncio
async def test_inmemory_repository_get_event_valid_data(valid_event, inmemory_repo):
    """ добавить описание """
    await inmemory_repo.create_event_in_repo(valid_event)
    stored_event = await inmemory_repo.get_event_by_id(valid_event.id)
    assert stored_event == valid_event

@pytest.mark.asyncio
async def test_inmemory_repository_get_non_exist_event_in_repo(valid_event, inmemory_repo):
    """ добавить описание """
    await inmemory_repo.create_event_in_repo(valid_event)
    non_exist_id = UUID("00000000-0000-0000-0000-000000000000")
    non_exist_event = await inmemory_repo.get_event_by_id(non_exist_id)
    assert non_exist_event is None

@pytest.mark.asyncio
async def test_inmemory_repository_create_event_valid_data(valid_event, inmemory_repo):
    """ добавить описание """
    await inmemory_repo.create_event_in_repo(valid_event)
    stored_event = await inmemory_repo.get_event_by_id(valid_event.id)
    assert stored_event == valid_event

@pytest.mark.asyncio
async def test_inmemory_repository_create_event_duplicate_id(valid_event, inmemory_repo):
    """ добавить описание """
    await inmemory_repo.create_event_in_repo(valid_event)
    with pytest.raises(ValueError) as exc:
        await inmemory_repo.create_event_in_repo(valid_event)
    assert str(exc.value) == f'событие event.id = {valid_event.id} уже существует в репозитории, повторная запись запрещена'

@pytest.mark.asyncio
async def test_inmemory_repository_delete_event_valid_data(valid_event, inmemory_repo):
    await inmemory_repo.create_event_in_repo(valid_event)
    await inmemory_repo.delete_event_in_repo(valid_event.id)

    deleted_event = await inmemory_repo.get_event_by_id(valid_event.id)
    assert deleted_event is None

@pytest.mark.asyncio
async def test_inmemory_repository_delete_non_exist_event_in_repo(valid_event, inmemory_repo):
    non_exist_event = await inmemory_repo.delete_event_in_repo(valid_event.id)
    assert non_exist_event is None

@pytest.mark.asyncio
@pytest.mark.parametrize('update_kwargs', [
        {'title' : 'новый заголовок события'},
        {'description' : 'новое описание события'},
        {'title': 'повторная смена заголовка', 'description' : 'повторная правка описания события'}
    ],
    ids = [
        'event_inmemory_repo_update_title',
        'event_inmemory_repo_update_description',
        'event_inmemory_repo_update_all_attributes'
    ])

async def test_inmemory_repository_update_event_valid_attributes(valid_event, inmemory_repo, update_kwargs):
    """ обновления записи в репозитории с корректными данными """
    await inmemory_repo.create_event_in_repo(valid_event)
    await inmemory_repo.update_event_in_repo(valid_event, **update_kwargs)

    updated_event = await inmemory_repo.get_event_by_id(valid_event.id)

    assert valid_event.id == updated_event.id
    for key, value in update_kwargs.items():
        assert getattr(updated_event, key) == value

@pytest.mark.asyncio
@pytest.mark.parametrize('update_kwargs', [
        {'start_at' : '2004-06-30T09:15:00'},
        {'end_at'   : '2024-07-02T09:15:00'},
        {'start_at' : '2024-06-30T09:15:00', 'end_at' : '2024-07-15T09:15:00'},
    ],
    ids = [
        'event_inmemory_repo_update_time_period.start_at',
        'event_inmemory_repo_update_time_period.end_at',
        'event_inmemory_repo_update_time_period_all'
    ])

async def test_inmemory_repository_update_event_valid_time_period(valid_event, inmemory_repo, update_kwargs):
    await inmemory_repo.create_event_in_repo(valid_event)
    await inmemory_repo.update_event_in_repo(valid_event, **update_kwargs)

    expected_start_time = update_kwargs.get('start_at', valid_event.period.start_at.isoformat())
    expected_end_time   = update_kwargs.get('end_at',   valid_event.period.end_at.isoformat())

    updated_event = await inmemory_repo.get_event_by_id(valid_event.id)

    assert valid_event.id == updated_event.id
    assert updated_event.period.start_at.isoformat() == expected_start_time
    assert updated_event.period.end_at.isoformat()   == expected_end_time

@pytest.mark.asyncio
@pytest.mark.parametrize('update_kwargs', [
        {'title' : 'новый заголовок события'},
        {'description' : 'новое описание события'},
        {'title': 'повторная смена заголовка', 'description' : 'повторная правка описания события'}
    ],
    ids = [
        'event_inmemory_repo_update_title',
        'event_inmemory_repo_update_description',
        'event_inmemory_repo_update_all_attributes'
    ])

async def test_inmemory_repository_update_non_exist_event_in_repo(valid_event, inmemory_repo, update_kwargs):
    """ добавить описание """

    with pytest.raises(ValueError) as exc:
        await inmemory_repo.update_event_in_repo(valid_event, **update_kwargs)
    assert str(
        exc.value) == f'событие event.id = {valid_event.id} не найдено в репозитории'



