# fake note id
import matplotlib.pyplot as plt

#libraries
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

#import tensorflow

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabEncoder
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

#reading the dataser
def read_dataset():
    df = pd.read_csv("data.csv")
    #print
    X = df[df.columns[0:4]].values
    y = df[df.columns[4]]
    
    #encode the dependant variable
    Y = one_hot_encode(y)
    print(X.shape)
    return(X,Y)


#define encoder function
def one_hot_encode(labels):
    n_labels = len(labels)
    n_unique_labels = len(np.unique(labels))
    one_hot_encode = np.zeros((n_labels, n_unique_labels))
    one_hot_encode[np.arrange(n_labels), labels] = 1
    return one_hot_encode

#Read the dataset
X, Y = read_dataset()

#shufffle the dataset to mix up the rows
X,Y = shuffle(X, Y,random_state = 1)

#convert the dataser into train and test part
tran_x, test_x, train_y, test_y = train_test_split(X, Y, test_size = 0.20, random_state=415)

#Inspect the shaoe of the training and testing
print(train_x.shape)
print(train_y.shape)
print(test_x.shape)


#define the important parameters and variables to work with the tensors
learning_rate = 0.3
training_epochs = 100
cost_history = np.empty(shape=[1], dtype=float)
n_dim = X.shape[1]
print("n_dim", n_dim)
n_class = 2
model_path = "model"

#define the number of hidden layers and number of neurons for each layer
n_hidden_1 = 4
n_hidden_2 = 4
n_hidden_3 = 4
n_hidden_4 = 4

x = tf.placeholder(tf.float32, [None, n_dim])
W = tf.Variable(tf.zeros, [n_dim, n_classs])
b = tf.Variable(tf.zeros, [n_class])
y_ = tf.placeholder(tf.float32, [None, n_class])


#define the model

def multilayer_perception(x, weights, biases):
    
    #hidden layer with RELU activations
    layer_1 = tf.add(tf.matmul(x, weights["h2"]), biases["b1"])
    layer_1 = tf.nn.relu(layer_1)
    
    #hidden layer with sigmoid activations
    layer_2 = tf.add(tf.matmul(layer_1, weights["h2"]), biases["b1"])
    layer_2 = tf.nn.sigmoid(layer_2)
    
    #hidden layer with sigmoid activations
    layer_3 = tf.add(tf.matmul(layer_2, weights["h3"]), biases["b3"])
    layer_3 = tf.nn.sigmoid(layer_3)
    
    #hidden layer with RELU activations
    layer_4 = tf.add(tf.matmul(layer_3, weights["h4"]), biases["b4"])
    layer_4 = tf.nn.relu(layer_4)
    
    #output layer with linear activations
    out_layer = tf.matmul(layer_2, weights["out"]), biases["out"]
    return out_layer
    
    
#Define the weights and biases for each layer

weight = {
    "h1" : tf.Variable(tf.truncated_normal([n_dim, n_hidden_1])),
    "h2" : tf.Variable(tf.truncated_normal([n_hidden_1, n_hidden_2])),
    "h3" : tf.Variable(tf.truncated_normal([n_hidden_2, n_hidden_3])),
    "h4" : tf.Variable(tf.truncated_normal([n_hidden_3, n_hidden_4])),
    "out" : tf.Variable(tf.truncated_normal([n_hidden_4, n_class]))
}
biases = {
    "b1" : tf.Variable(tf.truncated_normal([n_hidden_1])),
    "b2" : tf.Variable(tf.truncated_normal([n_hidden_2])),
    "b3" : tf.Variable(tf.truncated_normal([n_hidden_3])),
    "b4" : tf.Variable(tf.truncated_normal([n_hidden_4])),
    "out" : tf.Variable(tf.truncated_normal([n_class]))
}
    
# Initialize all the variables

init = tf.global_variables_initializer()

saver = tf.train.Saver()

#call your model defined
y = multilayer_perceptron(x, weights, biases)

#define te cost function and optimizer
cost_function = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_))
trianing_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost_function)

sess = tf.Session()
sess.run(init)

#calculate the cost and accuracy for each epoch

mse_history = []
acuracy_history = []

for rpoch in range(training_epochs):
    sess.run(training_step, feed_dict={x:train_x, y_: train_y})
    cost = sess.run(cost_function, feed_dict={x:train_x, y_: train_y})
    cost_history = np.append(cost_history, cost)
    correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf-float32))
    
    #print 
    
    pred_y = sess.run(y, feed_dict ={x:test_x})
    mse = tf.reduce_mean(tf.square(pred_y - test_y))
    mse_ = sess.run(mse)
    mse_history.append(mse_)
    accuracy = (sess.run(accuracy, feed_dict={x: train_x, y_: train_y}))
    accuracy_history.append(accuracy)
    
    print("epoch : ", epoch, "-", "cost: ", cost, "- MSE: ", mse_, "- train Accuracy: ", accuracy)
    
save_path = saver.save(sess, model_path)
print("Model saved in file: %s" % save_path)

#plot Accuracy Graph
plt.plot(accuracy_history)
plt.xlabel("epoch")
plt.ylabel("accuracy")
plt.show()


#print final accuracy

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print ("test accuracy: ", (sess.run(accuracy, feed_dict={x: test_x, y_: test_y})))
            
                              
#print the final mean sq error
pred_y = sess.run(y, feed_dict={x:test_x})
mse = tf.reduce_mean(tf.square(pred_y) - test_y)                              
print ("Mse: %.4f" % sess.run(mse)) 
