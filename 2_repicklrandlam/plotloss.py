import re
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from  matplotlib.pylab import *
import sys
fi = sys.argv[1]

res = {}
for lr in [0.001,0.0001]:
    for lam in [20.0,0.2,0.002]:
        lrr = str(lr)
        strr = '_'+lrr+'_'+str(lam)
        listnm = 'strr'
        listnm = eval(listnm)
        if listnm not in res:
            res[listnm] = []

def plotgrid():
    k = 0
    subplots_adjust(left=0.06, bottom=0.06,top=0.94,right=0.94,wspace = 0.3,hspace = 0.4)
    for lr in [0.001,0.0001]:
        for lam in [20.0,0.2,0.002]:
            lrr = str(lr)
            strr = '_'+lrr+'_'+str(lam)
            listnm = 'strr'
            listnm = eval(listnm)
            subplot(2,3,1+k)
            title(listnm)
            grid()
            plot(res[listnm])
            k += 1
    show()
    savefig('loss.png')

def fill_list(m_lr, m_lam, m_loss):
    for lr in [0.001,0.0001]:
        for lam in [20.0,0.2,0.002]:
            if lr == m_lr and m_lam == lam:
                lrr = str(lr)
                strr = '_'+lrr+'_'+str(lam)
                listnm = 'strr'
                listnm = eval(listnm)
                res[listnm].append(m_loss)

with open(fi) as f:
    lines = f.readlines()
for li in lines:
    li = li[:-1]
    if "epoch" in li:
        continue
    tmp = re.findall(r'\((.*?)\)',li)[0].split(',')
    #tmp = re.findall(r"\d+\.?\d*", tmp[0])
    lr = tmp[2].strip()
    loss = tmp[4].strip()
    lam = tmp[1].strip()
    if loss == 'nan':
        loss = 100
    print(tmp)
    print(lr, loss)
    fill_list(float(lr),float(lam),float(loss)) 

plotgrid()
