# -*- coding: utf-8 -*-

from __future__ import print_function
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils.training_utils import multi_gpu_model
import os
import pickle
import pandas as pd
import numpy as np
import argparse

# CLI
parser = argparse.ArgumentParser(description='Train a model for image classification.')
parser.add_argument('--gpus', type=int, default=0,
                    help='number of gpus to use, can be "1,2,3" or 0 for cpu only.')
parser.add_argument('--lr', type=float, default=0.0001,
                    help='learning rate. default is 0.1.')
parser.add_argument('--batch_size', type=int, default=32,
                    help='training batch size per device (CPU/GPU).')
parser.add_argument('--epochs', type=int, default=10,
                    help='number of training epochs.')
opt = parser.parse_args()

# global variables
print('Starting new image-classification task:, %s' % opt)
num_of_gpus, learn_rate, batch_size, epochs = opt.gpus, opt.lr, opt.batch_size, opt.epochs
num_classes = 10
image_channel = 3
save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = 'keras_cifar10_trained_model.h5'
model = Sequential()


def get_train_data():
    train_data = {b'data': [], b'labels': []}
    for i in range(5):
        with open(r"./data/cifar-10-batches-py/data_batch_" + str(i + 1), mode='rb') as file:
            data = pickle.load(file, encoding='bytes')
            train_data[b'data'] += list(data[b'data'])
            train_data[b'labels'] += data[b'labels']
    x_data = np.array(train_data[b'data']) / 255
    y_data = np.array(pd.get_dummies(train_data[b'labels']))
    return x_data, y_data


def get_test_data():
    test_data = {b'data': [], b'labels': []}
    with open(r"./data/cifar-10-batches-py/test_batch", mode='rb') as file:
        data = pickle.load(file, encoding='bytes')
        test_data[b'data'] += list(data[b'data'])
        test_data[b'labels'] += data[b'labels']
    x_data = np.array(test_data[b'data']) / 255
    y_data = np.array(pd.get_dummies(test_data[b'labels']))
    return x_data, y_data


def processing_data():
    # The data, split between train and test sets:
    x_train, y_train = get_train_data()
    x_test, y_test = get_test_data()
    x_train = x_train.reshape(x_train.shape[0], 32, 32, image_channel)
    x_test = x_test.reshape(x_test.shape[0], 32, 32, image_channel)
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    return x_train, y_train, x_test, y_test


def build_model(x_train):
    model.add(Conv2D(32, (3, 3), padding='same',
                     input_shape=x_train.shape[1:]))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))
    if num_of_gpus > 1:
        parallel_model = multi_gpu_model(model)
        adm = keras.optimizers.Adam(lr=learn_rate, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
        parallel_model.compile(loss="categorical_crossentropy",
                               optimizer=adm,
                               metrics=["accuracy"])
        return parallel_model
    else:
        # initiate RMSprop optimizer
        opt = keras.optimizers.rmsprop(lr=learn_rate, decay=1e-6)

        # Let's train the model using RMSprop
        model.compile(loss='categorical_crossentropy',
                      optimizer=opt,
                      metrics=['accuracy'])
        return model


def train_model(model_train, x_train, y_train, x_test, y_test):
    model_train.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    validation_data=(x_test, y_test),
                    shuffle=True)


def save_model():
    # Save model and weights
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    model_path = os.path.join(save_dir, model_name)
    model.save(model_path)
    print('Saved trained model at %s ' % model_path)


def test_model(model_test, x_test, y_test):
    # Score trained model.
    scores = model_test.evaluate(x_test, y_test, verbose=1)
    print('Test loss:', scores[0])
    print('Test accuracy:', scores[1])


def main():
    x_train, y_train, x_test, y_test = processing_data()
    if num_of_gpus > 1:
        parallel_model = build_model(x_train)
        train_model(parallel_model, x_train, y_train, x_test, y_test)
        test_model(parallel_model, x_test, y_test)
    else:
        build_model(x_train)
        train_model(model, x_train, y_train, x_test, y_test)
        test_model(model, x_test, y_test)
    save_model()


if __name__ == "__main__":
    main()
