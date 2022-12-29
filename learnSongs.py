import pandas
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression


def splitDataset(dataset, seed):
    array = dataset.values
    X = array[:, 1:4]
    Y = array[:, 4]
    validation_size = 0.20
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
    return X_train, X_validation, Y_train, Y_validation


def tryClassifiers(X_train, Y_train, seed, scoring):
    models = [('Linear Discriminant Analysis', LinearDiscriminantAnalysis()), ('K Neighbors', KNeighborsClassifier()),
              ('Decision Tree', DecisionTreeClassifier()),
              ('Logistic Regression', LogisticRegression(solver='liblinear', multi_class='ovr')),
              ('Support Vector Machine', SVC(gamma='auto')), ('Gaussian Naive Bayes', GaussianNB())]

    results = []
    names = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        mean = cv_results.mean()
        stdDev = cv_results.std()
        msg = "%s: %f (%f)" % (name, mean, stdDev)
        print(msg)

    figure = plt.figure()
    figure.suptitle('Differences in Algorithm Performance')
    ax = figure.add_subplot(111)
    plt.boxplot(results)
    ax.set_xticklabels(names)
    plt.show()


def checkModel(model, X_train, Y_train, X_validation, Y_validation):
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    return model


def main():
    dataset = pandas.read_csv("songMoods.csv", names=['id', 'danceability', 'energy', 'valence', 'mood'])
    seed = 100
    scoring = 'accuracy'
    X_train, X_validation, Y_train, Y_validation = splitDataset(dataset, seed)
    chosenModel = LogisticRegression(solver='liblinear', multi_class='ovr')
    model = checkModel(chosenModel, X_train, Y_train, X_validation, Y_validation)
    return model
