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

    # Counters for SATD removal times > 1000 days
    single_removal_count_greater_1000 = 0
    two_removal_count_greater_1000 = 0
    three_removal_count_greater_1000 = 0
    four_removal_count_greater_1000 = 0
    five_removal_count_greater_1000 = 0
    more_than_five_removal_count_greater_1000 = 0

    # Counters for SATD removal times <= 1000 days
    single_removal_count_less_1000 = 0
    two_removal_count_less_1000 = 0
    three_removal_count_less_1000 = 0
    four_removal_count_less_1000 = 0
    five_removal_count_less_1000 = 0
    six_removal_count_less_1000 = 0
    seven_removal_count_less_1000 = 0
    more_than_seven_removal_count_less_1000 = 0
    
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
                
                # Determine the number of removals and categorize accordingly
                num_removals = len(method_removal_times)

                if any(time > 1000 for time in method_removal_times):
                    if num_removals == 1:
                        single_removal_count_greater_1000 += 1
                    elif num_removals == 2:
                        two_removal_count_greater_1000 += 1
                    elif num_removals == 3:
                        three_removal_count_greater_1000 += 1
                    elif num_removals == 4:
                        four_removal_count_greater_1000 += 1
                    elif num_removals == 5:
                        five_removal_count_greater_1000 += 1
                    elif num_removals > 5:
                        more_than_five_removal_count_greater_1000 += 1
                else:
                    if num_removals == 1:
                        single_removal_count_less_1000 += 1
                    elif num_removals == 2:
                        two_removal_count_less_1000 += 1
                    elif num_removals == 3:
                        three_removal_count_less_1000 += 1
                    elif num_removals == 4:
                        four_removal_count_less_1000 += 1
                    elif num_removals == 5:
                        five_removal_count_less_1000 += 1
                    elif num_removals == 6:
                        six_removal_count_less_1000 += 1
                    elif num_removals == 7:
                        seven_removal_count_less_1000 += 1
                    elif num_removals > 7:
                        more_than_seven_removal_count_less_1000 += 1

    # Calculate and print percentages for SATD removal > 1000 days
    total_methods_greater_1000 = (
        single_removal_count_greater_1000 + two_removal_count_greater_1000 + 
        three_removal_count_greater_1000 + four_removal_count_greater_1000 + 
        five_removal_count_greater_1000 + more_than_five_removal_count_greater_1000
    )

    if total_methods_greater_1000 > 0:
        print(f"\nSATD Removal Times > 1000 Days:")
        print(f"Single removal count: {single_removal_count_greater_1000}")
        print(f"Two removals count: {two_removal_count_greater_1000}")
        print(f"Three removals count: {three_removal_count_greater_1000}")
        print(f"Four removals count: {four_removal_count_greater_1000}")
        print(f"Five removals count: {five_removal_count_greater_1000}")
        print(f"More than five removals count: {more_than_five_removal_count_greater_1000}")

        single_removal_percentage_greater_1000 = (single_removal_count_greater_1000 / total_methods_greater_1000) * 100
        two_removal_percentage_greater_1000 = (two_removal_count_greater_1000 / total_methods_greater_1000) * 100
        three_removal_percentage_greater_1000 = (three_removal_count_greater_1000 / total_methods_greater_1000) * 100
        four_removal_percentage_greater_1000 = (four_removal_count_greater_1000 / total_methods_greater_1000) * 100
        five_removal_percentage_greater_1000 = (five_removal_count_greater_1000 / total_methods_greater_1000) * 100
        more_than_five_removal_percentage_greater_1000 = (more_than_five_removal_count_greater_1000 / total_methods_greater_1000) * 100

        print(f"\nPercentage of methods with SATD > 1000 days removed only once: {single_removal_percentage_greater_1000:.2f}%")
        print(f"Percentage of methods with SATD > 1000 days removed twice: {two_removal_percentage_greater_1000:.2f}%")
        print(f"Percentage of methods with SATD > 1000 days removed three times: {three_removal_percentage_greater_1000:.2f}%")
        print(f"Percentage of methods with SATD > 1000 days removed four times: {four_removal_percentage_greater_1000:.2f}%")
        print(f"Percentage of methods with SATD > 1000 days removed five times: {five_removal_percentage_greater_1000:.2f}%")
        print(f"Percentage of methods with SATD > 1000 days removed more than five times: {more_than_five_removal_percentage_greater_1000:.2f}%")
    else:
        print("\nNo methods with SATD removal times greater than 1000 days were found.")

    # Calculate and print percentages for SATD removal <= 1000 days
    total_methods_less_1000 = (
        single_removal_count_less_1000 + two_removal_count_less_1000 + 
        three_removal_count_less_1000 + four_removal_count_less_1000 + 
        five_removal_count_less_1000 + six_removal_count_less_1000 +
        seven_removal_count_less_1000 + more_than_seven_removal_count_less_1000
    )

    if total_methods_less_1000 > 0:
        print(f"\nSATD Removal Times <= 1000 Days:")
        print(f"Single removal count: {single_removal_count_less_1000}")
        print(f"Two removals count: {two_removal_count_less_1000}")
        print(f"Three removals count: {three_removal_count_less_1000}")
        print(f"Four removals count: {four_removal_count_less_1000}")
        print(f"Five removals count: {five_removal_count_less_1000}")
        print(f"Six removals count: {six_removal_count_less_1000}")
        print(f"Seven removals count: {seven_removal_count_less_1000}")
        print(f"More than seven removals count: {more_than_seven_removal_count_less_1000}")

        single_removal_percentage_less_1000 = (single_removal_count_less_1000 / total_methods_less_1000) * 100
        two_removal_percentage_less_1000 = (two_removal_count_less_1000 / total_methods_less_1000) * 100
        three_removal_percentage_less_1000 = (three_removal_count_less_1000 / total_methods_less_1000) * 100
        four_removal_percentage_less_1000 = (four_removal_count_less_1000 / total_methods_less_1000) * 100
        five_removal_percentage_less_1000 = (five_removal_count_less_1000 / total_methods_less_1000) * 100
        six_removal_count_less_1000 = (six_removal_count_less_1000 / total_methods_less_1000) * 100
        seven_removal_count_less_1000 = (seven_removal_count_less_1000 / total_methods_less_1000) * 100
        more_than_seven_removal_count_less_1000 = (more_than_seven_removal_count_less_1000 / total_methods_less_1000) * 100

        print(f"\nPercentage of methods with SATD <= 1000 days removed only once: {single_removal_percentage_less_1000:.2f}%")
        print(f"Percentage of methods with SATD <= 1000 days removed twice: {two_removal_percentage_less_1000:.2f}%")
        print(f"Percentage of methods with SATD <= 1000 days removed three times: {three_removal_percentage_less_1000:.2f}%")
        print(f"Percentage of methods with SATD <= 1000 days removed four times: {four_removal_percentage_less_1000:.2f}%")
        print(f"Percentage of methods with SATD <= 1000 days removed five times: {five_removal_percentage_less_1000:.2f}%")
        print(f"Percentage of methods with SATD <= 1000 days removed six times: {six_removal_count_less_1000:.2f}%")
        print(f"Percentage of methods with SATD <= 1000 days removed seven times: {seven_removal_count_less_1000:.2f}%")
        print(f"Percentage of methods with SATD <= 1000 days removed more than seven times: {more_than_seven_removal_count_less_1000:.2f}%")
    else:
        print("\nNo methods with SATD removal times less than or equal to 1000 days were found.")

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
