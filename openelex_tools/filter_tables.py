import logging
import os

import click
import pandas as pd

import openelex_tools.mappings as ms

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))


def filter_df(df):
    dfx = df[~pd.isnull(df.office)]
    dfx = dfx[~pd.isnull(dfx.party)]
    dfx = dfx[dfx.party != 'np']
    return dfx


@click.command()
@click.option('--source_file')
def main(source_file):
    df = pd.read_csv(source_file, infer_datetime_format=True)
    df = filter_df(df)
    df['party'] = df['party'].map(ms.PARTY_MAPPINGS)
    df['party'] = df[pd.isnull(df['party'])]
    # TODO: drop nulls
    base_file = os.path.splitext(source_file)[0]
    output_filename = '%s-filtered.csv' % base_file
    logging.debug('Writing to %s' % output_filename)
    df.to_csv(output_filename, index=False)


if __name__ == '__main__':
    main()
