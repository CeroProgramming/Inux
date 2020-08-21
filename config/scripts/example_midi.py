from pygame.midi import Output


def execute(output_device: Output, a: int, b: int, c: int, d: int):
    print('%s : %s : %s : %s' % (a, b, c, d))
