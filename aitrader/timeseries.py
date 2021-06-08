from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM,Bidirectional
from keras.callbacks import ModelCheckpoint
import pickle
import numpy as np
from sklearn.metrics import r2_score

class Timeseries:
    def __init__ (self):

        self.scaler = MinMaxScaler()
        self.timestep = 60

        self.model = Sequential()
        self.model.add(Bidirectional(LSTM(units=40,return_sequences=True,input_shape = (self.timestep,1))))
        self.model.add(Bidirectional(LSTM(units=20,return_sequences=True)))
        self.model.add(Bidirectional(LSTM(units=20,return_sequences=True)))
        self.model.add(Bidirectional(LSTM(units=20,return_sequences=False)))

        self.model.add(Dense(units = 20))
        self.model.add(Dense(units = 10))

        self.model.add(Dense(units = 5))
        self.model.add(Dense(units = 1))
        self.model.compile(optimizer= 'adam',loss = 'mean_squared_error')

        
    def make_supervised(self,data):
        timeseriesX = []
        timeseriesY = []

        
        for i in range(self.timestep,len(data)):
            timeseriesX.append(data[i-self.timestep:i,-1])
            timeseriesY.append(data[i,-1])
        timeseriesX = np.array(timeseriesX)
        timeseriesY = np.array(timeseriesY)

        print('Because',self.timestep,'observations per timestep was used,', timeseriesX.shape[0]-self.timestep,'trainable samples created from',timeseriesX.shape[0],'rows of the original data')
        print('apparent percentage of data used               : ',(timeseriesX.shape[0]-self.timestep)/timeseriesX.shape[0])
        print('apparent percentage of data lost in conversion : ',1-(timeseriesX.shape[0]-self.timestep)/timeseriesX.shape[0])
        return timeseriesX,timeseriesY

    def train_test_split(self,data):
        train = data[0:int(len(data)*0.7)]
        test =  data[1+ int(len(data)*0.7):]
        return train,test

    def reshape_for_LSTM(self,x,y):
        X_supervised = np.reshape(x,(x.shape[0],x.shape[1],1))
        Y_supervised = np.reshape(y,(-1,1))
        return X_supervised,Y_supervised


    def train(self,xtrain,ytrain,xvalid,yvalid):
        self.model.fit(x = xtrain,y = ytrain,epochs =5,
                 validation_data=(xtest,ytest),
                 callbacks= ModelCheckpoint('forex.hdf5',save_best_only=True,mode = 'min',verbose = 1))
ts = Timeseries()
data = pickle.load(open('EURUSD-2021-05-23.pickle','rb'))
data = np.reshape(data['open'].values,(-1,1))
data = ts.scaler.fit_transform(data)


#print(data['open'].values)
x,y = ts.make_supervised(data)
xtrain,xtest = ts.train_test_split(x)
ytrain,ytest = ts.train_test_split(y)


print(len(xtrain),len(xtest),len(ytrain),len(ytest))
print(x)
print(y)

xtrain,ytrain = ts.reshape_for_LSTM(xtrain,ytrain)
xtest,ytest = ts.reshape_for_LSTM(xtest,ytest)

print(xtrain.shape,ytrain.shape,xtest.shape,ytest.shape)
ts.train(xtrain,ytrain,xtest,ytest)

xtrain_pred = ts.model.predict(xtrain)
xtest_pred = ts.model.predict(xtest)
print(r2_score(ytrain,xtrain_pred),r2_score(ytest,xtest_pred))