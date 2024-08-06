import os
import numpy as np
import matplotlib.pyplot as plt

# SRCDIR = "../../software-evolution/tech-debt-results/"
SRCDIR = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/csv-files-satd/'



def build_indices(line):
    indices = {}
    data = line.strip().split("\t")
    for i in range(len(data)):
        indices[data[i]] = i
    return indices    
            
def process():
    removal_times = []

    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            fr = open(SRCDIR + file, "r")
            header = fr.readline() # skip header
            indices = build_indices(header)
            lines = fr.readlines()
            
            for line in lines:
                row = line.strip().split("\t")             

                if int(row[indices['Age']]) > 730: # Make sure the method is at least 2 years old     
                    satd_list = row[indices['SATD']].split('#')
                    age_list = row[indices['ChangeAtMethodAge']].split('#')

                    start_index = None

                    for i, value in enumerate(satd_list):
                        if int(age_list[i]) > 730: # if the current commit is more than 2 yrs old, done
                            break

                        if value == '1' and start_index is None:
                            start_index = i
                        elif value == '0' and start_index is not None:
                            end_index = i

                            start_age = int(age_list[start_index])
                            end_age = int(age_list[end_index])
                            removal_time = end_age - start_age
                            
                            removal_times.append(removal_time)
                            
                            start_index = None  # Reset start index for next SATD segment   
    
    return removal_times         

def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]

def draw_graph(metrics):
    x, y = ecdf(metrics)
    ln = plt.plot(x,y)
    plt.setp(ln, ls="-", linewidth=3, color='r', label='Removal Times')
    plt.legend()
    plt.xlabel("SATD Removal Time (days)")
    plt.ylabel("CDF")
    # plt.xlim(0, 100)
    plt.savefig(f'figs/rq1/removal_times.pdf')
    # plt.show()

if __name__ == "__main__":
    metrics  = process()
    draw_graph(metrics)

