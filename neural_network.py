import random
import numpy as np

class MLP:

    def __init__(self, sizes):
        self.sizes = sizes
        self.num_layers = len(sizes)
        self.random_weight_biases()

    def random_weight_biases(self):
        """To a [i,j,k,l] list representing the layers, initializes the biases matrix j x 1, k x 1 e l x 1 and weights matrix j x i e k x j e l x k"""
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]

        # weights initialization with 0 mean and 1/sqrt(n) std deviation (Xavier weights initialization)
        self.weights = [np.random.randn(self.sizes[i], self.sizes[i - 1]) / np.sqrt(self.sizes[i - 1])
                        for i in range(1, len(self.sizes))]

    def sigmoid(self, z):
        """To an array z, return element-wise sigmoid function"""
        return 1.0/(1.0 + np.exp(-z))

    def sigmoid_derivative(self, z):
        """To an array z, return element-wise sigmoid prime function"""
        return self.sigmoid(z)*(1-self.sigmoid(z))

    def feedforward(self, a):
        """To an input a, with shape [[a1],[a2]...] return ANN feedforward output with shape [[y1],[y2],[y3]...]"""

        for w,b in zip(self.weights, self.biases):
            a = self.sigmoid(w @ a + b)
        return a



if __name__ == '__main__':
    training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
    net = MLP([784, 30, 10])
    net.train(training_data, 30, 10, 3.0, test_data=test_data)
