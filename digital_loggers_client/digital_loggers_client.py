# -*- coding: utf-8 -*-
import requests
import hashlib
import configparser
import os
from bs4 import BeautifulSoup

class DigitalLoggers():

    def __init__(self, config_file='~/.dl-power.ini'):
        config = configparser.ConfigParser()
        if '~/' in config_file:
            config_file = os.path.join(os.environ['HOME'], config_file.replace('~/',''))

        config.read(config_file)
        self.url = config['endpoint'].get('protocol','http') + '://' + config['endpoint'].get('fqdn')
        self.user = config['auth'].get('user')
        self.password = config['auth'].get('password')
        self.port_ids = list(range(1, int(config['hardware'].get('port_count', 8))))

    def _login(self):
        r = requests.get(self.url)
        b = BeautifulSoup(r.text, 'lxml')
        tags = b.find_all('input', attrs={'name': 'Challenge'})
        challenge_token = None
        security_token = None
        if not tags:
            raise RuntimeError('Could not get challenge key for power strip endpoint login')
        else:
            for tag in tags:
                if tag.get('value'):
                    challenge_token = tag.get('value')

        if not challenge_token:
            raise ReferenceError('Did not get challenge key.')
        else:
            login_password_raw = challenge_token + self.user + self.password + challenge_token
            m = hashlib.md5()
            m.update(login_password_raw.encode('utf-8'))
            login_password = m.hexdigest()
            l = requests.post(self.url + '/login.tgi', data={'Username': self.user, 'Password': login_password})
            if l.status_code == 200:
                security_token = l.cookies.get('DLILPC')
            else:
                raise RuntimeError('Cannot get DLILPC cookie value... Auth failed.')
        return security_token

    def _change_power_state(self, port_id, power_state='ON'):
        if power_state.upper() not in ['ON', 'OFF', 'CCL']:
            raise RuntimeError('Power State [' + power_state.upper() + '] is not an allowable value')
        elif port_id in self.port_ids or port_id.lower() == 'a':
            raise RuntimeError('Port id [' + port_id + '] not in range for the device configured')
        else:
            request_url = self.url + '/outlet?' + port_id + '=' + power_state.upper()
            security_token = self._login()
            r = requests.get(request_url, cookies={'DLILPC': security_token})
            print('Response code: [' + str(r.status_code) + ']')
            if r.status_code != 200:
                logger.error('Failed to perform ' + power_state + ' action on port ' + port_id)

    def on(self, port_id):
        return self._change_power_state(port_id, 'ON')

    def off(self, port_id):
        return self._change_power_state(port_id, 'OFF')

    def cycle(self, port_id):
        return self._change_power_state(port_id, 'CCL')
