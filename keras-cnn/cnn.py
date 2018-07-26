from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Dense, Flatten
from keras.utils import np_utils
from wandb.keras import WandbCallback
import wandb

run = wandb.init()
config = run.config

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.astype('float32')
X_train /= 255.
X_test = X_test.astype('float32')
X_test /= 255.

#reshape input data to be convolution friendly, fourth column is the channel
X_train = X_train.reshape(X_train.shape[0], config.img_width, config.img_height, 1)
X_test = X_test.reshape(X_test.shape[0], config.img_width, config.img_height, 1)

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]
labels=range(10)

# build model
model = Sequential()
model.add(Conv2D(16,
    (config.first_layer_conv_width, config.first_layer_conv_height),
    input_shape=(28, 28,1),
    activation='relu'))
# output is 24x24x32
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

#config has kernel size at 3x3
# you can take a out the input_shape in the second call
model.add(Conv2D(16,
    (config.first_layer_conv_width, config.first_layer_conv_height),
    activation='relu'))
# output is 26x26x32
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.5))

# output is 13x13x32
model.add(Flatten())

model.add(Dense(config.dense_layer_size, activation='relu'))

model.add(Dense(num_classes, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam',
                metrics=['accuracy'])


model.fit(X_train, y_train, validation_data=(X_test, y_test),
        epochs=config.epochs,
        callbacks=[WandbCallback(data_type="image")])
