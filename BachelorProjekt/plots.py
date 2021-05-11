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


def ABM_as_sir(data1,data2,data3,with_legend=False):
    plotted_df1,plotted_df2,plotted_df3 = pd.read_csv(data1), pd.read_csv(data2), pd.read_csv(data3)
    plotted_df1.columns,plotted_df2.columns,plotted_df3.columns = ['timestep', 'infected', 'susceptible', 'recovered'],['timestep', 'infected', 'susceptible', 'recovered'],['timestep', 'infected', 'susceptible', 'recovered']
    inf1, inf2, inf3 = list(plotted_df1['infected']),list(plotted_df2['infected']),list(plotted_df3['infected'])
    s1, s2, s3 = list(plotted_df1['susceptible']),list(plotted_df2['susceptible']),list(plotted_df3['susceptible'])
    r1, r2, r3 = list(plotted_df1['recovered']),list(plotted_df2['recovered']),list(plotted_df3['recovered'])

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    x_values = [x for x in range(21001)]

    for i in weekend_timesteps:
        plt.axvline(x=i, color='whitesmoke', linestyle='-')
    if with_legend == False:
        plt.plot(x_values,inf1,color=colors[0])
        plt.plot(x_values,inf2,color=colors[1])
        plt.plot(x_values,inf3,color=colors[2])
        plt.plot(x_values,s1,color=colors[0],linestyle='dashed')
        plt.plot(x_values,s2,color=colors[1],linestyle='dashed')
        plt.plot(x_values,s3,color=colors[2],linestyle='dashed')
        plt.plot(x_values,r1,color=colors[0],linestyle='dotted')
        plt.plot(x_values,r2,color=colors[1],linestyle='dotted')
        plt.plot(x_values,r3,color=colors[2],linestyle='dotted')
    if with_legend:
        legends = ['Hestesko', 'Rækker', 'Grupper']
        plt.plot(x_values,inf1,color=colors[0],label=legends[0])
        plt.plot(x_values,inf1,color=colors[1],label=legends[1])
        plt.plot(x_values,inf1,color=colors[2],label=legends[2])
        plt.plot(x_values,inf1,color=colors[0])
        plt.plot(x_values,inf2,color=colors[1])
        plt.plot(x_values,inf3,color=colors[2])
        plt.plot(x_values,s1,color=colors[0],linestyle='dashed')
        plt.plot(x_values,s2,color=colors[1],linestyle='dashed')
        plt.plot(x_values,s3,color=colors[2],linestyle='dashed')
        plt.plot(x_values,r1,color=colors[0],linestyle='dotted')
        plt.plot(x_values,r2,color=colors[1],linestyle='dotted')
        plt.plot(x_values,r3,color=colors[2],linestyle='dotted')
        plt.plot([], color='Black', label="Infektiøse")
        plt.plot([], color='Black', label='Modtagelige', linestyle='dashed')
        plt.plot([], color='Black', label='Raske', linestyle='dotted')
        plt.legend()
    plt.ylim(0,160)
    plt.xticks([0,5250,10500, 15750, 21000], [0, 10,20,30,40])
    plt.title("Gennemsnitsværdier af simulationer med mundbind 70%")
    plt.ylabel("Antal mennesker")
    plt.xlabel("Antal hverdage")
    plt.show()

data1_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind_70_2.csv"
data2_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind_70_3.csv"
data3_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind_70_4.csv"

ABM_as_sir(data1_3,data2_3,data3_3)
