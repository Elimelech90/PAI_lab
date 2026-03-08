
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os

# ============================================================
# 0.  CONFIGURATION
# ============================================================
TRAIN_PATH  = "train.csv"
TEST_PATH   = "test.csv"
OUTPUT_PATH = "submission.csv"

print("=" * 60)
print("  SPACESHIP TITANIC - PAI Lab 2")
print("=" * 60)

# ============================================================
# 1.  LOAD DATA
# ============================================================
if not os.path.exists(TRAIN_PATH):
    print("\n[!] train.csv not found - generating synthetic demo data ...")
    print("    Download the real data from:")
    print("    https://www.kaggle.com/competitions/spaceship-titanic\n")

    np.random.seed(42)
    n = 8693
    cabins = ["{}/{}{}".format(
        np.random.choice(['A','B','C','D','E','F','G']),
        np.random.randint(1, 300),
        np.random.choice(['P','S'])
    ) for _ in range(n)]

    df_train = pd.DataFrame({
        "PassengerId":    ["{:04d}_{:02d}".format(i, np.random.randint(1,3)) for i in range(1, n+1)],
        "HomePlanet":     np.random.choice(["Earth","Europa","Mars", np.nan], n, p=[0.42,0.36,0.20,0.02]),
        "CryoSleep":      np.random.choice([True, False, np.nan], n, p=[0.35,0.63,0.02]),
        "Cabin":          cabins,
        "Destination":    np.random.choice(["TRAPPIST-1e","55 Cancri e","PSO J318.5-22", np.nan], n, p=[0.49,0.33,0.17,0.01]),
        "Age":            np.random.choice(list(range(0,80)) + [np.nan], n),
        "VIP":            np.random.choice([True, False, np.nan], n, p=[0.02,0.96,0.02]),
        "RoomService":    np.random.choice(list(range(0, 15000)) + [np.nan], n),
        "FoodCourt":      np.random.choice(list(range(0, 30000)) + [np.nan], n),
        "ShoppingMall":   np.random.choice(list(range(0, 25000)) + [np.nan], n),
        "Spa":            np.random.choice(list(range(0, 20000)) + [np.nan], n),
        "VRDeck":         np.random.choice(list(range(0, 25000)) + [np.nan], n),
        "Name":           ["Person {}".format(i) for i in range(n)],
    })

    # Simulate realistic transport odds
    transported_prob = (
        0.5 +
        (df_train["CryoSleep"] == True).astype(float) * 0.3 +
        (df_train["HomePlanet"] == "Europa").astype(float) * 0.1 -
        (df_train["VIP"] == True).astype(float) * 0.1
    ).clip(0.1, 0.9)
    df_train["Transported"] = np.random.binomial(1, transported_prob).astype(bool)

    n_test = 4277
    df_test = df_train.drop("Transported", axis=1).sample(n_test, replace=True).reset_index(drop=True)
    df_test["PassengerId"] = ["{:04d}_{:02d}".format(i, np.random.randint(1,3)) for i in range(9000, 9000+n_test)]
    demo_mode = True
else:
    print("\n[OK] Loading " + TRAIN_PATH + " ...")
    df_train = pd.read_csv(TRAIN_PATH)
    df_test  = pd.read_csv(TEST_PATH)
    demo_mode = False

print("    Train shape : " + str(df_train.shape))
print("    Test shape  : " + str(df_test.shape))
print("    Transported rate: {:.1f}%".format(df_train["Transported"].mean() * 100))

# ============================================================
# 2.  EXPLORATORY DATA ANALYSIS
# ============================================================
print("\n" + "-" * 40)
print("  EXPLORATORY DATA ANALYSIS")
print("-" * 40)

print("\nDataset Info:")
print("  Columns     : " + str(df_train.shape[1]))
print("  Rows        : " + str(df_train.shape[0]))
print("  Transported : " + str(df_train["Transported"].sum()) + " passengers")
print("  Not Transported : " + str((~df_train["Transported"]).sum()) + " passengers")

missing_pct = (df_train.isnull().sum() / len(df_train) * 100).sort_values(ascending=False)
missing_pct = missing_pct[missing_pct > 0]
if len(missing_pct):
    print("\nMissing values (%):")
    for col, pct in missing_pct.items():
        print("  {:20s} : {:.1f}%".format(col, pct))

# ---- EDA PLOTS ----
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle("Spaceship Titanic - EDA", fontsize=16, fontweight='bold')
fig.patch.set_facecolor('#f5f5f5')

colors_t = ['#e74c3c', '#2ecc71']
labels_t = ['Not Transported', 'Transported']

# 1. Transport balance
t_counts = df_train["Transported"].value_counts()
axes[0, 0].bar(labels_t, [t_counts.get(False, 0), t_counts.get(True, 0)],
               color=colors_t, edgecolor='white', width=0.5)
axes[0, 0].set_title("Transport Status Balance")
axes[0, 0].set_ylabel("Count")
for i, v in enumerate([t_counts.get(False,0), t_counts.get(True,0)]):
    axes[0, 0].text(i, v + 50, str(v), ha='center', fontweight='bold')

# 2. Home Planet vs Transport
if "HomePlanet" in df_train.columns:
    hp_data = df_train.groupby("HomePlanet")["Transported"].mean() * 100
    bars = axes[0, 1].bar(hp_data.index, hp_data.values, color='#3498db', edgecolor='white')
    axes[0, 1].set_title("Transport Rate by Home Planet (%)")
    axes[0, 1].set_ylabel("Transport Rate (%)")
    axes[0, 1].set_ylim(0, 100)
    for bar, val in zip(bars, hp_data.values):
        axes[0, 1].text(bar.get_x() + bar.get_width()/2, val + 1,
                        "{:.1f}%".format(val), ha='center', fontsize=9)

# 3. CryoSleep vs Transport
if "CryoSleep" in df_train.columns:
    cryo_data = df_train.groupby("CryoSleep")["Transported"].mean() * 100
    axes[0, 2].bar([str(k) for k in cryo_data.index], cryo_data.values,
                   color=['#e67e22', '#9b59b6'], edgecolor='white')
    axes[0, 2].set_title("Transport Rate by CryoSleep (%)")
    axes[0, 2].set_ylabel("Transport Rate (%)")
    axes[0, 2].set_ylim(0, 100)
    axes[0, 2].set_xlabel("CryoSleep")
    for i, val in enumerate(cryo_data.values):
        axes[0, 2].text(i, val + 1, "{:.1f}%".format(val), ha='center', fontsize=10)

# 4. Age distribution
if "Age" in df_train.columns:
    transported_ages = df_train[df_train["Transported"] == True]["Age"].dropna()
    not_transported_ages = df_train[df_train["Transported"] == False]["Age"].dropna()
    axes[1, 0].hist(not_transported_ages, bins=40, alpha=0.6, color='#e74c3c', label='Not Transported')
    axes[1, 0].hist(transported_ages, bins=40, alpha=0.6, color='#2ecc71', label='Transported')
    axes[1, 0].set_title("Age Distribution by Transport Status")
    axes[1, 0].set_xlabel("Age")
    axes[1, 0].set_ylabel("Count")
    axes[1, 0].legend()

# 5. Spending vs Transport
spend_cols = [c for c in ["RoomService","FoodCourt","ShoppingMall","Spa","VRDeck"] if c in df_train.columns]
if spend_cols:
    transported_spend = df_train[df_train["Transported"] == True][spend_cols].mean()
    not_transported_spend = df_train[df_train["Transported"] == False][spend_cols].mean()
    x = range(len(spend_cols))
    axes[1, 1].bar([i - 0.2 for i in x], not_transported_spend.values, width=0.4,
                   color='#e74c3c', label='Not Transported', edgecolor='white')
    axes[1, 1].bar([i + 0.2 for i in x], transported_spend.values, width=0.4,
                   color='#2ecc71', label='Transported', edgecolor='white')
    axes[1, 1].set_title("Avg Spending by Transport Status")
    axes[1, 1].set_ylabel("Avg Spend")
    axes[1, 1].set_xticks(list(x))
    axes[1, 1].set_xticklabels([c[:5] for c in spend_cols], fontsize=8)
    axes[1, 1].legend()

# 6. Destination vs Transport
if "Destination" in df_train.columns:
    dest_data = df_train.groupby("Destination")["Transported"].mean() * 100
    bars = axes[1, 2].barh(dest_data.index, dest_data.values, color='#1abc9c', edgecolor='white')
    axes[1, 2].set_title("Transport Rate by Destination (%)")
    axes[1, 2].set_xlabel("Transport Rate (%)")
    axes[1, 2].set_xlim(0, 100)
    for bar, val in zip(bars, dest_data.values):
        axes[1, 2].text(val + 0.5, bar.get_y() + bar.get_height()/2,
                        "{:.1f}%".format(val), va='center', fontsize=9)

plt.tight_layout()
eda_path = "eda_plots.png"
plt.savefig(eda_path, dpi=150, bbox_inches="tight")
plt.close()
print("\n[OK] EDA plots saved: " + eda_path)

# ============================================================
# 3.  FEATURE ENGINEERING & PREPROCESSING
# ============================================================
print("\n" + "-" * 40)
print("  FEATURE ENGINEERING")
print("-" * 40)

passenger_ids = df_test["PassengerId"].copy()
y = df_train["Transported"].astype(int)

drop_cols = ["PassengerId", "Transported", "Name"]
df_train_proc = df_train.drop([c for c in drop_cols if c in df_train.columns], axis=1)
df_test_proc  = df_test.drop([c for c in ["PassengerId", "Name"] if c in df_test.columns], axis=1)

df_test_proc = df_test_proc.reindex(columns=df_train_proc.columns)
n_train = len(df_train_proc)
combined = pd.concat([df_train_proc, df_test_proc], axis=0).reset_index(drop=True)

# --- Feature Engineering ---
# Split Cabin into Deck / Num / Side
if "Cabin" in combined.columns:
    cabin_split = combined["Cabin"].str.split("/", expand=True)
    combined["CabinDeck"] = cabin_split[0] if 0 in cabin_split.columns else np.nan
    combined["CabinSide"] = cabin_split[2] if 2 in cabin_split.columns else np.nan
    combined.drop("Cabin", axis=1, inplace=True)
    print("  [OK] Cabin split into CabinDeck and CabinSide")

# Total spending feature
spend_cols = [c for c in ["RoomService","FoodCourt","ShoppingMall","Spa","VRDeck"] if c in combined.columns]
if spend_cols:
    combined["TotalSpend"] = combined[spend_cols].fillna(0).sum(axis=1)
    combined["IsSpender"]  = (combined["TotalSpend"] > 0).astype(int)
    print("  [OK] Created TotalSpend and IsSpender features")

# Boolean columns to int
for col in ["CryoSleep", "VIP"]:
    if col in combined.columns:
        combined[col] = combined[col].map({True: 1, False: 0, "True": 1, "False": 0})

# Encode categoricals
cat_cols = combined.select_dtypes(include=["object", "bool"]).columns.tolist()
le = LabelEncoder()
for col in cat_cols:
    combined[col] = combined[col].fillna("Missing")
    combined[col] = le.fit_transform(combined[col].astype(str))

# Impute numerics
num_cols = combined.select_dtypes(include=[np.number]).columns.tolist()
imputer = SimpleImputer(strategy="median")
for _col in combined.columns:
    _med = combined[_col].median() if combined[_col].dtype.kind in ['f','i','u'] else 0
    combined[_col] = combined[_col].fillna(_med)
# Final safety: fill any remaining NaN
combined = combined.fillna(0)

print("  [OK] Encoded " + str(len(cat_cols)) + " categorical columns")
print("  [OK] Imputed missing values")
print("  [OK] Final feature count: " + str(combined.shape[1]))

X_train_full = combined.iloc[:n_train].values
X_test_final = combined.iloc[n_train:].values

# Scale for models that need it
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_full)
X_test_scaled  = scaler.transform(X_test_final)

# Train/val split for evaluation
X_tr, X_val, y_tr, y_val = train_test_split(
    X_train_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# ============================================================
# 4.  MODEL TRAINING
# ============================================================
print("\n" + "-" * 40)
print("  MODEL TRAINING")
print("-" * 40)

kf = KFold(n_splits=5, shuffle=True, random_state=42)

def cv_accuracy(model, X, y):
    scores = cross_val_score(model, X, y, scoring="accuracy", cv=kf)
    return scores

results = {}

# Model 1: Naive Bayes (required by Lab 2)
print("\n  [1] Naive Bayes ...")
nb = GaussianNB()
nb_scores = cv_accuracy(nb, X_train_scaled, y)
nb.fit(X_tr, y_tr)
nb_val_acc = accuracy_score(y_val, nb.predict(X_val))
results["Naive Bayes"] = {"cv": nb_scores.mean(), "val": nb_val_acc, "model": nb}
print("      CV Accuracy : {:.4f} +/- {:.4f}".format(nb_scores.mean(), nb_scores.std()))
print("      Val Accuracy: {:.4f}".format(nb_val_acc))

# Model 2: Decision Tree (required by Lab 2)
print("\n  [2] Decision Tree ...")
dt = DecisionTreeClassifier(max_depth=8, min_samples_leaf=10, random_state=42)
dt_scores = cv_accuracy(dt, X_train_scaled, y)
dt.fit(X_tr, y_tr)
dt_val_acc = accuracy_score(y_val, dt.predict(X_val))
results["Decision Tree"] = {"cv": dt_scores.mean(), "val": dt_val_acc, "model": dt}
print("      CV Accuracy : {:.4f} +/- {:.4f}".format(dt_scores.mean(), dt_scores.std()))
print("      Val Accuracy: {:.4f}".format(dt_val_acc))

# Model 3: Logistic Regression
print("\n  [3] Logistic Regression ...")
lr = LogisticRegression(max_iter=1000, C=1.0, random_state=42)
lr_scores = cv_accuracy(lr, X_train_scaled, y)
lr.fit(X_tr, y_tr)
lr_val_acc = accuracy_score(y_val, lr.predict(X_val))
results["Logistic Regression"] = {"cv": lr_scores.mean(), "val": lr_val_acc, "model": lr}
print("      CV Accuracy : {:.4f} +/- {:.4f}".format(lr_scores.mean(), lr_scores.std()))
print("      Val Accuracy: {:.4f}".format(lr_val_acc))

# Model 4: Random Forest
print("\n  [4] Random Forest ...")
rf = RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1)
rf_scores = cv_accuracy(rf, X_train_scaled, y)
rf.fit(X_tr, y_tr)
rf_val_acc = accuracy_score(y_val, rf.predict(X_val))
results["Random Forest"] = {"cv": rf_scores.mean(), "val": rf_val_acc, "model": rf}
print("      CV Accuracy : {:.4f} +/- {:.4f}".format(rf_scores.mean(), rf_scores.std()))
print("      Val Accuracy: {:.4f}".format(rf_val_acc))

# Model 5: Gradient Boosting
print("\n  [5] Gradient Boosting ...")
gb = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1,
                                max_depth=5, random_state=42)
gb_scores = cv_accuracy(gb, X_train_scaled, y)
gb.fit(X_tr, y_tr)
gb_val_acc = accuracy_score(y_val, gb.predict(X_val))
results["Gradient Boosting"] = {"cv": gb_scores.mean(), "val": gb_val_acc, "model": gb}
print("      CV Accuracy : {:.4f} +/- {:.4f}".format(gb_scores.mean(), gb_scores.std()))
print("      Val Accuracy: {:.4f}".format(gb_val_acc))

best_name = max(results, key=lambda k: results[k]["cv"])
print("\n  [BEST] " + best_name + " (CV = {:.4f})".format(results[best_name]["cv"]))

# ============================================================
# 5.  DETAILED EVALUATION OF BEST MODEL
# ============================================================
print("\n" + "-" * 40)
print("  DETAILED EVALUATION")
print("-" * 40)

best_model = results[best_name]["model"]
y_pred_val = best_model.predict(X_val)

print("\nClassification Report (" + best_name + "):")
print(classification_report(y_val, y_pred_val,
                             target_names=["Not Transported", "Transported"]))

# ============================================================
# 6.  ENSEMBLE VOTING CLASSIFIER
# ============================================================
print("\n" + "-" * 40)
print("  ENSEMBLE (VOTING CLASSIFIER)")
print("-" * 40)

ensemble = VotingClassifier(estimators=[
    ("rf", RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1)),
    ("gb", GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)),
    ("lr", LogisticRegression(max_iter=1000, C=1.0, random_state=42)),
], voting="soft")

ensemble_scores = cv_accuracy(ensemble, X_train_scaled, y)
print("  Ensemble CV Accuracy: {:.4f} +/- {:.4f}".format(
    ensemble_scores.mean(), ensemble_scores.std()))

ensemble.fit(X_train_scaled, y)
final_preds = ensemble.predict(X_test_scaled).astype(bool)

# ============================================================
# 7.  RESULT PLOTS
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Model Results - Spaceship Titanic", fontsize=14, fontweight='bold')
fig.patch.set_facecolor('#f5f5f5')

# Plot 1: Model CV Comparison
model_names = list(results.keys())
cv_scores   = [results[m]["cv"] for m in model_names]
val_scores  = [results[m]["val"] for m in model_names]
x = range(len(model_names))

axes[0].bar([i - 0.2 for i in x], cv_scores, width=0.35,
            color='#3498db', label='CV Accuracy', edgecolor='white')
axes[0].bar([i + 0.2 for i in x], val_scores, width=0.35,
            color='#e67e22', label='Val Accuracy', edgecolor='white')
axes[0].set_title("Model Accuracy Comparison")
axes[0].set_ylabel("Accuracy")
axes[0].set_xticks(list(x))
axes[0].set_xticklabels([m.replace(" ", "\n") for m in model_names], fontsize=8)
axes[0].set_ylim(0.5, 1.0)
axes[0].legend()
axes[0].axhline(y=0.5, color='red', linestyle='--', alpha=0.3)

# Plot 2: Confusion Matrix of best model
cm = confusion_matrix(y_val, y_pred_val)
im = axes[1].imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
axes[1].set_title("Confusion Matrix\n(" + best_name + ")")
axes[1].set_xlabel("Predicted Label")
axes[1].set_ylabel("True Label")
axes[1].set_xticks([0, 1])
axes[1].set_yticks([0, 1])
axes[1].set_xticklabels(["Not Trans.", "Trans."])
axes[1].set_yticklabels(["Not Trans.", "Trans."])
thresh = cm.max() / 2
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        axes[1].text(j, i, str(cm[i, j]), ha='center', va='center',
                     color='white' if cm[i, j] > thresh else 'black', fontsize=14)

# Plot 3: Final prediction distribution
pred_counts = pd.Series(final_preds).value_counts()
axes[2].pie([pred_counts.get(False, 0), pred_counts.get(True, 0)],
            labels=["Not Transported", "Transported"],
            colors=['#e74c3c', '#2ecc71'],
            autopct='%1.1f%%', startangle=90,
            wedgeprops=dict(edgecolor='white', linewidth=2))
axes[2].set_title("Final Prediction Distribution\n(Test Set)")

plt.tight_layout()
result_path = "model_results.png"
plt.savefig(result_path, dpi=150, bbox_inches="tight")
plt.close()
print("[OK] Results plot saved: " + result_path)

# Feature importance (if RF or GB is best)
if hasattr(best_model, "feature_importances_"):
    feat_names = combined.columns.tolist()
    importances = pd.Series(best_model.feature_importances_, index=feat_names)
    top15 = importances.sort_values(ascending=False).head(15)

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#f5f5f5')
    colors_fi = plt.cm.viridis(np.linspace(0.3, 0.9, len(top15)))
    top15.plot(kind="barh", ax=ax, color=colors_fi, edgecolor='white')
    ax.set_title("Top 15 Feature Importances (" + best_name + ")", fontsize=13, fontweight='bold')
    ax.set_xlabel("Importance Score")
    ax.invert_yaxis()
    plt.tight_layout()
    fi_path = "feature_importance.png"
    plt.savefig(fi_path, dpi=150, bbox_inches="tight")
    plt.close()
    print("[OK] Feature importance plot saved: " + fi_path)

# ============================================================
# 8.  SAVE SUBMISSION
# ============================================================
submission = pd.DataFrame({
    "PassengerId": passenger_ids,
    "Transported": final_preds
})
submission.to_csv(OUTPUT_PATH, index=False)
print("[OK] Submission saved: " + OUTPUT_PATH)
print("     Rows: " + str(len(submission)))

# ============================================================
# 9.  SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("  RESULTS SUMMARY")
print("=" * 60)
print("\n  Model                  | CV Acc  | Val Acc")
print("  " + "-" * 45)
for name, res in results.items():
    marker = " <-- BEST" if name == best_name else ""
    print("  {:22s} | {:.4f}  | {:.4f}{}".format(
        name, res["cv"], res["val"], marker))
print("  {:22s} | {:.4f}  | ---".format("Ensemble (Voting)", ensemble_scores.mean()))

print("\n  DONE! Files generated:")
print("    " + eda_path)
print("    " + result_path)
print("    " + OUTPUT_PATH + "  <- upload this to Kaggle")
if demo_mode:
    print("\n  [!] Running on SYNTHETIC data.")
    print("  [!] Download real data from Kaggle for actual results.")
print("=" * 60)
