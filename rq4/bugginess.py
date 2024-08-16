import os
import numpy as np
import matplotlib.pyplot as plt

# SRCDIR = "../../software-evolution/tech-debt-results/"
SRCDIR = '/home/hisham-kidwai/Documents/HISHAM/Research/Tech-Debt/csv-files-satd/'

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

def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]

def draw_graph(metrics):
    x, y = ecdf(metrics['satd'])
    ln = (plt.plot(x, y))
    plt.setp(ln, ls="-", linewidth=3, color='r', label='SATD')

    x, y = ecdf(metrics['not_satd'])
    ln = (plt.plot(x, y))
    plt.setp(ln, ls="--", linewidth=3, color='blue', label='NOT_SATD')

    plt.legend()
    plt.xlabel("Buggy Method Proportion")
    plt.ylabel("CDF")
    # plt.xlim(0, 2000)
    plt.savefig('figs/rq4/tWHAT_bugginess.pdf')
    # plt.show()

def draw_graph_multiple(metrics):
    for metric_name, data in metrics.items():
        plt.figure()
        
        x, y = ecdf(data['satd'])
        ln = plt.plot(x, y)
        plt.setp(ln, ls="-", linewidth=3, color='r', label='SATD')
        
        x, y = ecdf(data['not_satd'])
        ln = plt.plot(x, y)
        plt.setp(ln, ls="--", linewidth=3, color='blue', label='NOT_SATD')
        
        plt.legend()
        plt.xlabel(f'Proportion of {metric_name}')
        plt.ylabel("CDF")
        
        SCALE = 'linear'

        plt.title(f"CDF of {metric_name}")
        # plt.show()

        plt.xscale(SCALE)
        plt.savefig(f'figs/rq4/{SCALE}/{metric_name}.pdf')

def find_index_to_stop(age_list: list):
    for i, age in enumerate(age_list):
        if int(age) > 730:
            return i
    return -1

# def process(metrics_list):
#     """
#     Find the proportion of each of the metric in metrics_list that are 1, with no care of anyhting else like tangled
#     so we will most likely be passing in Buggycommiit and RiskyCommit
#     So we will be checking the proportion of methods that have a 1 in Buggycommiit and are satd and not satd 
#     Same for RiskyCommit
#     """
#     metrics = {metric: {'satd': [], 'not_satd': []} for metric in metrics_list}
    
#     for file in os.listdir(SRCDIR):
#         if file.endswith('.csv'):
#             fr = open(SRCDIR + file, "r")
#             line = fr.readline() # skip header
#             indices = build_indices(line)
#             lines = fr.readlines()

#             s_buggy_methods = 0
#             s_not_buggy_methods = 0
#             ns_buggy_methods = 0
#             ns_not_buggy_methods = 0

#             num_satd_methods = 0
#             num_not_satd_methods = 0
#             total_methods = 0

#             for line in lines:
#                 row = line.strip().split("\t")
                
#                 if int(row[indices['Age']]) > 730:
#                     for metric_name in metrics_list:
#                         metric = row[indices[metric_name]].split("#")
#                         age_list = row[indices['ChangeAtMethodAge']].split('#')
#                         satd = row[indices["SATD"]].split("#")

#                         index_to_stop = find_index_to_stop(age_list)
#                         if index_to_stop != -1:
#                             metric = metric[:index_to_stop]
#                             satd = satd[:index_to_stop]

#                         is_satd = False
#                         if check_satd(satd):
#                             is_satd = True
                        
#                         if (is_satd):
#                             num_satd_methods += 1
#                         else:
#                             num_not_satd_methods += 1

#                         if (index_to_stop == -1):
#                             index_to_stop = len(metric)
                        
#                         buggy = False
#                         for i in range(0, index_to_stop):
#                             if (metric[i] == '1'):
#                                 buggy = True
#                                 if (is_satd):
#                                     s_buggy_methods += 1
#                                 else:
#                                     ns_buggy_methods += 1
#                                 break
                        
#                         if not buggy:
#                             if is_satd:
#                                 s_not_buggy_methods += 1
#                             else:
#                                 ns_not_buggy_methods += 1

def process(metrics_list):
    results = {}
    for metric in metrics_list:
        satd_buggy_proportions = []
        not_satd_buggy_proportions = []
        for file in os.listdir(SRCDIR):
            if file.endswith('.csv'):
                with open(SRCDIR + file, "r") as fr:
                    line = fr.readline()  # skip header
                    indices = build_indices(line)
                    lines = fr.readlines()

                    s_buggy_methods = 0
                    s_not_buggy_methods = 0
                    ns_buggy_methods = 0
                    ns_not_buggy_methods = 0

                    num_satd_methods = 0
                    num_not_satd_methods = 0

                    for line in lines:
                        row = line.strip().split("\t")
                        metric_values = row[indices[metric]].split("#")
                        satd = row[indices['SATD']].split("#")                                                                                                              
                        method_age = row[indices['Age']]
                        change_at_method_age = row[indices['ChangeAtMethodAge']].split("#")
                        index_to_stop = find_index_to_stop(change_at_method_age)

                        if index_to_stop != -1:
                            metric_values = metric_values[:index_to_stop]
                            satd = satd[:index_to_stop]

                        is_satd = check_satd(satd)

                        buggy = False   
                        if int(row[indices['Age']]) > 730:
                            if is_satd:
                                num_satd_methods += 1
                            else:
                                num_not_satd_methods += 1

                            if index_to_stop == -1:
                                index_to_stop = len(metric_values)

                            for i in range(0, index_to_stop):
                                if metric_values[i] == '1':
                                    buggy = True
                                    if is_satd:
                                        s_buggy_methods += 1
                                    else:
                                        ns_buggy_methods += 1
                                    break

                            if not buggy:
                                if is_satd:
                                    s_not_buggy_methods += 1
                                else:
                                    ns_not_buggy_methods += 1

                    if num_satd_methods > 0:
                        satd_buggy_proportion = s_buggy_methods / num_satd_methods
                    else:
                        satd_buggy_proportion = 0
                    
                    if num_not_satd_methods > 0:
                        not_satd_buggy_proportion = ns_buggy_methods / num_not_satd_methods
                    else:
                        not_satd_buggy_proportion = 0

                    satd_buggy_proportions.append(satd_buggy_proportion)
                    not_satd_buggy_proportions.append(not_satd_buggy_proportion)

        results[metric] = {
            'satd': satd_buggy_proportions,
            'not_satd': not_satd_buggy_proportions
        }
    return results


if __name__ == "__main__":
    metrics_list = ['Buggycommiit', 'RiskyCommit']
    metrics = process(metrics_list)
    draw_graph_multiple(metrics)


    satd_buggy_proportions = []
    not_satd_buggy_proportions = []
    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            fr = open(SRCDIR + file, "r")
            line = fr.readline() # skip header
            indices = build_indices(line)
            lines = fr.readlines()

            s_buggy_methods = 0
            s_not_buggy_methods = 0
            ns_buggy_methods = 0
            ns_not_buggy_methods = 0

            num_satd_methods = 0
            num_not_satd_methods = 0
            total_methods = 0

            # counter = 0

            for line in lines:
                # counter += 1
                # if counter > 100:
                #     break
                
                row = line.strip().split("\t")
                buggy_commit = row[indices['Buggycommiit']].split("#")
                tangled = row[indices['TangledWMoveandFileRename']].split("#")
                satd = row[indices['SATD']].split("#")                                                                                                              
                method_age = row[indices['Age']]
                change_at_method_age = row[indices['ChangeAtMethodAge']].split("#")
                index_to_stop = find_index_to_stop(change_at_method_age)


                # just trim all the rows (the var as above)
                # to the index_to_stop
                # print(file, row[indices['file']])
                # print(buggy_commit)
                if index_to_stop != -1:
                    buggy_commit = buggy_commit[:index_to_stop]
                    tangled = tangled[:index_to_stop]
                    satd = satd[:index_to_stop]
                # print(buggy_commit)    

                is_satd = False
                if check_satd(satd):
                    is_satd = True    

#                1153.json ['0', '1', '0']
# ['0', '1', '20']

                buggy = False   
                if int(row[indices['Age']]) > 730:
                    # print(file)
                    # print(row[indices['file']])
                    # print(buggy_commit)
                    # print(tangled)
                    # print(index_to_stop)
                    # if (row[indices['file'] == '1153.json']):
                        # print(index_to_stop, 'asdsdds\n\n\n\n')
                    if is_satd:
                        num_satd_methods += 1
                    else:
                        num_not_satd_methods += 1
                    # Important we DO NOT include the index_to_stop in the loop 
                    # as index_to_stop is the index of the first element that is greater than 730

                    # IMPORTANT: AS IF INDEX_TO_STOP IS -1 WE STILL WANT TO ENTER THE LOOP
                    # -1 MEANS GO TILL END
                    if (index_to_stop == -1):
                        index_to_stop = len(buggy_commit)
                    for i in range(0, index_to_stop):
                        if (len(buggy_commit) != len(tangled)):
                            print(file, row[indices['file']])
                            print('SMTHN WRONG, LOOK AT ME')
                        # elif (buggy_commit[i] == '1' and (tangled[i] == '1' or tangled[i] == '2' or tangled[i] == '3' or tangled[i] == '4' or tangled[i] == '5')):
                        elif (buggy_commit[i] == '1' and (tangled[i] == '1')):
                            buggy = True
                            if (is_satd):
                                s_buggy_methods += 1
                            else:
                                ns_buggy_methods += 1
                            break

                    if not buggy:
                        if is_satd:
                            s_not_buggy_methods += 1
                        else:
                            ns_not_buggy_methods += 1
                    total_methods += 1

            satd_buggy_proportion = s_buggy_methods / num_satd_methods
            not_satd_buggy_proportion = ns_buggy_methods / num_not_satd_methods

            satd_buggy_proportions.append(satd_buggy_proportion)
            not_satd_buggy_proportions.append(not_satd_buggy_proportion)

    metrics = {'satd' : satd_buggy_proportions, 'not_satd': not_satd_buggy_proportions}
    draw_graph(metrics)
