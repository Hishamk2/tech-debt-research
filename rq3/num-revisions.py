import os
import numpy as np
import matplotlib.pyplot as plt

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

def get_top_5_largest_files(srcdir):
    files_with_size = [(file, os.path.getsize(os.path.join(srcdir, file))) 
                       for file in os.listdir(srcdir) if file.endswith('.csv')]
    sorted_files = sorted(files_with_size, key=lambda x: x[1], reverse=True)
    return [file[0] for file in sorted_files[:5]]

def process(file):
    metrics = {'numRevisions': {'satd': [], 'not_satd': []}}
    
    fr = open(os.path.join(SRCDIR, file), "r")
    line = fr.readline()  # skip header
    indices = build_indices(line)
    lines = fr.readlines()

    for line in lines:
        row = line.strip().split("\t")

        if int(row[indices['Age']]) > 730:  # Make sure the method is at least 2 years old     
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
                        
    return metrics

def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]

def draw_graph(metrics, file_name):
    satd = metrics['numRevisions']['satd']
    not_satd = metrics['numRevisions']['not_satd']
    
    x, y = ecdf(satd)
    ln = plt.plot(x, y)
    plt.setp(ln, ls="-", linewidth=3, color='r', label='SATD Methods')
    
    x, y = ecdf(not_satd)
    ln = plt.plot(x, y)
    plt.setp(ln, ls="-", linewidth=3, color='b', label='Non-SATD Methods')
    
    plt.title(f'Number of Revisions For SATD and Non-SATD Methods ({file_name})')
    plt.legend()
    plt.xlabel("Number of Revisions")
    plt.ylabel("CDF")

    SCALE = 'linear'
    plt.xscale(SCALE)
    
    output_dir = f'figs/rq3/{file_name}/{SCALE}'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/NumRevisions.pdf')

    # plt.show()

if __name__ == "__main__":
    top_files = get_top_5_largest_files(SRCDIR)
    
    for file_name in top_files:
        metrics = process(file_name)
        draw_graph(metrics, file_name)
