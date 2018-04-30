import csv
import cv2
import numpy as np
path = '../carnd-behavioral-cloning/data/' #'../carnd-behavioral-cloning/data_02/'
#path = '../carnd-behavioral-cloning/data_02/' #'../carnd-behavioral-cloning/data_02/'
lines = []
with open(path + 'driving_log.csv') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        lines.append(line)
        
images = []
measurements = []
for line in lines:
#    for i in range(3):        
    source_path = line[0]
    filename = source_path.split('/')[-1] #source_path.split('/')[-1] #
#    filename = source_path.split('\\')[-1] #source_path.split('/')[-1] #
    current_path = path + 'IMG/' + filename
    
    left_path = line[1]
    left_filename = source_path.split('/')[-1] #source_path.split('/')[-1] #
#    left_filename = source_path.split('\\')[-1] #source_path.split('/')[-1] #
    left_path = path + 'IMG/' + filename
    
    right_path = line[1]
    right_filename = source_path.split('/')[-1] #source_path.split('/')[-1] #
#    right_filename = source_path.split('\\')[-1] #source_path.split('/')[-1] #
    right_path = path + 'IMG/' + filename
    
    image = cv2.imread(current_path)
    image_left = cv2.imread(left_path)
    image_right = cv2.imread(right_path)
    
    images.extend((image, image_left, image_right))
    measurement = float(line[3])
    measurements.extend((measurement, measurement-0.2, measurement+0.2))    
    #print(current_path)    




augmented_images, augmented_measurements = [], []
for image, measurement in zip(images, measurements):
    augmented_images.append(image)
    augmented_measurements.append(measurement)
    augmented_images.append(cv2.flip(image,1))
    augmented_measurements.append(measurement * -1.0)
    
X_train = np.array(augmented_images)
y_train = np.array(augmented_measurements)

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Cropping2D
from keras.layers import Convolution2D
from keras.layers.pooling import MaxPooling2D

model = Sequential()
model.add(Lambda(lambda x: x / 255.0 - 0.5, input_shape=(160,320,3)))
model.add(Cropping2D(cropping=((70,25),(0,0))))
model.add(Convolution2D(24,5,5,subsample=(2,2),activation="relu"))
model.add(Convolution2D(36,5,5,subsample=(2,2),activation="relu"))
model.add(Convolution2D(48,5,5,subsample=(2,2),activation="relu"))
model.add(Convolution2D(64,3,3,activation="relu"))
model.add(Convolution2D(64,3,3,activation="relu"))
model.add(Flatten())
model.add(Dense(100))
model.add(Dense(50))
model.add(Dense(1))

model.compile(loss='mse',optimizer='adam')
model.fit(X_train, y_train, validation_split=0.2, shuffle=True, nb_epoch=7)

model.save('model.h5')
#exit()

#from keras.models import Model
#import matplotlib.pyplot as plt
#
#history_object = model.fit_generator(X_train, samples_per_epoch =
#    len(augmented_images), validation_data = 
#    y_train,
#    nb_val_samples = len(augmented_measurements), 
#    nb_epoch=5, verbose=1)
#
#### print the keys contained in the history object
#print(history_object.history.keys())
#
#### plot the training and validation loss for each epoch
#plt.plot(history_object.history['loss'])
#plt.plot(history_object.history['val_loss'])
#plt.title('model mean squared error loss')
#plt.ylabel('mean squared error loss')
#plt.xlabel('epoch')
#plt.legend(['training set', 'validation set'], loc='upper right')
#plt.show()

#model = Sequential()
#model.add(Lambda(lambda x: x / 255.0 - 0.5, input_shape=(160,320,3)))
#model.add(Cropping2D(cropping=((70,25),(0,0))))
#model.add(Convolution2D(6,5,5,activation="relu"))
#model.add(MaxPooling2D())
#model.add(Convolution2D(6,5,5,activation="relu"))
#model.add(Flatten())
#model.add(Dense(120))
#model.add(Dense(84))
#model.add(Dense(1))