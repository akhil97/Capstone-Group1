import pandas as pd
from sklearn.neural_network import MLPClassifier
from pycaret.datasets import get_data
from pycaret.classification import *
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

data = pd.read_csv('../../../Data/final_input_lagos.csv')
data['Slum'].fillna(0, inplace=True)

# Changing label values from 1.0, 2.0 to 1
label_encoder = LabelEncoder()
data['Slum'] = label_encoder.fit_transform(data['Slum'])
data['Slum'] = data['Slum'].replace([1, 2], 1)

#Removing Slum label 3 since it is unsure
data = data[data['Slum'] != 3]

X = data.iloc[:, 3:]
y = data['Slum']

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,
                                                    random_state=1)
clf = MLPClassifier(random_state=1, max_iter=300).fit(X_train, y_train)
predictions = clf.predict(X_test)
print(classification_report(y_test, predictions))

clf1 = setup(data, target = 'Slum')
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

