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

# def get_method_category(satd: list) -> int:
#     """
#     Three different categories:
#     1. Never had SATD (always 0)
#     2. Had SATD but ended without SATD (1 somewhere, 0 at the end)
#     3. Had SATD and ended with SATD (1 somewhere, 1 at the end)
#     """ 
#     index = 0
#     for s in satd:
#         s = int(s)
#         last = satd[len(satd) - 1]
#         if (s == 1 and index != len(satd) - 1 and last == 0):
#             return 2
#         elif (s == 1 and index != len(satd) - 1 and last == 1):
#             return 3    
#         index += 1

#     return 1


def get_index_greater_than_730(change_at_method_age: list) -> int:
    """
    Get the index of the first element that is greater than 730

    IMPORTANT: shouldnt ever return -1 bc always enter loop and will increment index

    REturns teh index of the last element that is less than 730
    So can go up to and including this index
    """
    index = 0
    for age in change_at_method_age:
        if int(age) > 730:
            return index - 1
        index += 1
    # Return index - 1 because we want the index of the last element that is less than 730
    # also because if no elements are greater than 730, we want to return the last index
    return index - 1

def process():
    """"
    Have the three different categories in a dictionary
    Each key will be a category and the value will be a list the metric values
    Remember to make sure to discard any methods that are less than 2 years old
    And make sure to discard anything that happens after 2years old (use the ChangeAtMethodAge)
    """
    metrics = {}
    metrics['satd'] = []
    metrics['not_satd']= []

    # metrics['category_1'] = []
    # metrics['category_2'] = []
    # metrics['category_3'] = []
    

    
    for file in os.listdir(SRCDIR):
        if file.endswith('.csv'):
            fr = open(SRCDIR + file, "r")
            line = fr.readline() # skip header
            indices = build_indices(line)
            lines = fr.readlines()
            for line in lines:
                row = line.strip().split("\t")
                buggy_commit = row[indices['Buggycommiit']].split("#")
                tangled = row[indices['TangledWMoveandFileRename']].split("#")
                satd = row[indices['SATD']].split("#")                                                                                                              
                method_age = row[indices['Age']]
                change_at_method_age = row[indices['ChangeAtMethodAge']].split("#")
                index_to_stop = get_index_greater_than_730(change_at_method_age)
                # note the above index to stop only matters when/if we use the mean for calculation

                s_buggy_methods = 0
                s_not_buggy_methods = 0
                ns_buggy_methods = 0
                ns_not_buggy_methods = 0

                num_satd_methods = 0
                num_not_satd_methods = 0
                total_methods = 0

                
                is_satd = False
                if (check_satd(satd)):
                    is_satd = True

                buggy = False   
                if int(method_age) > 730:

                    if is_satd:
                        num_satd_methods += 1
                    else:
                        num_not_satd_methods += 1

                    for i in range(0, index_to_stop + 1):
                        if (buggy_commit[i] == '1' and tangled[i] == '1'):
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
                
            # total methods should equal s_buggy_methods + the other 3
            # and snotbugg and sbuggy should equal smethods
            print(total_methods)

        # calculate proportion
        # proportion_satd = s_buggy_methods / num_satd_methods
        # proportion_not_satd = s_not_buggy_methods / num_not_satd_methods
                
        # metrics['satd'].append(proportion_satd)
        # metrics['not_satd'].append(proportion_not_satd)

        # print(metrics)


            # data = line.strip().split("\t")
            # metric = data[indices["SLOCStandard"]]
            # metric = metric.split("#")
            # metric = float(metric[0])

            # satd = data[indices["SATD"]]
            # satd = satd.split("#")
            
            # if metric < 0:
            #    continue # something is wrong
            # if check_satd(satd):
            #    metrics['satd'].append(metric)
            # else:
            #     metrics['not_satd'].append(metric)
            # category = get_method_category(satd)
            # if category == 1:
            #     metrics['category_1'].append(metric)
            # elif category == 2:
            #     metrics['category_2'].append(metric)
            # else:
            #     metrics['category_3'].append(metric)

        # print(f'category_2: {metrics["category_2"]} ')   
    return metrics         

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

    # x, y = ecdf(metrics['category_1'])
    # ln = (plt.plot(x, y))
    # plt.setp(ln, ls="-", linewidth=3, color='r', label='SATD')

    # x, y = ecdf(metrics['category_2'])
    # ln = (plt.plot(x, y))
    # plt.setp(ln, ls="--", linewidth=3, color='blue', label='NOT_SATD')

    # x, y = ecdf(metrics['category_3'])
    # ln = (plt.plot(x, y))
    # plt.setp(ln, ls="--", linewidth=3, color='green', label='NOT_SATD')

    plt.legend()
    plt.xlabel("Buggy Method Proportion")
    plt.ylabel("CDF")
    # plt.xlim(0, 2000)
    # plt.savefig('figs/rq4/bugginess.pdf')
    plt.show()

if __name__ == "__main__":
    # metrics  = process()
    # draw_graph(metrics)

    # For now, just get the total number of satd buggy methods and non satd buggy methods
    # And teh total number of satd and non satd methods
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

            for line in lines:
                row = line.strip().split("\t")
                buggy_commit = row[indices['Buggycommiit']].split("#")
                tangled = row[indices['TangledWMoveandFileRename']].split("#")
                satd = row[indices['SATD']].split("#")                                                                                                              
                method_age = row[indices['Age']]
                change_at_method_age = row[indices['ChangeAtMethodAge']].split("#")
                index_to_stop = get_index_greater_than_730(change_at_method_age)

                is_satd = False
                if check_satd(satd):
                    is_satd = True    

                buggy = False   
                # if int(method_age) > 730:
                if is_satd:
                    num_satd_methods += 1
                else:
                    num_not_satd_methods += 1

                for i in range(0, index_to_stop + 1):
                    if (buggy_commit[i] == '1' and tangled[i] == '1'):
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



            print(file)
            print(s_buggy_methods + s_not_buggy_methods + ns_buggy_methods + ns_not_buggy_methods)
            print(num_satd_methods, num_not_satd_methods)
            print(total_methods)
            assert s_buggy_methods+s_not_buggy_methods+ ns_buggy_methods+ ns_not_buggy_methods == total_methods
            assert num_satd_methods+num_not_satd_methods == total_methods
            print(s_buggy_methods, s_not_buggy_methods, ns_buggy_methods, ns_not_buggy_methods)

            print('\n', '%.2f' % (s_buggy_methods / num_satd_methods), '%.2f' % (ns_buggy_methods / num_not_satd_methods))
    print([f'{x:.2f}' for x in satd_buggy_proportions])
    print([f'{x:.2f}' for x in not_satd_buggy_proportions])

    metrics = {'satd' : satd_buggy_proportions, 'not_satd': not_satd_buggy_proportions}
    draw_graph(metrics)
