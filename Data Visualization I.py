"""
Data Visualization I Practical

Exploratory Data Analysis (EDA) on the Titanic dataset using Python.

Operations covered:
a) Load Titanic dataset from Seaborn.
b) Display basic info: head, shape, columns.
c) Analyze survival by gender and passenger class.
d) Plot a histogram for Fare distribution with KDE.
e) Plot survival count by gender using countplot.
f) Save the plots and write observations.
"""

from pathlib import Path
import os

PROJECT_DIR = Path(__file__).resolve().parent
os.environ["MPLCONFIGDIR"] = str(PROJECT_DIR / "matplotlib_cache")
os.environ["SEABORN_DATA"] = str(PROJECT_DIR / "seaborn_data")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


OUTPUT_DIR = PROJECT_DIR / "plots"
OUTPUT_DIR.mkdir(exist_ok=True)

FARE_PLOT_PATH = OUTPUT_DIR / "fare_distribution.png"
SURVIVAL_GENDER_PLOT_PATH = OUTPUT_DIR / "survival_count_by_gender.png"
OBSERVATIONS_PATH = OUTPUT_DIR / "titanic_eda_observations.txt"


# a) Load Titanic dataset from Seaborn.
titanic = sns.load_dataset("titanic")


# b) Display basic information.
print("\nFirst five rows of Titanic dataset:")
print(titanic.head())

print("\nShape of the dataset:")
print(titanic.shape)

print("\nColumns in the dataset:")
print(titanic.columns.tolist())

print("\nDataset information:")
titanic.info()

print("\nMissing values:")
print(titanic.isnull().sum())


# c) Analyze survival by gender and passenger class.
survival_by_gender = titanic.groupby("sex")["survived"].agg(
    ["count", "sum", "mean"]
)
survival_by_gender = survival_by_gender.rename(
    columns={
        "count": "Total Passengers",
        "sum": "Survived Passengers",
        "mean": "Survival Rate",
    }
)

survival_by_class = titanic.groupby("pclass")["survived"].agg(
    ["count", "sum", "mean"]
)
survival_by_class = survival_by_class.rename(
    columns={
        "count": "Total Passengers",
        "sum": "Survived Passengers",
        "mean": "Survival Rate",
    }
)

print("\nSurvival analysis by gender:")
print(survival_by_gender)

print("\nSurvival analysis by passenger class:")
print(survival_by_class)


# d) Plot histogram for Fare distribution with KDE.
plt.figure(figsize=(8, 5))
sns.histplot(data=titanic, x="fare", kde=True, bins=30, color="steelblue")
plt.title("Titanic Fare Distribution")
plt.xlabel("Fare")
plt.ylabel("Passenger Count")
plt.tight_layout()
plt.savefig(FARE_PLOT_PATH, dpi=300)
plt.close()


# e) Plot survival count by gender using countplot.
plt.figure(figsize=(8, 5))
sns.countplot(data=titanic, x="sex", hue="survived", palette="Set2")
plt.title("Survival Count by Gender")
plt.xlabel("Gender")
plt.ylabel("Passenger Count")
plt.legend(title="Survived", labels=["No", "Yes"])
plt.tight_layout()
plt.savefig(SURVIVAL_GENDER_PLOT_PATH, dpi=300)
plt.close()


# f) Save observations.
best_gender = survival_by_gender["Survival Rate"].idxmax()
best_class = survival_by_class["Survival Rate"].idxmax()
fare_mean = titanic["fare"].mean()
fare_median = titanic["fare"].median()

observations = f"""
Titanic EDA Observations

1. The dataset contains {titanic.shape[0]} rows and {titanic.shape[1]} columns.
2. Survival by gender shows that '{best_gender}' passengers had the higher
   survival rate.
3. Passenger class analysis shows that class {best_class} had the highest
   survival rate.
4. The fare distribution is right-skewed. Most passengers paid lower fares,
   while a smaller number paid very high fares.
5. The mean fare is {fare_mean:.2f}, while the median fare is {fare_median:.2f}.
   Since the mean is greater than the median, high fare values influence the
   average.
6. The survival count plot by gender shows that survival was not evenly
   distributed across male and female passengers.

Saved plots:
- {FARE_PLOT_PATH}
- {SURVIVAL_GENDER_PLOT_PATH}
"""

OBSERVATIONS_PATH.write_text(observations.strip(), encoding="utf-8")

print("\nPlots saved successfully:")
print(FARE_PLOT_PATH)
print(SURVIVAL_GENDER_PLOT_PATH)

print("\nObservations saved successfully:")
print(OBSERVATIONS_PATH)
print("\n" + observations.strip())
