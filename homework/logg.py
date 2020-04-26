import logging

logger_new_change = logging.getLogger("Info")
logger_error = logging.getLogger("Error")

logger_new_change.setLevel(logging.INFO)
logger_error.setLevel(logging.ERROR)

New_ChangePat_handler = logging.FileHandler('good_log.txt', 'a', 'utf-8')
Error_handler = logging.FileHandler('error_log.txt', 'a', 'utf-8')

New_ChangePat_format = logging.Formatter('%(levelname)s - %(message)s')
Error_format = logging.Formatter('%(levelname)s - %(message)s')

New_ChangePat_handler.setFormatter(New_ChangePat_format)
Error_handler.setFormatter(Error_format)

logger_error.addHandler(Error_handler)
logger_new_change.addHandler(New_ChangePat_handler)