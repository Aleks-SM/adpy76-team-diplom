## О боте
Бот предлагает различные варианты для знакомств в социальной сети ВКонтакте в виде диалога с пользователем.

## Технические требования
На вашем ПК должен быть установлен:
1. Python 3.10, если нет необходимо установить с [офсайта](https://www.python.org/downloads/)
2. PostgreSQL ```sudo apt update && sudo apt install postgresql-12```
3. Создать БД в PostgreSQL, например 'testDb' введя команду в терминале ```sudo su - postgres -c "createdb testDb"```

   ![Схема БД](https://github.com/Aleks-SM/adpy76-team-diplom/raw/main/database/schema.png)
5. Установить командой необходимые библиотеки ```pip install -r requirements.txt```
5. Создать файл '.envrc' для переменных окружения командой 
    ```
    echo "export bd_name=<db_name>" > .envrc &&
    echo "export bd_username=<db_username>" >> .envrc &&
    echo "export bd_pass=<db_password>" >> .envrc &&
    echo "export bd_port=<db_port" >> .envrc &&
    echo "export bd=postgres" >> .envrc &&
    echo "export bd_host=<db_hoste>" >> .envrc &&
    echo "export vk_token=<token>" >> .envrc
    ``` 
   заполнив <...> данными
6. Добавить созданный файл переменных окружения в .gitignore ```echo ".envrc" >> .gitignore```
* команды приведены для ОС Ubuntu/Debian

## Возможности бота

1. Поиск по заданым критериям при регистрации в чате 
2. Добавлять пользователя в список друзей или в "чёрный" список нажав соответствующую кнопку меню
3. Показать список друзей