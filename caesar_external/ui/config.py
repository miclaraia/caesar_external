

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
@click.option('--last_id', type=int,
              help='Exclude classifications before this classification id.')
@click.option('--caesar_name',
              help='Name used for swap as a reducer in caesar\'s configuration'
                   ', see https://zooniverse.github.io/caesar/#introduction '
                   'about setting up a reducer in caesar.')
@click.option('--sqs_queue',
              help='Specify whether caesar should subscribe to an SQS '
                   'queue for classifications. If left blank will default '
                   'to panoptes api as classification source.')
@click.option('--staging', is_flag=True,
              help='Flag to use staging endpoints for panoptes and caesar')
@click.option('--auth_mode',
              help='interactive,environment,api_key\n'
                   'If api_key is selected, make sure client id and client '
                   'secret are stored in environment variables in '
                   'PANOPTES_CLIENT_ID and PANOPTES_CLIENT_SECRET')
def new(name, project, workflow, last_id, caesar_name, sqs_queue,
        staging, auth_mode):
    """
    Generate new configuration for a project.

    \b
    Arguments
    ---------
    name - Arbitrary name used to store configuration
    project - Zooniverse project id
    workflow - Zooniverse workflow id
    """

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
