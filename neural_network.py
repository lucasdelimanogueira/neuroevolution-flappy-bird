import random
import numpy as np

### Técnicas utilizadas
# Weight decay
# Xavier Weight initialization
# Cross-pEntropy Cost Function

class MLP:

    def __init__(self, sizes):
        self.sizes = sizes
        self.num_layers = len(sizes)
        self.random_weight_biases()

    def random_weight_biases(self):
        """Para uma lista [i,j,k,l] representando os layers, inicializa os biases jx1, kx1 e lx1 e os weights jxi e kxj e lxk"""
        self.biases = [np.random.randn(y, 1) for y in self.sizes[1:]]

        # inicialização dos pesos com média 0 e desvio padrão de 1/sqrt(n) para evitar problemas com saturação
        self.weights = [np.random.randn(self.sizes[i], self.sizes[i - 1]) / np.sqrt(self.sizes[i - 1])
                        for i in range(1, len(self.sizes))]

    def sigmoid(self, z):
        """Para um array z, retorna o sigmoid de cada elemento"""
        return 1.0/(1.0 + np.exp(-z))

    def sigmoid_derivative(self, z):
        """Para um array z, retorna a derivada sigmoid de cada elemento"""
        return self.sigmoid(z)*(1-self.sigmoid(z))

    def feedforward(self, a):
        """Para uma entrada a, no formato [[a1],[a2]...] retorna a saída [[y1],[y2],[y3]...]"""

        for w,b in zip(self.weights, self.biases):
            a = self.sigmoid(w @ a + b)
        return a



if __name__ == '__main__':
    training_data, validation_data, test_data = mnist_loader.load_data_wrapper()
    net = MLP([784, 30, 10])
    net.train(training_data, 30, 10, 3.0, test_data=test_data)