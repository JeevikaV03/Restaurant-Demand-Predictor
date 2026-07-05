from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
import json
import os

from preprocess import load_and_preprocess

# Load dataset
X, y = load_and_preprocess("data/orders.csv")

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = LinearRegression()

# Train model
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Evaluate
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("Model Evaluation")
print("----------------")
print("MAE:", round(mae, 2))
print("R2 Score:", round(r2, 2))

# Save model
model_path = os.path.join("model", "model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully!")

# Save metrics
metrics = {
    "MAE": round(mae, 2),
    "R2 Score": round(r2, 2)
}

metrics_path = os.path.join("model", "metrics.json")
with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=4)

print("Metrics saved successfully!")