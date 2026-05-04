"""
Data Analytics III Practical

Naive Bayes Classification on the Iris dataset.

Operations covered:
a) Load the Iris dataset and drop the Id column.
b) Split dataset into train (70%) and test (30%) sets.
c) Apply Gaussian Naive Bayes classifier.
d) Compute Confusion Matrix.
e) Calculate Accuracy and Error Rate.
f) Print the full Classification Report.
"""

import numpy as np
import pandas as pd


# Iris CSV dataset with Id column.
# Source page: https://huggingface.co/datasets/scikit-learn/iris/blob/main/Iris.csv
DATASET_URL = (
    "https://huggingface.co/datasets/scikit-learn/iris/"
    "resolve/main/Iris.csv"
)

TARGET_COLUMN = "Species"
RANDOM_SEED = 42
TEST_SIZE = 0.30
EPSILON = 1e-9


def train_gaussian_naive_bayes(X_train, y_train):
    classes = np.unique(y_train)
    model = {}

    for class_name in classes:
        X_class = X_train[y_train == class_name]
        model[class_name] = {
            "prior": len(X_class) / len(X_train),
            "mean": X_class.mean(axis=0),
            "variance": X_class.var(axis=0) + EPSILON,
        }

    return model


def gaussian_probability(X, mean, variance):
    exponent = np.exp(-((X - mean) ** 2) / (2 * variance))
    return (1 / np.sqrt(2 * np.pi * variance)) * exponent


def predict_gaussian_naive_bayes(X_test, model):
    predictions = []

    for row in X_test:
        class_scores = {}

        for class_name, stats in model.items():
            probabilities = gaussian_probability(
                row,
                stats["mean"],
                stats["variance"],
            )
            class_scores[class_name] = np.log(stats["prior"]) + np.sum(
                np.log(probabilities)
            )

        predictions.append(max(class_scores, key=class_scores.get))

    return np.array(predictions)


def build_confusion_matrix(y_true, y_pred, classes):
    matrix = pd.DataFrame(0, index=classes, columns=classes)

    for actual, predicted in zip(y_true, y_pred):
        matrix.loc[actual, predicted] += 1

    matrix.index.name = "Actual"
    matrix.columns.name = "Predicted"
    return matrix


def classification_report(y_true, y_pred, classes):
    rows = []

    for class_name in classes:
        tp = np.sum((y_true == class_name) & (y_pred == class_name))
        fp = np.sum((y_true != class_name) & (y_pred == class_name))
        fn = np.sum((y_true == class_name) & (y_pred != class_name))

        precision = tp / (tp + fp) if (tp + fp) != 0 else 0
        recall = tp / (tp + fn) if (tp + fn) != 0 else 0
        f1_score = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) != 0
            else 0
        )
        support = np.sum(y_true == class_name)

        rows.append(
            {
                "Class": class_name,
                "Precision": precision,
                "Recall": recall,
                "F1-score": f1_score,
                "Support": support,
            }
        )

    return pd.DataFrame(rows)


# a) Load the Iris dataset and drop the Id column.
df = pd.read_csv(DATASET_URL)

print("\nOriginal dataset head:")
print(df.head())

print("\nOriginal dataset shape:")
print(df.shape)

df = df.drop(columns=["Id"])

print("\nDataset after dropping Id column:")
print(df.head())
print("\nShape after dropping Id column:")
print(df.shape)


# b) Split dataset into train (70%) and test (30%) sets.
feature_columns = [column for column in df.columns if column != TARGET_COLUMN]

X = df[feature_columns].to_numpy(dtype=float)
y = df[TARGET_COLUMN].to_numpy()

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


# c) Apply Gaussian Naive Bayes classifier.
model = train_gaussian_naive_bayes(X_train, y_train)
y_pred = predict_gaussian_naive_bayes(X_test, model)


# d) Compute Confusion Matrix.
classes = np.unique(y)
confusion_matrix = build_confusion_matrix(y_test, y_pred, classes)

print("\nConfusion Matrix:")
print(confusion_matrix)


# e) Calculate Accuracy and Error Rate.
accuracy = np.mean(y_test == y_pred)
error_rate = 1 - accuracy

print("\nAccuracy:", accuracy)
print("Error Rate:", error_rate)


# f) Print the full Classification Report.
report = classification_report(y_test, y_pred, classes)

print("\nClassification Report:")
print(report)

sample_predictions = pd.DataFrame(
    {
        "Actual Species": y_test,
        "Predicted Species": y_pred,
    }
)

print("\nSample Predictions:")
print(sample_predictions.head(10))
