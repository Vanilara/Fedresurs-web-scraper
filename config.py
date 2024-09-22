import os
from dotenv import load_dotenv

load_dotenv()

IS_DEBUG = os.getenv('DEBUG_MODE', 'False').lower() in ('true', '1', 't')

class BaseConfig:
    @property
    def track_url(self):
        return 'http://127.0.0.1:5001' if IS_DEBUG else os.getenv('SERVER_URL')

    @property
    def server_or_local(self):
        return 'LOCAL' if IS_DEBUG else 'SERVER'

class ConfigMaker(BaseConfig):
    IS_DEBUG = IS_DEBUG
    class Flask:
        ADMIN_KEY = os.getenv('FLASK_ADMIN_KEY')
        SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
        URL = f'{BaseConfig().track_url}'

    class Email:
        EMAIL_ADDR = os.getenv('EMAIL_ADDR')
        EMAIL_PASS = os.getenv('EMAIL_PASS')

    class FailsHandler:
        TOKEN = os.getenv('FAILS_BOT_TOKEN')
        GROUP = os.getenv('FAILS_GROUP')
        class Threads:
            ERROR = 1080

    class Cloud:
        TOKEN = os.getenv('CLOUD_TOKEN')

Config = ConfigMaker()