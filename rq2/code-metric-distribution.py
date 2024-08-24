import os
import numpy as np
import matplotlib.pyplot as plt
from cliffs_delta import cliffs_delta  
from scipy.stats import mannwhitneyu, kstest

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

def process(metrics_list, METRIC_VALUE):
    metrics = {metric: {'satd': [], 'not_satd': []} for metric in metrics_list}
    
    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            with open(SRCDIR + file, "r", encoding='utf-8') as fr:
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
                            if index_to_stop != -1:  # if index_to_stop is -1, then there are no commits with age > 730 so keep as is
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

def calculate_cliffs_delta(metrics_list):
    metrics = process(metrics_list, METRIC_VALUE='first')

    print(f"{'Metric':<25}{'Delta':>10}{'Magnitude':>15}")
    print("=" * 50)

    for metric_name, data in metrics.items():
        satd_values = np.array(data['satd'])
        not_satd_values = np.array(data['not_satd'])

        delta, magnitude = cliffs_delta(satd_values, not_satd_values)

        print(f"{metric_name:<25}{delta:>10.2f}{magnitude:>15}")

def calculate_mannwhitneyu(metrics_list):
    metrics = process(metrics_list, METRIC_VALUE='first')

    print(f"{'Metric':<25}{'Statistic':>15}{'p-value':>20}")
    print("=" * 60)

    for metric_name, data in metrics.items():
        satd_values = np.array(data['satd'])
        not_satd_values = np.array(data['not_satd'])

        stat, p_value = mannwhitneyu(satd_values, not_satd_values, alternative='two-sided')

        print(f"{metric_name:<25}{stat:>15.2f}{p_value:>20.2f}")

def calculate_ks_test(metrics_list):
    metrics = process(metrics_list, METRIC_VALUE='first')

    print(f"{'Metric':<25}{'SATD p-value':>20}{'Non-SATD p-value':>20}")
    print("=" * 65)

    for metric_name, data in metrics.items():
        satd_values = np.array(data['satd'])
        not_satd_values = np.array(data['not_satd'])

        # Perform the K-S test against a normal distribution
        ks_stat_satd, ks_p_value_satd = kstest(satd_values, 'norm', args=(np.mean(satd_values), np.std(satd_values)))
        ks_stat_not_satd, ks_p_value_not_satd = kstest(not_satd_values, 'norm', args=(np.mean(not_satd_values), np.std(not_satd_values)))

        print(f"{metric_name:<25}{ks_p_value_satd:>20.2f}{ks_p_value_not_satd:>20.2f}")

if __name__ == "__main__":
    metrics_list = ['SLOCStandard', 'Readability', 'SimpleReadability', 'MaintainabilityIndex', 'McCabe', 'totalFanOut', 'uniqueFanOut']

    # Calculate and display Cliff's Delta for each metric
    calculate_cliffs_delta(metrics_list)
    print()
    
    # Calculate and display Mann-Whitney U test results for each metric
    calculate_mannwhitneyu(metrics_list)
    print()

    # Calculate and display K-S test results for each metric
    calculate_ks_test(metrics_list)
