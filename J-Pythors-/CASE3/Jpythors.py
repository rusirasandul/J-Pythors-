import pandas as pd
from pathlib import Path


data_dir = Path(r"C:/Users/rusir/OneDrive/Desktop/J'Pythors/CASE3/CASE3/PassengerVehicle_Stats")


csv_files = data_dir.glob("*.csv")
dataframes = [pd.read_csv(file) for file in csv_files]


vehicles_df = pd.concat(dataframes, ignore_index=True)


vehicles_df.to_csv(data_dir / "vehicles.csv", index=False)


print(vehicles_df.info())
print(vehicles_df.describe())
print(vehicles_df.columns)
print(vehicles_df.shape)
print(vehicles_df.dtypes)
print(vehicles_df.isnull().sum())
print(vehicles_df.nunique())
print(vehicles_df.head())


print("Duplicate Rows except first occurrence based on all columns are :", vehicles_df.duplicated().sum())
vehicles_df.drop_duplicates(keep='first', inplace=True)


for col in vehicles_df.select_dtypes(include="object"):
    vehicles_df[col] = vehicles_df[col].fillna(vehicles_df[col].mode()[0])


for col in vehicles_df.select_dtypes(include=["int", "float"]):
    vehicles_df[col] = vehicles_df[col].fillna(vehicles_df[col].median())

print("Missing values in the dataset after filling:")
print(vehicles_df.isnull().sum())


for col in vehicles_df.select_dtypes(include=["int", "float"]):
    Q1 = vehicles_df[col].quantile(0.25)
    Q3 = vehicles_df[col].quantile(0.75)
    IQR = Q3 - Q1


    vehicles_df = vehicles_df[(vehicles_df[col] >= Q1 - 1.5 * IQR) & (vehicles_df[col] <= Q3 + 1.5 * IQR)]


vehicles_df["Vehicle Type"] = vehicles_df["Record ID"].str.split("_").str[0]


vehicles_df.columns = vehicles_df.columns.str.strip()


if "Address" in vehicles_df.columns:
    vehicles_df.drop(columns=["Address"], inplace=True)
else:
    print("'Address' column not found. Skipping drop operation.")



vehicles_df.to_csv("vehicles_cleaned.csv", index=False)


print(vehicles_df.describe())
print(vehicles_df.head())
