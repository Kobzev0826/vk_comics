# VK Comics
**Что делает**:
-  Скачивает сомиксы с сайта [xkcd.com](https://xkcd.com/).
-  Загружает комиксы на стену VK сообщества.


**Запустить автоматическую загрузку комиксов**.\
Запустить файл `main.py`\
Скрипт ОДИН раз загрузит СЛУЧАЙНЫЙ комикс с сайта  [xkcd.com](https://xkcd.com/)\
__пример запуска__
```
python3 main.py
```

## Что понадобится

токен от API VK [Процедура Implicit Flow](https://vk.com/dev/implicit_flow_user)\
id сообщества
### Куда положить конфигурационные данные?
поместите необходимые данные в файл `.env` или создайте соответствующие переменные окружения
пример структуры `.env` файла
```
VK_TOKEN=
VK_COMMUNITY_ID=
```
## Как установить
Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```