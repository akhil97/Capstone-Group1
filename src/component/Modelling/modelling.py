import pandas as pd
import re
from pycaret.classification import *
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv('../../../Data/final_output_lagos.csv')
data['Slum'].fillna(0, inplace=True)

# Changing label values from 1.0, 2.0 to 1
label_encoder = LabelEncoder()
data['Slum'] = label_encoder.fit_transform(data['Slum'])
data['Slum'] = data['Slum'].replace([1, 2], 1)

#Drop id column
data = data.drop(['id'], axis = 1)

#Get longitudes and latitudes from geometric points
data['long'] = ''
data['lat'] = ''
for i in range(len(data['geometry'])):
    point_str = data['geometry'][i]
    matches = re.findall(r'[-+]?\d*\.\d+', point_str)
    coordinates = [float(match) for match in matches]
    data['long'][i] = coordinates[0]
    data['lat'][i] = coordinates[1]

#Remove -9999 no data rows from the dataset
data = data[~data.isin([-9999]).any(axis=1)]

#Drop geometry column
data = data.drop(['geometry'], axis = 1)

#Slum labels unsure
data3 = data[data['Slum'] == 3]

#Removing Slum label 3 since it is unsure
data = data[data['Slum'] != 3]

#Pycaret experimentation setup
clf1 = setup(data, target = 'Slum', include = ['ada', 'gbc', 'et', 'lightgbm', 'dummy', 'svm', 'nb'])
best_model = compare_models()

#Logistic Regression
lr = create_model('lr')
predict_model(lr)

#Random Forest
rf = create_model('rf')
predict_model(rf)

#K Nearest Neighbors
knn = create_model('knn')
predict_model(knn)

#XGBoost
xgboost = create_model('xgboost')
predict_model(xgboost)

#MLP
mlp = create_model('mlp')
predict_model(mlp)

#Decision Trees
dt = create_model('dt')
predict_model(dt)


#Ridge Classifier
ridge = create_model('ridge')
predict_model(ridge)


#Quadratic Discriminant Analysis
qda = create_model('qda')
predict_model(qda)

#Ada Boost Classifier
ada = create_model('ada')
predict_model(ada)

#Gradient Boosting Classifier
gbc = create_model('gbc')
predict_model(gbc)

#Extra Trees Classifier
et = create_model('et')
predict_model(et)

#Light Gradient Boosting Machine
lightgbm = create_model('lightgbm')
predict_model(lightgbm)

#Dummy Classifier
dummy = create_model('dummy')
predict_model(dummy)

#SVM - Linear Kernel
svm = create_model('svm')
predict_model(svm)

#Naive Bayes
nb = create_model('nb')
predict_model(nb)

#save model
save_model(xgboost, 'modelling_imbalanced')

#Save experiment
save_experiment('my_experiment1')

X_test = get_config('X_test')

predictions = predict_model(xgboost, data=X_test)
predictions.to_csv('../../../Data/test_results_lagos_balanced.csv')


#Tune best model
tuned_model = tune_model(xgboost)

#AUC-ROC plot
plot_model(estimator = xgboost, plot = 'pr')

#Plotting the confusion Matrix
plot_model(estimator = xgboost, plot = 'confusion_matrix')

#SHAP plot
interpret_model(xgboost)

predict_model(xgboost, data = data3)

