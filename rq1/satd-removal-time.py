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

    # Dictionaries to store counts for each project
    project_stats = {}

    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            fr = open(SRCDIR + file, "r", encoding='utf-8')
            header = fr.readline() # skip header
            indices = build_indices(header)
            lines = fr.readlines()

            project_name = os.path.splitext(file)[0]
            if project_name not in project_stats:
                project_stats[project_name] = {'more_than_1000': 0, 'less_or_equal_1000': 0}
            
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
                
                # Determine if any of the removal times exceed 1000 days
                if any(time > 1000 for time in method_removal_times):
                    project_stats[project_name]['more_than_1000'] += 1
                else:
                    project_stats[project_name]['less_or_equal_1000'] += 1

                # Print details if any removal time exceeds 1000 days
                # if any(time > 1000 for time in method_removal_times):
                    # print(f"\nFile: {file}")
                    # print('SATD:', satd_list)
                    # print('Ages:', age_list)
                    # print(f"Method File Value: {row[indices['file']]}")
                    # print(f"SATD Removal Times: {method_removal_times}")

    # Calculate and print percentages for each project
    for project_name, stats in project_stats.items():
        total_methods = stats['more_than_1000'] + stats['less_or_equal_1000']
        if total_methods > 0:
            more_than_1000_percentage = (stats['more_than_1000'] / total_methods) * 100
            less_or_equal_1000_percentage = (stats['less_or_equal_1000'] / total_methods) * 100

            if more_than_1000_percentage > 1:
                print(f"\nProject: {project_name}")
                print(f"Percentage of methods with SATD > 1000 days: {more_than_1000_percentage:.2f}%")
                print(f"Percentage of methods with SATD <= 1000 days: {less_or_equal_1000_percentage:.2f}%")
        else:
            print(f"\nProject: {project_name}")
            print("No methods found.")

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
