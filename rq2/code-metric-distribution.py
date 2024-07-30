import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Read the data
file_path = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/csv-results/full/full_atmosphere.csv'  # Replace with your file path
data = pd.read_csv(file_path, delimiter=',', encoding='latin1')

# Filter methods that are at least 730 days old
data = data[data['Age'] > 730]

# Extract relevant columns
columns = ['SLOCStandard', 'SATD', 'ChangeAtMethodAge']
filtered_data = data[columns]

# Classify methods into three categories
category_1 = []
category_2 = []
category_3 = []

for index, row in filtered_data.iterrows():
    sloc_values = row['SLOCStandard'].split('#')
    satd_values = row['SATD'].split('#')
    change_at_method_age_values = row['ChangeAtMethodAge'].split('#')
    
    # Filter out commits older than 2 years (730 days)
    valid_commits = [i for i, age in enumerate(change_at_method_age_values) if int(age) <= 730]
    
    if valid_commits:
        sloc_values = [sloc_values[i] for i in valid_commits]
        satd_values = [satd_values[i] for i in valid_commits]
    
        # Classify the method
        if all(val == '0' for val in satd_values):
            category_1.extend(sloc_values)
        elif '1' in satd_values and satd_values[-1] == '0':
            category_2.extend(sloc_values)
        elif '1' in satd_values and satd_values[-1] == '1':
            category_3.extend(sloc_values)

def compute_cdf(values):
    unique_vals, counts = np.unique(values, return_counts=True)
    cumulative_counts = np.cumsum(counts)
    cdf = cumulative_counts / cumulative_counts[-1]
    return unique_vals, cdf

# Convert SLOC values to integers
category_1 = [int(val) for val in category_1]
category_2 = [int(val) for val in category_2]
category_3 = [int(val) for val in category_3]

# Compute CDFs
x1, y1 = compute_cdf(category_1)
x2, y2 = compute_cdf(category_2)
x3, y3 = compute_cdf(category_3)

# Plot CDFs
plt.plot(x1, y1, marker='o', linestyle='-', color='b', label='Never had SATD')
plt.plot(x2, y2, marker='o', linestyle='-', color='g', label='Had SATD but ended without SATD')
plt.plot(x3, y3, marker='o', linestyle='-', color='r', label='Had SATD and ended with SATD')

# Customize plot
plt.title('CDF of SLOCStandard')
plt.xlabel('SLOCStandard')
plt.ylabel('CDF')
plt.grid(True)
plt.legend()
plt.savefig('cdf_plot.pdf')

print("CDF plot saved as 'cdf_plot.pdf'")
