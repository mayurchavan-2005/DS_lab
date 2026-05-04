"""
Data Visualization II Practical

Box plot analysis on the Titanic dataset using Python.

Operations covered:
a) Load and clean Titanic dataset by removing null ages.
b) Plot box plot for Age distribution by Gender and Survival Status.
c) Display box plot statistics: Min, Q1, Median, Q3, and Max for each group.
d) Write observations comparing distributions and identifying outliers.
"""

from pathlib import Path
import os

PROJECT_DIR = Path(__file__).resolve().parent
os.environ["MPLCONFIGDIR"] = str(PROJECT_DIR / "matplotlib_cache")
os.environ["SEABORN_DATA"] = str(PROJECT_DIR / "seaborn_data")
os.environ["MPLBACKEND"] = "Agg"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


OUTPUT_DIR = PROJECT_DIR / "plots"
OUTPUT_DIR.mkdir(exist_ok=True)

BOX_PLOT_PATH = OUTPUT_DIR / "age_boxplot_by_gender_survival.png"
STATISTICS_PATH = OUTPUT_DIR / "age_boxplot_statistics.csv"
OBSERVATIONS_PATH = OUTPUT_DIR / "age_boxplot_observations.txt"


def count_outliers(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = series[(series < lower_bound) | (series > upper_bound)]
    return len(outliers), lower_bound, upper_bound


# a) Load and clean Titanic dataset by removing null ages.
titanic = sns.load_dataset("titanic")
titanic_clean = titanic.dropna(subset=["age"]).copy()
titanic_clean["survival_status"] = titanic_clean["survived"].map(
    {0: "Did Not Survive", 1: "Survived"}
)

print("\nOriginal Titanic dataset shape:")
print(titanic.shape)

print("\nShape after removing null ages:")
print(titanic_clean.shape)

print("\nFirst five rows after cleaning:")
print(titanic_clean[["sex", "age", "survival_status"]].head())


# b) Plot box plot for Age distribution by Gender and Survival Status.
plt.figure(figsize=(9, 6))
sns.boxplot(
    data=titanic_clean,
    x="sex",
    y="age",
    hue="survival_status",
    palette="Set2",
)
plt.title("Age Distribution by Gender and Survival Status")
plt.xlabel("Gender")
plt.ylabel("Age")
plt.legend(title="Survival Status")
plt.tight_layout()
plt.savefig(BOX_PLOT_PATH, dpi=300)
plt.close()


# c) Display box plot statistics for each group.
boxplot_statistics = (
    titanic_clean.groupby(["sex", "survival_status"])["age"]
    .agg(
        Min="min",
        Q1=lambda x: x.quantile(0.25),
        Median="median",
        Q3=lambda x: x.quantile(0.75),
        Max="max",
        Count="count",
    )
    .reset_index()
)

outlier_rows = []
for (gender, status), group in titanic_clean.groupby(["sex", "survival_status"]):
    outlier_count, lower_bound, upper_bound = count_outliers(group["age"])
    outlier_rows.append(
        {
            "sex": gender,
            "survival_status": status,
            "Outlier Count": outlier_count,
            "Lower Bound": lower_bound,
            "Upper Bound": upper_bound,
        }
    )

outlier_statistics = pd.DataFrame(outlier_rows)
boxplot_statistics = boxplot_statistics.merge(
    outlier_statistics,
    on=["sex", "survival_status"],
)

boxplot_statistics.to_csv(STATISTICS_PATH, index=False)

print("\nBox plot statistics by Gender and Survival Status:")
print(boxplot_statistics)


# d) Write observations.
female_survived_median = boxplot_statistics.loc[
    (boxplot_statistics["sex"] == "female")
    & (boxplot_statistics["survival_status"] == "Survived"),
    "Median",
].iloc[0]

female_not_survived_median = boxplot_statistics.loc[
    (boxplot_statistics["sex"] == "female")
    & (boxplot_statistics["survival_status"] == "Did Not Survive"),
    "Median",
].iloc[0]

male_survived_median = boxplot_statistics.loc[
    (boxplot_statistics["sex"] == "male")
    & (boxplot_statistics["survival_status"] == "Survived"),
    "Median",
].iloc[0]

male_not_survived_median = boxplot_statistics.loc[
    (boxplot_statistics["sex"] == "male")
    & (boxplot_statistics["survival_status"] == "Did Not Survive"),
    "Median",
].iloc[0]

total_outliers = boxplot_statistics["Outlier Count"].sum()

observations = f"""
Titanic Age Box Plot Observations

1. After removing records with null ages, the dataset contains
   {titanic_clean.shape[0]} rows.
2. Female passengers who survived have a median age of
   {female_survived_median:.2f}, while female passengers who did not survive
   have a median age of {female_not_survived_median:.2f}.
3. Male passengers who survived have a median age of {male_survived_median:.2f},
   while male passengers who did not survive have a median age of
   {male_not_survived_median:.2f}.
4. The box plots show that age distributions vary by both gender and survival
   status. The interquartile range shows the middle 50% of ages in each group.
5. Outliers are identified using the 1.5 * IQR rule. The total number of age
   outliers across all gender-survival groups is {total_outliers}.
6. Wider boxes indicate more variation in ages, while points beyond the whiskers
   represent possible age outliers.

Saved files:
- {BOX_PLOT_PATH}
- {STATISTICS_PATH}
"""

OBSERVATIONS_PATH.write_text(observations.strip(), encoding="utf-8")

print("\nBox plot saved successfully:")
print(BOX_PLOT_PATH)

print("\nStatistics saved successfully:")
print(STATISTICS_PATH)

print("\nObservations saved successfully:")
print(OBSERVATIONS_PATH)
print("\n" + observations.strip())
