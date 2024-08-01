# import os
# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd

# def process_csv(file_path, metrics):
#     # data = pd.read_csv(file_path, delimiter=',', encoding='latin1')
#     data = pd.read_csv(file_path, delimiter='\t', encoding='latin1')
#     data = data[data['Age'] > 730]
    
#     filtered_data = data[metrics + ['SATD', 'ChangeAtMethodAge']]
    
#     categories = {metric: {'category_1': [], 'category_2': [], 'category_3': []} for metric in metrics}
    
#     for index, row in filtered_data.iterrows():
#         metric_values = {metric: row[metric].split('#') for metric in metrics}

#         satd_values = row['SATD'].split('#')
#         change_at_method_age_values = row['ChangeAtMethodAge'].split('#')
        
#         valid_commits = [i for i, age in enumerate(change_at_method_age_values) if int(age) <= 730]
        
#         if valid_commits:
#             metric_values = {metric: [values[i] for i in valid_commits] for metric, values in metric_values.items()}
#             satd_values = [satd_values[i] for i in valid_commits]
        
#             for metric in metrics:
#                 if all(val == '0' for val in satd_values):
#                     categories[metric]['category_1'].extend(metric_values[metric])
#                 elif '1' in satd_values and satd_values[-1] == '0':
#                     categories[metric]['category_2'].extend(metric_values[metric])
#                 elif '1' in satd_values and satd_values[-1] == '1':
#                     categories[metric]['category_3'].extend(metric_values[metric])
    
#     return categories

# def compute_cdf(values):
#     unique_vals, counts = np.unique(values, return_counts=True)
#     cumulative_counts = np.cumsum(counts)
#     cdf = cumulative_counts / cumulative_counts[-1]
#     return unique_vals, cdf

# def plot_cdf(x1, y1, x2, y2, x3, y3, title, output_file):
#     plt.figure()
#     plt.plot(x1, y1, marker='o', linestyle='-', color='b', label='Never had SATD')
#     plt.plot(x2, y2, marker='o', linestyle='-', color='g', label='Had SATD but ended without SATD')
#     plt.plot(x3, y3, marker='o', linestyle='-', color='r', label='Had SATD and ended with SATD')
#     plt.title(title)
#     plt.xlabel(title.split()[-1])
#     plt.ylabel('CDF')
#     plt.grid(True)
#     plt.legend()
#     plt.savefig(output_file)
#     plt.close()

# def main(input_folder):
#     metrics = [
#         'SLOCStandard', 'Readability', 'SimpleReadability', 
#         'MaintainabilityIndex', 'McCabe', 'totalFanOut', 'uniqueFanOut'
#     ]
    
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
#         output_file = f'figs/rq2-1/cdf_{metric}.pdf'
        
#         plot_cdf(x1, y1, x2, y2, x3, y3, title, output_file)

#         print(f"CDF plot saved as '{output_file}'")

# if __name__ == "__main__":
#     # input_folder = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/csv-results/part'
#     input_folder = '/home/student/kidwaih1/Documents/Tech-Debt/software-evolution/tech-debt-results'
#     main(input_folder)

# Three different categories:
# 1. Never had SATD (always 0)
# 2. Had SATD but ended without SATD (1 somewhere, 0 at the end)
# 3. Had SATD and ended with SATD (1 somewhere, 1 at the end)
# Find the code metric distribution between the three different categories (as above) for a given metric: 
# SLOCStandard

# import os
# import numpy as np
# import matplotlib.pyplot as plt

# SRCDIR = "../../software-evolution/tech-debt-results/"



# def build_indices(line):
#     indexes = {}
#     data = line.strip().split("\t")
#     for i in range(len(data)):
#         indexes[data[i]] = i
#     return indexes    

# def check_satd(satd):
#     for s in satd:
#         s = int(s)
#         if s == 1:
#             return True
#     return False

# # def get_method_category(satd: list) -> int:
# #     """
# #     Three different categories:
# #     1. Never had SATD (always 0)
# #     2. Had SATD but ended without SATD (1 somewhere, 0 at the end)
# #     3. Had SATD and ended with SATD (1 somewhere, 1 at the end)
# #     """ 
# #     index = 0
# #     for s in satd:
# #         s = int(s)
# #         last = satd[len(satd) - 1]
# #         if (s == 1 and index != len(satd) - 1 and last == 0):
# #             return 2
# #         elif (s == 1 and index != len(satd) - 1 and last == 1):
# #             return 3    
# #         index += 1

# #     return 1

# def process():
#     """"
#     Have the three different categories in a dictionary
#     Each key will be a category and the value will be a list the metric values
#     Remember to make sure to discard any methods that are less than 2 years old
#     And make sure to discard anything that happens after 2years old (use the ChangeAtMethodAge)
#     """
#     metrics = {}
#     metrics['satd'] = []
#     metrics['not_satd']= []

#     # metrics['category_1'] = []
#     # metrics['category_2'] = []
#     # metrics['category_3'] = []
    
#     for file in os.listdir(SRCDIR):
#         fr = open(SRCDIR + file, "r")
#         line = fr.readline() # skip header
#         indices = build_indices(line)
#         lines = fr.readlines()
#         for line in lines:
#             data = line.strip().split("\t")
#             metric = data[indices["SLOCStandard"]]
#             metric = metric.split("#")
#             metric = float(metric[0])

#             satd = data[indices["SATD"]]
#             satd = satd.split("#")
            
#             if metric < 0:
#                continue # something is wrong
#             if check_satd(satd):
#                metrics['satd'].append(metric)
#             else:
#                 metrics['not_satd'].append(metric)
#             # category = get_method_category(satd)
#             # if category == 1:
#             #     metrics['category_1'].append(metric)
#             # elif category == 2:
#             #     metrics['category_2'].append(metric)
#             # else:
#             #     metrics['category_3'].append(metric)

#         # print(f'category_2: {metrics["category_2"]} ')   
#     return metrics         

# def ecdf(a):
#     x, counts = np.unique(a, return_counts=True)
#     cusum = np.cumsum(counts)
#     return x, cusum / cusum[-1]

# def draw_graph(metrics):
#     x, y = ecdf(metrics['satd'])
#     ln = (plt.plot(x, y))
#     plt.setp(ln, ls="-", linewidth=3, color='r', label='SATD')

#     x, y = ecdf(metrics['not_satd'])
#     ln = (plt.plot(x, y))
#     plt.setp(ln, ls="--", linewidth=3, color='blue', label='NOT_SATD')

#     # x, y = ecdf(metrics['category_1'])
#     # ln = (plt.plot(x, y))
#     # plt.setp(ln, ls="-", linewidth=3, color='r', label='SATD')

#     # x, y = ecdf(metrics['category_2'])
#     # ln = (plt.plot(x, y))
#     # plt.setp(ln, ls="--", linewidth=3, color='blue', label='NOT_SATD')

#     # x, y = ecdf(metrics['category_3'])
#     # ln = (plt.plot(x, y))
#     # plt.setp(ln, ls="--", linewidth=3, color='green', label='NOT_SATD')

#     plt.legend()
#     plt.xlabel("MI")
#     plt.ylabel("CDF")
#     plt.xlim(0, 2000)
#     plt.show()

# if __name__ == "__main__":
#     metrics  = process()
#     draw_graph(metrics)

import os
import numpy as np
import matplotlib.pyplot as plt

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
                    metric = float(metric[0])

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
        plt.setp(ln, ls="-", linewidth=3, color='r', label=f'{metric_name} SATD')
        
        x, y = ecdf(data['not_satd'])
        ln = plt.plot(x, y)
        plt.setp(ln, ls="--", linewidth=3, color='blue', label=f'{metric_name} NOT_SATD')
        
        plt.legend()
        plt.xlabel(metric_name)
        plt.ylabel("CDF")
        plt.xlim(0, 1)
        plt.title(f"CDF of {metric_name}")
        # plt.show()
        plt.savefig(f'{metric_name}.pdf')


if __name__ == "__main__":
    # SLOCStandard
# Readability
# SimpleReadability
# MaintainabilityIndex
# McCabe
# totalFanOut
# uniqueFanOut
# 
    metrics_list = ['SLOCStandard', 'Readability', 'SimpleReadability', 'MaintainabilityIndex', 'McCabe', 'totalFanOut', 'uniqueFanOut']
    metrics = process(metrics_list)
    draw_graph(metrics)

