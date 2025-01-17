import pandas as pd
import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

df = pd.read_csv("final.csv")

winner_encoder = LabelEncoder()
df['winner_encoded'] = winner_encoder.fit_transform(df['winner'])

df['weather_encoded'] = df['weather'].map({'f':0, 't':1})

features = [
    'race_name', 'circuit', 'weather_encoded', 'winner_constructor_points',
    'winner_constructor_wins', 'winner_constructor_podiums',
    'winner_car_name', 'winner_car_wins', 'winner_car_podiums'
]
X = df[features]
y = df['winner_encoded']

numeric_features = [
    'weather_encoded', 'winner_constructor_points',
    'winner_constructor_wins', 'winner_constructor_podiums',
    'winner_car_wins', 'winner_car_podiums'
]
categorical_features = ['race_name', 'circuit', 'winner_car_name']

for col in numeric_features:
    if X[col].isnull().any():
        imputer = SimpleImputer(strategy='mean')
        X[[col]] = imputer.fit_transform(X[[col]])

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_features),
        ('passthrough', 'passthrough', numeric_features)
    ],
    remainder='drop'
)

class KMeansTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, n_clusters=3, random_state=42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=self.random_state)
        
    def fit(self, X, y=None):
        self.kmeans.fit(X)
        return self
    
    def transform(self, X):
        clusters = self.kmeans.predict(X)
        return clusters.reshape(-1, 1)

cluster_encoder = ColumnTransformer(
    transformers=[
        ('cluster_onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), [0])
    ],
    remainder='drop'
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = Pipeline([
    ('preprocessing', preprocessor),
    ('scaler', StandardScaler()),
    ('kmeans', KMeansTransformer(n_clusters=3, random_state=42)),
    ('cluster_encode', cluster_encoder),
    ('logreg', LogisticRegression(max_iter=5000, penalty='l2'))
])

param_grid = {
    'scaler': [StandardScaler(), MinMaxScaler()],
    'logreg__C': [0.01, 0.1, 1, 10, 100],
    'logreg__solver': ['lbfgs', 'newton-cg', 'saga']
}

grid = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid.fit(X_train, y_train)

model = grid.best_estimator_

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
labels = np.unique(y_test)
target_names = winner_encoder.inverse_transform(labels)
report = classification_report(y_test, y_pred, labels=labels, target_names=target_names, zero_division=0)

print("Model Evaluation:")
print("Best Params:", grid.best_params_)
print("Best CV Accuracy:", grid.best_score_)
print("Test Accuracy:", acc)
print("Classification Report:")
print(report)

logreg_model = model.named_steps['logreg']
intercepts = logreg_model.intercept_.tolist()
coefficients = logreg_model.coef_.tolist()

cat_transformer = model.named_steps['preprocessing'].transformers_[0][1]
preprocessor_feature_names = cat_transformer.get_feature_names_out(categorical_features).tolist() + numeric_features

cluster_feature_names = ['cluster_1', 'cluster_2']
all_features = preprocessor_feature_names + cluster_feature_names

best_params = grid.best_params_.copy()
best_params['scaler'] = str(best_params['scaler'])  # Convert scaler object to string

model_data = {
    "classes": winner_encoder.classes_.tolist(),
    "intercepts": intercepts,
    "coefficients": coefficients,
    "winner_classes": {str(i): winner for i, winner in enumerate(winner_encoder.classes_)},
    "feature_order": all_features,
    "weather_encoding": {"f":0, "t":1},
    "best_params": best_params
}

with open('model_params.json', 'w') as f:
    json.dump(model_data, f, indent=4)

print("Model training complete. Parameters saved to model_params.json.")





