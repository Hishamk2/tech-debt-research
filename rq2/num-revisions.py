# make cdf of the number of revisions of satd and not satd methods
# when DiffSizes is not zero, that means the method has been changed (so num revisions ++)
# Get teh sum for each row

import os
import numpy as np
import matplotlib.pyplot as plt

# SRCDIR = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/csv-results/full/'
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

def process():
    """
    Have the different metrics in a dictionary
    Each key will be a metric and the value will be a dictionary with 'satd' and 'not_satd' lists
    """
    metrics = {'numRevisions': {'satd': [], 'not_satd': []}}
    
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
                    metric = row[indices['DiffSizes']].split("#")
                    age_list = row[indices['ChangeAtMethodAge']].split('#')
                    satd = row[indices["SATD"]].split("#")

                    index_to_stop = find_index_to_stop(age_list)
                    if index_to_stop != -1:
                        metric = metric[:index_to_stop]
                        satd = satd[:index_to_stop]
                    
                    numRevisions = 0
                    for m in metric:
                        if int(m) != 0:
                            numRevisions += 1
                    
                    if check_satd(satd):
                        metrics['numRevisions']['satd'].append(numRevisions)
                    else:
                        metrics['numRevisions']['not_satd'].append(numRevisions)

                    # print all the relevant info to make sure this is working properly
                    print(f'File: {file}')
                    print(f'Metric: {metric}')
                    print(f'Age List: {age_list}')
                    print(f'SATD: {satd}')
                    print(f'Num Revisions: {numRevisions}\n')
                        
    return metrics

def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]

def draw_graph(metrics):
    satd = metrics['numRevisions']['satd']
    not_satd = metrics['numRevisions']['not_satd']
    
    x, y = ecdf(satd)
    ln = plt.plot(x,y)
    plt.setp(ln, ls="-", linewidth=3, color='r', label='SATD Methods')
    
    x, y = ecdf(not_satd)
    ln = plt.plot(x,y)
    plt.setp(ln, ls="-", linewidth=3, color='b', label='Non-SATD Methods')
    
    plt.legend()
    plt.xlabel("Number of Revisions")
    plt.ylabel("CDF")
    plt.show()

if __name__ == "__main__":
    metrics  = process()
    draw_graph(metrics)