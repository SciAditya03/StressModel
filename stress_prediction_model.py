# -*- coding: utf-8 -*-
"""Stress_prediction_model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11eOpAikQNyDU40gV3j8KlMZ3tpJuRoFe
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
import pickle

# Load the training dataset
training_data_file_path = "Stress_dataset.csv"  # Replace with the actual path to the file
stress_data = pd.read_csv(training_data_file_path)

# Assign column names to the dataset
stress_data.columns = ['HRV', 'HeartRate', 'GSR', 'StressLevel']

# Separate features and target
features = stress_data[['HRV', 'HeartRate', 'GSR']]
labels = stress_data['StressLevel']

# Normalize the features
scaler = StandardScaler()
features_normalized = scaler.fit_transform(features)

# Convert labels to categorical format (for multi-class classification)
labels_categorical = np.zeros((labels.size, labels.max() + 1))
labels_categorical[np.arange(labels.size), labels] = 1

# Split into training and validation data
X_train, X_val, y_train, y_val = train_test_split(features_normalized, labels_categorical, test_size=0.2, random_state=42)

# Build the neural network model
model = Sequential([
    Dense(128, activation='relu', input_dim=X_train.shape[1]),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(3, activation='softmax')  # 3 output classes: No Stress, Mild Stress, High Stress
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_val, y_val), verbose=1)

# Save the scaler using pickle
scaler_file_path = "stress_scaler.pkl"
with open(scaler_file_path, 'wb') as f:
    pickle.dump(scaler, f)
print(f"Scaler saved to: {scaler_file_path}")

# Save the trained model
model_file_path = "stress_model.h5"
model.save(model_file_path)
print(f"Model saved in HDF5 format at: {model_file_path}")

# Load the generated test dataset
test_data_file_path = "stress_test.csv"  # Replace with the actual path to the test dataset
test_data = pd.read_csv(test_data_file_path)

# Normalize the test dataset using the same scaler
test_data_normalized = scaler.transform(test_data)

# Make predictions on the test dataset
predictions = model.predict(test_data_normalized)
predicted_classes = np.argmax(predictions, axis=1)  # Convert predictions to class labels

# Add predictions to the test dataset
test_data['PredictedStressLevel'] = predicted_classes

# Save the test dataset with predictions to a new CSV file
test_data_with_predictions_file_path = "stress_test_data_with_predictions.csv"  # Replace with desired output path
test_data.to_csv(test_data_with_predictions_file_path, index=False)

print(f"Test data with predictions saved to: {test_data_with_predictions_file_path}")

# Example: Loading the saved scaler and model for future predictions
# Load the scaler
with open(scaler_file_path, 'rb') as f:
    loaded_scaler = pickle.load(f)
print("Scaler loaded successfully.")

# Load the model
loaded_model = load_model(model_file_path)
print("Model loaded successfully.")

# Example prediction using loaded scaler and model
new_sample = np.array([[0.5, 85, 1.2]])  # Replace with an actual test sample (3 features: HRV, HeartRate, GSR)
new_sample_normalized = loaded_scaler.transform(new_sample)

# Predict stress level
new_prediction = loaded_model.predict(new_sample_normalized)
predicted_stress_class = np.argmax(new_prediction, axis=1)[0]  # Class label (0, 1, or 2)
stress_labels = ["No Stress", "Mild Stress", "High Stress"]
print(f"Predicted Stress Level: {stress_labels[predicted_stress_class]}")