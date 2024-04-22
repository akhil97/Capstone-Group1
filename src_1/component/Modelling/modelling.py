import pandas as pd
from pycaret.classification import *
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv('../../../Data/final_output_lagos.csv')
data['Slum'].fillna(0, inplace=True)

# Changing label values from 1.0, 2.0 to 1
label_encoder = LabelEncoder()
data['Slum'] = label_encoder.fit_transform(data['Slum'])
data['Slum'] = data['Slum'].replace([1, 2], 1)

data3 = data[data['Slum'] == 3]

#Removing Slum label 3 since it is unsure
data = data[data['Slum'] != 3]

data = data.drop(['geometry', 'id'], axis = 1)

#X = data.iloc[:, 1:]
#y = data['Slum']
data = data[~data.isin([-9999]).any(axis=1)]
clf1 = setup(data, target = 'Slum')
best_model = compare_models(include = ['xgboost'])

#XGBoost
xgboost = create_model('xgboost')
predict_model(xgboost)

#Tune best model
tuned_model = tune_model(xgboost)

#AUC-ROC plot
plot_model(estimator = tuned_model, plot = 'auc')

#Plotting the confusion Matrix
plot_model(estimator = tuned_model, plot = 'confusion_matrix')

#Plotting the confusion Matrix
interpret_model(tuned_model)

predict_model(xgboost, data = data3)
