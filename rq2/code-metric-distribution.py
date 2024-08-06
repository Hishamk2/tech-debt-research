import os
import numpy as np
import matplotlib.pyplot as plt

METRIC_VALUE = 'last' # first, mean, last

# SRCDIR = "../../software-evolution/tech-debt-results/"
SRCDIR = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/csv-files-satd/'

def build_indices(line):
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

def process(metrics_list):
    """
    Have the different metrics in a dictionary
    Each key will be a metric and the value will be a dictionary with 'satd' and 'not_satd' lists
    """
    metrics = {metric: {'satd': [], 'not_satd': []} for metric in metrics_list}
    
    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            fr = open(SRCDIR + file, "r")
            line = fr.readline()  # skip header
            indices = build_indices(line)
            lines = fr.readlines()
            for line in lines:
                data = line.strip().split("\t")
                for metric_name in metrics_list:
                    metric = data[indices[metric_name]]
                    metric = metric.split("#")

                    if METRIC_VALUE == 'first':
                        metric = float(metric[0])
                    elif METRIC_VALUE == 'mean':
                        metric = [float(m) for m in metric]
                        metric = np.mean(metric)
                    elif METRIC_VALUE == 'last':
                        metric = float(metric[-1])
                    else:
                        print('ENTER A VALID METRIC VALUE')


                    satd = data[indices["SATD"]]
                    satd = satd.split("#")
                    
                    if metric < 0:
                        continue  # something is wrong
                    if check_satd(satd):
                        metrics[metric_name]['satd'].append(metric)
                    else:
                        metrics[metric_name]['not_satd'].append(metric)
    return metrics

def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]

def draw_graph(metrics):
    for metric_name, data in metrics.items():
        plt.figure()
        
        x, y = ecdf(data['satd'])
        ln = plt.plot(x, y)
        plt.setp(ln, ls="-", linewidth=3, color='r', label='SATD')
        
        x, y = ecdf(data['not_satd'])
        ln = plt.plot(x, y)
        plt.setp(ln, ls="--", linewidth=3, color='blue', label='NOT_SATD')
        
        plt.legend()
        plt.xlabel(metric_name)
        plt.ylabel("CDF")
        if metric_name == 'SLOCStandard':
            plt.xlim(0, 250)
        elif metric_name == 'Readability':
            pass
        elif metric_name == 'SimpleReadability':
            pass
        elif metric_name == 'MaintainabilityIndex':
            pass
        elif metric_name == 'McCabe':
            plt.xlim(0, 75)
        elif metric_name == 'totalFanOut':
            plt.xlim(0, 100)
        elif metric_name == 'uniqueFanOut':
            plt.xlim(0, 75)
            
        # plt.xlim(0, 1)
        plt.title(f"CDF of {metric_name}")
        # plt.show()
        if METRIC_VALUE == 'first':
            plt.savefig(f'figs/rq2/first/f_{metric_name}.pdf')
        elif METRIC_VALUE == 'mean':
            plt.savefig(f'figs/rq2/mean/m_{metric_name}.pdf')
        elif METRIC_VALUE == 'last':
            plt.savefig(f'figs/rq2/last/l_{metric_name}.pdf')


if __name__ == "__main__":
    metrics_list = ['SLOCStandard', 'Readability', 'SimpleReadability', 'MaintainabilityIndex', 'McCabe', 'totalFanOut', 'uniqueFanOut']
    metrics = process(metrics_list)
    draw_graph(metrics)

