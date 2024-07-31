import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def process_csv(file_path):
    data = pd.read_csv(file_path, delimiter=',', encoding='latin1')
    data = data[data['Age'] > 730]
    
    filtered_data = data[['Buggycommiit', 'SATD', 'ChangeAtMethodAge', 'PotentiallyBuggycommit', 'RiskyCommit']]

    categories = {
        'Buggycommiit': {'category_1': [], 'category_2': [], 'category_3': []},
        'PotentiallyBuggycommit': {'category_1': [], 'category_2': [], 'category_3': []},
        'RiskyCommit': {'category_1': [], 'category_2': [], 'category_3': []}
    }
    buggy_rows = []

    for index, row in filtered_data.iterrows():
        buggy_values = row['Buggycommiit'].split('#')
        satd_values = row['SATD'].split('#')
        change_at_method_age_values = row['ChangeAtMethodAge'].split('#')
        potentially_buggy_values = row['PotentiallyBuggycommit'].split('#')
        risky_values = row['RiskyCommit'].split('#')
        
        valid_commits = [i for i, age in enumerate(change_at_method_age_values) if int(age) <= 730]
        
        if valid_commits:
            buggy_values = [buggy_values[i] for i in valid_commits]
            satd_values = [satd_values[i] for i in valid_commits]
            potentially_buggy_values = [potentially_buggy_values[i] for i in valid_commits]
            risky_values = [risky_values[i] for i in valid_commits]
        
            for i in range(len(buggy_values)):
                if buggy_values[i] == '1':
                    buggy_rows.append(index + 1)  # +1 to make it 1-based index for rows
                    if all(val == '0' for val in satd_values):
                        categories['Buggycommiit']['category_1'].append(1)
                    elif '1' in satd_values and satd_values[-1] == '0':
                        categories['Buggycommiit']['category_2'].append(1)
                    elif '1' in satd_values and satd_values[-1] == '1':
                        categories['Buggycommiit']['category_3'].append(1)
                if potentially_buggy_values[i] == '1':
                    if all(val == '0' for val in satd_values):
                        categories['PotentiallyBuggycommit']['category_1'].append(1)
                    elif '1' in satd_values and satd_values[-1] == '0':
                        categories['PotentiallyBuggycommit']['category_2'].append(1)
                    elif '1' in satd_values and satd_values[-1] == '1':
                        categories['PotentiallyBuggycommit']['category_3'].append(1)
                if risky_values[i] == '1':
                    if all(val == '0' for val in satd_values):
                        categories['RiskyCommit']['category_1'].append(1)
                    elif '1' in satd_values and satd_values[-1] == '0':
                        categories['RiskyCommit']['category_2'].append(1)
                    elif '1' in satd_values and satd_values[-1] == '1':
                        categories['RiskyCommit']['category_3'].append(1)
    
    return categories, buggy_rows

def main(input_folder):
    combined_categories = {
        'Buggycommiit': {'category_1': [], 'category_2': [], 'category_3': []},
        'PotentiallyBuggycommit': {'category_1': [], 'category_2': [], 'category_3': []},
        'RiskyCommit': {'category_1': [], 'category_2': [], 'category_3': []}
    }
    all_buggy_rows = []

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_folder, file_name)
            categories, buggy_rows = process_csv(file_path)
            
            for metric in combined_categories.keys():
                combined_categories[metric]['category_1'].extend(categories[metric]['category_1'])
                combined_categories[metric]['category_2'].extend(categories[metric]['category_2'])
                combined_categories[metric]['category_3'].extend(categories[metric]['category_3'])
            
            all_buggy_rows.extend(buggy_rows)

    # Print buggy rows
    print("Rows with buggy commits:")
    for row in all_buggy_rows:
        print(f"Row {row}")

    for metric in combined_categories.keys():
        # Create a DataFrame for plotting
        data_to_plot = []
        for category, values in combined_categories[metric].items():
            for value in values:
                data_to_plot.append({'Category': category, 'Count': value})
        
        df = pd.DataFrame(data_to_plot)

        # Plotting Bar Plot
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Category', y='Count', data=df, estimator=sum)
        plt.title(f'Total {metric} Across SATD Categories')
        plt.ylabel(f'Total {metric}')
        plt.xlabel('SATD Category')
        plt.grid(True)
        plt.savefig(f'figs/rq4/no-tangled/barplot_{metric}.pdf')
        plt.show()

if __name__ == "__main__":
    input_folder = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/csv-results/full'
    main(input_folder)
