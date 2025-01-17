# -*- coding: utf-8 -*-
"""machine_learning_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GKPJm2X9hmBrjxdzoMZHczU5Bj-mDriv

About the database

Two files will be sent to you:
* air_system_previous_years.csv: File containing all information from the maintenance sector for years prior to 2022 with 178 columns.
* air_system_present_year.csv: File containing all information from the maintenance sector in this year.
* Any missing value in the database is denoted by na.

The final results that will be presented to the executive board need to be evaluated against air_system_present_year.csv.
"""

# Import the necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, f1_score
import matplotlib.pyplot as plt
import seaborn as sns

#Connection with google drive
from google.colab import drive
drive.mount('/content/drive')

"""*Mount Google Drive to access the data files stored in it."""

# Path to files in Google Drive
df_previous_years = pd.read_csv('/content/drive/MyDrive/Pruebas/Dataset_for_candidates/air_system_present_year.csv',na_values='na')
df_present_year = pd.read_csv('/content/drive/MyDrive/Pruebas/Dataset_for_candidates/air_system_previous_years.csv',na_values='na')

"""**Data Loading:**

* Load the datasets from Google Drive. Missing values are specified with na_values='na'.
"""

#Show data for each CSV
df_previous_years.head(10)

df_present_year.head(10)

"""* Display the first few rows of each dataset to understand their structure."""

# Separate numerical and categorical features
numerical_cols = df_previous_years.select_dtypes(include=[np.number]).columns
categorical_cols =df_previous_years.select_dtypes(exclude=[np.number]).columns

"""* Identify numerical and categorical columns in the dataset for appropriate preprocessing."""

# Handle missing values ​​in numeric features
df_previous_years[numerical_cols] = df_previous_years[numerical_cols].fillna(df_previous_years[numerical_cols].mean())
df_present_year[numerical_cols] = df_present_year[numerical_cols].fillna(df_present_year[numerical_cols].mean())

"""* Fill missing values in numerical features with the mean of each column."""

# Separate features and target in previous years data set
X_previous = df_previous_years.drop(columns=['class'])
y_previous = df_previous_years['class']

"""* Separate the features (X_previous) and the target variable (y_previous)."""

# Encode the target variable
y_previous = y_previous.map({'pos': 1, 'neg': 0})

"""* The **class** column was encoded as 1 for 'pos' and 0 for 'neg'"""

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_previous, y_previous, test_size=0.2, random_state=42)

"""* Split the data into training and test sets using an 80/20 split."""

# Normalize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""* Normalize the features to have zero mean and unit variance."""

#Dimensionality reduction with PCA
pca = PCA(n_components=20)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

"""* The dimensionality of the data is reduced to 20 principal components using PCA.

"""

# Model training
rf_model = RandomForestClassifier(random_state=42)
gb_model = GradientBoostingClassifier(random_state=42)Evalúe los modelos utilizando informes de clasificación que incluyen precisión, recuperación y puntuación F1.
svm_model = SVC(random_state=42)

rf_model.fit(X_train_pca, y_train)
gb_model.fit(X_train_pca, y_train)
svm_model.fit(X_train_pca, y_train)

"""* Three different models are trained: Random Forest, Gradient Boosting and SVM."""

# Evaluation of the models on the test set
rf_pred = rf_model.predict(X_test_pca)
gb_pred = gb_model.predict(X_test_pca)
svm_pred = svm_model.predict(X_test_pca)

# Evaluation metrics
print("Random Forest Classification Report:")
rf_report = classification_report(y_test, rf_pred)
print(rf_report)

print("Gradient Boosting Classification Report:")
gb_report = classification_report(y_test, gb_pred)
print(gb_report)

print("SVM Classification Report:")
svm_report = classification_report(y_test, svm_pred)
print(svm_report)

"""* Models are evaluated using classification reports that include precision, recall, and F1 score."""

# Select the best model based on the F1-score for class 1
rf_f1 = f1_score(y_test, rf_pred, pos_label=1)
gb_f1 = f1_score(y_test, gb_pred, pos_label=1)
svm_f1 = f1_score(y_test, svm_pred, pos_label=1)

best_model = None
best_f1 = 0

if rf_f1 > best_f1:
    best_f1 = rf_f1
    best_model = rf_model
if gb_f1 > best_f1:
    best_f1 = gb_f1
    best_model = gb_model
if svm_f1 > best_f1:
    best_f1 = svm_f1
    best_model = svm_model

print(f"Best Model: {best_model}")
print(f"Best F1-Score for class 1: {best_f1}")

"""* Here a selection is automatically made of the best model according to the highest F1 score for class 1 (defective air system)."""

# Preprocess the current year's data set
X_present = df_present_year.drop(columns=['class'])
y_present = df_present_year['class']
y_present = y_present.map({'pos': 1, 'neg': 0})

X_present_scaled = scaler.transform(X_present)
X_present_pca = pca.transform(X_present_scaled)

"""* Preprocess the current year's data similarly to the training data."""

# Evaluate the best model on the current year's data set
present_pred = best_model.predict(X_present_pca)

# Evaluation metrics for this year
print("Present Year Classification Report:")
print(classification_report(y_present, present_pred))

"""* Evaluation of the best model using current year data."""

# Feature importance (only for Random Forest and Gradient Boosting)
if hasattr(best_model, "feature_importances_"):
    importances = best_model.feature_importances_
    indices = np.argsort(importances)[::-1]

# Graph the most important characteristics
plt.figure()
plt.title("Feature Importances")
plt.bar(range(X_train_pca.shape[1]), importances[indices], align="center")
plt.show()

"""* Plot of feature importance if the selected model supports it."""

# Financial impact
cost_preventive = 25
cost_corrective = 500
cost_inspection = 10

# Calculate current costs and costs with the model
actual_preventive_cost = (y_present.sum() * cost_preventive) + ((len(y_present) - y_present.sum()) * cost_inspection)
actual_corrective_cost = ((len(y_present) - y_present.sum()) * cost_corrective)

model_preventive_cost = (present_pred.sum() * cost_preventive) + ((len(present_pred) - present_pred.sum()) * cost_inspection)
model_corrective_cost = ((len(present_pred) - present_pred.sum()) * cost_corrective)

print(f"Actual Preventive Cost: ${actual_preventive_cost}")
print(f"Actual Corrective Cost: ${actual_corrective_cost}")
print(f"Model Preventive Cost: ${model_preventive_cost}")
print(f"Model Corrective Cost: ${model_corrective_cost}")

"""Here the calculation and comparison of the financial impact of using the model versus the current maintenance costs is carried out.

Analysis:

**Preventive Costs:**

The preventive cost is slightly lower when using the model ($605880) compared to the actual preventive cost

without the model ($615000). This suggests the model is slightly more efficient in identifying trucks that do not need preventive maintenance, reducing unnecessary inspections.

**Corrective Costs:**

The corrective cost is slightly higher when using the model ($29804000) compared to the actual corrective

cost without the model ($29500000).
This indicates that the model may have missed some trucks that required preventive maintenance, leading to higher corrective costs.

**Conclusion:**

The total costs using the model are slightly higher compared to the current approach.

**Current Total Cost:** $30115000 ($615000 + $29500000)

**Model Total Cost:** $30409880 ($605880 + $29804000)

While the model has the potential to reduce some preventive costs, it is currently leading to slightly higher corrective costs. This indicates that further optimization of the model might be necessary to improve its accuracy in identifying trucks needing preventive maintenance and thereby reducing overall maintenance costs.
"""

# Optimizing hyperparameters for selected model using RandomizedSearchCV
if best_model is rf_model:
    param_dist = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
elif best_model is gb_model:
    param_dist = {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7]
    }
elif best_model is svm_model:
    param_dist = {
        'C': [0.1, 1, 10],
        'gamma': [1e-4, 1e-3, 1e-2],
        'kernel': ['linear', 'rbf']
    }

random_search = RandomizedSearchCV(estimator=best_model, param_distributions=param_dist, n_iter=50, cv=3, n_jobs=-1, verbose=2, random_state=42)
random_search.fit(X_train_pca, y_train)

# Best model after hyperparameter optimization
best_model = random_search.best_estimator_

print("Best Model Parameters:")
print(random_search.best_params_)

"""* Here the optimization of the best selected model is carried out"""

# Save the trained model for deployment to production
import joblib
joblib.dump(best_model, '/content/drive/MyDrive/Pruebas/Dataset_for_candidates/Modelo_Entrenado/modelo_entrenado.pkl')