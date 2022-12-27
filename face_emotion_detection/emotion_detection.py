##################
# With much help from https://github.com/bnsreenu/python_for_microscopists/blob/master/239_train_emotion_detection/239_train_emotion_detection.py
##################

"""
Train a deep learning model on facial emotion detection
Dataset from: https://www.kaggle.com/msambare/fer2013
"""

from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
import os
from matplotlib import pyplot as plt
import numpy as np
from tensorflow.keras.models import load_model

IMG_HEIGHT = 48
IMG_WIDTH = 48
batch_size = 16

train_data_dir = '../data/face_emotion_recognition/train/'
validation_data_dir = '../data/face_emotion_recognition/test/'

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=30,
    shear_range=0.3,
    zoom_range=0.3,
    horizontal_flip=True,
    fill_mode='nearest')

validation_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    color_mode='grayscale',
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True)

validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    color_mode='grayscale',
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True)

# Verify our generator by plotting a few faces and printing corresponding labels
class_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

input_shape = (None, 48, 48, 1)

learning_rate = 0.1

# Create the model
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))

model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.1))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.1))

model.add(Conv2D(256, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.1))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(7, activation='softmax'))

decayed_lr = tf.keras.optimizers.schedules.ExponentialDecay(learning_rate,
                                                            10000, 0.95, staircase=True)
opt = tf.keras.optimizers.Adam(decayed_lr)
callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.build(input_shape)

print(model.summary())

train_path = "../data/face_emotion_recognition/train/"
test_path = "../data/face_emotion_recognition/test/"

num_train_imgs = 0
for root, dirs, files in os.walk(train_path):
    num_train_imgs += len(files)

num_test_imgs = 0
for root, dirs, files in os.walk(test_path):
    num_test_imgs += len(files)

epochs = 100

with tf.device("/device:GPU:0"):
    history = model.fit(train_generator,
                        steps_per_epoch=num_train_imgs // batch_size,
                        epochs=epochs,
                        validation_data=validation_generator,
                        validation_steps=num_test_imgs // batch_size,
                        callbacks=[callback])

model.save('saved_models/emotion_detection_model_100epochs.h5')

# plot the training and validation accuracy and loss at each epoch
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'y', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

plt.plot(epochs, acc, 'y', label='Training acc')
plt.plot(epochs, val_acc, 'r', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

my_model = load_model('saved_models/emotion_detection_model_100epochs.h5', compile=False)

# Generate a batch of images
test_img, test_lbl = validation_generator.__next__()
predictions = my_model.predict(test_img)

predictions = np.argmax(predictions, axis=1)
test_labels = np.argmax(test_lbl, axis=1)