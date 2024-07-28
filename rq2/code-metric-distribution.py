# three different categories I am using for my research questions are the following:
# 1. Methods that never had SATD (so always 0)
# 2. Methods that had SATD (1) and ended with SATD (1)
# 3. Methods that had SATD (1) and ended without SATD (0)

# Write a python script that takes in a folder of csv files and makes a cdf 
# (save it to somewhere instead of showing since I am working on ubuntu) 
# of various code metric distributions between the three above categories. 
# 
# Use the following columns for each cdf, SLOCStandard
# Readability
# SimpleReadability
# MaintainabilityIndex
# McCabe
# totalFanOut
# uniqueFanOut

# Use one for loop (like don't iterate through the whole csv file to get the categories THEN again iterate through the categores (O(2n)))
# 
# row_category(row) -> category:
#   # 0 means never had SATD, 1 means had SATD and ended with SATD, 2 means had SATD and ended without SATD
#   # Assuming row is a string (if not, convert to string)
#   if splitted row has all 0's, return 0   
#   if splitted row has 1's and the last element is 1, return 1
#   if splitted row has 1's and the last element is 0, return 2
# 
# for row in csv file:
#   for metric in metrics:
#       if row is category1:
#           metric1.append(row[metric].split()[0])
#       if row is category2:
#           metric2.append(row[metric].split()[0])      
#       if row is category3:
#           metric3.append(row[metric].split()[0])
# 
# for metric in metrics:
#   for each category in [metric1, metric2, metric3]:
#       plot cdf of category
#


# TODO MAKE SURE TO DISCARD METHODS THAT ARE LESS THAN 2 YEARS AND TRIM TO 2 YRS

print('TODO MAKE SURE TO DISCARD METHODS THAT ARE LESS THAN 2 YEARS AND TRIM TO 2 YRS')

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_cdf(data, metric, output_folder):
    data = np.array(data)
    data = data.astype(np.float)
    data = np.sort(data)
    yvals = np.arange(len(data))/float(len(data))
    plt.plot(data, yvals, label=metric)
    plt.xlabel(metric)
    plt.ylabel('CDF')
    plt.legend()
    plt.savefig(os.path.join(output_folder, metric + '.png'))
    plt.close()

def row_category(row: pd.Series) -> int:
    # convert row to string
    row = row.to_string()
    splitted_row = row.split('#')
    if all([int(x) == 0 for x in splitted_row]):
        return 0
    elif any([int(x) == 1 for x in splitted_row]) and int(splitted_row[-1]) == 1:
        return 1
    elif any([int(x) == 1 for x in splitted_row]) and int(splitted_row[-1]) == 0:
        return 2
    

def generate_cdfs(input_folder, output_folder):
    # iterate through each row in each csv file in the input folder

    for file in os.listdir(input_folder):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(input_folder, file))
            metrics = ['SLOCStandard', 'Readability', 'SimpleReadability', 'MaintainabilityIndex', 'McCabe', 'totalFanOut', 'uniqueFanOut']

    for file in os.listdir(input_folder):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(input_folder, file))
            metrics = ['SLOCStandard', 'Readability', 'SimpleReadability', 'MaintainabilityIndex', 'McCabe', 'totalFanOut', 'uniqueFanOut']
            metric1 = {}
            metric2 = {}
            metric3 = {}

            for index, row in df.iterrows():
                category = row_category(row)
                row = row.to_string()
                for metric in metrics:
                    if category == 0:
                        if metric not in metric1:
                            metric1[metric] = []
                        metric1[metric].append(row[metric].split('#')[0])
                    elif category == 1:
                        if metric not in metric2:
                            metric2[metric] = []
                        metric2[metric].append(row[metric].split('#')[0])
                    elif category == 2:
                        if metric not in metric3:
                            metric3[metric] = []
                        metric3[metric].append(row[metric].split('#')[0])

            for metric in metrics:
                plot_cdf(metric1[metric], metric, output_folder)
                plot_cdf(metric2[metric], metric, output_folder)
                plot_cdf(metric3[metric], metric, output_folder)

if __name__ == '__main__':
    input_folder = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/csv-results/part'
    output_folder = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/figs'

    generate_cdfs(input_folder, output_folder)