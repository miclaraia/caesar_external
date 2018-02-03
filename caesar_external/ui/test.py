

import click
import code
from caesar_external.ui import ui
from caesar_external.data import Config
from caesar_external.extractor import Extractor
from caesar_external.reducer import Reducer


@ui.cli.group()
def test():
    pass


@test.command()
@click.argument('name')
@click.argument('project', type=int)
@click.argument('workflow', type=int)
@click.argument('last_id', type=int)
@click.option('--caesar_name')
def new(name, project, workflow, last_id, caesar_name):
    config = Config(**{
        'name': name,
        'project': project,
        'workflow': workflow,
        'last_id': last_id,
        'caesar_name': caesar_name,
    })

    config.save()


@test.command()
@click.argument('name')
def load(name):
    config = Config.load(name)

    code.interact(local={**locals(), **globals()})
