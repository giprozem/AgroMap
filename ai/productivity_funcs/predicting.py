import pickle

productivity_model_path = './ModelProductivityLinear2.pkl'


def productivity_predict(predicting, model_path=productivity_model_path):
    predicting = [[predicting]]
    # load the trained model from the .pkl file
    with open(model_path, 'rb') as f:
        linr = pickle.load(f)

    # make predictions on new features
    return float(linr.predict(predicting))
