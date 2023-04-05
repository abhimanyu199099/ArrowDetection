import numpy as np
import matplotlib as plt

#chose the iris dataset for using with the perceptron
from sklearn.datasets import load_iris

#defining the perceptron
class perceptron:
    def __init__ (self, learning_rate, epochs):
        self.weights = None
        self.bias = None
        self.learning_rate = learning_rate
        self.epochs = epochs
        
    def activation_function (self,z):
        return np.heaviside (z,0)
    
    def fit(self, X, y):
        n_features = X.shape[1]
        self.weights = np.zeros((n_features))
        self.bias = 0
        for epoch in range(self.epochs):
            for i in range(len(X)):
                z = np.dot(X, self.weights) + self.bias
                y_pred = self.activation_function (z)

                self.weights = self.weights + self.learning_rate * (y[i] - y_pred[i]) * X[i]
                self.bias = self.bias + self.learning_rate * (y[i] - y_pred[i])
                
        return self.weights, self.bias
    
    def predict(self, X):
        z = np.dot(X, self.weights) + self.bias
        return self.activation_function(z)
    
iris = load_iris

X = iris.data[:, (0, 1)] # petal length, petal width
y = (iris.target == 0).astype(np.int)

from sklearn.model_selection import train_test_split

X_train, y_train, X_test, y_test = load_iris(("C:\Users\Abhim\Downloads\iris.data","C:\Users\Abhim\Downloads\iris.data"))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.6, random_state=42)

perceptron = perceptron(0.001, 100)
perceptron.fit(X_train, y_train)

#predicting the type of iris, based on petal length and width
pred = perceptron.predict(X_test)


from sklearn.metrics import accuracy_score
accuracy_score(pred, y_test)