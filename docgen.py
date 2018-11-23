# -*- coding: utf-8 -*-

"""Doc gen module"""


import json
import logging

from typing import Dict
from pathlib import Path

import click


__version__ = '0.1.0'


LOG = logging.getLogger('docgen')


OUTPUT_PATH = Path('.')


@click.group()
@click.option('--debug/--no-debug', default=False,
              help='In debug mode all log messages are shown.')
@click.version_option(version=__version__)
def docgen(debug):
    """Simple script to create open api documentation"""
    log_level = (logging.DEBUG if debug else logging.INFO)
    logging.basicConfig(level=log_level, format='%(message)s')
    if debug:
        LOG.debug('Debug mode is on.')


@docgen.command()
@click.option('--name', '-n', prompt=True)
@click.option('--verb', '-v', prompt=True)
@click.option('--tags', '-t', prompt=True, help='List of space separated tags')
@click.option('--path', '-p', prompt=True)
@click.option('--summary', '-s', prompt=True)
@click.option('--responses', '-r', multiple=True)
def route(name: str, verb: str, tags: str, path: str, summary: str, responses) -> None: #pylint: disable=too-many-arguments
    """Creates the documentation for a route"""
    route_path = generate_route(name, verb, tags, path, summary, responses)
    generate_path(name, path, route_path)


def generate_path(name: str, path: str, route_path: Path) -> Path:
    """Generates json doc for paths"""
    paths: Dict[str, Dict] = {'paths': {}}
    filename = f'{name}-paths.json'
    file_path = OUTPUT_PATH / filename
    if file_path.exists():
        paths = load_json(file_path)

    paths['paths'][path] = path_block(route_path)
    save_json(file_path, paths)
    return file_path


def generate_route(name: str,  #pylint: disable=too-many-arguments
                   verb: str,
                   tags: str,
                   path: str,
                   summary: str,
                   responses) -> Path:
    """Generates json soc for route"""
    config: Dict[str, Dict] = {}
    filename = f'{name}.json'
    file_path = OUTPUT_PATH / filename
    if file_path.exists():
        config = load_json(file_path)

    config[verb] = verb_block(tags, path, summary)

    for res_code in responses:
        config[verb]['responses'][res_code] = response_block()

    save_json(file_path, config)
    return file_path


def path_block(file_path):
    """Gets a path block"""
    return  {'$ref': str(file_path)} #not correct file name


def verb_block(tags: str, path: str, summary: str) -> Dict:
    """Gets a verb block"""
    return {
        'tags': [
            tags
        ],
        'path': path,
        'summary': summary,
        'description': '',
        "parameters": [
            {
                '$ref': 'SET SCHEMA REF FOR THE PARAMETER OR DELETE'
            }
        ],
        'responses': {}
    }


def response_block() -> Dict:
    """Generates a reponse block"""
    return {
        'description': 'SET DESCRIPTION FOR THIS REPONSE',
        'content': {
            'application/json': {
                'schema': {
                    '$ref': 'SET SCHEMA REF FOR THE RESPONSE OR DELETE'
                }
            }
        }
    }


def load_json(filepath: Path) -> Dict:
    """Loads a json object from file"""
    with open(str(filepath), 'r') as file:
        return json.load(file)


def save_json(filepath: Path, payload: Dict) -> None:
    """Saves a payload to a file in JSON format"""
    with open(str(filepath), 'w') as file:
        json.dump(payload, file, indent=2, separators=(',', ': '))


if __name__ == '__main__':
    docgen()  # pylint: disable=no-value-for-parameter
