import numpy as np
import csv
import collections
import pickle
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
import scipy.sparse
import math
from logevl import logger

def calLoss(P):
    return math.sqrt(P.power(2).sum().sum() / len(P.data))

def Process(R, V, W, s):
    product = [[],[],[]]
    for i in range(len(R)):
        [row,col,d] = R[i]
        res = V.getrow(row).dot(W.getrow(col).transpose()).data[0]
        d -= res
        product[0].append(row)
        product[1].append(col)
        product[2].append(d)
    return csr_matrix(coo_matrix((product[2], (product[0], product[1])), shape=s))

def calMRR(R, V, W):
    users = collections.defaultdict(list)
    for i in range(len(R)):
        [u,m,r] = R[i]
        users[u].append([m,r])
    MRR = []
    for u,movieList in users.items():
        ranking = []
        for m in movieList:
            ranking.append([m[0],m[1],V.getrow(u).dot(W.getrow(m[0]).transpose()).data[0]])
        ranking= sorted(ranking, key=lambda x: x[2], reverse=True)
        #print(ranking)
        res = 0
        count = 0
        for i in range(len(ranking)):
            if ranking[i][1] >= 3:
                res += 1 / (i+1)
                count += 1
        if count>0:
            MRR.append(res/count)
    return sum(MRR)/len(MRR)


if __name__ == "__main__":
    m_dir = '/home/yuchaohui/fcl/3_retrainfixedrlrlam/five/'
    V = scipy.sparse.load_npz(m_dir+'VW_100000_5/V_spr_15_0001_0002.npz')
    W = scipy.sparse.load_npz(m_dir+'VW_100000_5/W_spr_15_0001_0002.npz')
    logger.info((type(V)))
    with open(m_dir+"size.txt",'rb') as f:
        size = pickle.load(f)
    logger.info((size))
    train_mat = np.load(m_dir+"train.npy")
    test_mat = np.load(m_dir+"test.npy")
    logger.info((train_mat.shape, test_mat.shape))
    train_RMSE = calLoss(Process(train_mat,V,W,size))
    logger.info((train_RMSE))
    test_RMSE = calLoss(Process(test_mat,V,W,size))
    logger.info((test_RMSE))
    train_MRR = calMRR(train_mat,V,W)
    logger.info((train_MRR))
    test_MRR = calMRR(test_mat,V,W)
    logger.info((test_MRR))
    with open("res5.txt",'wb') as f:
        pickle.dump([train_RMSE,test_RMSE,train_MRR,test_MRR],f)  










