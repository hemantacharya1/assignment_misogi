# src/train_classifier.py
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# TEMP: For OpenAI
EMB_PATH = "embeddings/openai_embeddings.npy"
LABEL_PATH = "embeddings/openai_labels.npy"
MODEL_PATH = "models/openai_classifier.pkl"
ENCODER_PATH = "models/openai_label_encoder.pkl"


def main():
    X = np.load(EMB_PATH)
    y = np.load(LABEL_PATH)

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("Classification Report (GloVe):")
    print(classification_report(
    y_test, y_pred,
    labels=le.transform(le.classes_),   # ensures all 6 classes are reported
    target_names=le.classes_))

    joblib.dump(clf, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)
    print("✅ Trained and saved GloVe classifier.")

if __name__ == "__main__":
    main()
