import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import random

weekend_timesteps = [525*i for i in range(5,40,5)]

data2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_2.csv"
data3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_3.csv"
data4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_4.csv"

basis_all2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/Basis_2.csv"
basis_all3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/Basis_3.csv"
basis_all4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/Basis_4.csv"

basis_all2_plotted = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/plotted_data_Basis100_2.csv"
basis_all3_plotted = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/plotted_data_Basis100_3.csv"
basis_all4_plotted = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/plotted_data_Basis100_4.csv"
mundbind_70_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind70_2.csv"
mundbind_70_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind70_3.csv"
mundbind_70_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind70_4.csv"
def get_hist_data(data):
    "TO USE WITH RAW DATA"
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'Agent_count', 'recovered', 'Home','d','f', 'Iteration']
    minute_list = []
    for i in range(1,len(df.infected)):
        if df.infected[i-1]<df.infected[i]:
            minute_list.append(df.timestep[i]%525)
    return minute_list
def plot_histogram(bordopstilling,hist):
    plt.figure()
    if bordopstilling == 'H':
        plt.title("Infektionsfrekvens for H på daglig basis med mundbind")
        hist_list = hist
    elif bordopstilling == 'R':
        plt.title('Infektionsfrekvens for R på daglig basis med mundbind')
        hist_list = hist
    elif bordopstilling == 'G':
        plt.title('Infektionsfrekvens for G på daglig basis med mundbind')
        hist_list = hist
    print(len(hist))
    andel_undervisning, andel_fællesareal = [], []
    for h in hist:
        if h < 35 or 105 < h < 150 or 225 < h < 340 or 405 < h < 450:
            andel_fællesareal.append(h)
        else:
            andel_undervisning.append(h)
    print(len(andel_undervisning),100*sum(andel_undervisning)/(sum(andel_undervisning)+sum(andel_fællesareal)),len(andel_fællesareal),100*sum(andel_fællesareal)/(sum(andel_undervisning)+sum(andel_fællesareal)))
    plt.axvspan(0, 35, alpha=0.5, color='green')
    plt.axvspan(105, 150, alpha=0.5, color='green', label='Ophold i fællesarealet')
    plt.axvspan(225, 340, alpha=0.5, color='green')
    plt.axvspan(405, 450, alpha=0.5, color='green')
    plt.hist(hist_list, bins=np.arange(0,525,5), ec='b', density=True)
    plt.xlabel('Minutter efter start på dag')
    plt.ylim(0,0.015)
    plt.legend()
    plt.ylabel('Frekvens af smittende interaktioner')
    plt.show()

def infected_bounds(data):
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'Agent_count', 'recovered', 'Home','f','d', 'Iteration']
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
    plt.title("G med mundbind")
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
    plt.title("G med mundbind")
    plt.ylabel('Antal inficerede')
    plt.xlabel('Antal hverdage')
    plt.show()
    return

def ABM_as_sir(data1,data2,data3,with_legend=False):
    plotted_df1,plotted_df2,plotted_df3 = pd.read_csv(data1), pd.read_csv(data2), pd.read_csv(data3)
    plotted_df1.columns,plotted_df2.columns,plotted_df3.columns = ['timestep', 'infected', 'susceptible', 'recovered'], ['timestep', 'infected', 'susceptible', 'recovered'], ['timestep', 'infected', 'susceptible', 'recovered']
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
    plt.title("Gående og stående bærer mundbind")
    plt.ylabel("Antal mennesker")
    plt.xlabel("Antal hverdage")
    plt.show()

def calc_mean_imax_std_peak_day(data):
    """ Returns which day infection peaks. Use this with the raw data"""
    df = pd.read_csv(data)
    df.columns =['timestep','infected','Agent_count','recovered','at_home','d','f','n_sim']
    imax, imaxindex, imaxsim = [],[],[]
    peakday = []
    stdimax_ = []
    tu = []
    s_end = []
    for i in range(1,51):
        correct_sim = df.loc[df['n_sim'] == i]
        index_max = correct_sim[correct_sim['infected'] == max(correct_sim.infected)].index.values[0]
        imax.append(correct_sim.loc[index_max]['infected'])
        stdimax_.append(np.std(correct_sim['infected']))
        peakday.append(correct_sim.loc[index_max]['timestep']/525)
        imaxindex.append(index_max)
        imaxsim.append(i)
        tu.append((correct_sim.loc[index_max]['infected'],i))
        s_end.append(min(correct_sim['Agent_count']-correct_sim['recovered']-correct_sim['infected']))
    sorted_ = sorted(tu,key=lambda x:x[0])
    print("min,max",np.min(imax),np.max(imax))
    print("gns , sd",np.mean(s_end),np.std(s_end))
    print("MEAN IMAX",np.mean(imax),"STD IMAX",np.std(imax),"MEAN peakday",np.mean(peakday),"std peakday",np.std(peakday))
    print(sorted_)

data2_1inf_p = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_Basis_1weekend_2.csv"
data3_1inf_p = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_Basis_1weekend_3.csv"
data4_1inf_p = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_Basis_1weekend_4.csv"
data2_1inf = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/Basis_1weekend_2.csv"
data3_1inf = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/Basis_1weekend_3.csv"
data4_1inf = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/Basis_1weekend_4.csv"
data2_halvinf = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/basis_1infected_hverandenweekend_2.csv"
data3_halvinf = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/basis_1infected_hverandenweekend_3.csv"
data4_halvinf = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/basis_1infected_hverandenweekend_4.csv"


data2_025 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/Basis_025infection_2.csv"
data3_025 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/Basis_025infection_3.csv"
data4_025 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/Basis_025infection_4.csv"
data2_04 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/Basis_04infection_2.csv"
data3_04 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/Basis_04infection_3.csv"
data4_04 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/Basis_04infection_4.csv"



mundbind70_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind70_2.csv"
mundbind70_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind70_3.csv"
mundbind70_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind70_4.csv"
mundbind60_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind60_2.csv"
mundbind60_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind60_3.csv"
mundbind60_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind60_4.csv"
mundbind50_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind50_2.csv"
mundbind50_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind50_3.csv"
mundbind50_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind50_4.csv"
plot_histogram("H",get_hist_data(mundbind70_4))
#calc_mean_imax_std_peak_day(mundbind60_2)
#calc_mean_imax_std_peak_day(mundbind50_3)

def kontakttal_plot(data):
    "TO USE WITH RAW DATA"
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'Agent_count', 'recovered', 'Home', 'Iteration']
    plt.figure()
    Re_lists = []
    for j in range(1,51):
        indx_df = df[df['Iteration'] == j].index.to_numpy()  #list of indexes for the j'th iteration
        mean_list_j = [1]
        for i in range(min(indx_df),max(indx_df)-524,525):
            mean_list_j.append(np.mean([df.infected[x] for x in range(i,i+525)]))
        growth = [] #initalisere med 1 som kontakttal
        for i in range(len(mean_list_j)-1):
            if mean_list_j[i] != 0:
                growth.append((mean_list_j[i+1]-mean_list_j[i])/mean_list_j[i])
            else:
                growth.append(0)
        Re_lists.append([(i*2.7)+1 for i in growth])
    Std_list = np.std(Re_lists, axis=0)
    Re_lists = np.mean(Re_lists, axis=0)
    x_values = [x for x in range(1,len(Re_lists)+1)]
    print(next(x[0] for x in enumerate(Re_lists) if x[1] < 1)) #prints first index for which R_e < 1
    "Når index=20 betyder det at mellem dag 19 og 20 er kontakttallet under 1 for første gang"
    for i in range(0,41,5):
        plt.axvline(x=i, color='whitesmoke', linestyle='-')
    plt.axhline(y=1, color='indianred', linestyle='--')
    plt.plot(x_values, Re_lists, color='k', linewidth='2')
    plt.plot(x_values, Re_lists+Std_list, color='grey', linewidth='1')
    plt.plot(x_values, Re_lists-Std_list, color='grey', linewidth='1')
    plt.fill_between(x_values,Re_lists-Std_list , Re_lists+Std_list, color='lightgrey', alpha=.1)
    plt.ylabel('Kontakttal')
    plt.xlabel('Hverdage')
    plt.title("Kontakttal for R")
    plt.show()
    return x_values, Re_lists, Std_list

#ABM_as_sir(basis_all2_plotted,basis_all3_plotted,basis_all4_plotted,True)
#ABM_as_sir(data1_3,data2_3,data3_3,True)
#infected_bounds(mundbind70_2)

#calc_mean_imax_std_peak_day(basis_all2)
#calc_mean_imax_std_peak_day(basis_all3)
#calc_mean_imax_std_peak_day(basis_all4)
def data_for_reproduction_raw(data):
    "TO USE WITH RAW DATA"
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'Agent_count', 'recovered', 'Home', 'Iteration']
    Re_lists = []
    for j in range(1,51):
        indx_df = df[df['Iteration'] == j].index.to_numpy()  #list of indexes for the j'th iteration
        mean_list_j = [1]
        for i in range(min(indx_df),max(indx_df)-524,525):
            mean_list_j.append(np.mean([df.infected[x] for x in range(i,i+525)]))
        growth = [] #initalisere med 1 som kontakttal
        for i in range(len(mean_list_j)-1):
            if mean_list_j[i] != 0:
                growth.append((mean_list_j[i+1]-mean_list_j[i])/mean_list_j[i])
            else:
                growth.append(0)
        Re_lists.append([(i*2.7)+1 for i in growth])
    Std_list = np.std(Re_lists, axis=0)
    Re_lists = np.mean(Re_lists, axis=0)
    x_values = [x for x in range(1,len(Re_lists)+1)]
    return x_values, Re_lists, Std_list

def plot_true_reproduction(data1,data2, data3=False):
    "Raw data"
    data1 = data_for_reproduction_raw(data1)
    data2 = data_for_reproduction_raw(data2)
    if data3:
        data3 = data_for_reproduction_raw(data3)
        Re_list3, Std_list3= data3[1],data3[2]
    x_values = data1[0]
    Re_list1,Std_list1 = data1[1],data1[2]
    Re_list2,Std_list2 = data2[1],data2[2]
    plt.figure()
    for i in range(0,41,5):
        plt.axvline(x=i, color='whitesmoke', linestyle='-')
    plt.axhline(y=1, color='red', linestyle='dashed')
    plt.plot(x_values, Re_list1, color='dimgrey', linewidth='1', linestyle='dashed', label='Uden vacciner')
    #plt.plot(x_values, Re_list1+Std_list1, color='darkgrey', linewidth='1')
    #plt.plot(x_values, Re_list1-Std_list1, color='darkgrey', linewidth='1')
    #plt.fill_between(x_values,Re_list1-Std_list1 , Re_list1+Std_list1, color='grey', alpha=.1)
    plt.plot(x_values, Re_list2, color='black', linewidth='2.5', label='Med vacciner')
    #plt.plot(x_values, Re_list2+Std_list2, color='green', linewidth='1')
    #plt.plot(x_values, Re_list2-Std_list2, color='green', linewidth='1')
    #plt.fill_between(x_values,Re_list2-Std_list2 , Re_list2+Std_list2, color='lightgreen', alpha=.1)
    if data3:
        plt.plot(x_values, Re_list3, color='darkblue', linewidth='2')
    #plt.plot(x_values, Re_list3+Std_list3, color='blue', linewidth='1')
    #plt.plot(x_values, Re_list3-Std_list3, color='blue', linewidth='1')
    #plt.fill_between(x_values,Re_list3-Std_list3 , Re_list3+Std_list3, color='lightblue', alpha=.1)
    plt.ylabel('Kontakttal')
    plt.xlabel('Hverdage')
    plt.legend()
    plt.title('Udvikling i kontakttal for G ved 70% vaccinerede')
    plt.show()

def true_reproduction_numbers(data):
    "TO USE WITH RAW DATA"
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'Agent_count', 'recovered', 'Home','Iteration']
    plt.figure()
    Re_lists = []
    for j in range(1,51):
        indx_df = df[df['Iteration'] == j].index.to_numpy()  #list of indexes for the j'th iteration
        mean_list_j = [1]
        for i in range(min(indx_df),max(indx_df)-524,525):
            mean_list_j.append(np.mean([df.infected[x] for x in range(i,i+525)]))
        growth = [] #initalisere med 1 som kontakttal
        for i in range(len(mean_list_j)-1):
            if mean_list_j[i] != 0:
                growth.append((mean_list_j[i+1]-mean_list_j[i])/mean_list_j[i])
            else:
                growth.append(0)
        Re_lists.append([(i*2.7)+1 for i in growth])
    Std_list = np.std(Re_lists, axis=0)
    Re_lists = np.mean(Re_lists, axis=0)
    Re_lists = [max(x,0) for x in Re_lists]
    x_values = [x for x in range(1,len(Re_lists)+1)]
    Re_minus_sd= Re_lists-Std_list
    Re_minus_sd=[max(x,0) for x in Re_minus_sd]
    print(next(x[0] for x in enumerate(Re_lists) if x[1] < 1)) #prints first index for which R_e < 1
    "Når index=20 betyder det at mellem dag 19 og 20 er kontakttallet under 1 for første gang"
    for i in range(0,41,5):
        plt.axvline(x=i, color='whitesmoke', linestyle='-')
    plt.axhline(y=1, color='indianred', linestyle='--')
    plt.plot(x_values, Re_lists, color='k', linewidth='2', label='Gennemsnit')
    plt.plot(x_values, Re_lists+Std_list, color='grey', linewidth='1', label='Gennemsnit plus/minus 1 SD')
    plt.plot(x_values, Re_minus_sd, color='grey', linewidth='1')
    plt.fill_between(x_values,Re_minus_sd , Re_lists+Std_list, color='lightgrey', alpha=.1)
    plt.ylabel('Kontakttal')
    plt.xlabel('Hverdage')
    plt.ylim(0,7)
    plt.legend()
    plt.title('Udvikling i kontakttal i basismodellen')
    plt.show()
    return x_values, Re_lists, Std_list

def find_day_of_peak(data):
    """ Returns which day infection peaks. Use this with the plotted_data"""
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'susceptible', 'recovered']
    indx = df[df['infected'] == max(df.infected)].index.values[0]
    return max(df.infected), indx/525
#plot_true_reproduction(basis_all2,basis_all3,basis_all4)
true_reproduction_numbers(basis_all4)
print(find_day_of_peak(data4))
#ABM_as_sir(data2,data3,data4)
def parse_data_mean_sd(data):
    "TO USE WITH RAW DATA"
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'Agent_count', 'recovered', 'Home', 'Iteration']
    print(np.mean(df.infected))
    print(np.std(df.infected))
