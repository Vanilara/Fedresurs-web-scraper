# Fedresurs-web-scraper

The project consists of two components:
1. An hourly parser on the fedresurs.ru website to detect new bankruptcy announcements for individual entrepreneurs and companies.
2. A web interface built with Flask, featuring a CloudPayments payment system for monetizing collected data.

## Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Technologies](#technologies)

## Installation

To clone the repository and install dependencies, run the following commands:

```bash
git clone https://github.com/Vanilara/Fedresurs-web-parser.git
cd Fedresurs-web-parser
pip install -r requirements.txt
python3 remake_database.py
python3 -m flask run --debug --port=5001
```

Add the following line to the crontab file to run `parse.py` hourly:

```bash
0 * * * * python3 /path/to/Fedresurs-web-parser/parse.py
```

## Usage
Before registration, users will see a demo layout of the interface. After logging in, they will access a dashboard where they can purchase collected data using their balance. User information can be found at /admin.

## Configuration

Before running the project, you need to set up the `.env` file. Example configuration file:

# .env
```
DEBUG_MODE=True/False
SERVER_URL=For debug mode when DEBUG_MODE=False (https://example.com)
EMAIL_ADDR=Gmail address to send verification codes
EMAIL_PASS=Gmail app password
FLASK_ADMIN_KEY=Key to access /admin
FLASK_SECRET_KEY=Flask session secret key
FAILS_BOT_TOKEN=Bot token for Telegram notifications about failures
FAILS_GROUP=Group ID for Telegram notifications about failures
CLOUD_TOKEN=CloudPayments account ID
```

## Technologies
* Python 3.10
* Flask 3.x
* Aiogram 4.x
* Aiohttp
* Pandas
* Openpyxl
* Numpy
* Python-dotenv
* Gunicorn