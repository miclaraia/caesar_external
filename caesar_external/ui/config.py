

import click
import code
import os
from caesar_external.ui import ui
from caesar_external.data import Config
from caesar_external.extractor import Extractor
from caesar_external.reducer import Reducer


import logging
logging.basicConfig(level=logging.DEBUG)


@ui.cli.group()
def config():
    pass


@config.command()
@click.argument('name')
@click.argument('project', type=int)
@click.argument('workflow', type=int)
@click.option('--last_id', type=int)
@click.option('--caesar_name',
              help='Name used for swap as a reducer in caesar\'s configuration'
                   ', see https://zooniverse.github.io/caesar/#introduction '
                   'about setting up a reducer in caesar.')
@click.option('--sqs_queue')
@click.option('--staging', is_flag=True)
@click.option('--auth_mode', prompt='interactive,environment,api_key')
def new(name, project, workflow, last_id, caesar_name, sqs_queue,
        staging, auth_mode):

    kwargs = {
        'name': name,
        'project': project,
        'workflow': workflow,
        'last_id': last_id,
        'sqs_queue' : sqs_queue,
        'staging_mode' : staging,
    }

    if auth_mode == 'api_key':
        kwargs.update({
            'client_id': os.environ.get('PANOPTES_CLIENT_ID'),
            'client_secret': os.environ.get('PANOPTES_CLIENT_SECRET')
        })

    if caesar_name is not None:
        kwargs.update({'caesar_name': caesar_name})

    config = Config(**kwargs)
    config.save()


@config.command()
@click.argument('name')
def load(name):
    config = Config.load(name)

    code.interact(local={**globals(), **locals()})
