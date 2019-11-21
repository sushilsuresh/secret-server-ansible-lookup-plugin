# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
        lookup: thycotic_sdk
        author: Paulo Dorado <pdorado@tsiva.com>
        version_added: "1.0"
        short_description: Look up secrets from Thycoptic Secret Server
        description:
          - This lookup uses the Thycotic SDK python library to lookup
            secrets from a Thycotic Secret Server
        notes:
          - This module expects the the sdk client which includes the files
            'tss' and relevant *.dll files to be present in the path specifed
            in variable 'sdk_client_path'. This is in addition to installting
            the python module - secret-server-sdk-client
"""

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils._text import to_text
from ansible.plugins.lookup import LookupBase

from secret_server.sdk_client import SDK_Client

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        config_dict = variables[kwargs['thycotic_config']]
        result = []

        client = SDK_Client()
        client.configure(config_dict['sdk_client_path'],
                         config_dict['secret_server_url'],
                         config_dict['sdk_client_rule'],
                         config_dict['sdk_client_key'])

        if config_dict['config_reset']:
            display.vvvv(client.commands.remove())

        display.vvvv(client.commands.initialize())

        try:
            cache_result = ''
            if config_dict['sdk_cache_strategy'] == 0:
                cache_result = client.set_cache(config_dict['sdk_cache_strategy'])
            else:
                cache_result = client.set_cache(config_dict['sdk_cache_strategy'], config_dict['sdk_cache_age'])

            display.vvvv(cache_result)
        except KeyError as e:
            if e.args[0] == 'sdk_cache_age':
                KeyError('If cache age is invalid or missing')

        if(config_dict['sdk_cache_clear']):
            client.commands.clear_cache()

        result.append(to_text(client.commands.get_secret(kwargs['secret'], field=kwargs['field'])))

        return result
