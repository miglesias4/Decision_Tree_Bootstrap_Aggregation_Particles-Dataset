#Created by: Dr. Olac Fuentes
#Modified by: Matthew Iglesias

import numpy as np
from utils import *
import math 
import time
from sklearn.ensemble import RandomForestRegressor
 

if __name__ == "__main__":  
    
    print('ENSEMBLE WITH RANDOM TRAINING EXAMPLE SELECTION')
    plt.close('all')
    
    #data_path = 'C:\\Users\\OFuentes\\Documents\\Research\\data\\'  # Use your own path here
    
    X = np.load('particles_X.npy').astype(np.float32)
    y = np.load('particles_y.npy').astype(np.float32)
    X_train, X_test, y_train, y_test = split_train_test(X,y,seed=20)
    
    ensemble = []
    start = time.time()
    ensemble_size = 11
    for i in range(ensemble_size):
        print('Training ensemble model',i)
        model = RandomForestRegressor(max_depth=12,random_state=0,n_jobs=-1)
        a = np.random.randint(low=0, high=X_train.shape[0], size=X_train.shape[0])
        model.fit(X_train[a], y_train[a])
        ensemble.append(model)
        elapsed_time = time.time()-start
        print('Elapsed time training so far {:.6f} secs'.format(elapsed_time))  
    
    start = time.time()    
    votes = np.zeros((X_test.shape[0],np.amax(y)+1),dtype=int)
    row_ind = np.arange(y_test.shape[0])
    for i, model in enumerate(ensemble):
        pred = model.predict(X_test)
        print('Model {} accuracy: {:.6f}'.format(i,accuracy(y_test,pred)))
        votes[row_ind,pred]+=1
           
    ens_pred = np.argmax(votes,axis =1)     
    elapsed_time = time.time()-start
    print('Ensemble accuracy: {:.6f}'.format(accuracy(y_test,ens_pred)))
    print('Elapsed time testing {:.6f} secs'.format(elapsed_time))   