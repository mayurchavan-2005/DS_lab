"""
Data Analytics II Practical

Logistic Regression on the Social Network Ads dataset.

Operations covered:
a) Read the dataset and display its head and shape.
b) Select features (Age, EstimatedSalary) and target (Purchased).
c) Split dataset into train and test sets (75:25).
d) Apply feature scaling using StandardScaler.
e) Train Logistic Regression and predict results.
f) Compute Confusion Matrix and print TP, TN, FP, FN.
g) Calculate Accuracy, Error Rate, Precision, and Recall.
h) Print Classification Report.
"""

import numpy as np
import pandas as pd


# Social Network Ads dataset.
# Source page:
# https://huggingface.co/datasets/Rodrigopiva/Social_Network_Ads.csv
DATASET_URL = (
    "https://huggingface.co/datasets/Rodrigopiva/Social_Network_Ads.csv/"
    "resolve/main/Social_Network_Ads.csv"
)

FEATURE_COLUMNS = ["Age", "EstimatedSalary"]
TARGET_COLUMN = "Purchased"
RANDOM_SEED = 42
TEST_SIZE = 0.25
LEARNING_RATE = 0.1
EPOCHS = 5000


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def standard_scale_train_test(X_train, X_test):
    mean = X_train.mean(axis=0)
    std = X_train.std(axis=0)
    return (X_train - mean) / std, (X_test - mean) / std


def train_logistic_regression(X_train, y_train, learning_rate, epochs):
    X_train_intercept = np.c_[np.ones(X_train.shape[0]), X_train]
    weights = np.zeros(X_train_intercept.shape[1])

    for _ in range(epochs):
        probabilities = sigmoid(X_train_intercept @ weights)
        errors = probabilities - y_train
        gradient = (X_train_intercept.T @ errors) / len(y_train)
        weights -= learning_rate * gradient

    return weights


def predict_logistic_regression(X_test, weights):
    X_test_intercept = np.c_[np.ones(X_test.shape[0]), X_test]
    probabilities = sigmoid(X_test_intercept @ weights)
    predictions = (probabilities >= 0.5).astype(int)
    return probabilities, predictions


def classification_metrics(y_true, y_pred, positive_label):
    tp = np.sum((y_true == positive_label) & (y_pred == positive_label))
    fp = np.sum((y_true != positive_label) & (y_pred == positive_label))
    fn = np.sum((y_true == positive_label) & (y_pred != positive_label))

    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0
    f1_score = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) != 0
        else 0
    )
    support = np.sum(y_true == positive_label)

    return precision, recall, f1_score, support


# a) Read the dataset and display its head and shape.
df = pd.read_csv(DATASET_URL)

print("\nFirst five rows of the dataset:")
print(df.head())

print("\nShape of the dataset:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())


# b) Select features and target.
X = df[FEATURE_COLUMNS].to_numpy(dtype=float)
y = df[TARGET_COLUMN].to_numpy(dtype=int)


# c) Split dataset into train and test sets (75:25).
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


# d) Apply feature scaling using StandardScaler.
X_train_scaled, X_test_scaled = standard_scale_train_test(X_train, X_test)

print("\nScaled training feature sample:")
print(pd.DataFrame(X_train_scaled, columns=FEATURE_COLUMNS).head())


# e) Train Logistic Regression and predict results.
weights = train_logistic_regression(
    X_train_scaled,
    y_train,
    learning_rate=LEARNING_RATE,
    epochs=EPOCHS,
)
probabilities, y_pred = predict_logistic_regression(X_test_scaled, weights)


# f) Compute Confusion Matrix and print TP, TN, FP, FN.
tp = np.sum((y_test == 1) & (y_pred == 1))
tn = np.sum((y_test == 0) & (y_pred == 0))
fp = np.sum((y_test == 0) & (y_pred == 1))
fn = np.sum((y_test == 1) & (y_pred == 0))

confusion_matrix = pd.DataFrame(
    [[tn, fp], [fn, tp]],
    index=["Actual 0", "Actual 1"],
    columns=["Predicted 0", "Predicted 1"],
)

print("\nConfusion Matrix:")
print(confusion_matrix)
print("\nTrue Positive (TP):", tp)
print("True Negative (TN):", tn)
print("False Positive (FP):", fp)
print("False Negative (FN):", fn)


# g) Calculate Accuracy, Error Rate, Precision, and Recall.
accuracy = (tp + tn) / len(y_test)
error_rate = (fp + fn) / len(y_test)
precision = tp / (tp + fp) if (tp + fp) != 0 else 0
recall = tp / (tp + fn) if (tp + fn) != 0 else 0

print("\nEvaluation Metrics:")
print("Accuracy:", accuracy)
print("Error Rate:", error_rate)
print("Precision:", precision)
print("Recall:", recall)


# h) Print Classification Report.
report_rows = []
for label in [0, 1]:
    label_precision, label_recall, label_f1, label_support = classification_metrics(
        y_test,
        y_pred,
        positive_label=label,
    )
    report_rows.append(
        {
            "Class": label,
            "Precision": label_precision,
            "Recall": label_recall,
            "F1-score": label_f1,
            "Support": label_support,
        }
    )

classification_report = pd.DataFrame(report_rows)

print("\nClassification Report:")
print(classification_report)

sample_results = pd.DataFrame(
    {
        "Actual Purchased": y_test,
        "Predicted Purchased": y_pred,
        "Purchase Probability": probabilities,
    }
)

print("\nSample Predictions:")
print(sample_results.head(10))
