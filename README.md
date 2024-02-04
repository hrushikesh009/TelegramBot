# Bot for Yo-Mama Jokes

## Introduction

This bot shares Yo-Mama jokes, inspired by [this tutorial](https://github.com/abhay1/django-facebook-messenger-bot-tutorial). 

## Requirements

- Python 3.0
- Ensure pip is installed (`pip --version`)
- Install virtual environment: `pip install virtualenv`
- Telegram messenger (or web version at [web.telegram.org](https://web.telegram.org))

## Setup Steps

### Step 0: Clone the Repository

```sh
git clone https://github.com/hrushikesh009/TelegramBot.git
```

### Step 1: Install Dependencies

```sh
pip install -r requirements.txt
```

### Step 2: Database Setup

Utilized MySQL Database in this tutorial. Modify settings in `Telegram_Bot.settings`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Your Database Name',
        'HOST': 'localhost',
        'USER': 'Database Username',
        'PASSWORD': 'Database Password',
        'PORT': 'Database Port'
    }
}
```

Refer to [this link](https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8) for PostgreSQL setup.

### Step 3: Run Migrations

```sh
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Start the Local Server

```sh
python manage.py runserver
```

### Step 5: Download and Use Ngrok

For HTTPS URL during development, use [ngrok](https://ngrok.com/):

```sh
ngrok http 8000
```

Add the URLs to ALLOWED_HOSTS in `Telegram_Bot.settings`.

### Step 6: Set Your Bot Token

Talk to BotFather on Telegram (`/newbot` command) to create a bot and get a token. Copy and paste the token in `FunBot/views.py`.

### Step 7: Set Webhook

Run the following command or use services like Postman:

```sh
curl -F “url=<ngrok_url>/chat/c817304a3d163ebd58b44dd446eba29572300724098cdbca1a/“ https://api.telegram.org/bot<bot_token>/setWebhook
```

### Step 8: Talk to the Bot

Initiate a conversation and receive responses from the bot.

### Step 9: Capture the ClickStream

Visit `<ngrok_url>/chat/home/` to view user interactions and data captured in the database.