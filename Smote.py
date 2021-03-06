import numpy as np
from random import randrange, choice
from sklearn.neighbors import NearestNeighbors

def shuffle(X):
    n, d = X.shape
    idx = np.arange(n)
    np.random.seed(13)
    np.random.shuffle(idx)
    X = X[idx]
    return X

def SMOTE(T, N, k):
    """
    Returns (N/100) * n_minority_samples synthetic minority samples.

    Parameters
    ----------
    T : array-like, shape = [n_minority_samples, n_features]
        Holds the minority samples
    N : percetange of new synthetic samples: If N > 100, should be multiple of 100 
        n_synthetic_samples = N/100 * n_minority_samples. Can be < 100.
    k : int. Number of nearest neighbours. 

    Returns
    -------
    S : array, shape = [(N/100) * n_minority_samples, n_features]
    """    
    n_minority_samples, n_features = T.shape
    
    if N < 100:
    	S = shuffle(T)
    	return S[:N, :]

    # if (N % 100) != 0:
    #     raise ValueError("N must be < 100 or multiple of 100")
    
    N = int(N * 1.0/100)
    n_synthetic_samples = N * n_minority_samples
    S = np.zeros(shape=(n_synthetic_samples, n_features))
    
    #Learn nearest neighbours
    neigh = NearestNeighbors(n_neighbors = k)
    neigh.fit(T)
    
    #Calculate synthetic samples
    for i in xrange(n_minority_samples):
        # print i
        nn = neigh.kneighbors(T[i], n_neighbors = k,return_distance=False)
        #print nn[0]
        for n in xrange(N):
            nn_index = choice(nn[0])
            #NOTE: nn includes T[i], we don't want to select it 
            while nn_index == i:
                nn_index = choice(nn[0])
            for j in range(n_features):    
                dif = T[nn_index][j] - T[i][j]
                gap = np.random.random()
                S[n + i * N, j] = T[i, j] + gap * dif
    
    return S

def underSampling(T, N, minority_size):
    S = shuffle(T)
    end = int(minority_size * 100/N)
    return S[:end, :]



def splitDataLabelWise(allData):
    temp = allData[allData[:,-1].argsort()]
    pos = np.where(temp[:, -1] == 1)[0][0]
    dataNeg = temp[: pos, :]
    dataPos = temp[pos:, :]
    return dataNeg, dataPos

def sampleData(X, Y, N_oversample, N_undersample, k):
    allData = np.c_[X, Y]
    dataNeg, dataPos = splitDataLabelWise(allData)
    pos = np.where(dataPos[:, -1] == 0)[0]
    if dataNeg.shape[0] < dataPos.shape[0]:
        temp = SMOTE(dataNeg[:, :-1], N_oversample, k)
        dataNeg = np.append(dataNeg, np.c_[temp, np.zeros(temp.shape[0])], axis = 0)
        # temp = underSampling(dataPos[:, :-1], N_undersample, dataNeg.shape[0])
        # dataPos = np.c_[temp, np.ones(temp.shape[0])]

    else:
        temp = SMOTE(dataPos[:, :-1], N_oversample, k)
        dataPos = np.append(dataPos, np.c_[temp, np.ones(temp.shape[0])], axis = 0)
        # temp = underSampling(dataNeg[:, :-1], N_undersample, dataPos.shape[0])
        # dataNeg = np.c_[temp, np.zeros(temp.shape[0])]

    pos = np.where(dataPos[:, -1] == 0)[0]
    S = np.append(dataPos, dataNeg, axis = 0)
    S = shuffle(S)
    return S[:, :-1], S[:, -1]




