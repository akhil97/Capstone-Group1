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

X = data.iloc[:, 1:]
y = data['Slum']

data = data.drop(['geometry', 'id'], axis = 1)
data = data[~data.isin([-9999]).any(axis=1)]
clf1 = setup(data, target = 'Slum', fix_imbalance = True)
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


#Tune best model
tuned_model = tune_model(xgboost)

#AUC-ROC plot
plot_model(estimator = tuned_model, plot = 'auc')

#Plotting the confusion Matrix
plot_model(estimator = tuned_model, plot = 'confusion_matrix')

#Plotting the confusion Matrix
interpret_model(tuned_model)

predict_model(xgboost, data = data3)

