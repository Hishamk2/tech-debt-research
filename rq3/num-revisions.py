import os
import numpy as np
import matplotlib.pyplot as plt
from cliffs_delta import cliffs_delta
from scipy.stats import mannwhitneyu

# SRCDIR = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/csv-files-satd/'
SRCDIR = r'D:\\OneDrive - University of Manitoba\\Documents\\HISHAM\\Research\\Tech-Debt\\csv-files-satd\\'

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

def process(file):
    metrics = {'numRevisions': {'satd': [], 'not_satd': []}}
    
    with open(os.path.join(SRCDIR, file), "r", encoding='utf-8') as fr:
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
                
                numRevisions = sum(1 for m in metric if int(m) != 0)
                
                if check_satd(satd):
                    metrics['numRevisions']['satd'].append(numRevisions)
                else:
                    metrics['numRevisions']['not_satd'].append(numRevisions)
                        
    return metrics

def aggregate_metrics():
    aggregated_metrics = {'numRevisions': {'satd': [], 'not_satd': []}}
    
    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            file_metrics = process(file)
            for metric_name, data in file_metrics.items():
                aggregated_metrics[metric_name]['satd'].extend(data['satd'])
                aggregated_metrics[metric_name]['not_satd'].extend(data['not_satd'])
                
    return aggregated_metrics

def draw_graph(metrics):
    satd = metrics['numRevisions']['satd']
    not_satd = metrics['numRevisions']['not_satd']
    
    x, y = ecdf(satd)
    ln = plt.plot(x, y)
    plt.setp(ln, ls="-", linewidth=3, color='r', label='SATD Methods')
    
    x, y = ecdf(not_satd)
    ln = plt.plot(x, y)
    plt.setp(ln, ls="-", linewidth=3, color='b', label='Non-SATD Methods')
    
    plt.title('Number of Revisions For SATD and Non-SATD Methods (Aggregated)')
    plt.legend()
    plt.xlabel("Number of Revisions")
    plt.ylabel("CDF")

    SCALE = 'linear'
    plt.xscale(SCALE)
    
    output_dir = f'figs/rq3/aggregated/{SCALE}'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/NumRevisions.pdf')

    # plt.show()

def print_statistical_tests(aggregated_metrics):
    print("Aggregated Statistical Analysis for Number of Revisions")
    print(f"{'Metric':<25} {'Cliff\'s Delta':>15} {'Magnitude':>12} {'Mann-Whitney U':>20} {'p-value':>10}")
    print("=" * 80)
    
    for metric_name, data in aggregated_metrics.items():
        if len(data['satd']) > 0 and len(data['not_satd']) > 0:
            delta, magnitude = cliffs_delta(data['satd'], data['not_satd'])
            stat, p_value = mannwhitneyu(data['satd'], data['not_satd'], alternative='two-sided')
            
            print(f"{metric_name:<25} {delta:>15.4f} {magnitude:>12} {stat:>20.2f} {p_value:>10.4f}")
    print()

if __name__ == "__main__":
    # Aggregate metrics across all files
    aggregated_metrics = aggregate_metrics()
    
    # Perform and print aggregated statistical tests
    print_statistical_tests(aggregated_metrics)
    
    # Draw graph for the aggregated data
    # draw_graph(aggregated_metrics)
