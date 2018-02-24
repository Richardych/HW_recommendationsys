import re
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from  matplotlib.pylab import *
import sys
fi = sys.argv[1]

res = {}
for r in [35,25,20,15,10]:
    for lam in [0.0002,0.002,0.02,0.2,20.0,40.0]:
        lamm = str(lam).split('.')[0]+str(lam).split('.')[1]
        strr = '_'+str(r)+'_'+lamm
        listnm = 'strr'
        listnm = eval(listnm)
        if listnm not in res:
            res[listnm] = []

def plotgrid():
    k = 0
    subplots_adjust(left=0.06, bottom=0.06,top=0.94,right=0.94,wspace = 0.9,hspace = 1.5)
    for r in [35,25,20,15,10]:
        for lam in [0.0002,0.002,0.02,0.2,20.0,40.0]:
            lamm = str(lam).split('.')[0]+str(lam).split('.')[1]
            strr = '_'+str(r)+'_'+lamm
            listnm = 'strr'
            listnm = eval(listnm)
            subplot(5,6,1+k)
            grid()
            title(listnm)
            plot(res[listnm])
            k += 1
            #plt.tight_layout()
    show()
    savefig('loss.png')

def fill_list(m_r,m_lam,m_loss):
    for r in [35,25,20,15,10]:
        for lam in [0.0002,0.002,0.02,0.2,20.0,40.0]:
            if r==m_r and lam==m_lam:
                lamm = str(lam).split('.')[0]+str(lam).split('.')[1]
                strr = '_'+str(r)+'_'+lamm
                listnm = 'strr'
                listnm = eval(listnm)
                res[listnm].append(m_loss)

with open(fi) as f:
    lines = f.readlines()
for li in lines:
    li = li[:-1]
    if "epoch" in li:
        continue
    tmp = re.findall(r'\(.*?\)',li)
    tmp = re.findall(r"\d+\.?\d*", tmp[0])
    r = tmp[0]
    lam = tmp[1]
    loss = tmp[3]
    print(tmp)
    print(r,lam,loss)
    fill_list(int(r),float(lam),float(loss)) 

plotgrid()
