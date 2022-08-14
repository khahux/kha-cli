import os
import json

import click

from kha import print_version
from kha.scripts.translate import translate
from kha.utils.file_utils import exists, mkdirs


BASE_CONFIG_PATH = os.path.expanduser('~/.kha')
T_CONFIG_FILENAME = os.path.join(BASE_CONFIG_PATH, 't.json')
CONTEXT_SETTINGS = dict(
    default_map={
        't': {'key': 0, 'keyfrom': ''},
    }
)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug/--no-debug', default=False)
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug

    if not exists(BASE_CONFIG_PATH):
        mkdirs(BASE_CONFIG_PATH, all_dir=True)

    # read t config
    if exists(T_CONFIG_FILENAME):
        with open(T_CONFIG_FILENAME) as t_config:
            ctx.obj['t'] = json.load(t_config)

    @ctx.call_on_close
    def close():
        pass


@cli.command()
@click.option('--string', default='world')
@click.pass_context
def greet(ctx, string):
    click.echo(f'🦄 hello, {string}.')
    click.echo(json.dumps(ctx.obj, indent=2))


@cli.command()
@click.argument('text', nargs=-1, type=str)
@click.option('--key', type=int)
@click.option('--keyfrom', type=str)
@click.pass_context
def t(ctx, text, key, keyfrom):
    if key and keyfrom:
        with open(T_CONFIG_FILENAME, 'w') as config:
            json.dump(
                {'key': key, 'keyfrom': keyfrom}, config, sort_keys=True, indent=2)
            return

    click.echo()
    if ctx.obj.get('t') and isinstance(ctx.obj.get('t'), dict):
        key = ctx.obj.get('t').get('key')
        keyfrom = ctx.obj.get('t').get('keyfrom')
    translate(' '.join(text), keyfrom, key)
    click.echo()

@cli.command()
@click.pass_context
def ssh(ctx):
    click.echo('ssh')


if __name__ == '__main__':
    cli()
