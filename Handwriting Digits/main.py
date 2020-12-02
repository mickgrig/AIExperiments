import numpy as np
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import SGD, RMSprop, Adam, Nadam
from keras.utils import np_utils

digitsNum = 10 #цифровые выходы

#some change from master

(trainInp, trainOut), (testInp, testOut) = mnist.load_data() #обучающий и тестовый наборы

# trainInp: 60000 картинок (28x28)

pixelsNum = 28 * 28

# 60000 x 28 x 28 -> 60000 x 784
trainInp = trainInp.reshape(60000, pixelsNum)
testInp = testInp.reshape(10000, pixelsNum)
trainInp = trainInp.astype('float32')
testInp = testInp.astype('float32')

#нормировка
#
trainInp /= 255
testInp /= 255

#унитарное кодирование
trainOutCoded = np_utils.to_categorical(trainOut, digitsNum)
testOutCoded = np_utils.to_categorical(testOut, digitsNum)


dropout = 0.2
epochNum = 15
batchCount = 128
optimizerObj = Adam()
hiddenNCount = 180
validationSplit = 0.2

model = Sequential()

model.add(Dense(hiddenNCount, input_shape=(pixelsNum, )))
model.add(Activation('relu'))

model.add(Dropout(dropout))

model.add(Dense(hiddenNCount))
model.add(Activation('relu'))

#model.add(Dropout(dropout))

model.add(Dense(hiddenNCount))
model.add(Activation('relu'))

model.add(Dropout(dropout))

model.add(Dense(digitsNum))
model.add(Activation('softmax'))

model.summary()

model.compile(loss='categorical_crossentropy', optimizer=optimizerObj, metrics=['accuracy'])
history = model.fit(trainInp, trainOutCoded, batch_size=batchCount, epochs=epochNum, validation_split=validationSplit)
evalres = model.evaluate(testInp, testOutCoded)
print("Eval loss:", evalres[0])
print('Eval accuracy:', evalres[1])
