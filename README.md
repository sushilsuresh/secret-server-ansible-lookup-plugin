# Thycotic Secret Server Ansible Lookup Plugin

This is a lookup plugin for Ansible that works with the Thycotic SDK Python package
to facilitate the connection to the Thycotic Secret Server

## Prerequisites

Python 2.7* and Python 3.*

Ansible 2.3.1 and later

Thycotic Secret Server Python package installed on Ansible Server environment.

Installing the Thycotic Secret Server Python package on Ansible Server

``` python
pip install secret-server-sdk-client
```

## Deployment

To deploy the lookup plugin, place the lookup python file 'thycotic_secret.py' to the
lookup folder based on your ansible configurations. Edit the 'thycotic_sdk_config.yml'
with the appropriate configurations for the sdk and place it in a directory where other
variable files are located within the environment.

When creating a playbook, make sure to include the 'thycotic_sdk_config.yml' variable file
in your play when the lookup plugin is being used. __The lookup plugin takes three variables:

- ```thycotic_config``` - name assigned to the 'thycotic_sdk_config.yml' reference
- ```secret``` - the secret id
- ```field``` - field slug name

For example,

``` yaml
  - hosts: localhost
    vars:
        contents: "{{ lookup('thycotic_secret', thycotic_config='thycotic', secret=4, field='password'") }}
    tasks:
      - include_vars:
            file: thycotic_sdk_config.yml
            name: thycotic
```

## Authors

Paulo Dorado

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Thycotic Secret Server Python Client

Thycotic SDK