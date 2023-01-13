import logging
import sys

def init_logger(logger, logfile):
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')

#    stdout_handler = logging.StreamHandler(sys.stdout)
#    stdout_handler.setLevel(logging.DEBUG)
#    stdout_handler.setFormatter(formatter)
#    logger.addHandler(stdout_handler)

    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
