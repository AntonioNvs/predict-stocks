import numpy as np

from typing import List

def reLU(x) -> np.ndarray:
  return (np.maximum(0, x))

def tanh(x) -> np.ndarray:
  return np.tanh(x)

class NeuralNetwork:
  def __init__(self, input_size: int, layer_dims: List[int], output_size: int) -> None:
    self.n_x = input_size
    self.n_y = output_size
    self.layer_dims = [self.n_x] + layer_dims + [self.n_y]

    L = len(self.layer_dims)

    self.W = [np.random.randn(self.layer_dims[i-1], self.layer_dims[i]) for i in range(1, L)]

    self.b = [np.zeros((1, self.layer_dims[i])) for i in range(1, L)]
  
  def forward(self, X) -> None:
    self.A = [X]
    self.Z = [X]

    L = len(self.layer_dims)
    
    for i in range(L-1):
      self.Z.append(np.dot(self.A[i], self.W[i]) + self.b[i])
      A = reLU(self.Z[i+1]) if i < L-1 else tanh(self.Z[i])
      self.A.append(A)
    
    return self.A[-1]

  def comput_cost(self, Y_hat, Y) -> float:
    m = Y.shape[1]

    cost = 1/m * np.sum(np.power(Y_hat-Y, 2))

    return cost

  def tanh_backward(self, x):
    return 1 - np.power(tanh(x), 2)

  def relu_backward(self, x):
    return np.greater(x, 0).astype(int)

  def backward(self, Y, lr):    
    dZ = []
    dW = []
    db = []

    dZ.append((self.A[-1] - Y) * self.tanh_backward(self.A[-1]))
    dW.append(np.dot(self.A[-2].T, dZ[-1]))
    db.append(np.sum(dZ[-1], axis=0, keepdims=True))

    for i in range(len(self.layer_dims)-2, 0, -1):
      dZ.append(np.dot(dZ[-1], self.W[i].T) * self.relu_backward(self.Z[i]))
      dW.append(np.dot(self.A[i-1].T, dZ[-1]))
      db.append(np.sum(dZ[-1], axis=0, keepdims=True))

    dW.reverse()
    db.reverse()

    # Update params
    for i in range(len(self.W)):
      self.W[i] -= lr*dW[i]
      self.b[i] -= lr*db[i]

  def train(self, inputs, predicts, learning_rate, n_iter: int):
    for i in range(n_iter):
      Y_hat = self.forward(inputs)
      cost = self.comput_cost(Y_hat, predicts)
      
      if (i+1) % 50 == 0:
        print(f"Epoch {i}: {cost}")

      self.backward(predicts, learning_rate)

  def predict(self, X, threshold = 0.5) -> bool:
    A = self.forward(X)
    Y_hat = np.squeeze(A)
    return Y_hat >= threshold

if __name__ == "__main__":
  inputs = np.array([
    [0, 1],
    [0, 0],
    [1, 0],
    [1, 1]
  ])

  predicts = np.array([
    [1],
    [0],
    [1],
    [1]
  ])

  neural = NeuralNetwork(2, [3, 3, 3], 1)
  neural.train(inputs, predicts, 0.003, 1000)

  print(neural.predict(np.array([0, 0])))