import os
import numpy as np
from scipy.stats import mannwhitneyu
from cliffs_delta import cliffs_delta

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

def categorize_cliffs_delta(delta):
    """ Categorize Cliff's Delta effect size """
    if abs(delta) < 0.147:
        return 'N'  # Negligible
    elif abs(delta) < 0.33:
        return 'S'  # Small
    elif abs(delta) < 0.474:
        return 'M'  # Medium
    else:
        return 'L'  # Large

def process_project(file, metrics_list):
    metrics = {metric: {'satd': [], 'not_satd': []} for metric in metrics_list}
    
    with open(os.path.join(SRCDIR, file), "r", encoding='utf-8') as fr:
        line = fr.readline()  # skip header
        indices = build_indices(line)
        lines = fr.readlines()

        for line in lines:
            row = line.strip().split("\t")
            
            if int(row[indices['Age']]) > 730:  # Ensure the method is at least 2 years old
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

def analyze_projects(metrics_list):
    project_results = {metric: {'N': 0, 'S': 0, 'M': 0, 'L': 0, 'total': 0} for metric in metrics_list}

    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            metrics = process_project(file, metrics_list)

            for metric_name, data in metrics.items():
                if len(data['satd']) > 0 and len(data['not_satd']) > 0:
                    # Calculate Cliff's Delta
                    delta, _ = cliffs_delta(data['satd'], data['not_satd'])
                    category = categorize_cliffs_delta(delta)
                    project_results[metric_name][category] += 1
                    project_results[metric_name]['total'] += 1

    # Calculate the percentage of projects with each Cliff's Delta category
    for metric_name, results in project_results.items():
        if results['total'] > 0:
            n_percent = (results['N'] / results['total']) * 100
            s_percent = (results['S'] / results['total']) * 100
            m_percent = (results['M'] / results['total']) * 100
            l_percent = (results['L'] / results['total']) * 100
            print(f"{metric_name:<25} N: {n_percent:>6.2f}%  S: {s_percent:>6.2f}%  M: {m_percent:>6.2f}%  L: {l_percent:>6.2f}%")

if __name__ == "__main__":
    metrics_list = ['NewAdditions', 'DiffSizes', 'EditDistances', 'CriticalEditDistances']
    analyze_projects(metrics_list)
