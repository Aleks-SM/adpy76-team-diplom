## О боте
Бот предлагает различные варианты для знакомств в социальной сети ВКонтакте в виде диалога с пользователем.

## Технические требования
На вашем ПК должен быть установлен:
1. Python 3.9+, если нет необходимо установить с [офсайта](https://www.python.org/downloads/).
2. PostgreSQl ```sudo apt update && sudo apt install postgresql-12```
3. Создать БД в PostgreSQL, например 'testDb' введя команду в терминале ```sudo su - postgres -c "createdb testDb"```
4. 
4. Установить командой необходимые библиотеки ```pip install -r requirements.txt```
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
   заполнив <...> необходимыми данными
6. Добавить созданный файл переменных окружения в .gitignore ```echo ".envrc" >> .gitignore```
* команды приведены для ОС Ubuntu/Debian