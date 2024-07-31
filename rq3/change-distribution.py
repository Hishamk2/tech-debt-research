import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def process_csv(file_path, metrics):
    data = pd.read_csv(file_path, delimiter=',', encoding='latin1')
    data = data[data['Age'] > 730]  # Filter methods at least 730 days old
    
    filtered_data = data[metrics + ['SATD']]
    
    # Initialize categories
    categories = {metric: {'category_1': [], 'category_2': [], 'category_3': []} for metric in metrics}
    
    for index, row in filtered_data.iterrows():
        metric_values = {metric: row[metric].split('#') for metric in metrics}
        satd_values = row['SATD'].split('#')
        
        # Take the second value (index 1) for each metric
        metric_values = {metric: values[1] if len(values) > 1 else values[0] for metric, values in metric_values.items()}
        
        for metric in metrics:
            # Determine category based on SATD values
            if all(val == '0' for val in satd_values):
                categories[metric]['category_1'].append(metric_values[metric])
            elif '1' in satd_values and satd_values[-1] == '0':
                categories[metric]['category_2'].append(metric_values[metric])
            elif '1' in satd_values and satd_values[-1] == '1':
                categories[metric]['category_3'].append(metric_values[metric])
    
    return categories

def compute_cdf(values):
    unique_vals, counts = np.unique(values, return_counts=True)
    cumulative_counts = np.cumsum(counts)
    cdf = cumulative_counts / cumulative_counts[-1]
    return unique_vals, cdf

def plot_cdf(x1, y1, x2, y2, x3, y3, title, output_file, x_min=None, x_max=None):
    plt.figure()
    plt.plot(x1, y1, marker='o', linestyle='-', color='b', label='Never had SATD')
    plt.plot(x2, y2, marker='o', linestyle='-', color='g', label='Had SATD but ended without SATD')
    plt.plot(x3, y3, marker='o', linestyle='-', color='r', label='Had SATD and ended with SATD')
    plt.title(title)
    plt.xlabel(title.split()[-1])
    plt.ylabel('CDF')
    plt.grid(True)
    plt.legend()
    
    # Set x-axis limits if specified
    if x_min is not None and x_max is not None:
        plt.xlim(x_min, x_max)

    plt.savefig(output_file)
    plt.close()

def main(input_folder):
    metrics = ['NewAdditions', 'DiffSizes', 'EditDistances']
    
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
        x_min = 0
        x_max = 1000
        
        plot_cdf(x1, y1, x2, y2, x3, y3, title, output_file, x_min, x_max)

        print(f"CDF plot saved as '{output_file}'")

if __name__ == "__main__":
    input_folder = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/csv-results/part'
    main(input_folder)
