import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

print("🚀 Training started...")

# Load encoded dataset
df = pd.read_csv("data/erosion_encoded.csv")

print("Columns:", df.columns)

# =====================
# Feature selection
# =====================
FEATURES = ["slope", "rainfall", "soil_type_encoded"]
TARGET = "erosion_risk"

# Safety checks
for col in FEATURES + [TARGET]:
    if col not in df.columns:
        raise Exception(f"❌ Missing column: {col}")

X = df[FEATURES]
y = df[TARGET]

# =====================
# Train / Test split
# =====================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =====================
# Train Decision Tree
# =====================
model = DecisionTreeClassifier(
    max_depth=4,
    random_state=42
)

model.fit(X_train, y_train)

print("✅ Model training completed")

# =====================
# Evaluate model
# =====================
y_pred = model.predict(X_test)
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

# =====================
# Save model
# =====================
with open("models/erosion_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("💾 Model saved as models/erosion_model.pkl")
