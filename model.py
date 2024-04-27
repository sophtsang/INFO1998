import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt 

class Model(object): 
    def linearModel(self, zipcode, yearBuilt, lotArea, df): 
        features = df[['zipcode', 'year built', 'lot area (acres)']] 
        target = df['sold price'] 
        x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        model = LinearRegression() 
        model.fit(x_train, y_train) 
        
        predicted = model.predict([[zipcode, yearBuilt, lotArea]])[0] 
        trainScore = model.score(x_train,y_train) 
        validation = model.score(x_test,y_test) 
        
        values = [predicted, trainScore, validation] 
        return values 