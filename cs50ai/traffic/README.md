For this project, I started by using the same layers as from the lecture, which is to say:

1 2D convolutional layer of 32 filters
1 Max-Pooling layer with a pool size of 2x2
1 flattening layer
1 dense hidden layer of 128 neurons
1 dropout layer with a rate of 50%

Result: 333/333 - 1s - 4ms/step - accuracy: 0.0542 - loss: 3.4944

=> reduce dropout:
