import numpy as np
import csv
import collections
import pickle
from random import randint
from random import shuffle
from random import sample
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
import scipy.sparse
import math
import sys
import multiprocessing
import time
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from logre import logger

"""
"""

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

def train_func(R, size, r,lam, lr):
    u,c = size
    V = np.random.rand(u,r)
    W = np.random.rand(c,r)
    V_spr = csr_matrix(V)
    W_spr = csr_matrix(W)
    loss = 1;
    lr = lr  #0.0001
    count = 0
    print("Start training")
    while loss > 0.01:
        count += 1
        batch = 100000 
        for i in range(len(R)//batch): 
            lro = lr
            P = Process(R[i*batch:(i+1)*batch], V_spr, W_spr, size)
            W_spr_new = W_spr - lro * (-P.transpose().dot(V_spr) + W_spr.multiply(2 * lam))
            V_spr_new = V_spr - lro * (-P.dot(W_spr) + V_spr.multiply(2 * lam))
            W_spr,V_spr = W_spr_new, V_spr_new
            loss = calLoss(P)
            if i % 2 == 0:
                logger.info((r,lam, lr,i,loss))
            if i % 5 == 0:
                lamm = str(lam).split('.')[0]+str(lam).split('.')[1]
                scipy.sparse.save_npz('VW_100000_3/V_spr_15_0001_0002', V_spr, compressed=True)
                scipy.sparse.save_npz('VW_100000_3/W_spr_15_0001_0002', W_spr, compressed=True)
        logger.info(("epoch",count,loss))




## data load
#filename = "/home/yuchaohui/fcl/ml-20m/ratings.csv"
#train = []
#test = []
#maxusr = 0
#maxmovie = 0
#with open(filename, newline='') as csvfile:
##with open(filename, 'rb') as csvfile:
#    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#    for row in spamreader:
#        if row[0].isdigit():
#            maxusr = max(maxusr, int(row[0]))
#            maxmovie = max(maxmovie, int(row[1]))
#            a = randint(0,1)
#            if a == 0:
#                train.append([int(row[0]),int(row[1]),float(row[2])])
#            else:
#                test.append([int(row[0]),int(row[1]),float(row[2])])
#print(len(train))
#print(len(test))
#maxusr += 1
#maxmovie += 1
#shuffle(train)
#np.save("train.npy",np.asarray(train))
#np.save("test.npy",np.asarray(test))
#with open("size.txt",'wb') as f:
#    pickle.dump([maxusr,maxmovie],f)  

with open("size.txt",'rb') as f:
    size = pickle.load(f)
train_mat = np.load("train.npy")
test_mat = np.load("test.npy")
print(len(train_mat))
print(len(test_mat))
print(size)

#with open("train.txt",'wb') as f:
#    pickle.dump(R,f)
#with open("test.txt",'wb') as f:
#    pickle.dump(test,f)

m = multiprocessing.Manager()
d = m.dict()
l = m.list()

#train_func(train_mat,size, 30,0.0002)
p = multiprocessing.Process(target = train_func, args = (train_mat,size,15,0.2,0.001))        
p.start()
p.join()

print("The number of CPU is:" + str(multiprocessing.cpu_count()))
for p in multiprocessing.active_children():
    print("child   p.name:" + p.name + "\tp.id" + str(p.pid))
print("END!!!!!!!!!!!!!!!!!")

