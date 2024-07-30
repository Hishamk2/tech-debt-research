
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def process_csv(file_path, metrics):
    data = pd.read_csv(file_path, delimiter=',', encoding='latin1')
    data = data[data['Age'] > 730]
    
    filtered_data = data[metrics + ['SATD', 'ChangeAtMethodAge']]
    
    categories = {metric: {'category_1': [], 'category_2': [], 'category_3': []} for metric in metrics}
    
    for index, row in filtered_data.iterrows():
        metric_values = {metric: row[metric].split('#') for metric in metrics}
        satd_values = row['SATD'].split('#')
        change_at_method_age_values = row['ChangeAtMethodAge'].split('#')
        
        valid_commits = [i for i, age in enumerate(change_at_method_age_values) if int(age) <= 730]
        
        if valid_commits:
            metric_values = {metric: [values[i] for i in valid_commits] for metric, values in metric_values.items()}
            satd_values = [satd_values[i] for i in valid_commits]
        
            for metric in metrics:
                if all(val == '0' for val in satd_values):
                    categories[metric]['category_1'].extend(metric_values[metric])
                elif '1' in satd_values and satd_values[-1] == '0':
                    categories[metric]['category_2'].extend(metric_values[metric])
                elif '1' in satd_values and satd_values[-1] == '1':
                    categories[metric]['category_3'].extend(metric_values[metric])
    
    return categories

def compute_cdf(values):
    unique_vals, counts = np.unique(values, return_counts=True)
    cumulative_counts = np.cumsum(counts)
    cdf = cumulative_counts / cumulative_counts[-1]
    return unique_vals, cdf

def plot_cdf(x1, y1, x2, y2, x3, y3, title, output_file):
    plt.figure()
    plt.plot(x1, y1, marker='o', linestyle='-', color='b', label='Never had SATD')
    plt.plot(x2, y2, marker='o', linestyle='-', color='g', label='Had SATD but ended without SATD')
    plt.plot(x3, y3, marker='o', linestyle='-', color='r', label='Had SATD and ended with SATD')
    plt.title(title)
    plt.xlabel(title.split()[-1])
    plt.ylabel('CDF')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_file)
    plt.close()

def main(input_folder):
    metrics = [
        'NewAdditions', 'DiffSizes', 'EditDistances'
    ]
    
    combined_categories = {metric: {'category_1': [], 'category_2': [], 'category_3': []} for metric in metrics}

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_folder, file_name)
            categories = process_csv(file_path, metrics)
            
            for metric in metrics:
                combined_categories[metric]['category_1'].extend(categories[metric]['category_1'])
                combined_categories[metric]['category_2'].extend(categories[metric]['category_2'])
                combined_categories[metric]['category_3'].extend(categories[metric]['category_3'])

    for metric in metrics:
        combined_categories[metric]['category_1'] = [float(val) for val in combined_categories[metric]['category_1']]
        combined_categories[metric]['category_2'] = [float(val) for val in combined_categories[metric]['category_2']]
        combined_categories[metric]['category_3'] = [float(val) for val in combined_categories[metric]['category_3']]
        
        x1, y1 = compute_cdf(combined_categories[metric]['category_1'])
        x2, y2 = compute_cdf(combined_categories[metric]['category_2'])
        x3, y3 = compute_cdf(combined_categories[metric]['category_3'])
        
        title = f'CDF of {metric}'
        output_file = f'figs/rq3/cdf_{metric}.pdf'
        
        plot_cdf(x1, y1, x2, y2, x3, y3, title, output_file)

        print(f"CDF plot saved as '{output_file}'")

if __name__ == "__main__":
    input_folder = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/csv-results/part'
    main(input_folder)
