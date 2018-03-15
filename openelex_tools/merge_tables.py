from collections import namedtuple

import logging
import os

import click
import pandas as pd

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))

Configuration = namedtuple('Configuration', ['source_directory, filter_string', 'output', ])

def get_files(config):
    pass

@click.command()
@click.option('--source_directory')
@click.option('--filter_string', default='general')
@click.option('--output', default='stdout')
def main(source_directory, output):
    filenames = []
    for root, dirs, files in os.walk(source_directory, topdown=False):
        for name in files:
            if name.endswith('csv'):
                full_name = os.path.join(root, name)
                logging.debug(full_name)

if __name__ == '__main__':
    main()
