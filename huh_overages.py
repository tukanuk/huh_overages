import pandas as pd


def fileOpen():
    data = pd.read_csv(r"~/Desktop/huh_data/raw-data.csv")
    df = pd.DataFrame(
        data, columns=['Tenant UUID', 'Hour', 'Host Name', 'Host Units'])
    df = df.rename(columns={'Host Units': 'HHU'})
    # print(df)
    # print("Info")
    # df.info()

    # Drop the Summary Rows
    # print("Drop NaN")
    df = df.dropna()

    # Covert to datea
    # print("Convert date")
    df['Hour'] = pd.to_datetime(df['Hour'], format='%Y-%m-%d %H:%M:%S')
    # df.info()
    # print(df)

    return df


def csvExport(df):
    # df = df.round({'Host Units': 0, 'Excess': 0})
    df['Excess'] = df['Excess'].astype(int)
    df['HHU'] = df['HHU'].astype(int)
    df.to_csv("~/Desktop/huh_data/hourly_hhu_total.csv", index=False)


df = fileOpen()

# Group by each hour
hourlyDF = df.groupby("Hour", as_index=False)['HHU'].sum()
# print(hourlyDF)

# hourlyDF.info()

# Add the excess column
hourlyDF['Excess'] = hourlyDF['HHU'] - 320

# Remove 'negative excess'
hourlyDF.loc[hourlyDF['Excess'] <= 0, 'Excess'] = 0
print(hourlyDF)

# Sum
print(hourlyDF['Excess'].sum())

# Export
csvExport(hourlyDF)
