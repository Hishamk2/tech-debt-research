import os
import numpy as np
import matplotlib.pyplot as plt
from cliffs_delta import cliffs_delta  
# from scipy.stats import wilcoxon
from scipy.stats import mannwhitneyu


# SCALE = 'log'
# METRIC_VALUE = 'mean' # first, mean, last

# SRCDIR = "../../software-evolution/tech-debt-results/"
# SRCDIR = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/csv-files-satd/'
SRCDIR = r'D:\\OneDrive - University of Manitoba\\Documents\\HISHAM\\Research\\Tech-Debt\\csv-files-satd\\'
# SRCDIR = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/csv-results/full/'

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
    """
    Have the different metrics in a dictionary
    Each key will be a metric and the value will be a dictionary with 'satd' and 'not_satd' lists
    """
    metrics = {metric: {'satd': [], 'not_satd': []} for metric in metrics_list}
    
    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            fr = open(SRCDIR + file, "r", encoding='utf-8')
            line = fr.readline()  # skip header
            indices = build_indices(line)
            lines = fr.readlines()

            # counter = 0

            for line in lines:
                # counter += 1
                # if counter > 100:
                #     break

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
                            # print(metric)
                            metric = float(metric[0])
                            # print(file, row[indices['file']])
                            # print(metric)
                        elif METRIC_VALUE == 'mean':
                            # print(file, row[indices['file']])
                            # print(metric)
                            metric = [float(m) for m in metric]
                            metric = np.mean(metric)
                            # print(metric)
                        elif METRIC_VALUE == 'last':
                            # print(metric)
                            metric = float(metric[-1])
                            # print(file, row[indices['file']])
                            # print(metric)
                        else:
                            print('ENTER A VALID METRIC VALUE')
                        
                        if metric < 0:
                            # print('NEGATIVE METRIC VALUE')
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

def draw_graph(metrics, METRIC_VALUE, SCALE):
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
                # pass
                plt.xlim(0, 75)
            elif metric_name == 'totalFanOut':
                # pass
                plt.xlim(0, 100)
            elif metric_name == 'uniqueFanOut':
                # pass
                plt.xlim(0, 75)
            
        # plt.xlim(0, 1)
        plt.title(f"CDF of {metric_name}")
        # plt.show()
        if METRIC_VALUE == 'first':
            if SCALE == 'log':
                plt.savefig(f'figs/rq2/first/log/f_{metric_name}.pdf')
            else:
                plt.savefig(f'figs/rq2/first/linear/f_{metric_name}.pdf')
        elif METRIC_VALUE == 'mean':
            if SCALE == 'log':
                plt.savefig(f'figs/rq2/mean/log/m_{metric_name}.pdf')
            else:
                plt.savefig(f'figs/rq2/mean/linear/m_{metric_name}.pdf')
        elif METRIC_VALUE == 'last':
            if SCALE == 'log':
                plt.savefig(f'figs/rq2/last/log/l_{metric_name}.pdf')
            else:
                plt.savefig(f'figs/rq2/last/linear/l_{metric_name}.pdf')

def calculate_cliffs_delta(metrics_list):
    metrics = process(metrics_list, METRIC_VALUE='first') 

    for metric_name, data in metrics.items():
        satd_values = np.array(data['satd'])
        not_satd_values = np.array(data['not_satd'])
        
        delta, magnitude = cliffs_delta(satd_values, not_satd_values)
        
        print(f"Cliff's Delta for {metric_name}: Delta = {delta}, Magnitude = {magnitude}")

def calculate_mannwhitneyu(metrics_list):
    metrics = process(metrics_list, METRIC_VALUE='first')

    for metric_name, data in metrics.items():
        satd_values = np.array(data['satd'])
        not_satd_values = np.array(data['not_satd'])

        stat, p_value = mannwhitneyu(satd_values, not_satd_values, alternative='two-sided')

        print(f"Mann-Whitney U test for {metric_name}: Statistic = {stat}, p-value = {p_value}")



if __name__ == "__main__":
    metrics_list = ['SLOCStandard', 'Readability', 'SimpleReadability', 'MaintainabilityIndex', 'McCabe', 'totalFanOut', 'uniqueFanOut']
    # metrics_list = ['SLOCStandard']
    # metrics = process(metrics_list)
    # draw_graph(metrics)
    # Loop over METRIC_VALUE and SCALE
        # Calculate and display Cliff's Delta for each metric
    calculate_cliffs_delta(metrics_list)

    calculate_mannwhitneyu(metrics_list)

    # for METRIC_VALUE in ['first', 'mean', 'last']:
    #     for SCALE in ['log', 'linear']:
    #         metrics = process(metrics_list, METRIC_VALUE)
    #         draw_graph(metrics, METRIC_VALUE, SCALE)

