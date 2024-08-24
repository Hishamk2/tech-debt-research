import os
import numpy as np
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

def process_project(file, metrics_list, METRIC_VALUE):
    metrics = {metric: {'satd': [], 'not_satd': []} for metric in metrics_list}
    
    fr = open(SRCDIR + file, "r", encoding='utf-8')
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
                    continue  # something is wrong
                if check_satd(satd):
                    metrics[metric_name]['satd'].append(metric)
                else:
                    metrics[metric_name]['not_satd'].append(metric)
    
    return metrics

def analyze_projects(metrics_list, METRIC_VALUE='mean'):
    project_results = {metric: {'significant': 0, 'total': 0, 'non_significant_files': []} for metric in metrics_list}

    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            metrics = process_project(file, metrics_list, METRIC_VALUE)

            for metric_name, data in metrics.items():
                if len(data['satd']) > 0 and len(data['not_satd']) > 0:
                    stat, p_value = mannwhitneyu(data['satd'], data['not_satd'], alternative='two-sided')
                    project_results[metric_name]['total'] += 1
                    if p_value < 0.05:  # commonly used threshold for statistical significance
                        project_results[metric_name]['significant'] += 1
                    else:
                        project_results[metric_name]['non_significant_files'].append((file, p_value))

    # Calculate the percentage of projects with statistically significant differences
    for metric_name, results in project_results.items():
        print()
        if results['total'] > 0:
            percentage_significant = (results['significant'] / results['total']) * 100
            print(f"{metric_name:<25}{percentage_significant:>10.2f}% of projects show statistically significant difference")
            if results['non_significant_files']:
                print(f"Projects with no significant difference for {metric_name}:")
                for non_sig_file, p_value in results['non_significant_files']:
                    print(f"  - {non_sig_file} (p-value: {p_value:.4f})")

if __name__ == "__main__":
    metrics_list = ['SLOCStandard', 'Readability', 'SimpleReadability', 'MaintainabilityIndex', 'McCabe', 'totalFanOut', 'uniqueFanOut']
    analyze_projects(metrics_list, METRIC_VALUE='first')
