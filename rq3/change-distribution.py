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

def process(metrics_list, file):
    metrics = {metric: {'satd': [], 'not_satd': []} for metric in metrics_list}
    
    fr = open(os.path.join(SRCDIR, file), "r")
    line = fr.readline()  # skip header
    indices = build_indices(line)
    lines = fr.readlines()

    for line in lines:
        row = line.strip().split("\t")
        
        if int(row[indices['Age']]) > 730:  # Make sure the method is at least 2 years old
            for metric_name in metrics_list:
                metric = row[indices[metric_name]].split("#")
                age_list = row[indices['ChangeAtMethodAge']].split('#')
                satd = row[indices["SATD"]].split("#")

                index_to_stop = find_index_to_stop(age_list)
                if index_to_stop != -1:
                    metric = metric[:index_to_stop]
                    satd = satd[:index_to_stop]

                # get the sum of the metric
                total_sum = sum(int(m) for m in metric)
                
                if total_sum < 0:
                    continue  # something is wrong

                if check_satd(satd):
                    metrics[metric_name]['satd'].append(total_sum)
                else:
                    metrics[metric_name]['not_satd'].append(total_sum)
    return metrics

def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]

def draw_graph(metrics, file_name):
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
        
        SCALE = 'linear'
        if SCALE == 'linear':
            if metric_name == 'NewAdditions':
                plt.xlim(0, 500)
            elif metric_name == 'DiffSizes':
                plt.xlim(0, 1000)
            elif metric_name == 'EditDistances':
                plt.xlim(0, 20000)
            elif metric_name == 'CriticalEditDistances':
                plt.xlim(0, 20000)
        
        plt.title(f"CDF of {metric_name}")
        
        plt.xscale(SCALE)
        output_dir = f'figs/rq3/{file_name}/{SCALE}'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/{metric_name}.pdf')

if __name__ == "__main__":
    metrics_list = ['NewAdditions', 'DiffSizes', 'EditDistances', 'CriticalEditDistances']
    
    top_files = get_top_5_largest_files(SRCDIR)
    
    for file_name in top_files:
        metrics = process(metrics_list, file_name)
        draw_graph(metrics, file_name)
