# _Учебный проект "ca_practice" vers. 0.0.3_

### _Описание текущей версии:_
_V.0.0.3 настройка проекта, добавление конфигурационных файлов_

### _Структура проекта:_

```
project/
 ├───── app/
 │      └─ events/
 │         ├── domain/
 │         │   ├── value_objects.py
 │         │   ├── entities.py
 │         │   └── interfaces.py
 │         ├── application/
 │         │   └── use_cases.py
 │         ├── infrastructure/
 │         │   └── repositories.py
 │         └── api/
 │             ├── routes.py
 │             └── schemas.py
 │ 
 ├───── test/
 │      ├─── conftest.py
 │      └─── test_event_obj.py
 │  
 ├───── .github/
 │       └── workflows/
 │           └── python-app.yml  
 │ 
 ├───── .gitignore
 ├───── pytest.ini
 ├───── readme.md
 └───── requirements.txt


```
### _Реализуемые функции:_
1. _настроен github.workflow: запуск тестирования после комита в main_
2. _добавлены файлы requirements.txt, .gitignore, pytest.ini_
3. _актуализирована структура проекта_