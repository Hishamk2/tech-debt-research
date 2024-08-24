import os
import numpy as np
from scipy.stats import mannwhitneyu
from cliffs_delta import cliffs_delta

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

def process_project(file):
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

def analyze_projects():
    project_results = {'numRevisions': {'significant': 0, 'total': 0}}

    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            metrics = process_project(file)

            data = metrics['numRevisions']
            if len(data['satd']) > 0 and len(data['not_satd']) > 0:
                # Perform the Mann-Whitney U test (Wilcoxon rank-sum test)
                stat, p_value = mannwhitneyu(data['satd'], data['not_satd'], alternative='two-sided')
                project_results['numRevisions']['total'] += 1
                if p_value < 0.05:  # Commonly used threshold for statistical significance
                    project_results['numRevisions']['significant'] += 1

    # Calculate the percentage of projects with statistically significant differences
    results = project_results['numRevisions']
    if results['total'] > 0:
        percentage_significant = (results['significant'] / results['total']) * 100
        print(f"Number of Revisions: {percentage_significant:.2f}% of projects show statistically significant difference")

if __name__ == "__main__":
    # Analyze projects for statistically significant differences
    analyze_projects()
