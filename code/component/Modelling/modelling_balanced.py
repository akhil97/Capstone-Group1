import pandas as pd
from sklearn.neural_network import MLPClassifier
from imblearn.over_sampling import SMOTE
from pycaret.classification import *
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

data = pd.read_csv('../../../Data/lagos_input.csv')
data['Slum'].fillna(0, inplace=True)

# Changing label values from 1.0, 2.0 to 1
label_encoder = LabelEncoder()
data['Slum'] = label_encoder.fit_transform(data['Slum'])
data['Slum'] = data['Slum'].replace([1, 2], 1)

#Removing Slum label 3 since it is unsure
data = data[data['Slum'] != 3]

X = data.iloc[:, 1:]
y = data['Slum']

data = data.drop(['geometry', 'id'], axis = 1)

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=1)
#sm = SMOTE(random_state=42)
#X_res, y_res = sm.fit_resample(X_train, y_train)
#clf = MLPClassifier(random_state=1, max_iter=300).fit(X_res, y_res)
#predictions = clf.predict(X_test)
#print(classification_report(y_test, predictions))

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

#XGBoost
xgboost = create_model('xgboost')
predict_model(xgboost)

#Tune best model
tuned_model = tune_model(xgboost)

#Feature importance
plot_model(estimator = tuned_model, plot = 'feature')

#Plotting the confusion Matrix
plot_model(estimator = tuned_model, plot = 'confusion_matrix')

#plotting the ROC curve
plot_model(estimator = tuned_model, plot = 'auc')

