import logging

logger_new_change = logging.getLogger("Info")
logger_error = logging.getLogger("Error")

logger_new_change.setLevel(logging.INFO)
logger_error.setLevel(logging.ERROR)

new_ChangePat_handler = logging.FileHandler('good_log.txt', 'a', 'utf-8')
error_handler = logging.FileHandler('error_log.txt', 'a', 'utf-8')

new_ChangePat_format = logging.Formatter('%(levelname)s - %(message)s')
error_format = logging.Formatter('%(levelname)s - %(message)s')

new_ChangePat_handler.setFormatter(new_ChangePat_format)
error_handler.setFormatter(error_format)

logger_error.addHandler(error_handler)
logger_new_change.addHandler(new_ChangePat_handler)