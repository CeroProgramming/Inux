from logging import Logger

LOGGER: Logger = None


def set_logger(logger: Logger):
    global LOGGER
    LOGGER = logger


def input_event(code: int, value: int):
    global LOGGER

    LOGGER.debug(f'code: {code} - value: {value}')
