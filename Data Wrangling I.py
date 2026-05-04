"""
Data Wrangling I Practical

Tasks covered:
a) Import required Python libraries.
b) Locate an open source dataset from the web.
c) Load the dataset into a pandas DataFrame.
d) Data preprocessing: missing values, descriptions, variable details, data types,
   and dimensions.
e) Data formatting and normalization.
f) Convert categorical variables into quantitative variables.
"""

import pandas as pd


# b) Open source dataset from the web:
# Iris dataset from the UCI Machine Learning Repository.
# Dataset information: https://archive.ics.uci.edu/dataset/53/iris
DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

COLUMN_NAMES = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
    "species",
]


# c) Load the dataset into a pandas DataFrame.
df = pd.read_csv(DATASET_URL, names=COLUMN_NAMES)

print("\nFirst five rows of the dataset:")
print(df.head())


# d) Data preprocessing.
print("\nDimensions of the dataset:")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nVariable descriptions:")
print(df.describe(include="all"))

print("\nMissing values in each column:")
print(df.isnull().sum())

print("\nTotal number of missing values in the dataset:")
print(df.isnull().sum().sum())

print("\nTypes of variables:")
print(df.dtypes)

print("\nDataset information:")
df.info()


# e) Data formatting and normalization.
numeric_columns = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
categorical_columns = ["species"]

df[numeric_columns] = df[numeric_columns].astype(float)
df[categorical_columns] = df[categorical_columns].astype("category")

print("\nData types after formatting:")
print(df.dtypes)

df_normalized = df.copy()
df_normalized[numeric_columns] = (
    df[numeric_columns] - df[numeric_columns].min()
) / (df[numeric_columns].max() - df[numeric_columns].min())

print("\nNormalized numeric columns using Min-Max normalization:")
print(df_normalized.head())


# f) Turn categorical variables into quantitative variables.
df_encoded = df_normalized.copy()
df_encoded["species_encoded"] = df_encoded["species"].cat.codes

print("\nCategorical variable converted into quantitative variable:")
print(df_encoded[["species", "species_encoded"]].drop_duplicates())

print("\nFinal encoded dataset:")
print(df_encoded.head())


# Optional one-hot encoding, another common way to convert categorical data.
df_one_hot_encoded = pd.get_dummies(df_normalized, columns=["species"])

print("\nOne-hot encoded dataset:")
print(df_one_hot_encoded.head())
