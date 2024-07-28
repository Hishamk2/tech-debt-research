import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to classify methods into categories based on SATD
def classify_methods(df):
    categories = {1: [], 2: [], 3: []}
    for index, row in df.iterrows():
        satd_values = row['SATD'].split('#')
        if len(satd_values) == 2:
            initial, final = satd_values
            initial, final = int(initial), int(final)
            if initial == 0 and final == 0:
                categories[1].append(row)
            elif initial == 1 and final == 1:
                categories[2].append(row)
            elif initial == 1 and final == 0:
                categories[3].append(row)
    return categories

# Function to plot and save CDFs
def plot_cdf(data, metric, category_name, output_dir):
    data = np.sort(data)
    cdf = np.arange(1, len(data)+1) / len(data)
    plt.figure()
    plt.plot(data, cdf, marker='.', linestyle='none')
    plt.xlabel(metric)
    plt.ylabel('CDF')
    plt.title(f'{metric} CDF - {category_name}')
    output_path = os.path.join(output_dir, f'{metric}_CDF_{category_name}.png')
    plt.savefig(output_path)
    plt.close()

# Main function to process files and generate CDFs
def generate_cdfs(input_dir, output_dir):
    metrics = ['SLOCStandard', 'Readability', 'SimpleReadability', 'MaintainabilityIndex', 'McCabe', 'totalFanOut', 'uniqueFanOut']
    
    all_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.csv')]
    
    for file in all_files:
        df = pd.read_csv(file)
        categories = classify_methods(df)
        
        for category, rows in categories.items():
            if rows:
                category_name = f'Category_{category}'
                category_df = pd.DataFrame(rows)
                
                for metric in metrics:
                    data = category_df[metric].apply(lambda x: float(x.split('#')[-1]))
                    plot_cdf(data, metric, category_name, output_dir)

# Run the script
input_directory = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/csv-results/part'  # Replace with your input directory path
output_directory = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/figs'  # Replace with your output directory path

os.makedirs(output_directory, exist_ok=True)
generate_cdfs(input_directory, output_directory)
