import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Exemplo: suponha que você exportou os dados do banco para CSV
# Colunas: user_feature1, user_feature2, event_feature1, event_feature2, liked
df = pd.read_csv("user_event_history.csv")
X = df[["user_feature1", "user_feature2", "event_feature1", "event_feature2"]]
y = df["liked"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "recommendation_model.pkl")

# Exemplo de uso do modelo (pode ser importado em update_recommendations.py)


def predict_score(user_features, event_features):
    model = joblib.load("recommendation_model.pkl")
    features = user_features + event_features
    score = model.predict_proba([features])[0][1]  # probabilidade de "like"
    return score
