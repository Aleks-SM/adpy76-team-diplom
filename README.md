## О боте
Бот предлагает различные варианты для знакомств в социальной сети ВКонтакте в виде диалога с пользователем.

## Технические требования
На вашем ПК должен быть установлен:
1. Python 3.10, если нет необходимо установить с [офсайта](https://www.python.org/downloads/)
2. PostgreSQL ```sudo apt update && sudo apt install postgresql-14```

<details>
   <summary>Схема БД</summary>
   
   ![Схема БД](https://github.com/Aleks-SM/adpy76-team-diplom/raw/main/database/schema.png)
</details>

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
   заполнив <...> данными
6. Добавить созданный файл переменных окружения в .gitignore ```echo ".envrc" > .gitignore```
* _команды приведены для ОС Ubuntu/Debian_

## Возможности бота

1. Используя информацию (возраст, пол, город) о пользователе, который общается с ботом в ВКонтакте, осуществляет поиск других пользователей ВКонтакте для знакомств.
2. У тех людей, которые подошли под критерии поиска, получает три самые популярные фотографии в профиле по количеству лайков.
3. Выводит в чат с ботом информацию о найденных пользователях в формате:
```
- имя и фамилия,
- ссылка на профиль,
- три фотографии
```
4. Перейти к следующему человеку с помощью кнопки.
5. Сохранить пользователя в список избранных.
6. Вывести список избранных людей.
7. Добавлять человека в чёрный список
8. К списку фотографий из аватарок добавляет список фотографий, где отмечен пользователь.

## Запуск бота
```python
python main.py
```