import logging

logger = None

def init_logger():
    global logger
    logging.basicConfig(
        level="INFO", format='%(filename)s:%(funcName)s - %(message)s')
    return logging.getLogger()