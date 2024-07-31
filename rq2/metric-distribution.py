import os
import numpy as np
import matplotlib.pyplot as plt

SRCDIR = "../../software-evolution/tech-debt-results/"



def build_indexes(line):
    indexes = {}
    data = line.strip().split("\t")
    for i in range(len(data)):
        indexes[data[i]] = i
    return indexes    

def check_satd(satd):
    for s in satd:
        s = int(s)
        if s == 1:
            return True
    return False
            
def process():
    metrics = {}
    metrics['satd'] = []
    metrics['not_satd']= []
    
    for file in os.listdir(SRCDIR):
        fr = open(SRCDIR + file, "r")
        line = fr.readline() # skip header
        indexes = build_indexes(line)
        lines = fr.readlines()
        for line in lines:
            data = line.strip().split("\t")
            metric = data[indexes["SLOCStandard"]]
            metric = metric.split("#")
            metric = float(metric[0])
            satd = data[indexes["SATD"]]
            satd = satd.split("#")
            if metric < 0:
               continue # something is wrong
            if check_satd(satd):
               metrics['satd'].append(metric)
            else:
                metrics['not_satd'].append(metric)   
    return metrics         

def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]

def draw_graph(metrics):
    x, y = ecdf(metrics['satd'])
    ln = (plt.plot(x, y))
    plt.setp(ln, ls="-", linewidth=3, color='r', label='SATD')

    x, y = ecdf(metrics['not_satd'])
    ln = (plt.plot(x, y))
    plt.setp(ln, ls="--", linewidth=3, color='blue', label='NOT_SATD')
    plt.legend()
    plt.xlabel("MI")
    plt.ylabel("CDF")
    plt.xlim(0, 100)
    plt.show()

if __name__ == "__main__":
    metrics  = process()
    draw_graph(metrics)

