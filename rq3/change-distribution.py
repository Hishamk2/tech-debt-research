import os
import numpy as np
import matplotlib.pyplot as plt

# global variable for whehter to take the metric as the first value, last value or average

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

def find_index_to_stop(age_list: list):
    for i, age in enumerate(age_list):
        if int(age) > 730:
            return i
    return -1

def process(metrics_list):
    """
    Have the different metrics in a dictionary
    Each key will be a metric and the value will be a dictionary with 'satd' and 'not_satd' lists
    IMPORTANT, ALL 3 METRICS (NewAdditions, DiffSizes, EditDistances) ARE 0 IN THE FIRST COMMIT
    """
    metrics = {metric: {'satd': [], 'not_satd': []} for metric in metrics_list}
    # metrics = {}
    # for i, metric in enumerate(metrics_list):
    #     metrics[i] = {metric: {'satd': [], 'not_satd': []}}
    #     print(metrics)
    # metrics[len(metrics_list)] = {'numRevisions': {'satd': [], 'not_satd': []}}
    # print(metrics)
    
    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            fr = open(SRCDIR + file, "r")
            line = fr.readline()  # skip header
            indices = build_indices(line)
            lines = fr.readlines()

            # counter = 0
            
            for line in lines:
                # counter += 1
                # if counter > 100:
                #     break

                row = line.strip().split("\t")
                
                if int(row[indices['Age']]) > 730: # Make sure the method is at least 2 years old
                    for metric_name in metrics_list:
                        metric = row[indices[metric_name]].split("#")
                        age_list = row[indices['ChangeAtMethodAge']].split('#')
                        satd = row[indices["SATD"]].split("#")

                        index_to_stop = find_index_to_stop(age_list)
                        if index_to_stop != -1:
                                metric = metric[:index_to_stop]
                                satd = satd[:index_to_stop]

                        # get the sum of the metric
                        sum = 0
                        for m in metric:
                            sum += int(m)
                        
                        if sum < 0:
                            continue  # something is wrong
                        if check_satd(satd):
                            metrics[metric_name]['satd'].append(sum)
                        else:
                            metrics[metric_name]['not_satd'].append(sum)
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
        
        
        SCALE = 'log'

        if SCALE == 'linear':
            if metric_name == 'NewAdditions':
                plt.xlim(0, 500)
            elif metric_name == 'DiffSizes':
                plt.xlim(0, 1000)
            elif metric_name == 'EditDistances':
                plt.xlim(0, 20000)
            elif metric_name == 'CriticalEditDistances':
                plt.xlim(0, 20000)
        # plt.xlim(0, 1)
        plt.title(f"CDF of {metric_name}")
        # plt.show()

        plt.xscale(SCALE)
        plt.savefig(f'figs/rq3/{SCALE}/{metric_name}.pdf')



if __name__ == "__main__":
    metrics_list = ['NewAdditions', 'DiffSizes', 'EditDistances', 'CriticalEditDistances']
    # metrics_list = ['NewAdditions']
    metrics = process(metrics_list)
    draw_graph(metrics)

