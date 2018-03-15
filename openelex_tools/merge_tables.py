from collections import namedtuple

import logging
import os

import click
import pandas as pd

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))

Configuration = namedtuple('Configuration', [
    'source_directory',
    'filter_string',
    'output',
])


def get_files(config):
    names = []
    for root, dirs, files in os.walk(config.source_directory, topdown=False):
        for name in files:
            if name.endswith('csv'):
                full_name = os.path.join(root, name)
                if config.filter_string and config.filter_string in name:
                    names.append(full_name)
                    logging.debug('Adding: %s' % full_name)
                else:
                    logging.debug('Skipping: %s' % full_name)
    return names


def read_frame(filename):
    return pd.read_csv(filename, infer_datetime_format=True)


def is_ok(frame):
    return True


@click.command()
@click.option('--source_directory')
@click.option('--filter_string', default='general__precinct')
@click.option('--output', default='stdout')
def main(source_directory, filter_string, output):
    config = Configuration(source_directory, filter_string, output)
    filenames = get_files(config)


if __name__ == '__main__':
    main()
