# -*- coding: utf-8 -*-
import requests
import hashlib
import configparser
import os
from bs4 import BeautifulSoup
import logging
import json

class DigitalLoggers():

    def __init__(self, profile=None, config_file='~/.dl-power.ini'):
        self.logger = logging.getLogger('digital_loggers_client.DigitalLoggers')
        self.logger.debug('Initializing DigitalLoggers client class.')
        self.config_keys = ['protocol', 'fqdn', 'user', 'password', 'port_count']
        self.config_data = {}
        self.get_config_info(profile, config_file)
        self.logger.info('DigitalLoggers client initialized.')

    def get_config_info(self, profile=None, config_file='~/.dl-power.ini'):
        self.logger.debug('Getting config data for profile [' + profile if profile else 'NoneType' + '] in config file located at [' + config_file + ']')
        config = self._get_configparser(config_file)
        if len(config.sections()) > 0:
            if not profile:
                if 'global' in config.sections():
                    profile = config['global'].get('default_profile')
                else:
                    profile = 'default'
            full_profile_name = 'profile:' + profile
            if full_profile_name in config.sections():
                for key in self.config_keys:
                    if key in list(config[full_profile_name].keys()):
                        self.logger.debug('Setting key [' + key + '] to value [' + config[full_profile_name][key] + '] from configuration file.')
                        self.config_data[key] = config[full_profile_name][key]
                    else:
                        self.logger.warn('No such key [' + key + '] available in the configuration file [' + config_file + '] for profile [' + profile + '].')
            else:
                self.logger.warn('Cannot find profile [' + profile + '] within config file [' + config_file + '].')
        for key in self.config_keys:
            if 'DL_' + key.upper() in list(os.environ.keys()):
                self.logger.debug('Setting key [' + key + '] to value [' + os.getenv('DL_' + key.upper()) + '] from environment variable.')
                self.config_data[key] = os.getenv('DL_' + key.upper())
        self.logger.debug('Configuration data loaded [' + json.dumps(self.config_data) + '].')
        missing_keys = []

        # check for valid config
        for key in self.config_keys:
            if not self.config_data.get(key):
                missing_keys.append(key)
        if len(missing_keys) > 0:
            err_message ='The following configuration keys were not detected via config file or environment variables [' + ','.join([str(x) for x in missing_keys]) + ']'
            self.logger.error(err_message)
            raise RuntimeError(err_message)

    def set_config_info(self, protocol, fqdn, user, password, port_count=8, profile='default', config_file='~/dl-power.ini'):
        config = self._get_configparser(config_file)
        config[profile] = {
            'protocol': protocol,
            'fqdn': fqdn,
            'user': user,
            'password': password,
            'port_count': port_count
        }
        self.logger.debug('Writing config file to [' + config_file + ']')
        with open(config_file, 'w') as configfile:
            config.write(configfile)

    def _get_configparser(self, config_file):
        self.logger.debug('Getting config parser for file [' + config_file + ']')
        config = configparser.ConfigParser()
        if '~/' in config_file:
            config_file = os.path.join(os.environ['HOME'], config_file.replace('~/',''))
        config.read(config_file)
        return config

    def _get_url(self):
        self.logger.debug('Formatting request URL for device.')
        if 'fqdn' not in self.config_data:
            raise RuntimeError('Cannot get API URL for requests - FQDN value not set.')
        return self.config_data.get('protocol', 'http') + '://' + self.config_data.get('fqdn')

    def _get_port_ids(self, default_capacity=8):
        return list(range(1,int(self.config_data.get('port_count', default_capacity))))

    def _get_challenge_token(self):
        r = requests.get(self._get_url())
        b = BeautifulSoup(r.text, 'lxml')
        tags = b.find_all('input', attrs={'name': 'Challenge'})
        if not tags:
            raise RuntimeError('Could not get challenge key for DLI endpoint login')
        elif len(tags) == 1:
            return tags[0].get('value')
        else:
            raise ReferenceError('More than one instance of a challenge key found in the login page response.')

    def _login(self):
        challenge_token = self._get_challenge_token()
        login_password_raw = challenge_token + self.config_data.get('user') + self.config_data.get('password') + challenge_token
        m = hashlib.md5()
        m.update(login_password_raw.encode('utf-8'))
        login_password = m.hexdigest()
        l = requests.post(self._get_url() + '/login.tgi', data={'Username': self.config_data.get('user'), 'Password': login_password})
        if l.status_code == 200:
            security_token = l.cookies.get('DLILPC')
            self.logger.debug('Received security token: [' + security_token + ']')
        else:
            raise RuntimeError('Cannot get DLILPC cookie value... Auth failed.')
        return security_token

    def _change_power_state(self, port_id, power_state='ON'):
        if power_state.upper() not in ['ON', 'OFF', 'CCL']:
            raise RuntimeError('Power State [' + power_state.upper() + '] is not an allowable value ')
        elif port_id in self._get_port_ids(self.config_data.get('port_count', 8)) or port_id.lower() == 'a':
            raise RuntimeError('Port id [' + port_id + '] not in range for the device configured')
        else:
            request_url = self._get_url() + '/outlet?' + port_id + '=' + power_state.upper()
            security_token = self._login()
            r = requests.get(request_url, cookies={'DLILPC': security_token})
            print('Response code: [' + str(r.status_code) + ']')
            if r.status_code != 200:
                self.logger.error('Failed to perform ' + power_state + ' action on port ' + port_id)
                return False
            else:
                self.logger.info('Successfully changed state of port [' + port_id + '] to [' + power_state + '].')
                return True

    def on(self, port_id):
        self.logger.info('Turning port [' + port_id+ '] on.')
        return self._change_power_state(port_id, 'ON')

    def off(self, port_id):
        self.logger.info('Turning port [' + port_id  + '] off.')
        return self._change_power_state(port_id, 'OFF')

    def cycle(self, port_id):
        self.logger.info('Cycling port [' + port_id + '].')
        return self._change_power_state(port_id, 'CCL')
