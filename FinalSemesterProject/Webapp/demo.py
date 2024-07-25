import pandas as pd

df2 = pd.read_csv("/Users/whitegg/Documents/GitHub/Project/FinalSemesterProject/ehresp_2014.csv")
df2

df = df2[["erbmi", "euhgt", "euwgt"]]
df


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import numpy as np


# Handle missing and invalid values (simple approach)
df = df[(df['euhgt'] > 0) & (df['euwgt'] > 0)]
df.dropna(inplace=True)

# Features and target
X = df[['euhgt', 'euwgt']]
y = df['erbmi']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(),
    'Lasso Regression': Lasso(),
    'Decision Tree': DecisionTreeRegressor(),
    'Random Forest': RandomForestRegressor(),
    'Support Vector Machine': SVR(),
    'Gradient Boosting': GradientBoostingRegressor()
}

# Train and evaluate each model
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    results[name] = mse

# Print the results
for name, mse in results.items():
    print(f"{name}: MSE = {mse}")

# Find the best model based on MSE
best_model_name = min(results, key=results.get)
print(f"Best model: {best_model_name} with MSE = {results[best_model_name]}")
