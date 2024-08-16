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

def process(metrics_list, METRIC_VALUE, file):
    metrics = {metric: {'satd': [], 'not_satd': []} for metric in metrics_list}
    
    fr = open(os.path.join(SRCDIR, file), "r")
    line = fr.readline()  # skip header
    indices = build_indices(line)
    lines = fr.readlines()

    for line in lines:
        row = line.strip().split("\t")

        if int(row[indices['Age']]) > 730: # Make sure the method is at least 2 years old     
            for metric_name in metrics_list:
                metric = row[indices[metric_name]].split("#")
                age_list = row[indices['ChangeAtMethodAge']].split('#')
                satd = row[indices["SATD"]].split("#")

                index_to_stop = find_index_to_stop(age_list)
                if index_to_stop != -1: # if index_to_stop is -1, then there are no commits with age > 730 so keep as is
                    metric = metric[:index_to_stop]
                    satd = satd[:index_to_stop]

                if METRIC_VALUE == 'first':
                    metric = float(metric[0])
                elif METRIC_VALUE == 'mean':
                    metric = [float(m) for m in metric]
                    metric = np.mean(metric)
                elif METRIC_VALUE == 'last':
                    metric = float(metric[-1])
                else:
                    print('ENTER A VALID METRIC VALUE')
                
                if metric < 0:
                    print('NEGATIVE METRIC VALUE')
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

def draw_graph(metrics, METRIC_VALUE, SCALE, file_name):
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

        plt.xscale(SCALE)
        if SCALE != 'log':
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
            
        plt.title(f"CDF of {metric_name}")

        output_dir = f'figs/rq2/{METRIC_VALUE}/{file_name}/{SCALE}'
        os.makedirs(output_dir, exist_ok=True)

        if METRIC_VALUE == 'first':
            plt.savefig(f'{output_dir}/f_{metric_name}.pdf')
        elif METRIC_VALUE == 'mean':
            plt.savefig(f'{output_dir}/m_{metric_name}.pdf')
        elif METRIC_VALUE == 'last':
            plt.savefig(f'{output_dir}/l_{metric_name}.pdf')

if __name__ == "__main__":
    metrics_list = ['SLOCStandard', 'Readability', 'SimpleReadability', 'MaintainabilityIndex', 'McCabe', 'totalFanOut', 'uniqueFanOut']
    
    top_files = get_top_5_largest_files(SRCDIR)

    for METRIC_VALUE in ['first', 'mean', 'last']:
        for SCALE in ['log', 'linear']:
            for file_name in top_files:
                metrics = process(metrics_list, METRIC_VALUE, file_name)
                draw_graph(metrics, METRIC_VALUE, SCALE, file_name)
