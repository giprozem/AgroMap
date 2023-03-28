import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from ai.models.productivity import ProductivityML

model_path = './model.pkl'


def read_json_del(path):
    # read json and sort it
    df = pd.read_json(path)
    # delete all null rows
    df = df[['id', 'NDVI', 'NDMI', 'NDWI', 'NDRE', 'productivity']]
    df = df.dropna()
    return df


def read_json_del_predict(path):
    df = pd.read_json(path)
    # delete all null rows
    df = df[['id', 'NDVI', 'NDMI', 'NDWI', 'NDRE']]
    df = df.dropna()
    return df


def x_y_split(df):
    try:
        # Selecting X features
        X = df.copy()
        y = X.pop('productivity')
        return X, y
    except:
        # Selecting X features
        X = df.copy()
        return X


def classification_12(array):
    # create array of productivity
    bins = [0, 1.6, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    labels = list(range(len(bins) - 1))
    return pd.cut(array, bins=bins, labels=labels).astype(int)


def train_test_split_del(X, y):
    # Train-test-split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    return X_train, X_test, y_train, y_test


def train_and_save(X_train, X_test, y_train, y_test, model_path, max_depth=10, min_samples_leaf=1):
    # train the model
    clf = DecisionTreeClassifier(criterion="entropy", max_depth=max_depth, min_samples_leaf=min_samples_leaf)
    clf.fit(X_train, y_train)

    train_score = clf.score(X_train, y_train)
    test_score = clf.score(X_test, y_test)

    print('DecisionTreeClassifier Score on the Train data = ', train_score)
    print('DecisionTreeClassifier Score on the Test data = ', test_score)

    # save the trained model as a .pkl file
    with open(model_path, 'wb') as f:
        pickle.dump(clf, f)

    ProductivityML.save(model_path)

    return clf


def initialize(train_path):
    df = read_json_del(train_path)
    # apply classification to the 'productivity' column
    array = df['productivity'].to_numpy()
    df['productivity'] = classification_12(array)

    # perform X-Y split
    X, y = x_y_split(df)

    # perform train-test split on X and y
    X_train, X_test, y_train, y_test = train_test_split_del(X, y)

    # train and return the model
    return train_and_save(X_train, X_test, y_train, y_test, model_path)


def predict(model_path, predict_path):
    df = read_json_del_predict(predict_path)
    # perform X-Y split
    predicting = x_y_split(df)

    # load the trained model from the .pkl file
    with open(model_path, 'rb') as f:
        clf = pickle.load(f)

    # make predictions on new features
    return int(clf.predict(predicting))
