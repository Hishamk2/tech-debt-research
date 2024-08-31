import os
import numpy as np
import matplotlib.pyplot as plt

# SRCDIR = "../../software-evolution/tech-debt-results/"
# SRCDIR = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/csv-files-satd/'
SRCDIR = r'D:\\OneDrive - University of Manitoba\\Documents\\HISHAM\\Research\\Tech-Debt\\csv-files-satd\\'

def build_indices(line):
    indices = {}
    data = line.strip().split("\t")
    for i in range(len(data)):
        indices[data[i]] = i
    return indices    
            
def process():
    removal_times = []

    # Counters for methods with SATD removed only once or more than once
    single_removal_count = 0
    multiple_removal_count = 0

    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            fr = open(SRCDIR + file, "r", encoding='utf-8')
            header = fr.readline() # skip header
            indices = build_indices(header)
            lines = fr.readlines()
            
            for line in lines:
                row = line.strip().split("\t")             

                satd_list = row[indices['SATD']].split('#')
                age_list = row[indices['ChangeAtMethodAge']].split('#')

                start_index = None
                method_removal_times = []

                for i, value in enumerate(satd_list):
                    if value == '1' and start_index is None:
                        start_index = i
                    elif value == '0' and start_index is not None:
                        end_index = i

                        start_age = int(age_list[start_index])
                        end_age = int(age_list[end_index])
                        removal_time = end_age - start_age
                        
                        method_removal_times.append(removal_time)
                        removal_times.append(removal_time)

                        start_index = None  # Reset start index for next SATD segment   
                
                # Check if any removal time exceeds 1000 days and print details
                if any(time > 1000 for time in method_removal_times):
                    print(f"\nFile: {file}")
                    print('SATD:', satd_list)
                    print('Ages:', age_list)
                    print(f"Method File Value: {row[indices['file']]}")
                    print(f"SATD Removal Times: {method_removal_times}")

                    # Check if SATD was removed only once or more than once
                    if len(method_removal_times) == 1:
                        single_removal_count += 1
                    else:
                        multiple_removal_count += 1

    # Calculate percentages
    total_methods = single_removal_count + multiple_removal_count
    if total_methods > 0:
        single_removal_percentage = (single_removal_count / total_methods) * 100
        multiple_removal_percentage = (multiple_removal_count / total_methods) * 100

        print(f"\nPercentage of methods with SATD > 1000 days removed only once: {single_removal_percentage:.2f}%")
        print(f"Percentage of methods with SATD > 1000 days removed more than once: {multiple_removal_percentage:.2f}%")
    else:
        print("\nNo methods with SATD removal times greater than 1000 days were found.")

    return removal_times         

def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]

def draw_graph(metrics):
    x, y = ecdf(metrics)
    ln = plt.plot(x,y)
    plt.setp(ln, ls="-", linewidth=3, color='r', label='Removal Times')
    plt.legend()
    plt.xlabel("SATD Removal Time (days)")
    plt.ylabel("CDF")

    scale = 'log'
    if scale == 'log':
        plt.xscale('log')
        plt.savefig(f'figs/rq1/log/all_removal_times.pdf')
    else:
        plt.savefig(f'figs/rq1/all_removal_times.pdf')

if __name__ == "__main__":
    metrics = process()
    # draw_graph(metrics)
