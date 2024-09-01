import os
import numpy as np
from cliffs_delta import cliffs_delta
from scipy.stats import mannwhitneyu

SRCDIR = r'D:\\OneDrive - University of Manitoba\\Documents\\HISHAM\\Research\\Tech-Debt\\csv-files-satd\\'

EXPECTED_SIGNS = {
    'SLOCAsItIs': 0.65,
    'SLOCNoCommentPrettyPrinter': 0.54,
    'SLOCStandard': 0.56,
    'CommentCodeRation': 0.72,
    'Readability': -0.37,
    'SimpleReadability': -0.49,
    'NVAR': 0.46,
    'NCOMP': 0.46,
    'Mcclure': 0.46,
    'McCabe': 0.50,
    'McCabeWOCases': 0.49,
    'IndentSTD': 0.36,
    'MaximumBlockDepth': 0.47,
    'totalFanOut': 0.52,
    'uniqueFanOut': 0.52,
    'n1': 0.56,
    'n2': 0.55,
    'N1': 0.57,
    'N2': 0.55,
    'Vocabulary': 0.57,
    'Length': 0.56,
    'Volume': 0.56,
    'Difficulty': 0.54,
    'Effort': 0.56,
    'Time': 0.56,
    'HalsteadBugs': 0.56,
    'MaintainabilityIndex': -0.57,
    'Parameters': 0.26,
    'LocalVariables': 0.49,
}

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
    satd_count = 0
    not_satd_count = 0
    
    with open(SRCDIR + file, "r", encoding='utf-8') as fr:
        line = fr.readline()  # skip header
        indices = build_indices(line)
        lines = fr.readlines()

        for line in lines:
            row = line.strip().split("\t")

            if int(row[indices['Age']]) > 730:  # Ensure the method is at least 2 years old
                satd = row[indices["SATD"]].split("#")
                if check_satd(satd):
                    satd_count += 1
                else:
                    not_satd_count += 1

                for metric_name in metrics_list:
                    metric = row[indices[metric_name]].split("#")
                    age_list = row[indices['ChangeAtMethodAge']].split('#')
                    satd = row[indices["SATD"]].split("#")

                    index_to_stop = find_index_to_stop(age_list)
                    if index_to_stop != -1:  # If index_to_stop is -1, then there are no commits with age > 730
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
    
    return metrics, satd_count, not_satd_count

def analyze_projects(metrics_list, METRIC_VALUE='first'):
    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            metrics, satd_count, not_satd_count = process_project(file, metrics_list, METRIC_VALUE)
            if satd_count < 30:
                print(f"{file}: Methods with SATD = {satd_count}, Ratio of SATD: {(satd_count / (satd_count + not_satd_count)):.2f}, Methods without SATD = {not_satd_count}")
                for metric_name, data in metrics.items():
                    if len(data['satd']) > 0 and len(data['not_satd']) > 0:
                        delta, magnitude = cliffs_delta(data['satd'], data['not_satd'])
                        expected_delta = EXPECTED_SIGNS[metric_name]
                        # Check if the sign matches the expected delta
                        if (delta < 0 and expected_delta > 0) or (delta > 0 and expected_delta < 0):
                            print(f"  {metric_name} Cliff Delta = {delta:.2f}, expected = {expected_delta:.2f}")

if __name__ == "__main__":
    metrics_list = ['SLOCAsItIs', 'SLOCNoCommentPrettyPrinter', 'SLOCStandard', 'CommentCodeRation', 'Readability', 
                    'SimpleReadability', 'NVAR', 'NCOMP', 'Mcclure', 'McCabe', 'McCabeWOCases', 'IndentSTD', 
                    'MaximumBlockDepth', 'totalFanOut', 'uniqueFanOut', 'n1', 'n2', 'N1', 'N2', 'Vocabulary', 
                    'Length', 'Volume', 'Difficulty', 'Effort', 'Time', 'HalsteadBugs', 'MaintainabilityIndex', 
                    'Parameters', 'LocalVariables']
    analyze_projects(metrics_list, METRIC_VALUE='first')
