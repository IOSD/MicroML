#importing required libraries
from microml.linear_model.linear_regressor import Linear_Model
from sklearn.linear_model import LinearRegression

#importing dataset
from sklearn.datasets import load_diabetes
dataset = load_diabetes()
print("Dataset Loaded")

#splitting data into train and test
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(dataset['data'],dataset['target'])

#creating and training a linear model
regessor = LinearRegression()
regessor.fit(x_train,y_train)
y_pred = regessor.predict(x_test)
print("Weights: "+str(regessor.coef_))
print("Intercept: "+str(regessor.intercept_))

#testing it on computer
x = [ 4.53409833e-02, -4.46416365e-02, -2.56065715e-02, -1.25563519e-02,1.76943802e-02, -6.12835791e-05,  8.17748397e-02, -3.94933829e-02,-3.19914449e-02, -7.56356220e-02]
print(regessor.predict([x]))

#generating ino file for arduino to be loaded
ardu_model = Linear_Model('COM3',9600)
ardu_model.generate_ino(regessor)

#after loading the ino file onto arduino using arduino ide
print(ardu_model.predict(x))