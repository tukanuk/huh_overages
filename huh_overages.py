#!/usr/bin/env python3

import pandas as pd
import argparse

from pandas.io import parsers


def fileOpen(file):
    data = pd.read_csv(file)
    df = pd.DataFrame(
        data, columns=['Tenant UUID', 'Hour', 'Host Name', 'Host Units'])
    df = df.rename(columns={'Host Units': 'HHU'})

    # Drop the Summary Rows
    df = df.dropna()

    # Covert to date
    df['Hour'] = pd.to_datetime(df['Hour'], format='%Y-%m-%d %H:%M:%S')

    return df


def csvExport(df):
    # df = df.round({'Host Units': 0, 'Excess': 0})
    df['Excess'] = df['Excess'].astype(int)
    df['HHU'] = df['HHU'].astype(int)
    df.to_csv("~/Desktop/huh_data/hourly_hhu_total.csv", index=False)


# Commmand line args parsing
parser = argparse.ArgumentParser(
    description="Find when host units hours were consumed"
)
parser.add_argument("raw_data_file", nargs=1, metavar="<raw-data-file>")
parser.add_argument("-hu", "--hostunits", required=True,
                    help="The account host unit limit")
args = parser.parse_args()

rawDataFile = args.raw_data_file[0]
hostUnitLimit = args.hostunits

print()
print(rawDataFile)
print(type(rawDataFile))
print()

df = fileOpen(rawDataFile)

# Group by each hour
hourlyDF = df.groupby("Hour", as_index=False)['HHU'].sum()

# Add the excess column
hourlyDF['Excess'] = hourlyDF['HHU'] - int(hostUnitLimit)

# Remove 'negative excess'
hourlyDF.loc[hourlyDF['Excess'] <= 0, 'Excess'] = 0
print(hourlyDF)

# Sum
print(hourlyDF['Excess'].sum())

# Export
csvExport(hourlyDF)
