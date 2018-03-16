from dateutil.parser import parse as dateparse
from parse import parse
from recordclass import recordclass


import logging
import os
import yaml

import click
import pandas as pd

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))

Configuration = recordclass('Configuration', [
    'source_directory',
    'filter_string',
    'output',
    'skip_load',
])

Dataset = recordclass('Dataset', [
    'filename',
    'year',
    'date',
    'state',
    'data',
    'src_columns',
])


def line_to_dataset(filename):
    FMT = 'third_party/sources/openelections-data-{}/{}/{}__{}.csv'
    # Example:
    # third_party/sources/openelections-data-pa/2002/20021105__pa__general__precinct.csv
    parsed = parse(FMT, filename)
    return Dataset(
        filename=filename,
        state=parsed[0].upper(),
        year=int(parsed[1]),
        date=dateparse(parsed[2]),
        data=None,
        src_columns=[],
    )


def load_frame_for_dataset(dataset, skip_load):
    df = pd.read_csv(dataset.filename, infer_datetime_format=True)
    logging.debug('Loading %s with shape: %s' % (dataset.filename, df.shape))
    df.year = dataset.year
    df.date = dataset.date
    dataset.src_columns = df.columns.tolist()
    if not skip_load:
        dataset.data = df


def get_files(config):
    datasets = []
    for root, dirs, files in os.walk(config.source_directory, topdown=False):
        for name in files:
            if name.endswith('csv'):
                full_name = os.path.join(root, name)
                if config.filter_string and config.filter_string in name:
                    try:
                        dataset = line_to_dataset(full_name)
                        datasets.append(dataset)
                    except:
                        logging.error('Ignoring: %s' % full_name)
                    logging.debug('Adding: %s' % full_name)
                else:
                    logging.debug('Skipping: %s' % full_name)
    return datasets


@click.command()
@click.option('--source_directory')
@click.option('--filter_string', default='general__precinct')
@click.option('--output_file', default='state_results.yaml')
@click.option('--skip_load', is_flag=True, default=False)
def main(source_directory, filter_string, output_file, skip_load):
    config = Configuration(source_directory, filter_string, output_file, skip_load)
    datasets = sorted(get_files(config), key=lambda v: v.filename)
    logging.debug('Found %d datasets.' % len(datasets))
    logging.debug('Loading datasets.')
    for dataset in datasets:
        try:
            load_frame_for_dataset(dataset, config.skip_load)
        except:
            logging.error('Ignoring: %s' % dataset.filename)
    #
    with open(output_file, 'w+') as f:
        logging.debug('Writing to %s.' % output_file)
        metadata = [dict(dat._asdict()) for dat in datasets]
        f.write(yaml.safe_dump({'states': metadata}))



if __name__ == '__main__':
    main()
