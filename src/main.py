#!venv/bin/python3

from config import Config
from arguments import Arguments
from logging import getLogger, FileHandler, StreamHandler, Formatter, DEBUG

from midi.controller import Controller as MIDIController
from keyboard.controller import Controller as KeyboardController

logger = getLogger('inux')
logger.setLevel(DEBUG)
formatter = Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
file_handler = FileHandler(filename='logs/inux.log', encoding='utf-8', mode='w')
file_handler.setFormatter(formatter)
stream_handler = StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

args = Arguments()

try:
    config = Config(args.get_config_fp(), logger)

    # midi_controller = MIDIController(config, logger)
    keyboard_controller = KeyboardController(config, logger)
except KeyboardInterrupt:
    stream_handler.close()
    file_handler.close()
    logger.removeHandler(stream_handler)
    logger.removeHandler(file_handler)
