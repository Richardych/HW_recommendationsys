import re
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import sys
fi = sys.argv[1]

res = {}
strr = '_15_0001_02'
listnm = 'strr'
listnm = eval(listnm)
if listnm not in res:
    res[listnm] = []

def plotgrid():
    k = 0
    strr = '_15_0001_02'
    listnm = 'strr'
    listnm = eval(listnm)
    plt.subplot(1,1,1+k)
    plt.title(listnm)
    plt.grid()
    plt.plot(res[listnm])
    k += 1
    plt.show()
    plt.savefig('loss.png')

def fill_list(m_lr, m_lam, m_loss):
    strr = '_15_0001_02'
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
    print(tmp)
    print(lr, loss)
    fill_list(float(lr),float(lam),float(loss)) 

plotgrid()
