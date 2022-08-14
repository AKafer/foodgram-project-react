![workflow](https://github.com/AKafer/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# FOODGRAM

### «Продуктовый помощник»: сайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

## Запустить проект локально:

### Клонировать репозиторий и перейти в папку backend:

```
git clone https://github.com/AKafer/foodgram-project-react.git
cd backend/
```

### Создать и активировать виртуальное окружение:

```
python -m venv venv
source venv/Scripts/activate
```

### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Перейти в папку foodgram и выполнить миграции:

```
cd foodgram/
python manage.py migrate
```

### Загрузить данные:

```
python manage.py loaddata dump.json
```

### Запустить проект

`python manage.py runserver`

## Запуск проекта на сервере:

### 1. На странице [https://github.com/AKafer/foodgram-project-reac]() сделать fork проекта в свой GitHUB;

### 2. В разделе проекта Setting/Secrets указать логин и пароль DockerHUB с ключами:

```
DOCKER_USERNAME, DOCKER_PASSWORD
```

### 3. В разделе проекта Setting/Secrets указать параметры (хост, логин, ssh-key, пароль ) DockerHUB с ключами:

```
HOST, USER, SSH_KEY, PASSPHRASE
```

### 4. В разделе проекта Setting/Secrets указать параметры базы данных с ключами:

```
DB_ENGINE, DB_NAME , POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT
```

### 5. В разделе проекта Setting/Secrets указать ID телеграм-канала и токен телеграм-бота для получения уведомлений с ключами:

```
TELEGRAM_TO, TELEGRAM_TOKEN
```

### 7. Подготовить сервер:

#### - Установить докер:

```
 sudo apt install docker.io 
```

#### - Установить docker-compose в соответствии с официальной документацией;

#### - Скопировать файлы docker-compose.yaml и nginx.conf из проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx.conf соответственно.

### 8. На GitHUB выполнить commit, после которого запустятся процедуры workflow;

### 9. На сервере выполнить миграции, импортировать данные, собрать статику:

```
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py loaddata dump2.json
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input

```

### 10. Набрать в браузере:

```
http://<ip_сервера>/
```

### Работоспособность приложения можно проверить без развертывания на уже запущенном сервере: http://51.250.17.147/

## Стек технологий

### Python 3, Django 2.2, Django REST framework, PostgreSQL, Djoser

## Автор проекта:

### Сергей Сторожук [https://github.com/AKafer]()
