import joblib


class Model():

    def __init__(self, name: str) -> None:
        self.model_name = name
        self.path = 'data/models/' + self.model_name
        self.model = joblib.load(self.path + '.joblib')

    def predict(self, df):
        pred = self.model.predict(df)
        return pred
