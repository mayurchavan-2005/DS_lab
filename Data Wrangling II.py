"""
Data Wrangling II Practical

Operations covered:
a) Handle missing values using median imputation.
b) Detect and handle outliers using the IQR method.
c) Handle data inconsistency: marks greater than 100 are treated as invalid.
d) Apply data transformation using log transformation.
"""

import numpy as np
import pandas as pd


# Open source dataset:
# Students Performance in Exams dataset.
# Original Kaggle dataset page:
# https://www.kaggle.com/datasets/spscientist/students-performance-in-exams
DATASET_URL = (
    "https://gist.githubusercontent.com/brian-yu/"
    "b622b1119fc0f6913aacc416eede9777/raw/studentperformance.csv"
)

MARK_COLUMNS = ["math score", "reading score", "writing score"]


df = pd.read_csv(DATASET_URL)

print("\nOriginal dataset:")
print(df.head())
print("\nOriginal dimensions:", df.shape)
print("\nOriginal missing values:")
print(df.isnull().sum())


# The original dataset is mostly clean. These values are added only to demonstrate
# missing-value imputation, invalid marks, and outlier handling clearly.
df_dirty = df.copy()
df_dirty.loc[0, "math score"] = np.nan
df_dirty.loc[1, "reading score"] = np.nan
df_dirty.loc[2, "writing score"] = np.nan
df_dirty.loc[3, "math score"] = 125
df_dirty.loc[4, "reading score"] = 130
df_dirty.loc[5, "writing score"] = 150

print("\nDataset after adding sample data-quality issues:")
print(df_dirty.head(8))


# c) Handle data inconsistency: marks greater than 100 are invalid.
for column in MARK_COLUMNS:
    invalid_count = (df_dirty[column] > 100).sum()
    print(f"\nInvalid values in {column} greater than 100:", invalid_count)
    df_dirty.loc[df_dirty[column] > 100, column] = np.nan

print("\nMissing values after replacing invalid marks with NaN:")
print(df_dirty[MARK_COLUMNS].isnull().sum())


# a) Handle missing values using median imputation.
df_imputed = df_dirty.copy()
for column in MARK_COLUMNS:
    median_value = df_imputed[column].median()
    df_imputed[column] = df_imputed[column].fillna(median_value)
    print(f"Median used for {column}: {median_value}")

print("\nMissing values after median imputation:")
print(df_imputed[MARK_COLUMNS].isnull().sum())


# b) Detect and handle outliers using the IQR method.
df_no_outliers = df_imputed.copy()

print("\nOutlier detection using IQR:")
for column in MARK_COLUMNS:
    q1 = df_no_outliers[column].quantile(0.25)
    q3 = df_no_outliers[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = (
        (df_no_outliers[column] < lower_bound)
        | (df_no_outliers[column] > upper_bound)
    )

    print(f"\n{column}")
    print("Q1:", q1)
    print("Q3:", q3)
    print("IQR:", iqr)
    print("Lower bound:", lower_bound)
    print("Upper bound:", upper_bound)
    print("Number of outliers:", outliers.sum())

    # Handle outliers by capping them to the calculated IQR limits.
    df_no_outliers[column] = df_no_outliers[column].clip(
        lower=lower_bound,
        upper=upper_bound,
    )

print("\nData after handling outliers with IQR capping:")
print(df_no_outliers[MARK_COLUMNS].describe())


# d) Apply log transformation.
# np.log1p(x) calculates log(1 + x), so it safely handles marks with value 0.
df_transformed = df_no_outliers.copy()
for column in MARK_COLUMNS:
    df_transformed[f"log_{column}"] = np.log1p(df_transformed[column])

print("\nDataset after log transformation:")
print(
    df_transformed[
        MARK_COLUMNS
        + ["log_math score", "log_reading score", "log_writing score"]
    ].head()
)

print("\nFinal cleaned dataset dimensions:", df_transformed.shape)
