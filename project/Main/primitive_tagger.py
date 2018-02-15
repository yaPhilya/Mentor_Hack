from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
import os

import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.preprocessing import LabelBinarizer, LabelEncoder
from sklearn.metrics import confusion_matrix

import keras

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.preprocessing import text, sequence
from keras import utils

# # Get data
# f


data_stack = pd.read_csv('../DB/stack-overflow-data.csv')
read = open('../DB/stack-overflow-data-tags')
tags_stack = read.readline().split('|')
read.close()

data_stack.rename(columns={'post': 'Body', 'tags': 'Tag'}, inplace=True)

data_free = pd.read_csv('../DB/freelance_data.csv', index_col=0)
read = open('../DB/freelance_data_tags')
tags_free = read.readline().split('|')
read.close()

data_start = pd.read_csv('../DB/startup_data.csv', index_col=0)
read = open('../DB/startup_data_tags')
tags_start = read.readline().split('|')
read.close()

all_tags = tags_stack.copy()
all_tags.extend(tags_free.copy())
all_tags.extend(tags_start.copy())

all_read_post = pd.DataFrame(columns=['Body', 'Tag'])

all_read_post = all_read_post.append(data_free)
all_read_post = all_read_post.append(data_start)
all_read_post = all_read_post.append(data_stack)

from sklearn.cross_validation import train_test_split


def process_tags(tags):
    tmp = list(tags)
    for i in range(len(tmp)):
        if tmp[i][0] == '[' and tmp[i][-1] == ']':
            tmp[i] = tmp[i][1:-1].split(',')
            for j in range(len(tmp[i])):
                tmp[i][j] = tmp[i][j].strip()
                tmp[i][j] = tmp[i][j][1:-1]
        else:
            tmp[i] = [tmp[i]]
    return tmp


train_posts, test_posts, train_tags, test_tags = train_test_split(all_read_post.Body, all_read_post.Tag,
                                                                  random_state=42, test_size=0.2)

test_tags = process_tags(test_tags)
train_tags = process_tags(train_tags)
test_posts = list(test_posts)
train_posts = list(train_posts)

# # Process data

# Prosess posts to vectors

max_words = 2500
all_tags = list(set(all_tags))
num_classes = len(all_tags)

tokenize = text.Tokenizer(num_words=max_words, char_level=False)
tokenize.fit_on_texts(train_posts)

x_train = tokenize.texts_to_matrix(train_posts)
x_test = tokenize.texts_to_matrix(test_posts)

# Prosess tags to vectors
tokenize_y = text.Tokenizer(num_words=num_classes, char_level=False, filters='')
tokenize_y.fit_on_texts(all_tags)

y_train = []
for tag in train_tags:
    y_train.append(tokenize_y.texts_to_matrix(tag).sum(axis=0))

y_test = []
for tag in test_tags:
    y_test.append(tokenize_y.texts_to_matrix(tag).sum(axis=0))

y_train = np.array(y_train)
y_test = np.array(y_test)

# # NN Part

label_from_prediction = list(np.zeros(num_classes))
for t in all_tags:
    label_from_prediction[tokenize_y.word_index[t] - 1] = t
label_from_prediction = np.array(label_from_prediction)

model = keras.models.load_model('../models/primitive_model')


def tagger_unpacked(input_str):
    print('Test input of NN:', input_str)
    tokens = tokenize.texts_to_matrix([input_str])
    print('Test shape of tokenized text:', tokens.shape)
    pred = model.predict(tokens)
    pred_tags = label_from_prediction[pred.ravel() > 0.1]
    return ','.join(pred_tags)


def custom_tagger(input_str):
    return tagger_unpacked(input_str)

print(custom_tagger(' c++,java,english,programming,math'))
''' usage
str - string you want to process 
tagger(str, model, tokenize, label_from_prediction)
'''
#print(custom_tagger(' c++,java,english,programming,math'))