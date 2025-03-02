#!/usr/bin/env python3

# Project: VUT FIT SUI Project - Dice Wars
# Authors:
#   - Josef Kolář      <xkolar71@stud.fit.vutbr.cz>
#   - Dominik Harmim   <xharmi00@stud.fit.vutbr.cz>
#   - Petr Kapoun      <xkapou04@stud.fit.vutbr.cz>
#   - Jindřich Šesták  <xsesta05@stud.fit.vutbr.cz>
# Year: 2020
# Description: Trains a neuron network model.

import os

import numpy as np
import tensorflow as tf

PLAYERS_COUNT = 4

DATA_DIR = os.path.join(os.path.dirname(__file__), '../../sui-learning-data-mixed')

TRAIN_DATA = np.load(os.path.join(DATA_DIR, 'data-train.npy'))
TRAIN_DATA_COUNT = TRAIN_DATA.shape[0]

VALIDATE_DATA = np.load(os.path.join(DATA_DIR, 'data-val.npy'))
VALIDATE_DATA_COUNT = VALIDATE_DATA.shape[0]

BATCH_SIZE = 32


def reshape_results(results: np.array) -> np.array:
    return np.reshape(
        tf.keras.utils.to_categorical(
            results,
            num_classes=PLAYERS_COUNT
        ),
        newshape=[results.shape[0], PLAYERS_COUNT]
    )


def get_model() -> tf.keras.models.Model:
    input_data = tf.keras.Input(shape=(499,))

    NGC = 16

    x = tf.keras.layers.Dense(NGC * 2 ** 2, activation='relu')(input_data)
    x = tf.keras.layers.Dropout(0.25)(x)
    x = tf.keras.layers.Dense(NGC * 2, activation='relu')(x)
    x = tf.keras.layers.Dense(PLAYERS_COUNT, activation='softmax')(x)

    return tf.keras.models.Model(input_data, x)


model = get_model()

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=['accuracy']
)

model.fit(
    x=TRAIN_DATA[:, 1:],
    y=reshape_results(TRAIN_DATA[:, 0]),

    validation_data=(
        VALIDATE_DATA[:, 1:],
        reshape_results(VALIDATE_DATA[:, 0]),
    ),
    steps_per_epoch=TRAIN_DATA_COUNT // BATCH_SIZE,
    validation_steps=VALIDATE_DATA_COUNT // BATCH_SIZE,
    epochs=15,
    batch_size=BATCH_SIZE,
    verbose=1,
)

model.save(os.path.join(os.path.dirname(__file__), 'model.h5'))
