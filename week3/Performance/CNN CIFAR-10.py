import tensorflow as tf
from tensorflow.keras import datasets,layers,models
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix,classification_report

classes=["airplane","automobile","bird","cat","deer","dog","frog","horse","ship","truck"]

def plot_sample(X,y,index):
    plt.figure(figsize=(15,2))
    plt.imshow(X[index])
    plt.xlabel(classes[index])

(X_train,y_train),(X_test,y_test) = datasets.cifar10.load_data()

#X_train.shape=10,000,32,32,3-> no of im,pixels,pixels,rgb range

#Reshaping 2-D array to 1-D array

y_train=y_train.reshape(-1,)  #==(-1,1)

#Scaling rgb ranges

X_train=X_train/255
X_test=X_test/255

ann = models.Sequential([
    layers.Flatten(input_shape=(32,32,3)),
    layers.Dense(3000,activation='relu'),
    layers.Dense(1000,activation='relu'),
    layers.Dense(10,activation='sigmoid')
])

ann.compile(optimizer='SGD',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

ann.fit(X_train,y_train,epochs=5)

ann.evaluate(X_test,y_test)

print("Classification report: \n",classification_report(y_test,y_pred_classes))

#Using CNN to improve model

cnn = models.Sequential([
    #CNN
    layers.Conv2D(filters=32,kernel_size=(3,3),activation="relu", input_shape=(32,32,3)),
    layers.MaxPooling2D((2,2)),

    layers.Conv2D(filters=64,kernel_size=(3,3),activation='relu'),
    layers.MaxPooling2D((2,2)),

    #Filters are how many features my model can detect, kernel size is the size of the matrix we shift to recognize features
    #i.e feature maps. Here stride is (1,1) ny default 

    #dense
    layers.Flatten(),
    layers.Dense(64,activation='relu'),
    layers.Dense(10,activation='softmax'),
])

cnn.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

cnn.fit(X_train,y_train,epochs=10)

cnn.evaluate(X_test,y_test)

print("Classification report: \n",classification_report(y_test,classes))

