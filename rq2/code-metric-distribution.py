import os
import numpy as np
from cliffs_delta import cliffs_delta  # Assuming this is already installed and working
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

def analyze_projects(metrics_list, METRIC_VALUE='first'):
    # Initialize the summary table
    summary = {metric: {'N': 0, 'S': 0, 'M': 0, 'L': 0, 'total': 0} for metric in metrics_list}

    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            metrics = process_project(file, metrics_list, METRIC_VALUE)
            # print(metrics)
            for metric_name, data in metrics.items():
                if len(data['satd']) > 0 and len(data['not_satd']) > 0:
                    delta, magnitude = cliffs_delta(data['satd'], data['not_satd'])
                    # print(f"File: {file}, Metric: {metric_name}, Delta: {delta}, Magnitude: {magnitude}")
                    category = categorize_cliffs_delta(delta)
                    # print(f"File: {file}, Metric: {metric_name}, Category: {category}")
                    summary[metric_name][category] += 1
                    summary[metric_name]['total'] += 1
                    # print(f"Updated summary for {metric_name}: {summary[metric_name]}")


            # print(summary)
    # Print the summary table
    print(f"{'Metric':<20} {'N (%)':<10} {'S (%)':<10} {'M (%)':<10} {'L (%)':<10}")
    print("=" * 60)
    for metric_name, counts in summary.items():
        if counts['total'] > 0:
            n_percent = (counts['N'] / counts['total']) * 100
            s_percent = (counts['S'] / counts['total']) * 100
            m_percent = (counts['M'] / counts['total']) * 100
            l_percent = (counts['L'] / counts['total']) * 100
            print(f"{metric_name:<20} {n_percent:<10.0f} {s_percent:<10.0f} {m_percent:<10.0f} {l_percent:<10.0f}")

if __name__ == "__main__":
    metrics_list = ['SLOCStandard', 'Readability', 'SimpleReadability', 'MaintainabilityIndex', 'totalFanOut']
    analyze_projects(metrics_list, METRIC_VALUE='first')
