import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def get_removal_times(df):
    removal_times = []
    removal_indices = []

    for index, row in df.iterrows():
        # Only process methods older than 730 days
        if int(row['Age']) <= 730:
            continue
        
        satd_list = row['SATD'].split('#')
        age_list = row['ChangeAtMethodAge'].split('#')

        start_index = None

        for i, value in enumerate(satd_list):
            if int(age_list[i]) > 730:
                break

            if value == '1' and start_index is None:
                start_index = i
            elif value == '0' and start_index is not None:
                end_index = i
                start_age = int(age_list[start_index])
                end_age = int(age_list[end_index])
                removal_times.append(end_age - start_age)
                removal_indices.append(index)
                start_index = None  # Reset start index for next SATD segment

    return removal_times, removal_indices

def plot_cdf(removal_times):
    # Calculate the CDF of the removal times
    removal_times_sorted = np.sort(removal_times)
    cdf = np.arange(1, len(removal_times_sorted) + 1) / len(removal_times_sorted)

    # Plot the CDF
    plt.figure(figsize=(10, 6))
    plt.plot(removal_times_sorted, cdf, marker='o', linestyle='-', color='b')
    plt.title('Cumulative Distribution Function (CDF) of SATD Removal Times')
    plt.xlabel('Removal Time (days)')
    plt.ylabel('CDF')
    plt.grid(True)
    # plt.show()

    plt.savefig('satd_removal_cdf.pdf')
    print("CDF plot saved as 'satd_removal_cdf.pdf'.")

def process_files_in_folder(folder_path):
    all_removal_times = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            removal_times, _ = get_removal_times(df)
            all_removal_times.extend(removal_times)
    
    return all_removal_times

def main():
    folder_path = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/tech-debt-research/csv-results/part'
    all_removal_times = process_files_in_folder(folder_path)

    print("Total removal times from all files:", all_removal_times)

    plot_cdf(all_removal_times)

if __name__ == '__main__':
    main()
