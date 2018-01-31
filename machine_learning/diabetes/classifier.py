# I made this using this tutorial: https://youtu.be/T91fsaG2L0s
# Great explanation of neural networks: https://youtu.be/aircAruvnKk
# I removed a few lines from 'pima-indians-diabetes.data' and put it in
# 'never-seen-data.data' to have something to test with.

from keras.models import Sequential
from keras.layers import Dense
import numpy

numpy.random.seed(7)

dataset = numpy.loadtxt("pima-indians-diabetes.data", delimiter=",")

X = dataset[:,0:8]
Y = dataset[:,8]

model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(15, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])

model.fit(X, Y, epochs = 1000, batch_size=10)
print("\n[*] Training finished, evaluating...")
scores = model.evaluate(X, Y)
print("\n[*] Accuracy: " + str(scores[1]*100) + "\n")

while True:
    try:
        n1 = input("[1/8] Number of times pregnant: ")
        n2 = input("[2/8] Plasma glucose concentration a 2 hours in an oral glucose tolerance test: ")
        n3 = input("[3/8] Diastolic blood pressure (mm Hg): ")
        n4 = input("[4/8] Triceps skin fold thickness (mm): ")
        n5 = input("[5/8] 2-Hour serum insulin (mu U/ml): ")
        n6 = input("[6/8] Body mass index (weight in kg/(height in m)^2): ")
        n7 = input("[7/8] Diabetes pedigree function: ")
        n8 = input("[8/8] Age (years): ")

        predict_data = numpy.array([[n1,n2,n3,n4,n5,n6,n7,n8]])

        prediction = model.predict(predict_data)

        print("\n[*] Prediction: " + str(int(prediction[0]*100)) + "% chance of diabetes.\n")
    except KeyboardInterrupt:
        print("\nExiting...")
        raise SystemExit
    except:
        print("\nSomething went wrong, exiting...")
        raise SystemExit
