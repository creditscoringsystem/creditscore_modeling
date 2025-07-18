# -*- coding: utf-8 -*-
"""ACS Modeling

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Atr7armdjD2qEiFibdxLtUtG6SCnIQaB
"""

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# Simulate dataset
def simulate_data(n=1000):
    np.random.seed(42)
    df = pd.DataFrame({
        "age": np.random.randint(18, 60, n),
        "education_level": np.random.choice([0, 1, 2], size=n),
        "employment_status": np.random.choice([0, 1], size=n),
        "monthly_income": np.random.randint(1000, 10000, n),
        "bill_payment_timely": np.random.choice([0, 1], size=n),
        "phone_minutes": np.random.randint(100, 2000, n),
        "sms_count": np.random.randint(10, 300, n),
        "social_media_score": np.random.randint(0, 101, n),
        "ecommerce_score": np.random.randint(0, 101, n)
    })
    df["label"] = (
        (df["monthly_income"] > 5000)
        & (df["employment_status"] == 1)
        & (df["bill_payment_timely"] == 1)
        & (df["ecommerce_score"] > 50)
    ).astype(int)
    return df

df = simulate_data()
print(df.info())

# PyTorch Dataset
class CreditDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.long)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# Deep Neural Network Model
class CreditNet(nn.Module):
    def __init__(self, input_dim):
        super(CreditNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.BatchNorm1d(32),
            nn.Linear(32, 2)
        )

    def forward(self, x):
        return self.net(x)

# Plotting utilities
def plot_confusion_matrix(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=labels, yticklabels=labels, cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig("confusion_matrix.png")
    plt.close()

def plot_loss_curve(losses):
    plt.figure()
    plt.plot(losses, marker='o')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training Loss Over Epochs")
    plt.tight_layout()
    plt.savefig("training_loss.png")
    plt.close()

# Train Model
def train_model(df):
    X = df.drop("label", axis=1).values
    y = df["label"].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    train_dataset = CreditDataset(X_train, y_train)
    test_dataset = CreditDataset(X_test, y_test)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32)

    model = CreditNet(X.shape[1])
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    model.train()
    loss_log = []
    for epoch in range(70):
        total_loss = 0
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        avg_loss = total_loss / len(train_loader)
        loss_log.append(avg_loss)
        print(f"Epoch {epoch+1}, Loss: {avg_loss:.4f}")

    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for batch_X, batch_y in test_loader:
            outputs = model(batch_X)
            preds = torch.argmax(outputs, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(batch_y.cpu().numpy())

    print(classification_report(all_labels, all_preds))
    plot_confusion_matrix(all_labels, all_preds, labels=["Bad", "Good"])
    plot_loss_curve(loss_log)

    torch.save(model.state_dict(), "credit_model.pt")
    joblib.dump(scaler, "scaler.pkl")

os.makedirs("plots", exist_ok=True)

df = simulate_data()

train_model(df)

pip install catboost

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, StackingClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
import warnings
warnings.filterwarnings("ignore")

# Simulate dataset
def simulate_data(n=1000):
    np.random.seed(42)
    df = pd.DataFrame({
        "age": np.random.randint(18, 60, n),
        "education_level": np.random.choice([0, 1, 2], size=n),
        "employment_status": np.random.choice([0, 1], size=n),
        "monthly_income": np.random.randint(1000, 10000, n),
        "bill_payment_timely": np.random.choice([0, 1], size=n),
        "phone_minutes": np.random.randint(100, 2000, n),
        "sms_count": np.random.randint(10, 300, n),
        "social_media_score": np.random.randint(0, 101, n),
        "ecommerce_score": np.random.randint(0, 101, n)
    })
    df["label"] = (
        (df["monthly_income"] > 5000)
        & (df["employment_status"] == 1)
        & (df["bill_payment_timely"] == 1)
        & (df["ecommerce_score"] > 50)
    ).astype(int)
    return df

# Train and evaluate models
def train_models(X_train, X_test, y_train, y_test):
    results = {}

    models = {
        "LogisticRegression": LogisticRegression(),
        "RandomForest": RandomForestClassifier(n_estimators=100),
        "ExtraTrees": ExtraTreesClassifier(n_estimators=100),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
        "LightGBM": LGBMClassifier(),
        "CatBoost": CatBoostClassifier(verbose=0)
    }

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        results[name] = {
            "accuracy": accuracy_score(y_test, y_pred),
            "f1": f1_score(y_test, y_pred),
            "roc_auc": roc_auc_score(y_test, y_proba)
        }

    # Stacking Ensemble
    base_models = [(k, v) for k, v in models.items() if k != "LogisticRegression"]
    stack = StackingClassifier(estimators=base_models, final_estimator=LogisticRegression())
    stack.fit(X_train, y_train)
    y_pred = stack.predict(X_test)
    y_proba = stack.predict_proba(X_test)[:, 1]
    results["Stacking"] = {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba)
    }

    return results

# Plot results
def plot_results(results):
    df = pd.DataFrame(results).T
    df.sort_values("roc_auc", ascending=False, inplace=True)
    df.plot(kind="bar", figsize=(12, 6))
    plt.title("Model Comparison")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.savefig("model_comparison.png")
    plt.close()

df = simulate_data()
X = df.drop("label", axis=1)
y = df["label"]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

results = train_models(X_train, X_test, y_train, y_test)
for model, scores in results.items():
  print(f"{model}: {scores}")

plot_results(results)

"""# Performance

| Model          | Accuracy | F1     | ROC-AUC | Pros                                     |
| -------------- | -------- | ------ | ------- | ---------------------------------------- |
| **DCNN**       | 0.99     | 0.96   | \~0.98  | Strong overall, deep learning extensible |
| **LightGBM**   | 0.995    | 0.96   | 1.0     | Fast, accurate, interpretable            |
| **CatBoost**   | 0.995    | 0.96   | 1.0     | Best for categorical features            |
| **Stacking**   | 0.995    | 0.96   | 1.0     | Combines strengths of all models         |
| **ExtraTrees** | 0.99     | 0.9167 | 0.9998  | Robust, less overfitting                 |


--> Use Stacking or LightGBM as primary, keep DCNN for fallback or future upgrade.
"""

