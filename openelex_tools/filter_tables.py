import logging
import os

import click
import pandas as pd

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))


def filter_df(df):
    dfx = df[~pd.isnull(df.office)]
    dfx = dfx[~pd.isnull(dfx.party)]
    dfx = dfx[dfx.party != 'np']
    return dfx


@click.command()
@click.option('--source_file')
def main(source_file):
    pass


if __name__ == '__main__':
    main()
