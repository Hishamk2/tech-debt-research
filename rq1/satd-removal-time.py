import os
import numpy as np
import matplotlib.pyplot as plt

# SRCDIR = "../../software-evolution/tech-debt-results/"
SRCDIR = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/csv-files-satd/'



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
    removal_times = []

    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            fr = open(SRCDIR + file, "r")
            line = fr.readline() # skip header
            indexes = build_indexes(line)
            lines = fr.readlines()
            for line in lines:
                row = line.strip().split("\t")
                metric = row[indexes["SLOCStandard"]]
                metric = metric.split("#")
                metric = float(metric[0])
                
                if int(row[indexes['Age']]) <= 730:
                    continue
            
                satd_list = row[indexes['SATD']].split('#')
                age_list = row[indexes['ChangeAtMethodAge']].split('#')

                start_index = None

                for i, value in enumerate(satd_list):
                    if int(age_list[i]) > 730:
                        break

                    if value == '1' and start_index is None:
                        start_index = i
                    elif value == '0' and start_index is not None:
                        end_index = i
                        start_age = int(age_list[start_index])
                        end_age = int(age_list[end_index])
                        removal_times.append(end_age - start_age)
                        start_index = None  # Reset start index for next SATD segment   
    
    return removal_times         

def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]

def draw_graph(metrics):
    # x, y = ecdf(metrics['satd'])
    # ln = (plt.plot(x, y))
    # plt.setp(ln, ls="-", linewidth=3, color='r', label='SATD')

    # x, y = ecdf(metrics['not_satd'])
    # ln = (plt.plot(x, y))
    # plt.setp(ln, ls="--", linewidth=3, color='blue', label='NOT_SATD')

    x, y = ecdf(metrics)
    ln = plt.plot(x,y)
    plt.setp(ln, ls="-", linewidth=3, color='r', label='Removal Times')
    plt.legend()
    plt.xlabel("MI")
    plt.ylabel("CDF")
    # plt.xlim(0, 100)
    plt.show()

if __name__ == "__main__":
    metrics  = process()
    draw_graph(metrics)

