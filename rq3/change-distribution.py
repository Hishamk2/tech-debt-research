import os
import numpy as np
import matplotlib.pyplot as plt
from cliffs_delta import cliffs_delta
from scipy.stats import mannwhitneyu

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

def process(metrics_list, file):
    metrics = {metric: {'satd': [], 'not_satd': []} for metric in metrics_list}
    
    fr = open(os.path.join(SRCDIR, file), "r", encoding='utf-8')
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

def aggregate_metrics(metrics_list):
    aggregated_metrics = {metric: {'satd': [], 'not_satd': []} for metric in metrics_list}
    
    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            file_metrics = process(metrics_list, file)
            for metric_name, data in file_metrics.items():
                aggregated_metrics[metric_name]['satd'].extend(data['satd'])
                aggregated_metrics[metric_name]['not_satd'].extend(data['not_satd'])
                
    return aggregated_metrics

def print_statistical_tests(aggregated_metrics):
    print("Aggregated Statistical Analysis")
    print(f"{'Metric':<25} {'Cliff\'s Delta':>15} {'Magnitude':>12} {'Mann-Whitney U':>20} {'p-value':>10}")
    print("=" * 80)
    
    for metric_name, data in aggregated_metrics.items():
        if len(data['satd']) > 0 and len(data['not_satd']) > 0:
            delta, magnitude = cliffs_delta(data['satd'], data['not_satd'])
            stat, p_value = mannwhitneyu(data['satd'], data['not_satd'], alternative='two-sided')
            
            print(f"{metric_name:<25} {delta:>15.4f} {magnitude:>12} {stat:>20.2f} {p_value:>10.4f}")
    print()

if __name__ == "__main__":
    metrics_list = ['NewAdditions', 'DiffSizes', 'EditDistances', 'CriticalEditDistances']
    
    # Aggregate metrics across all files
    aggregated_metrics = aggregate_metrics(metrics_list)
    
    # Perform and print aggregated statistical tests
    print_statistical_tests(aggregated_metrics)
