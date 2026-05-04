"""
Data Visualization III Practical

Visualize feature distributions in the Iris dataset using Python.

Operations covered:
a) Load the Iris dataset and identify variable types.
b) Plot histograms for all four numeric features.
c) Plot boxplots for each feature grouped by Species.
d) Save both plots and write observations.
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
import seaborn as sns


OUTPUT_DIR = PROJECT_DIR / "plots"
OUTPUT_DIR.mkdir(exist_ok=True)

HISTOGRAM_PLOT_PATH = OUTPUT_DIR / "iris_feature_histograms.png"
BOXPLOT_PATH = OUTPUT_DIR / "iris_feature_boxplots_by_species.png"
OBSERVATIONS_PATH = OUTPUT_DIR / "iris_distribution_observations.txt"


# a) Load the Iris dataset and identify variable types.
iris = sns.load_dataset("iris")
iris = iris.rename(
    columns={
        "sepal_length": "SepalLengthCm",
        "sepal_width": "SepalWidthCm",
        "petal_length": "PetalLengthCm",
        "petal_width": "PetalWidthCm",
        "species": "Species",
    }
)

numeric_features = [
    "SepalLengthCm",
    "SepalWidthCm",
    "PetalLengthCm",
    "PetalWidthCm",
]

print("\nFirst five rows of the Iris dataset:")
print(iris.head())

print("\nShape of the dataset:")
print(iris.shape)

print("\nVariable types:")
print(iris.dtypes)

print("\nNumeric variables:")
print(numeric_features)

print("\nCategorical variables:")
print(["Species"])


# b) Plot histograms for all four numeric features.
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()

for index, feature in enumerate(numeric_features):
    sns.histplot(
        data=iris,
        x=feature,
        kde=True,
        bins=15,
        color="steelblue",
        ax=axes[index],
    )
    axes[index].set_title(f"Distribution of {feature}")
    axes[index].set_xlabel(feature)
    axes[index].set_ylabel("Frequency")

plt.tight_layout()
plt.savefig(HISTOGRAM_PLOT_PATH, dpi=300)
plt.close()


# c) Plot boxplots for each feature grouped by Species.
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes = axes.flatten()

for index, feature in enumerate(numeric_features):
    sns.boxplot(
        data=iris,
        x="Species",
        y=feature,
        hue="Species",
        palette="Set2",
        legend=False,
        ax=axes[index],
    )
    axes[index].set_title(f"{feature} by Species")
    axes[index].set_xlabel("Species")
    axes[index].set_ylabel(feature)

plt.tight_layout()
plt.savefig(BOXPLOT_PATH, dpi=300)
plt.close()


# d) Write observations.
feature_summary = iris[numeric_features].describe()
species_feature_means = iris.groupby("Species")[numeric_features].mean()

highest_petal_length_species = species_feature_means["PetalLengthCm"].idxmax()
lowest_petal_length_species = species_feature_means["PetalLengthCm"].idxmin()
highest_petal_width_species = species_feature_means["PetalWidthCm"].idxmax()

observations = f"""
Iris Feature Distribution Observations

1. The Iris dataset contains {iris.shape[0]} rows and {iris.shape[1]} columns.
2. The four measurement columns are numeric: SepalLengthCm, SepalWidthCm,
   PetalLengthCm, and PetalWidthCm. Species is categorical.
3. Histograms show the distribution of each numeric feature. PetalLengthCm and
   PetalWidthCm show clearer separation patterns than sepal measurements.
4. Boxplots grouped by Species show that {highest_petal_length_species} has the
   highest average PetalLengthCm, while {lowest_petal_length_species} has the
   lowest average PetalLengthCm.
5. {highest_petal_width_species} has the highest average PetalWidthCm.
6. Sepal features overlap more across species, while petal features are more
   useful for distinguishing Iris species.

Numeric feature summary:
{feature_summary}

Species-wise feature means:
{species_feature_means}

Saved plots:
- {HISTOGRAM_PLOT_PATH}
- {BOXPLOT_PATH}
"""

OBSERVATIONS_PATH.write_text(observations.strip(), encoding="utf-8")

print("\nHistograms saved successfully:")
print(HISTOGRAM_PLOT_PATH)

print("\nBoxplots saved successfully:")
print(BOXPLOT_PATH)

print("\nObservations saved successfully:")
print(OBSERVATIONS_PATH)
print("\n" + observations.strip())
