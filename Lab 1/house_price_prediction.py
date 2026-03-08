"""
============================================================
  Lab 1 Task - Kaggle House Price Prediction
  Course  : Programming for Artificial Intelligence
  Dataset : https://www.kaggle.com/competitions/home-data-for-ml-course
============================================================

HOW TO USE:
  1. Download train.csv and test.csv from Kaggle (link above)
  2. Place them in the same folder as this script
  3. Run: python house_price_prediction.py
  4. A file called submission.csv will be generated (upload to Kaggle)
============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import cross_val_score, KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import os

# ---------------------------------------------
# 0.  CONFIGURATION
# ---------------------------------------------
TRAIN_PATH = "train.csv"
TEST_PATH  = "test.csv"
OUTPUT_PATH = "submission.csv"

print("=" * 60)
print("  HOUSE PRICE PREDICTION - PAI Lab 1")
print("=" * 60)

# ---------------------------------------------
# 1.  LOAD DATA
# ---------------------------------------------
if not os.path.exists(TRAIN_PATH):
    print("\n[!] train.csv not found - generating synthetic demo data ...")
    print("    Download the real data from:")
    print("    https://www.kaggle.com/competitions/home-data-for-ml-course\n")

    # Synthetic dataset that mirrors the Kaggle structure
    np.random.seed(42)
    n = 1460
    df_train = pd.DataFrame({
        "Id":           range(1, n+1),
        "OverallQual":  np.random.randint(1, 11, n),
        "GrLivArea":    np.random.randint(500, 4000, n),
        "GarageCars":   np.random.randint(0, 5, n),
        "TotalBsmtSF":  np.random.randint(0, 3000, n),
        "FullBath":     np.random.randint(0, 4, n),
        "YearBuilt":    np.random.randint(1870, 2011, n),
        "YearRemodAdd": np.random.randint(1950, 2011, n),
        "LotArea":      np.random.randint(1300, 215000, n),
        "Neighborhood": np.random.choice(["NAmes","CollgCr","OldTown","Edwards","Somerst"], n),
        "HouseStyle":   np.random.choice(["1Story","2Story","1.5Fin","SLvl"], n),
        "ExterQual":    np.random.choice(["Ex","Gd","TA","Fa"], n),
        "KitchenQual":  np.random.choice(["Ex","Gd","TA","Fa"], n),
        "FireplaceQu":  np.random.choice(["Ex","Gd","TA","Fa", np.nan], n),
        "GarageType":   np.random.choice(["Attchd","Detchd","BuiltIn", np.nan], n),
        "MasVnrArea":   np.random.randint(0, 1600, n).astype(float),
    })
    # Realistic price based on features
    noise = np.random.normal(0, 15000, n)
    df_train["SalePrice"] = (
        df_train["OverallQual"] * 15000 +
        df_train["GrLivArea"]   * 55 +
        df_train["GarageCars"]  * 8000 +
        df_train["TotalBsmtSF"] * 30 +
        df_train["YearBuilt"]   * 200 +
        50000 + noise
    ).clip(50000, 755000).astype(int)

    n_test = 1459
    df_test = df_train.drop("SalePrice", axis=1).sample(n_test, replace=True).reset_index(drop=True)
    df_test["Id"] = range(1461, 1461 + n_test)
    demo_mode = True
else:
    print(f"\n[OK] Loading {TRAIN_PATH} ...")
    df_train = pd.read_csv(TRAIN_PATH)
    df_test  = pd.read_csv(TEST_PATH)
    demo_mode = False

print(f"    Train shape : {df_train.shape}")
print(f"    Test shape  : {df_test.shape}")


# ---------------------------------------------
# 2.  EXPLORATORY DATA ANALYSIS
# ---------------------------------------------
print("\n" + "-" * 40)
print("  EXPLORATORY DATA ANALYSIS")
print("-" * 40)

print(f"\nSalePrice Stats:")
print(df_train["SalePrice"].describe().to_string())

# Missing values summary
missing = df_train.isnull().sum()
missing = missing[missing > 0].sort_values(ascending=False)
if len(missing):
    print(f"\nTop columns with missing values:")
    print(missing.head(10).to_string())

# -- EDA Plots ----------------------------------
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle("House Price Prediction - EDA", fontsize=16, fontweight='bold', y=1.01)
fig.patch.set_facecolor('#f8f8f8')

# 1. Sale Price Distribution
axes[0, 0].hist(df_train["SalePrice"], bins=50, color="#6a5acd", edgecolor="white", alpha=0.85)
axes[0, 0].set_title("Sale Price Distribution")
axes[0, 0].set_xlabel("Sale Price ($)")
axes[0, 0].set_ylabel("Count")
axes[0, 0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# 2. Log Sale Price
axes[0, 1].hist(np.log1p(df_train["SalePrice"]), bins=50, color="#20b2aa", edgecolor="white", alpha=0.85)
axes[0, 1].set_title("Log(Sale Price) Distribution")
axes[0, 1].set_xlabel("log(Sale Price)")

# 3. Overall Quality vs Price
if "OverallQual" in df_train.columns:
    qual_price = df_train.groupby("OverallQual")["SalePrice"].median()
    axes[0, 2].bar(qual_price.index, qual_price.values, color="#ff7f50", edgecolor="white")
    axes[0, 2].set_title("Median Price by Overall Quality")
    axes[0, 2].set_xlabel("Overall Quality (1-10)")
    axes[0, 2].set_ylabel("Median Sale Price ($)")
    axes[0, 2].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# 4. GrLivArea vs Price
if "GrLivArea" in df_train.columns:
    axes[1, 0].scatter(df_train["GrLivArea"], df_train["SalePrice"],
                       alpha=0.4, color="#4682b4", s=10)
    axes[1, 0].set_title("Living Area vs Sale Price")
    axes[1, 0].set_xlabel("Above-grade Living Area (sqft)")
    axes[1, 0].set_ylabel("Sale Price ($)")
    axes[1, 0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# 5. YearBuilt vs Price
if "YearBuilt" in df_train.columns:
    year_price = df_train.groupby("YearBuilt")["SalePrice"].median()
    axes[1, 1].plot(year_price.index, year_price.values, color="#dc143c", linewidth=1.5)
    axes[1, 1].fill_between(year_price.index, year_price.values, alpha=0.15, color="#dc143c")
    axes[1, 1].set_title("Median Price by Year Built")
    axes[1, 1].set_xlabel("Year Built")
    axes[1, 1].set_ylabel("Median Sale Price ($)")
    axes[1, 1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

# 6. Correlation heatmap (numeric only)
num_cols = df_train.select_dtypes(include=[np.number]).columns.tolist()
if "SalePrice" in num_cols:
    corr = df_train[num_cols].corr()["SalePrice"].drop("SalePrice").sort_values()
    top_corr = pd.concat([corr.head(5), corr.tail(5)])
    colors = ["#e74c3c" if v < 0 else "#2ecc71" for v in top_corr.values]
    axes[1, 2].barh(top_corr.index, top_corr.values, color=colors)
    axes[1, 2].set_title("Top Feature Correlations\nwith Sale Price")
    axes[1, 2].set_xlabel("Pearson Correlation")
    axes[1, 2].axvline(0, color="black", linewidth=0.8)

plt.tight_layout()
eda_path = "eda_plots.png"
plt.savefig(eda_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"\n[OK] EDA plots saved → {eda_path}")


# ---------------------------------------------
# 3.  FEATURE ENGINEERING & PREPROCESSING
# ---------------------------------------------
print("\n" + "-" * 40)
print("  FEATURE ENGINEERING")
print("-" * 40)

test_ids = df_test["Id"].copy()

# Combine train + test for consistent encoding
y = np.log1p(df_train["SalePrice"])   # log-transform target
df_train_proc = df_train.drop(["Id", "SalePrice"], axis=1)
df_test_proc  = df_test.drop(["Id"], axis=1)

# Align columns
df_test_proc = df_test_proc.reindex(columns=df_train_proc.columns)
n_train = len(df_train_proc)
combined = pd.concat([df_train_proc, df_test_proc], axis=0).reset_index(drop=True)

# -- New features --
if "YearBuilt" in combined.columns and "YearRemodAdd" in combined.columns:
    combined["Age"]         = 2010 - combined["YearBuilt"]
    combined["RemodAge"]    = 2010 - combined["YearRemodAdd"]
    combined["WasRemodeled"]= (combined["YearBuilt"] != combined["YearRemodAdd"]).astype(int)

if "GrLivArea" in combined.columns and "TotalBsmtSF" in combined.columns:
    combined["TotalSF"] = combined["GrLivArea"] + combined["TotalBsmtSF"]

if "FullBath" in combined.columns and "GarageCars" in combined.columns:
    combined["TotalBath"] = combined.get("FullBath", 0) + 0.5 * combined.get("HalfBath", 0)

print("  OK Created: Age, RemodAge, WasRemodeled, TotalSF, TotalBath")

# -- Encode categoricals --
cat_cols = combined.select_dtypes(include=["object"]).columns.tolist()
le = LabelEncoder()
for col in cat_cols:
    combined[col] = combined[col].fillna("Missing")
    combined[col] = le.fit_transform(combined[col].astype(str))

# -- Impute numerics --
num_cols = combined.select_dtypes(include=[np.number]).columns.tolist()
imputer = SimpleImputer(strategy="median")
combined[num_cols] = imputer.fit_transform(combined[num_cols])

print(f"  OK Encoded {len(cat_cols)} categorical columns")
print(f"  OK Imputed {len(num_cols)} numeric columns")
print(f"  OK Final feature count: {combined.shape[1]}")

# Split back
X_train = combined.iloc[:n_train]
X_test  = combined.iloc[n_train:]


# ---------------------------------------------
# 4.  MODEL TRAINING
# ---------------------------------------------
print("\n" + "-" * 40)
print("  MODEL TRAINING")
print("-" * 40)

kf = KFold(n_splits=5, shuffle=True, random_state=42)

def rmse_cv(model, X, y):
    scores = cross_val_score(model, X, y,
                             scoring="neg_mean_squared_error",
                             cv=kf)
    return np.sqrt(-scores)

# Model 1: Random Forest
print("\n  [1] Random Forest ...")
rf = RandomForestRegressor(n_estimators=200, max_depth=15,
                            min_samples_leaf=3, random_state=42, n_jobs=-1)
rf_scores = rmse_cv(rf, X_train, y)
print(f"      CV RMSE: {rf_scores.mean():.4f} ± {rf_scores.std():.4f}")

# Model 2: Gradient Boosting
print("\n  [2] Gradient Boosting ...")
gb = GradientBoostingRegressor(n_estimators=300, learning_rate=0.05,
                                max_depth=4, subsample=0.8,
                                random_state=42)
gb_scores = rmse_cv(gb, X_train, y)
print(f"      CV RMSE: {gb_scores.mean():.4f} ± {gb_scores.std():.4f}")

# Model 3: Ridge Regression
print("\n  [3] Ridge Regression ...")
ridge = Ridge(alpha=10)
ridge_scores = rmse_cv(ridge, X_train, y)
print(f"      CV RMSE: {ridge_scores.mean():.4f} ± {ridge_scores.std():.4f}")

# Pick best model
scores = {
    "Random Forest":      rf_scores.mean(),
    "Gradient Boosting":  gb_scores.mean(),
    "Ridge Regression":   ridge_scores.mean(),
}
best_name = min(scores, key=scores.get)
print(f"\n  * Best model: {best_name} (RMSE = {scores[best_name]:.4f})")


# ---------------------------------------------
# 5.  FINAL FIT & ENSEMBLE
# ---------------------------------------------
print("\n" + "-" * 40)
print("  ENSEMBLE PREDICTION")
print("-" * 40)

# Fit all models on full training data
rf.fit(X_train, y)
gb.fit(X_train, y)
ridge.fit(X_train, y)

# Weighted ensemble (better models get more weight)
rf_w    = 1 / rf_scores.mean()
gb_w    = 1 / gb_scores.mean()
ridge_w = 1 / ridge_scores.mean()
total_w = rf_w + gb_w + ridge_w

pred_log = (
    (rf_w    * rf.predict(X_test) +
     gb_w    * gb.predict(X_test) +
     ridge_w * ridge.predict(X_test)) / total_w
)
pred_price = np.expm1(pred_log)   # reverse log transform

print(f"  Predicted price range: ${pred_price.min():,.0f} - ${pred_price.max():,.0f}")
print(f"  Mean predicted price : ${pred_price.mean():,.0f}")


# ---------------------------------------------
# 6.  FEATURE IMPORTANCE PLOT
# ---------------------------------------------
importances = pd.Series(gb.feature_importances_, index=X_train.columns)
top20 = importances.sort_values(ascending=False).head(20)

fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor('#f8f8f8')
colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(top20)))[::-1]
top20.plot(kind="barh", ax=ax, color=colors, edgecolor="white")
ax.set_title("Top 20 Feature Importances (Gradient Boosting)", fontsize=13, fontweight="bold")
ax.set_xlabel("Importance Score")
ax.invert_yaxis()
plt.tight_layout()
fi_path = "feature_importance.png"
plt.savefig(fi_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"\n[OK] Feature importance plot saved → {fi_path}")


# ---------------------------------------------
# 7.  SAVE SUBMISSION
# ---------------------------------------------
submission = pd.DataFrame({"Id": test_ids, "SalePrice": pred_price})
submission.to_csv(OUTPUT_PATH, index=False)
print(f"[OK] Submission file saved → {OUTPUT_PATH}")
print(f"    Rows: {len(submission)}")

# ---------------------------------------------
# 8.  MODEL COMPARISON PLOT
# ---------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Model Performance Comparison", fontsize=14, fontweight="bold")
fig.patch.set_facecolor('#f8f8f8')

model_names = list(scores.keys())
rmse_vals   = list(scores.values())
bar_colors  = ["#e74c3c" if n == best_name else "#3498db" for n in model_names]

axes[0].bar(model_names, rmse_vals, color=bar_colors, edgecolor="white", width=0.5)
axes[0].set_title("CV RMSE (lower = better)")
axes[0].set_ylabel("RMSE (log scale)")
for i, v in enumerate(rmse_vals):
    axes[0].text(i, v + 0.001, f"{v:.4f}", ha="center", fontsize=10, fontweight="bold")
axes[0].set_ylim(0, max(rmse_vals) * 1.25)

# Prediction distribution
axes[1].hist(pred_price, bins=50, color="#9b59b6", edgecolor="white", alpha=0.85)
axes[1].set_title("Predicted Price Distribution")
axes[1].set_xlabel("Predicted Sale Price ($)")
axes[1].set_ylabel("Count")
axes[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
comp_path = "model_comparison.png"
plt.savefig(comp_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"[OK] Model comparison plot saved → {comp_path}")

print("\n" + "=" * 60)
print("  DONE! Files generated:")
print(f"    [chart] {eda_path}")
print(f"    [chart] {fi_path}")
print(f"    [chart] {comp_path}")
print(f"    [file] {OUTPUT_PATH}  ← upload this to Kaggle")
if demo_mode:
    print("\n  [!]  Running on SYNTHETIC data.")
    print("  [!]  Download real data from Kaggle for actual submission.")
print("=" * 60)