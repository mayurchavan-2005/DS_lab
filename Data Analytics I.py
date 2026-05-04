"""
Data Analytics I Practical

Linear Regression on the Boston Housing dataset.

Operations covered:
a) Load the BostonHousing CSV dataset.
b) Display head, shape, statistical summary, and missing values.
c) Split dataset into train and test sets using an 80:20 split.
d) Apply Linear Regression and predict house prices (medv).
e) Compute and display MAE, MSE, RMSE, and R2 score.
f) Display feature coefficients and sample predictions vs actual values.
"""

import numpy as np
import pandas as pd


# Boston Housing CSV dataset.
# Source: https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv
DATASET_URL = "https://raw.githubusercontent.com/selva86/datasets/master/BostonHousing.csv"
TARGET_COLUMN = "medv"
RANDOM_SEED = 42
TEST_SIZE = 0.20


# a) Load the BostonHousing CSV dataset.
df = pd.read_csv(DATASET_URL)


# b) Display head, shape, statistical summary, and missing values.
print("\nFirst five rows of the dataset:")
print(df.head())

print("\nShape of the dataset:")
print(df.shape)

print("\nStatistical summary:")
print(df.describe())

print("\nMissing values in each column:")
print(df.isnull().sum())


# c) Split dataset into train and test sets (80:20).
feature_columns = [column for column in df.columns if column != TARGET_COLUMN]

X = df[feature_columns].to_numpy(dtype=float)
y = df[TARGET_COLUMN].to_numpy(dtype=float)

np.random.seed(RANDOM_SEED)
shuffled_indices = np.random.permutation(len(df))
test_count = int(len(df) * TEST_SIZE)

test_indices = shuffled_indices[:test_count]
train_indices = shuffled_indices[test_count:]

X_train = X[train_indices]
X_test = X[test_indices]
y_train = y[train_indices]
y_test = y[test_indices]

print("\nTraining set size:", X_train.shape)
print("Testing set size:", X_test.shape)


# d) Apply Linear Regression and predict house prices (medv).
# Add an intercept column of 1s because np.linalg.lstsq fits coefficients only.
X_train_with_intercept = np.c_[np.ones(X_train.shape[0]), X_train]
X_test_with_intercept = np.c_[np.ones(X_test.shape[0]), X_test]

coefficients, residuals, rank, singular_values = np.linalg.lstsq(
    X_train_with_intercept,
    y_train,
    rcond=None,
)

y_pred = X_test_with_intercept @ coefficients


# e) Compute and display MAE, MSE, RMSE, and R2 score.
mae = np.mean(np.abs(y_test - y_pred))
mse = np.mean((y_test - y_pred) ** 2)
rmse = np.sqrt(mse)

ss_residual = np.sum((y_test - y_pred) ** 2)
ss_total = np.sum((y_test - np.mean(y_test)) ** 2)
r2_score = 1 - (ss_residual / ss_total)

print("\nModel Evaluation Metrics:")
print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)
print("R2 Score:", r2_score)


# f) Display feature coefficients and sample predictions vs actual values.
feature_coefficients = pd.DataFrame(
    {
        "Feature": ["Intercept"] + feature_columns,
        "Coefficient": coefficients,
    }
)

print("\nFeature Coefficients:")
print(feature_coefficients)

sample_predictions = pd.DataFrame(
    {
        "Actual medv": y_test,
        "Predicted medv": y_pred,
        "Difference": y_test - y_pred,
    }
)

print("\nSample Predictions vs Actual Values:")
print(sample_predictions.head(10))
