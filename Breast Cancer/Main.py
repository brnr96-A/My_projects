

import numpy as np
import pandas
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from classifier_algorithm import RunMethods
from sklearn.preprocessing import MinMaxScaler



# read data and preprocessing
data_name='breast-cancer.csv'
data_pandas = pandas.read_csv(data_name,na_values='?')
data_pandas=data_pandas.fillna(0)




data_main=np.array(data_pandas)
lbl=data_main[:,-1]
data=data_main[:,:-1]

scaler = MinMaxScaler()
scaler.fit(data)
data=scaler.transform(data)

# split data
x_train, x_test, y_train, y_test = train_test_split(data, lbl, test_size=0.20,random_state=1)
str_out=""
class_names=["Healthy","sick"]

RunMethods(data,lbl,x_train,x_test,y_train,y_test,str_out,class_names)

