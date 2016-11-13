# -*- coding: utf-8 -*-

import click
from .digital_loggers_client import DigitalLoggers

@click.command()
@click.argument('port_id')
@click.argument('action')
@click.option('--config_file', default='~/.dl-power.ini', help='Location of the config ini file for interacting with the Digital Loggers Web Power Switch')
def main(port_id, action, config_file):
    """Console script for digital_loggers_client"""
    click.echo("Running action [" + action  + "] on port [" + port_id + "]")
    dl = DigitalLoggers(config_file=config_file)
    if action.lower() == 'on':
        dl.on(port_id)
    elif action.lower() == 'off':
        dl.off(port_id)
    elif action.lower() == 'cycle':
        dl.cycle(port_id)
    else:
        raise Exception('Action [' + action + '] not supported')

if __name__ == "__main__":
    main()
