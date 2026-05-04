"""
Descriptive Statistics Practical on the Iris Dataset

Operations covered:
a) Summary statistics: mean, median, min, max, and standard deviation.
b) Group by Species and compute mean, median, std, min, and max for
   SepalLengthCm and PetalLengthCm.
c) Display percentiles: 25%, 50%, and 75% for SepalLengthCm.
d) Display per-species detailed statistics using describe().
"""

import pandas as pd


# Iris dataset from the UCI Machine Learning Repository.
# Dataset information: https://archive.ics.uci.edu/dataset/53/iris
DATASET_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

COLUMN_NAMES = [
    "SepalLengthCm",
    "SepalWidthCm",
    "PetalLengthCm",
    "PetalWidthCm",
    "Species",
]


df = pd.read_csv(DATASET_URL, names=COLUMN_NAMES)

print("\nFirst five rows of the Iris dataset:")
print(df.head())


# a) Summary statistics for the dataset.
numeric_columns = [
    "SepalLengthCm",
    "SepalWidthCm",
    "PetalLengthCm",
    "PetalWidthCm",
]

summary_statistics = df[numeric_columns].agg(["mean", "median", "min", "max", "std"])

print("\na) Summary statistics for numeric columns:")
print(summary_statistics)


# b) Group by Species and compute statistics for SepalLengthCm and PetalLengthCm.
species_group_statistics = df.groupby("Species")[
    ["SepalLengthCm", "PetalLengthCm"]
].agg(["mean", "median", "std", "min", "max"])

print(
    "\nb) Species-wise Mean, Median, Std, Min, and Max "
    "for SepalLengthCm and PetalLengthCm:"
)
print(species_group_statistics)


# c) Percentiles for SepalLengthCm.
sepal_length_percentiles = df["SepalLengthCm"].quantile([0.25, 0.50, 0.75])

print("\nc) Percentiles for SepalLengthCm:")
print(sepal_length_percentiles)


# d) Per-species detailed statistics using describe().
per_species_describe = df.groupby("Species").describe()

print("\nd) Per-species detailed statistics using describe():")
print(per_species_describe)
