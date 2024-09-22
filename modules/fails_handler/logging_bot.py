from aiogram import Bot
import asyncio, logging
from functools import wraps
from config import Config


class TelegramLoggingHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        thread_id = self.get_thread_id(record.levelno)
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError as e:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        if loop.is_running():
            asyncio.run_coroutine_threadsafe(self.send_message(log_entry, thread_id), loop)
        else:
            loop.run_until_complete(self.send_message(log_entry, thread_id))
            
    def get_thread_id(self, levelno):
        if levelno == logging.CRITICAL:
            return Config.FailsHandler.Threads.CRITICAL
        elif levelno == logging.ERROR:
            return Config.FailsHandler.Threads.ERROR
        elif levelno == logging.WARNING:
            return Config.FailsHandler.Threads.WARNING
        elif levelno == logging.INFO:
            return Config.FailsHandler.Threads.INFO

    async def send_message(self, log, thread_id):
        bot = Bot(token=Config.FailsHandler.TOKEN)
        await bot.send_message(chat_id = Config.FailsHandler.GROUP, text=log, message_thread_id = thread_id)
        await bot.session.close()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(TelegramLoggingHandler())

# to_send_fails = Config.IS_DEBUG
to_send_fails = False


def error_handler_flask(request, level="error"):
    def decorator_errors(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if to_send_fails:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    log_message = (f"Flask Error: {str(e)}\n"
                                f"Path: {request.path}\n"
                                f"Method: {request.method}\n"
                                f"IP: {request.remote_addr}\n"
                                f"Query Params: {request.args}\n"  # Query parameters
                                f"Form Data: {request.form}\n"  # Form data (for POST requests)
                                f"JSON Body: {request.get_json(silent=True)}\n\n")
                    if level == 'error':
                        logger.error(log_message, exc_info=True)
                    elif level == 'critical':
                        logger.critical(log_message, exc_info=True)
                    return 'fail'
            else:
                return func(*args, **kwargs)
        return decorated_function
    return decorator_errors

def error_handler_aiogram(context_name='message', level="error"):
    def decorator_errors(func):
        async def decorated_function(*args, **kwargs):
            context = args[0] if args else kwargs.get(context_name)
            if to_send_fails:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    log_message = f"Aiogram {context_name} error: {str(e)}\n{str(context)}"
                    if level == 'error':
                        logger.error(log_message, exc_info=True)
                    elif level == 'critical':
                        logger.critical(log_message, exc_info=True)
                    if context_name == 'message':
                        await context.answer('Произошла ошибка, попробуйте позже')
            else:
                return await func(*args, **kwargs)
        return decorated_function
    return decorator_errors

def error_send_func(e=None, info_message=None, level = "error"):
    log_message = f'Common {level}: {info_message}\n{str(e)}'
    if to_send_fails:
        if level == 'critical':
            logger.critical(log_message, exc_info=True)
        elif level == 'error':
            logger.error(log_message, exc_info=True)
        elif level == 'warning':
            logger.warning(log_message, exc_info=True)
        elif level == 'info':
            logger.info(info_message)
    return 'fail'