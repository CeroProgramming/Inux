from argparse import ArgumentParser


class Arguments(object):

    def __init__(self):
        self._parser = ArgumentParser(description='Linux Multiple Keyboard Input Controller')
        self._parser.add_argument('--config', type=str, help='Pass the config file. Required!')
        self._args = self._parser.parse_args()

    def get_config_fp(self) -> str:
        return vars(self._args)['config']
