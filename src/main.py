#!venv/bin/python3

from config import Config
from signal import signal, SIGINT, SIGTERM
from logging import Logger, getLogger, FileHandler, StreamHandler, Formatter, DEBUG

from midi.controller import Controller as MIDIController
from device.controller import Controller as DeviceController


def setup_logger() -> Logger:
    _logger = getLogger('inux')
    _logger.setLevel(DEBUG)
    formatter = Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler = FileHandler(filename='logs/inux.log', encoding='utf-8', mode='w')
    file_handler.setFormatter(formatter)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    _logger.addHandler(file_handler)
    _logger.addHandler(stream_handler)
    return _logger


def dismantle_logger(logger: Logger):
    handlers = logger.handlers.copy()
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('mode', choices=['device', 'midi'], help='Whether to run in Midi or Device Mode')
    parser.add_argument('-c', '--config', help='Filepath to config file', type=str, default='~/.config/Inux/config.ini')
    args = parser.parse_args()

    logger = setup_logger()

    config = Config(args.config, logger)

    if args.mode == 'device':
        device_controller = DeviceController(config, logger)
        try:
            print('Booting up..')
            device_controller.run()
        except KeyboardInterrupt:
            device_controller.stop()
        except Exception as e:
            logger.exception(e)
            device_controller.stop()
        finally:
            print('Shutting down..')
            dismantle_logger(logger)

    elif args.mode == 'midi':
        print('Currently not supported')
        # midi_controller = MIDIController(config, logger)
        # midi_controller.run()
        # midi_controller.stop()

