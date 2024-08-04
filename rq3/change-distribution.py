# import os
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd

# def process_csv(file_path, metrics):
#     data = pd.read_csv(file_path, delimiter=',', encoding='latin1')
#     data = data[data['Age'] > 730]  # Filter methods at least 730 days old
    
#     filtered_data = data[metrics + ['SATD']]
    
#     # Initialize categories
#     categories = {metric: {'category_1': [], 'category_2': [], 'category_3': []} for metric in metrics}
    
#     for index, row in filtered_data.iterrows():
#         metric_values = {metric: row[metric].split('#') for metric in metrics}
#         satd_values = row['SATD'].split('#')
        
#         # Take the second value (index 1) for each metric
#         metric_values = {metric: values[1] if len(values) > 1 else values[0] for metric, values in metric_values.items()}
        
#         for metric in metrics:
#             # Determine category based on SATD values
#             if all(val == '0' for val in satd_values):
#                 categories[metric]['category_1'].append(metric_values[metric])
#             elif '1' in satd_values and satd_values[-1] == '0':
#                 categories[metric]['category_2'].append(metric_values[metric])
#             elif '1' in satd_values and satd_values[-1] == '1':
#                 categories[metric]['category_3'].append(metric_values[metric])
    
#     return categories

# def compute_cdf(values):
#     unique_vals, counts = np.unique(values, return_counts=True)
#     cumulative_counts = np.cumsum(counts)
#     cdf = cumulative_counts / cumulative_counts[-1]
#     return unique_vals, cdf

# def plot_cdf(x1, y1, x2, y2, x3, y3, title, output_file, x_min=None, x_max=None):
#     plt.figure()
#     plt.plot(x1, y1, marker='o', linestyle='-', color='b', label='Never had SATD')
#     plt.plot(x2, y2, marker='o', linestyle='-', color='g', label='Had SATD but ended without SATD')
#     plt.plot(x3, y3, marker='o', linestyle='-', color='r', label='Had SATD and ended with SATD')
#     plt.title(title)
#     plt.xlabel(title.split()[-1])
#     plt.ylabel('CDF')
#     plt.grid(True)
#     plt.legend()
    
#     # Set x-axis limits if specified
#     if x_min is not None and x_max is not None:
#         plt.xlim(x_min, x_max)

#     plt.savefig(output_file)
#     plt.close()

# def main(input_folder):
#     metrics = ['NewAdditions', 'DiffSizes', 'EditDistances']
    
#     combined_categories = {metric: {'category_1': [], 'category_2': [], 'category_3': []} for metric in metrics}

#     for file_name in os.listdir(input_folder):
#         if file_name.endswith('.csv'):
#             file_path = os.path.join(input_folder, file_name)
#             categories = process_csv(file_path, metrics)
            
#             for metric in metrics:
#                 combined_categories[metric]['category_1'].extend(categories[metric]['category_1'])
#                 combined_categories[metric]['category_2'].extend(categories[metric]['category_2'])
#                 combined_categories[metric]['category_3'].extend(categories[metric]['category_3'])

#     for metric in metrics:
#         combined_categories[metric]['category_1'] = [float(val) for val in combined_categories[metric]['category_1']]
#         combined_categories[metric]['category_2'] = [float(val) for val in combined_categories[metric]['category_2']]
#         combined_categories[metric]['category_3'] = [float(val) for val in combined_categories[metric]['category_3']]
        
#         x1, y1 = compute_cdf(combined_categories[metric]['category_1'])
#         x2, y2 = compute_cdf(combined_categories[metric]['category_2'])
#         x3, y3 = compute_cdf(combined_categories[metric]['category_3'])
        
#         title = f'CDF of {metric}'
#         output_file = f'figs/rq3/cdf_{metric}.pdf'
#         x_min = 0
#         x_max = 1000
        
#         plot_cdf(x1, y1, x2, y2, x3, y3, title, output_file, x_min, x_max)

#         print(f"CDF plot saved as '{output_file}'")

# if __name__ == "__main__":
#     input_folder = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/csv-results/part'
#     main(input_folder)



import os
import numpy as np
import matplotlib.pyplot as plt

# global variable for whehter to take the metric as the first value, last value or average
METRIC_VALUE = 'mean'

# SRCDIR = "../../software-evolution/tech-debt-results/"
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

def process(metrics_list):
    """
    Have the different metrics in a dictionary
    Each key will be a metric and the value will be a dictionary with 'satd' and 'not_satd' lists
    IMPORTANT, ALL 3 METRICS (NewAdditions, DiffSizes, EditDistances) ARE 0 IN THE FIRST COMMIT
    """
    metrics = {metric: {'satd': [], 'not_satd': []} for metric in metrics_list}
    
    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            fr = open(SRCDIR + file, "r")
            line = fr.readline()  # skip header
            indices = build_indices(line)
            lines = fr.readlines()
            for line in lines:
                data = line.strip().split("\t")
                for metric_name in metrics_list:
                    metric = data[indices[metric_name]]
                    metric = metric.split("#")

                    if METRIC_VALUE == 'first':
                        # first value of metric
                        if (len(metric) == 1):
                            metric = float(metric[0])
                        else:
                            metric = float(metric[1])
                    elif METRIC_VALUE == 'mean':
                        # get the average of the metric exlcuding the first one
                        if len(metric) == 1:
                            metric = float(metric[0])
                        else:
                            metric = metric[1:]
                            metric = [float(m) for m in metric]
                            metric = np.mean(metric)
                        # /home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/venv/lib/python3.12/site-packages/numpy/_core/fromnumeric.py:3596: RuntimeWarning: Mean of empty slice.
#   return _methods._mean(a, axis=axis, dtype=dtype,
# /home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/venv/lib/python3.12/site-packages/numpy/_core/_methods.py:138: RuntimeWarning: invalid value encountered in scalar divide
#   ret = ret.dtype.type(ret / rcount)
                    elif METRIC_VALUE == 'last':
                        # get the last value of the metric list
                        metric = float(metric[-1])
                    else:
                        print("ENTER A VALID METRIC VALUE")

                    satd = data[indices["SATD"]]
                    satd = satd.split("#")
                    
                    if metric < 0:
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

def draw_graph(metrics):
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
        # plt.xlim(0, 1)
        plt.title(f"CDF of {metric_name}")
        # plt.show()
        if METRIC_VALUE == 'first':
            plt.savefig(f'figs/rq3/first/f_{metric_name}.pdf')
        elif METRIC_VALUE == 'mean':
            plt.savefig(f'figs/rq3/mean/m_{metric_name}.pdf')
        elif METRIC_VALUE == 'last':
            plt.savefig(f'figs/rq3/last/l_{metric_name}.pdf')


if __name__ == "__main__":
    # SLOCStandard
# Readability
# SimpleReadability
# MaintainabilityIndex
# McCabe
# totalFanOut
# uniqueFanOut
# 
    metrics_list = ['NewAdditions', 'DiffSizes', 'EditDistances']
    metrics = process(metrics_list)
    draw_graph(metrics)

