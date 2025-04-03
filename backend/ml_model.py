from sklearn.ensemble import RandomForestClassifier
import numpy as np

def train_model():
    X_train = np.array([[80, 5000, 300], [60, 7000, 250], [90, 4000, 200]])
    y_train = np.array([1, 0, 1])

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model

def predict_disease(model, health_data):
    return model.predict([health_data])