#!/usr/bin/env python3

from os.path import isdir
import pandas as pd
import argparse
# import datetime
import os

# from pandas.io import parsers


def fileOpen(filePath, fileList):
    """ Opens a file or directory of .csv files """
    df = pd.DataFrame()
    for item in fileList:
        data = pd.read_csv(f"{filePath}/{item}")
        df2 = pd.DataFrame(
            data, columns=['Tenant UUID', 'Hour', 'Host Name', 'Host Units'])
        df = df.append(df2, ignore_index=True)

    df = df.rename(columns={'Host Units': 'HHU'})

    # Drop the Summary Rows
    df = df.dropna()

    # Covert to date
    df['Hour'] = pd.to_datetime(df['Hour'], format='%Y-%m-%d %H:%M:%S')

    return df


def csvExport(filePath, df):
    """ CSV Export & some summary statistics"""
    startDate = df['Hour'][0].strftime("%Y-%m-%d")
    endDate = df['Hour'].iloc[-1].strftime("%Y-%m-%d")
    print(f"From: {startDate} to {endDate}")
    # df['Excess'] = df['Excess'].astype(int)
    df['HHU'] = df['HHU'].astype(int)
    # if os.path.isdir(f"{filePath}/results") == False:
    os.makedirs(f"{filePath}/results", exist_ok=True)
    df.to_csv(
        f"{filePath}/results/hourly_hhu_{startDate}_to_{endDate}.csv", index=False)


# Commmand line args parsing
parser = argparse.ArgumentParser(
    description="Find when host units hours were consumed"
)
parser.add_argument("raw_data_file_or_folder", nargs=1, metavar="<raw-data-file>",
                    help="Include a .csv of a folder containing .csv")
parser.add_argument("-hu", "--hostunits", required=True,
                    help="The account host unit limit")
args = parser.parse_args()


filePath = args.raw_data_file_or_folder[0]
fileList = []


# builds a list of the files to be processed
if os.path.isfile(filePath):
    filePath, fileName = os.path.split(filePath)
    fileList = [fileName]
elif os.path.isdir(filePath):
    print("Adding all .csv files in directory")
    with os.scandir(filePath) as dirs:
        for entry in dirs:
            if entry.name.endswith(".csv"):
                # print(entry.name)
                fileList.append(entry.name)
    # print(fileList)
else:
    raise Exception("Couldn't find a valid file from the path provided")

hostUnitLimit = args.hostunits

print()
print(filePath)
print(fileList)
print()

df = fileOpen(filePath, fileList)

# Group by each hour
hourlyDF = df.groupby("Hour", as_index=False)['HHU'].sum()

# Add the excess column
hourlyDF['Excess'] = hourlyDF['HHU'] - int(hostUnitLimit)

# Remove 'negative excess'
hourlyDF.loc[hourlyDF['Excess'] <= 0, 'Excess'] = 0
print(hourlyDF)

# Sum
print(f"Total excess host unit hours: {hourlyDF['Excess'].sum():.0f}")

# Export
csvExport(filePath, hourlyDF)
