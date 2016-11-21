# -*- coding: utf-8 -*-

import click
from .digital_loggers_client import DigitalLoggers

@click.command()
@click.argument('port_id')
@click.argument('action')
@click.option('--profile', default='default', help='Name of the profile (ini file section header) to use for configuration data.')
@click.option('--config_file', default='~/.dl-client.ini', help='Location of the config ini file for interacting with the Digital Loggers Web Power Switch.')
def main(port_id, action, profile, config_file):
    """Console script for digital_loggers_client"""
    click.echo("Running action [" + action  + "] on port [" + port_id + "]")
    dl = DigitalLoggers(profile=profile, config_file=config_file)
    if action.lower() == 'on':
        dl.on(port_id)
    elif action.lower() == 'off':
        dl.off(port_id)
    elif action.lower() == 'cycle':
        dl.cycle(port_id)
    else:
        raise Exception('Action [' + action + '] not supported')

@click.command()
@click.option('--protocol', default='http', prompt='Enter protocol to access device [http/https]', help='Protocol to use when accessing Digital Loggers web interface.')
@click.option('--fqdn', prompt='Enter FQDN or IP address to access device', help='Fully qualified domain name or ip address to use when accessing the Digital Loggers web interface.')
@click.option('--user', prompt='Enter user for device login', help='Uername to use when accessing the Digital Loggers web interface.')
@click.option('--password', prompt='Enter password for device login', help='Password to use when accessing the Digital Loggers web interface.')
@click.option('--port_count', prompt='Enter number of switchable ports on device', default=8, help='Nuber of switchable ports on the Digital Loggers power device')
@click.option('--profile', default='default', help='Name of the profile (ini file section header) to use for configuration data.')
@click.option('--config_file', default='~/.dl-client.ini', help='Location of the config ini file for interacting with the Digital Loggers Web Power Switch.')
def config(protocol, fqdn, user, password, port_count, profile, config_file):
    click.echo('Updating configuration file at [' + config_file + '] to add configuration data to profile [' + profile + '].')
    dl = DigitalLoggers(profile=profile, config_file=config_file)
    dl.set_config_info(protocol, fqdn, user, password, port_count, profile, config_file)
    click.echo('Configuration profile [' + profile + '] updated.')

@click.command()
@click.option('--protocol', default='http', prompt='Enter protocol to access device [http/https]', help='Protocol to use when accessing Digital Loggers web interface.')
@click.option('--fqdn', prompt='Enter FQDN or IP address to access device', help='Fully qualified domain name or ip address to use when accessing the Digital Loggers web interface.')
@click.option('--user', prompt='Enter user for device login', help='Uername to use when accessing the Digital Loggers web interface.')
@click.option('--password', prompt='Enter password for device login', help='Password to use when accessing the Digital Loggers web interface.')
@click.option('--port', prompt='Enter the port number to query for status', help='Port number to query for status.')
@click.option('--profile', default='default', help='Name of the profile (ini file section header) to use for configuration data.')
@click.option('--config_file', default='~/.dl-client.ini', help='Location of the config ini file for interacting with the Digital Loggers Web Power Switch.')
def status(protocol, fqdn, user, password, port, profile, config_file):
    click.echo('Getting status for port [' + port + ']')
    dl = DigitalLoggers(profile=profile, config_file=config_file)
    click.echo('Status: ' + dl.get_status(port))

if __name__ == "__main__":
    main()
