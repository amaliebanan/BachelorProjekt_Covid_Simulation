import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import random

weekend_timesteps = [525*i for i in range(5,40,5)]

def infected_bounds(data):
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'Agent_count', 'recovered', 'Home', 'Iteration']
    min_per_step = []
    max_per_step = []
    mean_per_step = []
    std_minus1 = []
    std_plus1 = []
    for j in range(21001): #for hvert tidsskridt
        j_list = [] #list for specific timestep
        get_row_numbers = df[df['timestep'] == j].index.to_numpy() #alle indexer der svarer til tidsskridt j
        for i in get_row_numbers:
            j_list.append(df.infected[i]) #all infected counts for specific timesteps
        j_list.sort() #sort the list
        min_per_step.append(j_list[0])
        max_per_step.append(j_list[49])
        mean_per_step.append(np.mean(j_list))
        std_minus1.append(max(np.mean(j_list)-np.std(j_list),0))
        std_plus1.append(np.mean(j_list)+np.std(j_list))
    x_values = [x for x in range(21001)]
    plt.figure() #FIGURE1
    for i in weekend_timesteps:
        plt.axvline(x=i, color='whitesmoke', linestyle='-')
    plt.plot(x_values, std_minus1, color='firebrick', linewidth='1', label='plus/minus 1 standardafvigelse')
    plt.plot(x_values, std_plus1, color='firebrick', linewidth='1')
    plt.plot(x_values, mean_per_step, color='maroon', linewidth='3', label='middelværdi')
    plt.fill_between(x_values, min_per_step, max_per_step, color='lightcoral', alpha=.1, label='maximum- og minimumsværdier')
    plt.fill_between(x_values, std_minus1, std_plus1, color='indianred', alpha=.1)
    plt.xticks([0,5250,10500, 15750, 21000], [0, 10,20,30,40])
    plt.ylim(0,160)
    plt.legend()
    plt.ylabel('Antal inficerede')
    plt.xlabel('Antal hverdage')

    numbers = [x for x in range(1,51)]
    sample = random.sample(numbers, 10)

    plt.figure()
    for i in weekend_timesteps:
        plt.axvline(x=i, color='whitesmoke', linestyle='-')
    plt.plot(x_values, mean_per_step, color='maroon', linewidth='3', label='middelværdi')
    for i in range(5):
        plt.plot(x_values, df[df['Iteration']==sample[i]]['infected'], linewidth='0.8')
    plt.fill_between(x_values, min_per_step, max_per_step, color='lightcoral', alpha=.1, label='maximum- og minimumsværdier')
    plt.xticks([0,5250,10500, 15750, 21000], [0, 10,20,30,40])
    plt.legend()
    plt.ylim(0,160)
    plt.ylabel('Antal inficerede')
    plt.xlabel('Antal hverdage')

    plt.show()
    return
