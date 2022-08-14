import os

import click


__version__ = '1.0.1'


BASE_CONFIG_PATH = os.path.expanduser('~/.kha')
T_CONFIG_FILENAME = os.path.join(BASE_CONFIG_PATH, 't.json')


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()
