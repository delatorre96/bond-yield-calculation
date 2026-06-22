# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 22:30:27 2026

@author: ignacio.delatorre
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    accuracy_score,
    confusion_matrix,
    roc_curve,
    auc
)
import matplotlib.pyplot as plt


df = pd.read_csv('data_tmp/series_data_2026-06-14.csv')

X = df[['Interest', 'IPC_start', 'ExchangeRate_start']]
y = df[['rentability']]
y.iloc[:, 0] = (y.iloc[:, 0] >= np.median(y)).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )


hyperparams = {
        "random_state": 0,
        "n_estimators": 200,
        "max_depth": 3,
        "learning_rate": 0.01,
        "subsample": 0.8,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
    }

gbm = GradientBoostingClassifier(**hyperparams)

gbm.fit(X_train, y_train)

# Predictions
y_train_pred = gbm.predict(X_train)
y_test_pred = gbm.predict(X_test)
y_test_prob = gbm.predict_proba(X_test)[:, 1]

# Accuracy
train_acc = accuracy_score(y_train, y_train_pred)
test_acc = accuracy_score(y_test, y_test_pred)

print('accuracy in train:', train_acc)
print('accuracy in test:', test_acc)

# ROC and AUC
fpr, tpr, thresholds = roc_curve(y_test, y_test_prob)
roc_auc = auc(fpr, tpr)

# Confusion matrix
cm = confusion_matrix(y_test, y_test_pred)
TN, FP, FN, TP = cm.ravel()

TNR = TN / (TN + FP) if (TN + FP) > 0 else np.nan
FNR = FN / (FN + TP) if (FN + TP) > 0 else np.nan
TPR = TP / (TP + FN) if (TP + FN) > 0 else np.nan
FPR = FP / (FP + TN) if (FP + TN) > 0 else np.nan

# Print diagnostics
print(f"Train accuracy : {train_acc:.4f}")
print(f"Test accuracy  : {test_acc:.4f}")
print(f"AUC            : {roc_auc:.4f}")
print(f"TNR            : {TNR:.4f}")
print(f"FNR            : {FNR:.4f}")
print(f"TPR            : {TPR:.4f}")
print(f"FPR            : {FPR:.4f}")

# ROC curve
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, lw=2, label=f"AUC = {roc_auc:.3f}")
plt.plot([0, 1], [0, 1], "--", label="Random classifier")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Gradient Boosting")
plt.legend(loc="lower right")
plt.grid(True)
plt.show()


###########3 Shap values ##############

import shap

explainer = shap.TreeExplainer(gbm)

shap_values = explainer.shap_values(X_test)

shap.summary_plot(
    shap_values,
    X_test,
    feature_names=X_test.columns
)

shap.summary_plot(
    shap_values,
    X_test,
    plot_type="bar"
)

shap.dependence_plot(
    "Interest",
    shap_values,
    X_test
)
shap.dependence_plot(
    "IPC_start",
    shap_values,
    X_test
)


######### PDP ########3

from sklearn.inspection import PartialDependenceDisplay

fig, ax = plt.subplots(figsize=(6,4))

PartialDependenceDisplay.from_estimator(
    gbm,
    X_test,
    features=['Interest'],
    ax=ax
)

plt.show()



fig, ax = plt.subplots(figsize=(12,4))

PartialDependenceDisplay.from_estimator(
    gbm,
    X_test,
    features=['Interest', 'IPC_start', 'ExchangeRate_start']
)

plt.tight_layout()
plt.show()


PartialDependenceDisplay.from_estimator(
    gbm,
    X_test,
    features=[('Interest', 'ExchangeRate_start')]
)

plt.show()


