import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

weekend_timesteps = [525*i for i in range(5,40,5)]
mundbind_70_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind70_2.csv"
mundbind_70_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind70_3.csv"
mundbind_70_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind70_4.csv"


def parse_data_mean_sd_plotted(data):
    "TO USE WITH PLOTTED DATA"
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'susceptible', 'f','d','recovered']
    print(np.max(df.infected))
    print(np.mean(df.infected))
    print(np.std(df.infected))

#parse_data_mean_sd_plotted(mundbind_70_2)
#parse_data_mean_sd_plotted(mundbind_70_3)
#parse_data_mean_sd_plotted(mundbind_70_4)
def find_max(data):
    """ Returns which day infection peaks. Use this with the plotted_data"""
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'susceptible', 'f','d','recovered']
    indx = df[df['infected'] == max(df.infected)].index.values[0]
    return max(df.infected), indx/525

def timestep_to_day(timestep):
    return timestep/525+(np.floor((timestep/525)/5)*2)
def parse_datafile_infected(data, plotted_data):
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'Agent_count', 'recovered', 'Home', 'Iteration']
    plotted_df = pd.read_csv(plotted_data)
    plotted_df.columns = ['timestep', 'infected', 'susceptible', 'recovered']
    min_list = []
    max_list = []
    for j in range(21001):
        j_list = [] #list for specific timestep
        get_row_numbers = df[df['timestep'] == j].index.to_numpy()
        for i in get_row_numbers:
            j_list.append(df.infected[i]) #all infected counts for specific timesteps
        j_list.sort() #sort the list
        min_list.append(j_list[1])#removes the bottom 2.5%
        max_list.append(j_list[48])#removes the bottom 2.5%
    return min_list, max_list, plotted_df['infected'].tolist()

def parse_datafile_infected_new(data, plotted_data):
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'Agent_count', 'recovered', 'Home', 'Iteration']
    plotted_df = pd.read_csv(plotted_data)
    plotted_df.columns = ['timestep', 'infected', 'susceptible', 'recovered']
    allmax = []
    for i in range(1,51):
        subdataframes = df.loc[df['Iteration'] == i]
        allmax.append((max(subdataframes.infected), i))
    best_It_list = list((df.loc[df['Iteration'] == min(allmax)[1]]).infected)
    worst_It_list = list((df.loc[df['Iteration'] == max(allmax)[1]]).infected)
    return best_It_list, worst_It_list, list(plotted_df.infected)

data2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_2.csv"
data3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_3.csv"
data4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_4.csv"

basis_all2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/Basis_2.csv"
basis_all3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/Basis_3.csv"
basis_all4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/Basis_4.csv"

def calc_imax_and_peak_day(data):
    """ Returns which day infection peaks. Use this with the plotted_data"""
    df = pd.read_csv(data)
    df.columns =['timestep','infected','susceptible','d','l','recovered']
    Imax, peakday,susceptible21000 = [],[], []

    index_max = df[df['infected'] == max(df.infected)].index.values[0]
    Imax.append(df.loc[index_max]['infected'])
    peakday.append((df.loc[index_max]['timestep']))
   # print(Imax,peakday)
    print("I_max:",Imax,"Peak day:", peakday,"S21000",df['susceptible'][21000],df['infected'][21000],df['recovered'][21000])
    print("ses")

def calc_mean_imax_std_peak_day(data):
    """ Returns which day infection peaks. Use this with raw data """
    df = pd.read_csv(data)
    df.columns =['timestep','infected','Agent_count','recovered','at_home','n_sim']
    Imax, peakday,std = [],[], []
    sustilsidst = []
    d_peak = []
    for i in range(1,51):
        correct_sim = df.loc[df['n_sim'] == i]
        index_max = correct_sim[correct_sim['infected'] == max(correct_sim.infected)].index.values[0]
        Imax.append(correct_sim.loc[index_max]['infected'])
        sustilsidst.append(index_max)
        std.append(np.std(correct_sim['infected']))
        d_peak.append(correct_sim.loc[index_max]['timestep']/525)
  #      print(correct_sim.loc[index_max]['timestep']/525)
    print("mean+std of d_peak: mean",np.mean(d_peak), "std",np.std(d_peak))
    print("min(Imax);",min(Imax),"max(Imax);",max(Imax))
    print("Mean of std of all imax: ",np.mean(std))
    print("Mean of I_max:",np.mean(Imax),"Mean of peak day:", np.mean(d_peak))
    print("Std of I_max:",np.std(Imax),"Std of peak day:",np.std(d_peak))

def plot_three_infection_plotted(data1,data2,data3):
    plotted_df1,plotted_df2,plotted_df3 = pd.read_csv(data1), pd.read_csv(data2), pd.read_csv(data3)
    plotted_df1.columns,plotted_df2.columns,plotted_df3.columns = ['timestep', 'infected', 'susceptible', 'recovered'],['timestep', 'infected', 'susceptible', 'recovered'],['timestep', 'infected', 'susceptible', 'recovered']
    inf1, inf2, inf3 = list(plotted_df1['infected']),list(plotted_df2['infected']),list(plotted_df3['infected'])
    x_values = [x for x in range(21001)]
    plt.plot(x_values,inf1)
    plt.plot(x_values,inf2)
    plt.plot(x_values,inf3)
    plt.ylim(0,160)
    plt.show()

def plot_three_infection_raw(data1,data2,data3):
    "Plot S, I and R for one or more raw (50 sim) data files"
    df1,df2,df3 = pd.read_csv(data1), pd.read_csv(data2), pd.read_csv(data3)
    df1.columns,df2.columns,df3.columns = ['timestep','infected','Agent_count','recovered','at_home','f','g','n_sim'], ['timestep','infected','Agent_count','recovered','at_home','f','g','n_sim'], ['timestep','infected','Agent_count','recovered','at_home','f','g','n_sim']
    s_mean, i_mean, r_mean = [],[],[]
    for i in range(31501):
        s_,i_,r_= [],[],[]
        indexes_at_timestep_i = df1[df1['timestep'] == i].index.to_numpy()#alle indexer der svarer til tidsskridt i
        for index in indexes_at_timestep_i:
            s_.append(df1.Agent_count[index]-df1.infected[index]-df1.recovered[index])
            i_.append(df1.infected[index])
            r_.append(df1.recovered[index])
        s_mean.append(np.mean(s_))
        i_mean.append(np.mean(i_))
        r_mean.append(np.mean(r_))
    x_values = [x for x in range(31501)]
    print(s_mean[-1])
    print(i_mean[-1])
    plt.plot(x_values,s_mean)
    plt.plot(x_values,i_mean)
    plt.plot(x_values,r_mean)
    plt.ylim(0,160)
    plt.show()
#plot_three_infection_raw(basis_all4,basis_all3,basis_all4)

def plot_specific_simulation(data1,data2,data3):
    df1,df2,df3 = pd.read_csv(data1), pd.read_csv(data2), pd.read_csv(data3)
    df1.columns,df2.columns,df3.columns =['timestep','infected','Agent_count','recovered','at_home','n_sim'],['timestep','infected','Agent_count','recovered','at_home','n_sim'],['timestep','infected','Agent_count','recovered','at_home','n_sim']

    infH_,infR_,infG_ =[],[],[]
    infH_max, infR_max, infG_max = [],[],[]

    for i in [7,40,29,46,34]: #5 simulationer med højst Imax for H
        correctsim2 = df1.loc[df1['n_sim'] == i]
        infH_.append(list(correctsim2['infected']))
        index_max = correctsim2[correctsim2['infected'] == max(correctsim2.infected)].index.values[0]
        infH_max.append(correctsim2.loc[index_max]['infected'])
    for i in [12,41,32,30,14]:#5 simulationer med højst Imax for R
        correctsim2 = df2.loc[df2['n_sim'] == i]
        infR_.append(list(correctsim2['infected']))
        index_max = correctsim2[correctsim2['infected'] == max(correctsim2.infected)].index.values[0]
        infR_max.append(correctsim2.loc[index_max]['infected'])
    for i in [2,9,29,27,39]:
        correctsim2 = df3.loc[df3['n_sim'] == i]
        infG_.append(list(correctsim2['infected']))
        index_max = correctsim2[correctsim2['infected'] == max(correctsim2.infected)].index.values[0]
        infG_max.append(correctsim2.loc[index_max]['infected'])
    print(np.mean(infH_max),np.mean(infR_max),np.mean(infG_max))
    for i in weekend_timesteps:
        plt.axvline(x=i, color='whitesmoke', linestyle='-')
    plt.xticks([0,5250,10500, 15750, 21000], [0, 10,20,30,40])
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    x_values = [x for x in range(21001)]
    for j in infR_:
        plt.plot(x_values,j,color=colors[1],linewidth='0.75')
    for j in infH_:
        plt.plot(x_values,j,color=colors[0],linewidth='0.75')
    for j in infG_:
        plt.plot(x_values,j,color=colors[2],linewidth='0.75')
    plt.ylim(0,160)
    plt.ylabel('Antal inficerede')
    plt.xlabel('Antal dage')
    plt.legend()
    plt.show()
#plot_specific_simulation(basis_all2,basis_all3,basis_all4)

def get_last_sus(data1,data2,data3):
    "Plot S, I and R for one or more raw (50 sim) data files"
    df1,df2,df3 = pd.read_csv(data1), pd.read_csv(data2), pd.read_csv(data3)
    df1.columns,df2.columns,df3.columns = ['timestep','infected','Agent_count','recovered','at_home','f','g','n_sim'], ['timestep','infected','Agent_count','recovered','at_home','f','g','n_sim'], ['timestep','infected','Agent_count','recovered','at_home','f','g','n_sim']
    s_mean, i_mean, r_mean = [],[],[]
    s_,i_ = [],[]
    print(len(df1)/50)
    indexes_at_timestep_i = df1[df1['timestep'] == 31500].index.to_numpy()#alle indexer der svarer til tidsskridt i
    for index in indexes_at_timestep_i:
        i_.append(df1.infected[index])
        s_.append(df1.Agent_count[index]-df1.infected[index]-df1.recovered[index])
         #   i_.append(df1.infected[index])
         #   r_.append(df1.recovered[index])
    s_mean.append(np.mean(s_))
    i_mean.append(np.mean(i_))

    print(s_mean)
    print(i_mean)

#plot_three_infection_raw(basis_all4,basis_all3,basis_all4)


mundbind70_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind70_2.csv"
mundbind70_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind70_3.csv"
mundbind70_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind70_4.csv"
#calc_mean_imax_std_peak_day(mundbind70_2)
#calc_mean_imax_std_peak_day(basis_all2)
#calc_mean_imax_std_peak_day(basis_all3)
#calc_mean_imax_std_peak_day(basis_all4)
#calc_mean_imax_std_peak_day(mundbind70_3)
#calc_mean_imax_std_peak_day(mundbind70_4)
def plot_specific_simulation_(data1):
    df1,df2,df3 = pd.read_csv(data1), pd.read_csv(data2), pd.read_csv(data3)
    df1.columns,df2.columns,df3.columns =['timestep','infected','Agent_count','recovered','at_home','n_sim'],['timestep','infected','Agent_count','recovered','at_home','n_sim'],['timestep','infected','Agent_count','recovered','at_home','n_sim']

    infH_,infR_,infG_ =[],[],[]
    infH_max, infR_max, infG_max = [],[],[]

    for i in range(1,50): #50 simulationer
        correctsim2 = df1.loc[df1['n_sim'] == i]
        infH_.append(list(correctsim2['infected']))
        index_max = correctsim2[correctsim2['infected'] == max(correctsim2.infected)].index.values[0]
        infH_max.append(correctsim2.loc[index_max]['infected'])
    '''
    for i in range(1,21): #50 simulationer
        correctsim2 = df2.loc[df2['n_sim'] == i]
        infR_.append(list(correctsim2['infected']))
        index_max = correctsim2[correctsim2['infected'] == max(correctsim2.infected)].index.values[0]
        infR_max.append(correctsim2.loc[index_max]['infected'])
    for i in range(1,21): #50 simulationer
        correctsim2 = df3.loc[df3['n_sim'] == i]
        infG_.append(list(correctsim2['infected']))
        index_max = correctsim2[correctsim2['infected'] == max(correctsim2.infected)].index.values[0]
        infG_max.append(correctsim2.loc[index_max]['infected'])
    print(np.mean(infH_max),np.mean(infR_max),np.mean(infG_max))
    '''
    for i in weekend_timesteps:
        plt.axvline(x=i, color='whitesmoke', linestyle='-')
    plt.xticks([0,5250,10500, 15750, 21000], [0, 10,20,30,40])

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    x_values = [x for x in range(21001)]

    for j in infG_:
        plt.plot(x_values,j,color=colors[0],linewidth='0.75',label="50")

    for j in infR_:
        plt.plot(x_values,j,color=colors[1],linewidth='0.75',label="60")

    for j in infH_:
        plt.plot(x_values,j,color=colors[2],linewidth='0.75',label="70")

  #  plt.axvline(x=6567, color='black', linestyle='dashed',linewidth='0.9')
  #  plt.axvline(x=11880, color='black', linestyle='dashed',linewidth='0.9')

    plt.ylim(0,160)
    plt.ylabel('Antal inficerede')
    plt.xlabel('Antal dage')
    plt.title("Alle simulationer for H")
  #  plt.legend()
    plt.show()


m60_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind60_2.csv"
m60_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind60_3.csv"
m60_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind60_4.csv"
m50_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind50_2.csv"
m50_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind50_3.csv"
m50_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind50_4.csv"
m70_16_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind70_16_uger_2.csv"
m70_16_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind70_16_uger_3.csv"
m70_16_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind70_16_uger_4.csv"
#get_last_sus(m70_16_2,m60_3,m60_4)
#plot_three_infection_raw(m70_16_4,m70_16_2,m70_16_2)
'''
data3_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind_70_3.csv"
#plot_three_infection(data1_3,data2_3,data3_3)
data1_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind_50_2.csv"
data2_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind_60_2.csv"
data3_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind_70_2.csv"
#plot_three_infection(data1_2,data2_2,data3_2)
data1_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind_50_4.csv"
data2_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind_60_4.csv"
data3_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/plotted_data_mundbind_70_4.csv"
#plot_three_infection(data1_4,data2_4,data3_4)
'''
data1_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_2.csv"
data2_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_3.csv"
data3_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_4.csv"

#calc_mean_imax_std_peak_day("/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/Basis_4.csv")
#calc_mean_imax_and_peak_day(data1_3)
#calc_mean_imax_and_peak_day(data2_3)
#calc_mean_imax_and_peak_day(data3_3)
'''
x_values = [x for x in range(21001)]
x_values = [timestep_to_day(x) for x in x_values]

#iinfected rød
data3 = parse_datafile_infected(path1, path2)
min_list3 = data3[0]
max_list3 = data3[1]
mean_list3 = data3[2]
plt.figure()
plt.plot(x_values, min_list3, color='firebrick', linewidth='0.3', label='$I_{min}, I_{max}$')
plt.plot(x_values, max_list3, color='firebrick', linewidth='0.3')
plt.plot(x_values, mean_list3, color='maroon', linewidth='3', label='middelværdi')
plt.fill_between(x_values, min_list3, max_list3, color='lightcoral', alpha=.1)
plt.legend()
plt.ylabel('Antal inficerede')
plt.xlabel('Antal dage')
plt.title('Antal inficerede for Basismodellen ved ???')
plt.show()



klasselokale1000sim_rows_maxinfected_24studerende = [1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 4, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 3, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 3, 1, 3, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 3, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 3, 2, 1, 1, 2, 1, 1, 3, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 3, 1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 3, 2, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 3, 2, 1, 1, 1, 3, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 3, 2, 2, 1, 1, 1, 1, 4, 2, 1, 2, 1, 4, 1, 3, 1, 2, 2, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 4, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 4, 2, 1, 2, 1, 1, 1, 1, 1, 2, 3, 2, 2, 1, 1, 1, 2, 5, 1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 3, 1, 1, 1, 2, 3, 1, 1, 2, 3, 1, 4, 1, 1, 1, 1, 1, 2, 2, 3, 2, 1, 1, 1, 3, 1, 1, 1, 1, 2, 3, 2, 2, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 3, 1, 1, 3, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 4, 2, 2, 1, 1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 3, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 3, 3, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 3, 1, 2, 1, 1, 1, 2, 1, 1, 3, 1, 3, 1, 3, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 3, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 4, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 3, 2, 3, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 1, 2, 1, 4, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 3, 1, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 3, 2, 3, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 3, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 3, 1, 2, 1, 2, 1, 1, 1, 2, 3, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2]
klasselokale1000sim_grupper_maxinfected_24studerende  = [2, 4, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 3, 1, 1, 2, 1, 2, 3, 1, 2, 2, 1, 2, 1, 3, 1, 1, 2, 1, 3, 3, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 2, 1, 4, 1, 2, 1, 3, 1, 2, 3, 1, 1, 1, 2, 1, 2, 3, 1, 1, 2, 2, 1, 2, 1, 1, 2, 3, 1, 1, 1, 2, 1, 2, 2, 3, 2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 3, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 3, 2, 1, 2, 1, 2, 1, 1, 1, 2, 3, 2, 3, 3, 2, 1, 1, 3, 1, 3, 2, 1, 2, 1, 2, 3, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 3, 3, 2, 2, 2, 1, 3, 2, 2, 3, 1, 1, 1, 3, 1, 2, 1, 2, 2, 2, 1, 3, 1, 1, 4, 2, 1, 3, 1, 1, 2, 2, 3, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 4, 1, 2, 2, 2, 2, 1, 3, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 3, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 3, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 3, 2, 1, 2, 1, 2, 3, 1, 1, 1, 4, 2, 1, 2, 3, 1, 1, 2, 2, 2, 2, 3, 3, 2, 2, 1, 1, 3, 1, 1, 1, 1, 4, 1, 1, 2, 3, 2, 2, 1, 2, 1, 2, 2, 3, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2, 2, 1, 1, 2, 3, 2, 1, 2, 2, 2, 3, 4, 1, 3, 1, 1, 1, 2, 3, 2, 2, 1, 2, 1, 4, 2, 3, 1, 3, 1, 2, 1, 1, 2, 1, 1, 2, 2, 3, 1, 1, 2, 1, 3, 3, 3, 2, 2, 3, 2, 1, 1, 3, 1, 3, 1, 2, 3, 1, 2, 3, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 3, 1, 2, 2, 1, 1, 2, 2, 4, 1, 2, 2, 1, 1, 1, 3, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 3, 2, 4, 3, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 3, 3, 2, 3, 3, 1, 2, 2, 1, 2, 3, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 2, 2, 1, 3, 2, 2, 2, 2, 2, 3, 1, 1, 2, 2, 1, 2, 1, 1, 1, 3, 3, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 3, 4, 2, 2, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 4, 1, 1, 1, 2, 1, 2, 3, 1, 3, 1, 1, 1, 1, 3, 2, 1, 1, 1, 2, 3, 2, 1, 3, 1, 2, 3, 2, 1, 2, 2, 1, 1, 3, 3, 3, 1, 2, 1, 2, 3, 2, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 3, 2, 2, 1, 2, 1, 4, 2, 2, 1, 2, 1, 2, 2, 4, 1, 2, 1, 1, 2, 2, 2, 2, 1, 3, 2, 3, 2, 1, 1, 2, 3, 3, 2, 2, 1, 1, 1, 1, 2, 1, 2, 4, 1, 2, 2, 2, 3, 3, 1, 1, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 3, 2, 3, 1, 1, 2, 3, 1, 2, 2, 2, 1, 4, 1, 2, 3, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 2, 3, 1, 1, 1, 1, 1, 3, 2, 1, 2, 1, 1, 1, 3, 1, 3, 1, 3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 2, 3, 1, 1, 2, 2, 2, 1, 2, 2, 1, 1, 1, 2, 3, 1, 2, 3, 2, 2, 2, 1, 2, 1, 2, 1, 2, 2, 1, 3, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 3, 1, 1, 2, 2, 3, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 3, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 3, 2, 2, 1, 1, 2, 3, 1, 1, 2, 3, 2, 3, 3, 3, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 3, 3, 2, 3, 2, 2, 1, 2, 1, 3, 2, 3, 2, 3, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 2, 1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 3, 2, 1, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 2, 3, 3, 1, 2, 3, 1, 2, 1, 1, 1, 3, 3, 3, 1, 2, 1, 3, 5, 1, 2, 1, 1]
klasselokale1000sim_hestesko_maxinfected_24studerende  = [1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 3, 3, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 3, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 3, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 3, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 3, 1, 2, 1, 2, 2, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 3, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 1, 2, 3, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 4, 1, 2, 2, 3, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 3, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 3, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 3, 2, 2, 3, 2, 2, 2, 1, 2, 1, 1, 3, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 3, 1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 3, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 3, 1, 1, 1, 1, 1, 2, 2, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 3, 1, 1, 2, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 2, 3, 1, 4, 1, 2, 2, 3, 2, 1, 1, 1, 2, 1, 1, 2, 3, 1, 3, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 1, 1, 2, 1, 3, 1, 2, 2, 3, 1, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 3, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 3, 3, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 3, 1, 1, 2, 3, 2, 1, 1, 1, 1, 3, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 3, 3, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 5, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 2, 1, 3, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 3, 3, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 4, 1, 2, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1]
print("24 studerende mean,row: ",np.mean(klasselokale1000sim_hestesko_maxinfected_24studerende),"std: ",np.std(klasselokale1000sim_hestesko_maxinfected_24studerende))
print("24 studerende mean,group: ",np.mean(klasselokale1000sim_grupper_maxinfected_24studerende),"std: ",np.std(klasselokale1000sim_grupper_maxinfected_24studerende))
print("24 studerende mean,hest: ",np.mean(klasselokale1000sim_rows_maxinfected_24studerende),"std: ",np.std(klasselokale1000sim_rows_maxinfected_24studerende))

klasselokale1000sim_rows_maxinfected_22studerende = [1, 1, 2, 3, 1, 1, 1, 2, 1, 1, 2, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 3, 2, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 3, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 4, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 3, 2, 1, 3, 2, 1, 3, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 4, 2, 2, 2, 2, 1, 1, 2, 2, 3, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1, 1, 2, 1, 3, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 3, 1, 1, 3, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 3, 1, 1, 1, 1, 2, 2, 1, 1, 3, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 3, 2, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 3, 1, 1, 3, 1, 1, 3, 1, 1, 2, 2, 1, 1, 1, 2, 3, 2, 4, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 3, 3, 3, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 3, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 3, 1, 1, 3, 2, 2, 1, 3, 2, 2, 1, 1, 1, 2, 3, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 3, 5, 2, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 4, 1, 1, 1, 2, 1, 1, 1, 3, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 2, 2, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 3, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 3, 2, 2, 1, 1, 1, 3, 2, 1, 2, 2, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 3, 3, 1, 2, 1, 1, 2, 4, 1, 1, 2, 2, 2, 3, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 3, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 2]
klasselokale1000sim_grupper_maxinfected_22studerende  = [2, 1, 1, 2, 3, 1, 2, 1, 1, 1, 3, 3, 2, 1, 4, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 3, 1, 3, 1, 1, 1, 1, 2, 2, 1, 2, 3, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 2, 3, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 1, 1, 4, 1, 2, 1, 2, 1, 3, 3, 2, 2, 1, 3, 1, 2, 3, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2, 3, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 3, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 3, 2, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 3, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 1, 3, 1, 3, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 4, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 3, 3, 1, 2, 1, 2, 2, 3, 1, 3, 1, 2, 2, 1, 2, 2, 1, 2, 2, 3, 3, 1, 3, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 3, 2, 2, 2, 1, 2, 1, 3, 2, 2, 2, 2, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 1, 2, 2, 1, 1, 1, 2, 3, 2, 2, 2, 1, 2, 3, 1, 1, 2, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 3, 1, 1, 3, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 3, 1, 1, 2, 2, 2, 2, 2, 1, 1, 3, 1, 1, 1, 2, 1, 3, 1, 3, 1, 2, 2, 2, 2, 3, 3, 1, 2, 2, 2, 2, 2, 3, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 3, 2, 2, 1, 2, 3, 1, 1, 1, 1, 1, 2, 2, 1, 1, 3, 1, 1, 2, 2, 3, 1, 1, 1, 2, 1, 3, 3, 3, 2, 1, 1, 1, 2, 1, 3, 1, 2, 1, 2, 3, 1, 1, 1, 2, 1, 2, 1, 3, 2, 2, 3, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 3, 3, 2, 1, 1, 1, 2, 1, 1, 1, 1, 5, 1, 1, 2, 2, 2, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 3, 1, 3, 1, 1, 1, 2, 4, 1, 1, 1, 3, 2, 1, 2, 1, 1, 2, 2, 2, 1, 2, 1, 2, 2, 5, 1, 1, 4, 1, 2, 3, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 3, 1, 1, 3, 2, 1, 3, 2, 2, 1, 2, 2, 3, 2, 3, 2, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 3, 1, 2, 1, 2, 1, 2, 2, 1, 1, 2, 1, 3, 2, 1, 2, 3, 1, 1, 1, 2, 1, 2, 1, 2, 1, 3, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 3, 2, 3, 2, 1, 1, 2, 1, 2, 2, 1, 1, 2, 5, 2, 1, 1, 2, 3, 1, 2, 2, 2, 3, 1, 1, 2, 1, 2, 2, 2, 2, 3, 1, 2, 2, 1, 3, 2, 1, 3, 1, 2, 2, 2, 1, 1, 2, 1, 1, 3, 3, 3, 1, 3, 2, 1, 1, 1, 2, 1, 2, 3, 3, 2, 2, 1, 1, 2, 1, 3, 2, 3, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 3, 3, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 3, 1, 1, 2, 3, 1, 1, 1, 2, 2, 2, 2, 1, 2, 4, 2, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 3, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 3, 2, 2, 4, 2, 2, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 3, 1, 4, 2, 1, 1, 1, 1, 4, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 3, 1, 2, 2, 2, 1, 1, 3, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 2, 3, 2, 1, 3, 2, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 4, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 3, 2, 2, 1, 3, 2, 1, 3, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 3, 1, 3, 1, 3, 3, 2, 3, 2, 1, 3, 1, 1, 2, 1, 3, 2, 1, 2, 2, 2, 2, 1, 1, 1, 1, 4, 2, 2, 2, 1, 1, 1, 3, 1, 1, 2, 1, 2, 1, 2, 3, 1, 1, 2, 1, 2, 1, 1, 1, 2, 3, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 3, 2, 1, 3, 2, 1, 2, 2, 2, 1, 1, 2]
klasselokale1000sim_hestesko_maxinfected_22studerende  = [1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 2, 2, 1, 1, 3, 2, 1, 2, 3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 3, 2, 1, 1, 3, 3, 1, 1, 1, 1, 2, 1, 1, 2, 3, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 3, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 3, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 3, 1, 1, 2, 1, 1, 1, 3, 1, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 3, 1, 2, 3, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 3, 3, 2, 2, 1, 2, 2, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 3, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 3, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 3, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 3, 2, 2, 1, 1, 1, 1, 2, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 2, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 3, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 2, 3, 2, 1, 3, 2, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 2, 1, 3, 1, 2, 1, 1, 1, 1, 2, 1, 3, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 1, 3, 1, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2]
print("22 studerende mean,row: ",np.mean(klasselokale1000sim_rows_maxinfected_22studerende),"std: ",np.std(klasselokale1000sim_rows_maxinfected_22studerende))
print("22 studerende mean,group: ",np.mean(klasselokale1000sim_grupper_maxinfected_22studerende),"std: ",np.std(klasselokale1000sim_grupper_maxinfected_22studerende))
print("22 studerende mean,hest: ",np.mean(klasselokale1000sim_hestesko_maxinfected_22studerende),"std: ",np.std(klasselokale1000sim_hestesko_maxinfected_22studerende))

'''
klasselokale1000sim_rows_maxinfected_20studerende = [2, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 4, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2, 2, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 3, 1, 3, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 3, 3, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 4, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 3, 2, 3, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 3, 1, 1, 1, 1, 1, 2, 3, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 4, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 3, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 3, 1, 2, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 4, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1]
klasselokale1000sim_grupper_maxinfected_20studerende  = [3, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 3, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 2, 2, 3, 1, 4, 1, 1, 3, 1, 3, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 3, 1, 2, 2, 2, 2, 1, 2, 1, 3, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 1, 2, 1, 3, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 2, 1, 3, 1, 1, 3, 2, 1, 1, 2, 2, 1, 1, 1, 2, 3, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 3, 2, 1, 2, 1, 1, 2, 3, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 2, 2, 2, 2, 2, 3, 1, 1, 2, 3, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 3, 2, 2, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 4, 1, 2, 2, 1, 3, 2, 4, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 3, 2, 2, 1, 2, 1, 3, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 3, 1, 1, 2, 3, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 2, 3, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 3, 1, 2, 3, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 3, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 2, 1, 3, 1, 2, 2, 1, 1, 1, 1, 3, 2, 1, 3, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 1, 1, 3, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 3, 1, 3, 3, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 3, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 3, 2, 2, 2, 1, 3, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 3, 1, 2, 4, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 3, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 3, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 3, 1, 2, 2, 3, 1, 1, 1, 1, 2, 3, 3, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 4, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 3, 2, 2, 2, 3, 3, 2, 1, 1, 1, 2, 3, 1, 4, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 3, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 3, 2, 2, 2, 1, 1, 1, 4, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 3, 1, 1, 3, 3, 1, 3, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 3, 2, 2, 2, 1, 4, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 1, 3, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 1, 4, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 3, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2, 3, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2]
klasselokale1000sim_hestesko_maxinfected_20studerende  = [2, 1, 1, 2, 1, 2, 1, 3, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 2, 1, 2, 4, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 3, 1, 3, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 1, 3, 1, 1, 2, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 3, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 3, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 3, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1]
print("20 studerende mean,row: ",np.mean(klasselokale1000sim_rows_maxinfected_20studerende),"std: ",np.std(klasselokale1000sim_rows_maxinfected_20studerende))
print("20 studerende mean,group: ",np.mean(klasselokale1000sim_grupper_maxinfected_20studerende),"std: ",np.std(klasselokale1000sim_grupper_maxinfected_20studerende))
print("20 studerende mean,hest: ",np.mean(klasselokale1000sim_hestesko_maxinfected_20studerende),"std: ",np.std(klasselokale1000sim_hestesko_maxinfected_20studerende))

'''

klasselokale1000sim_rows_maxinfected_18studerende = [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 4, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 2, 3, 1, 1, 1, 4, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 4, 1, 2, 1, 2, 1, 2, 2, 3, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 2, 2, 2, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 4, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 3, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 3, 1, 2, 2, 1, 2, 1, 3, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 4, 1, 1, 2, 1, 1, 3, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 3, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 3, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 3, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 1, 3, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1]
klasselokale1000sim_grupper_maxinfected_18studerende  = [1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 4, 1, 1, 1, 1, 2, 2, 2, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 3, 1, 3, 2, 1, 1, 1, 1, 1, 1, 3, 2, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 3, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 2, 3, 2, 1, 2, 2, 3, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 3, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 3, 2, 2, 1, 2, 1, 1, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 3, 2, 1, 2, 2, 1, 2, 3, 1, 1, 2, 1, 1, 3, 2, 2, 1, 3, 1, 1, 1, 1, 3, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 3, 1, 2, 2, 1, 2, 3, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 3, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 3, 1, 2, 1, 2, 1, 2, 2, 2, 3, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 2, 3, 2, 2, 1, 1, 3, 2, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 3, 2, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 3, 1, 1, 1, 2, 3, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 3, 1, 2, 3, 1, 2, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 3, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 3, 2, 2, 1, 2, 1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 3, 2, 1, 2, 1, 2, 1, 3, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 3, 1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 3, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 2, 3, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 3, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 3, 2, 1, 1, 1, 1, 2, 2, 3, 1, 2, 2, 2, 2, 3, 1, 1, 1, 2, 2, 1, 2, 1, 2, 2, 3, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 3, 1, 1, 1, 2, 2, 4, 1, 2, 3, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 3, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 1, 1, 1, 3, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 3, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 2, 3, 1, 1, 2, 2, 1, 2, 3, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2, 2, 1, 2, 2, 3, 2, 1, 1, 1, 2, 1, 1, 2, 1, 3, 3, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 3, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 3, 1, 2, 1, 1, 2, 1, 3, 2, 1, 2, 2, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 3, 2, 1, 1, 1, 4, 2, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 3, 2, 1, 2, 3, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1]
klasselokale1000sim_hestesko_maxinfected_18studerende  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 3, 2, 1, 1, 1, 1, 2, 1, 4, 1, 1, 2, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 3, 1, 1, 4, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 3, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 2, 1, 3, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 1, 2, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 3, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1]
print("18 studerende mean,row: ",np.mean(klasselokale1000sim_rows_maxinfected_18studerende),"std: ",np.std(klasselokale1000sim_rows_maxinfected_18studerende))
print("18 studerende mean,group: ",np.mean(klasselokale1000sim_grupper_maxinfected_18studerende),"std: ",np.std(klasselokale1000sim_grupper_maxinfected_18studerende))
print("18 studerende mean,hest: ",np.mean(klasselokale1000sim_hestesko_maxinfected_18studerende),"std: ",np.std(klasselokale1000sim_hestesko_maxinfected_18studerende))


klasselokale1000sim_rows_maxinfected_24TA = [1, 2, 1, 1, 2, 2, 1, 3, 2, 2, 3, 2, 2, 4, 1, 2, 2, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 3, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 3, 1, 1, 4, 1, 1, 2, 1, 3, 1, 2, 1, 1, 3, 1, 3, 3, 1, 2, 2, 2, 1, 3, 1, 1, 1, 1, 1, 2, 2, 2, 3, 1, 2, 1, 2, 1, 2, 1, 1, 3, 2, 2, 1, 1, 2, 1, 3, 3, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 3, 1, 2, 2, 3, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 4, 1, 1, 2, 2, 2, 1, 2, 3, 2, 1, 1, 1, 1, 1, 3, 3, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 2, 2, 1, 3, 2, 2, 1, 1, 1, 1, 3, 2, 1, 1, 2, 1, 1, 1, 4, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 3, 3, 2, 2, 1, 1, 3, 2, 2, 1, 1, 1, 1, 3, 3, 1, 2, 1, 1, 3, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 3, 1, 2, 2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 3, 3, 1, 1, 1, 1, 1, 2, 1, 2, 4, 3, 2, 1, 1, 3, 2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 3, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 3, 1, 1, 4, 1, 2, 2, 1, 2, 1, 2, 2, 2, 2, 1, 3, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 3, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 3, 2, 2, 1, 2, 1, 2, 2, 3, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 3, 3, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 3, 1, 4, 4, 1, 1, 1, 2, 2, 1, 1, 2, 2, 3, 2, 4, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 4, 1, 2, 2, 1, 1, 1, 2, 3, 2, 2, 2, 1, 1, 2, 3, 1, 1, 2, 1, 4, 2, 1, 4, 2, 2, 2, 1, 2, 2, 1, 1, 5, 2, 2, 1, 2, 3, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 3, 2, 1, 2, 1, 2, 1, 2, 1, 3, 1, 1, 3, 1, 2, 1, 4, 1, 3, 1, 2, 1, 1, 3, 3, 1, 4, 2, 2, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 3, 3, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 3, 2, 2, 2, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 2, 2, 1, 1, 3, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 2, 3, 1, 1, 3, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 4, 1, 1, 3, 3, 3, 2, 2, 1, 2, 2, 3, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 3, 2, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 3, 2, 2, 1, 3, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 3, 3, 1, 1, 2, 2, 1, 1, 2, 2, 2, 3, 1, 2, 1, 1, 3, 1, 2, 1, 1, 2, 2, 2, 3, 2, 1, 2, 3, 2, 2, 3, 1, 1, 3, 1, 3, 1, 1, 1, 1, 1, 4, 3, 1, 2, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 4, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 4, 2, 1, 3, 2, 2, 3, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 3, 2, 1, 1, 2, 2, 1, 4, 1, 1, 1, 3, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 3, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 4, 2, 2, 1, 2, 1, 1, 1, 1, 1, 2, 3, 3, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 3, 2, 2, 3, 2, 1, 3, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 2]
klasselokale1000sim_grupper_maxinfected_24TA = [2, 1, 2, 2, 2, 3, 1, 2, 2, 2, 2, 2, 1, 3, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 3, 2, 2, 1, 1, 1, 1, 1, 4, 2, 1, 2, 3, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 4, 2, 1, 1, 2, 1, 2, 2, 1, 3, 2, 1, 2, 1, 1, 3, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 2, 4, 1, 2, 2, 1, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 3, 3, 2, 2, 1, 1, 2, 2, 2, 2, 3, 3, 1, 1, 1, 3, 1, 3, 1, 2, 3, 1, 1, 2, 1, 1, 3, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2, 2, 1, 1, 2, 1, 4, 1, 2, 1, 2, 1, 3, 1, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 3, 2, 1, 3, 2, 4, 2, 1, 1, 1, 2, 1, 2, 3, 1, 2, 3, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 3, 2, 1, 1, 4, 2, 4, 1, 2, 1, 1, 2, 2, 3, 1, 3, 2, 2, 2, 1, 2, 4, 1, 2, 1, 1, 6, 1, 2, 3, 1, 1, 2, 2, 2, 1, 2, 1, 3, 2, 1, 1, 1, 3, 3, 2, 2, 3, 2, 3, 1, 3, 1, 4, 2, 2, 1, 1, 1, 1, 2, 1, 1, 5, 1, 3, 1, 2, 1, 2, 4, 3, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 3, 3, 1, 1, 1, 3, 1, 2, 2, 2, 3, 4, 1, 3, 3, 2, 1, 3, 2, 1, 1, 2, 1, 1, 3, 3, 1, 2, 2, 1, 1, 4, 2, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 4, 1, 1, 1, 1, 3, 2, 2, 1, 3, 1, 1, 1, 1, 1, 1, 4, 2, 1, 4, 2, 2, 2, 1, 2, 1, 2, 3, 1, 1, 2, 2, 2, 1, 2, 1, 3, 1, 3, 3, 3, 2, 1, 1, 2, 1, 3, 3, 1, 1, 3, 2, 2, 1, 1, 1, 1, 2, 3, 3, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 3, 1, 1, 2, 1, 2, 1, 2, 1, 4, 1, 4, 1, 1, 3, 2, 1, 4, 1, 1, 1, 1, 1, 1, 2, 3, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 3, 4, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 1, 1, 2, 1, 1, 3, 1, 2, 2, 3, 3, 1, 2, 2, 2, 3, 1, 2, 2, 1, 2, 2, 1, 2, 3, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 4, 1, 2, 1, 3, 1, 1, 1, 2, 3, 1, 4, 3, 1, 4, 2, 2, 3, 1, 4, 3, 3, 3, 2, 1, 2, 1, 2, 1, 3, 1, 2, 2, 1, 2, 1, 2, 1, 3, 2, 1, 1, 1, 3, 1, 1, 2, 1, 2, 2, 1, 1, 4, 2, 2, 2, 2, 3, 1, 2, 2, 3, 2, 2, 1, 2, 1, 3, 3, 1, 6, 2, 3, 1, 2, 2, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 3, 5, 3, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 3, 2, 4, 2, 2, 1, 1, 1, 1, 5, 1, 1, 2, 1, 2, 3, 2, 2, 1, 2, 1, 2, 1, 2, 1, 3, 1, 1, 3, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 4, 1, 1, 2, 3, 2, 1, 2, 1, 1, 2, 2, 1, 3, 2, 2, 1, 1, 3, 2, 3, 2, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 3, 2, 1, 2, 1, 1, 3, 2, 1, 2, 2, 2, 2, 3, 1, 1, 2, 1, 1, 3, 2, 2, 2, 2, 1, 1, 3, 2, 1, 5, 1, 3, 3, 3, 1, 1, 3, 1, 2, 4, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 3, 1, 1, 2, 2, 2, 4, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 5, 1, 3, 1, 3, 3, 1, 4, 1, 1, 3, 2, 2, 3, 3, 2, 2, 2, 2, 4, 1, 4, 2, 2, 1, 2, 4, 3, 2, 4, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 2, 3, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 1, 4, 3, 1, 2, 3, 1, 2, 1, 1, 3, 2, 1, 1, 1, 1, 2, 1, 1, 5, 3, 2, 1, 2, 2, 2, 3, 1, 1, 1, 1, 3, 2, 1, 2, 2, 2, 3, 2, 1, 2, 2, 3, 2, 1, 1, 1, 4, 2, 1, 1, 3, 3, 2, 2, 3, 3, 4, 1, 1, 1, 2, 1, 4, 1, 3, 1, 1, 1, 2, 2, 3, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 3, 1, 3, 1, 1, 4, 1, 4, 3, 1, 1, 1, 1, 5, 1, 1, 2, 3, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 3, 2, 2, 1, 3, 2, 2, 1, 1, 2, 2, 1, 2, 1, 3, 1, 1, 3, 2, 3, 2, 2, 2, 1, 1, 1, 2, 4, 3, 3, 1, 1, 3, 2, 2, 1, 3, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 3, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1]
klasselokale1000sim_hestesko_maxinfected_24TA = [1, 1, 2, 1, 1, 1, 2, 2, 2, 3, 1, 1, 3, 2, 1, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2, 3, 2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 3, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 3, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 2, 2, 1, 2, 3, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 3, 2, 1, 1, 1, 1, 3, 1, 1, 2, 2, 2, 2, 1, 3, 2, 4, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 3, 1, 2, 2, 2, 1, 3, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 3, 1, 3, 2, 1, 1, 1, 3, 2, 3, 2, 1, 2, 1, 1, 3, 1, 1, 3, 2, 1, 2, 2, 1, 1, 2, 2, 1, 3, 1, 2, 1, 2, 1, 2, 1, 3, 2, 2, 2, 2, 1, 1, 2, 1, 2, 1, 3, 2, 1, 1, 3, 1, 1, 3, 1, 2, 3, 1, 2, 1, 1, 3, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 3, 2, 1, 2, 1, 3, 2, 1, 1, 3, 1, 1, 2, 1, 3, 2, 3, 1, 2, 2, 2, 1, 3, 2, 1, 2, 2, 2, 1, 1, 1, 3, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 2, 2, 3, 3, 1, 2, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 3, 1, 2, 1, 4, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 4, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 4, 2, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 2, 3, 2, 1, 2, 3, 3, 1, 2, 2, 3, 1, 2, 2, 1, 2, 3, 1, 1, 1, 2, 2, 1, 1, 2, 1, 3, 1, 1, 1, 3, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 3, 1, 2, 1, 1, 3, 1, 1, 1, 2, 2, 1, 1, 1, 3, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 3, 2, 4, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 2, 3, 2, 1, 2, 1, 2, 1, 3, 3, 2, 3, 2, 2, 2, 1, 2, 1, 2, 1, 2, 3, 3, 1, 2, 2, 2, 1, 1, 1, 2, 2, 1, 2, 2, 2, 1, 3, 2, 1, 1, 2, 2, 3, 1, 2, 2, 1, 1, 1, 3, 2, 2, 1, 2, 2, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 3, 1, 1, 1, 2, 3, 1, 1, 3, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 4, 1, 1, 1, 1, 1, 3, 1, 3, 1, 1, 2, 2, 3, 2, 1, 1, 1, 2, 2, 1, 1, 3, 2, 2, 3, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 2, 3, 1, 2, 3, 1, 1, 1, 3, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 2, 3, 2, 1, 1, 1, 4, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 3, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 4, 1, 2, 4, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 4, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 3, 2, 1, 1, 1, 1, 3, 1, 3, 1, 1, 1, 1, 2, 1, 4, 2, 2, 4, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 3, 1, 1, 1, 1, 3, 2, 2, 2, 3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 3, 3, 1, 1, 1, 3, 1, 1, 1, 2, 2, 2, 1, 3, 1, 1, 1, 2, 2, 3, 1, 1, 3, 1, 1, 1, 1, 2, 1, 3, 1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 2, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 2, 2, 1, 1]
print("24 TA mean,row: ",np.mean(klasselokale1000sim_rows_maxinfected_24TA),"std: ",np.std(klasselokale1000sim_rows_maxinfected_24TA))
print("24 TA mean,group: ",np.mean(klasselokale1000sim_grupper_maxinfected_24TA),"std: ",np.std(klasselokale1000sim_grupper_maxinfected_24TA))
print("24 TA mean,hest: ",np.mean(klasselokale1000sim_hestesko_maxinfected_24TA),"std: ",np.std(klasselokale1000sim_hestesko_maxinfected_24TA))

klasselokale1000sim_rows_maxinfected_22TA = [4, 1, 3, 2, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 3, 1, 1, 2, 3, 1, 1, 3, 2, 1, 2, 3, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 3, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 3, 1, 2, 2, 1, 4, 1, 1, 1, 4, 2, 1, 1, 1, 1, 1, 3, 1, 1, 3, 2, 2, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 2, 3, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 1, 1, 3, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 4, 1, 1, 2, 1, 1, 3, 2, 2, 4, 1, 1, 2, 2, 1, 1, 2, 2, 1, 3, 2, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 5, 2, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 3, 2, 1, 1, 3, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 4, 1, 1, 2, 1, 2, 1, 1, 3, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 3, 3, 2, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 1, 1, 1, 3, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 3, 2, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 1, 1, 3, 1, 2, 4, 2, 2, 2, 3, 1, 1, 2, 2, 1, 2, 1, 2, 2, 2, 1, 1, 4, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 3, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 3, 2, 1, 1, 2, 1, 1, 3, 1, 2, 1, 4, 1, 1, 1, 1, 2, 1, 2, 1, 3, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 2, 1, 2, 2, 2, 2, 3, 1, 2, 2, 1, 1, 3, 1, 2, 1, 1, 3, 1, 1, 1, 2, 2, 4, 1, 1, 1, 2, 3, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 4, 1, 1, 1, 2, 1, 3, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 3, 1, 1, 3, 2, 1, 3, 2, 1, 1, 1, 1, 1, 1, 3, 1, 2, 3, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 3, 2, 2, 1, 1, 1, 2, 3, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 3, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 3, 1, 1, 1, 1, 2, 2, 3, 1, 2, 2, 2, 2, 1, 1, 2, 1, 2, 2, 1, 3, 2, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 3, 2, 1, 1, 3, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 3, 1, 3, 2, 3, 1, 1, 3, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 3, 3, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 3, 1, 1, 1, 3, 1, 1, 3, 4, 1, 1, 1, 1, 3, 2, 1, 1, 1, 3, 2, 1, 3, 2, 1, 2, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 3, 2, 1, 3, 1, 1, 1, 1, 3, 2, 2, 2, 3, 1, 2, 2, 2, 3, 1, 3, 1, 2, 1, 1, 1, 1, 2, 1, 3, 1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 3, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 2, 3, 1, 1, 1, 2, 3, 2, 1, 2, 2, 2, 3, 2, 1, 2, 2, 3, 1, 2, 2, 1, 3, 3, 2, 2, 2, 3, 2, 1, 1, 1, 1, 1, 2, 1, 3, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 3, 3, 4, 1, 1, 1, 1, 3, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 3, 1, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1]
klasselokale1000sim_grupper_maxinfected_22TA = [4, 1, 4, 1, 2, 2, 1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 4, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 3, 1, 1, 2, 3, 2, 1, 1, 2, 1, 2, 1, 1, 2, 3, 3, 1, 2, 1, 1, 2, 2, 2, 1, 2, 3, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 3, 4, 1, 3, 1, 1, 2, 2, 3, 1, 1, 1, 1, 1, 1, 3, 2, 3, 3, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2, 3, 1, 3, 2, 3, 1, 2, 2, 1, 3, 2, 1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 2, 2, 1, 3, 2, 1, 3, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 3, 3, 2, 3, 1, 3, 1, 3, 1, 3, 2, 4, 2, 1, 1, 3, 1, 2, 1, 1, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 3, 1, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 3, 2, 1, 2, 3, 2, 3, 1, 1, 1, 2, 3, 1, 2, 1, 2, 1, 3, 1, 1, 3, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 1, 1, 3, 1, 3, 3, 2, 2, 1, 1, 3, 3, 2, 2, 1, 2, 3, 3, 1, 1, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 4, 3, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 3, 2, 1, 1, 1, 3, 3, 2, 3, 3, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 2, 3, 1, 1, 3, 2, 1, 3, 2, 3, 2, 1, 2, 2, 1, 2, 3, 4, 2, 3, 1, 3, 4, 1, 2, 3, 1, 2, 2, 3, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 4, 4, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 4, 1, 1, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 3, 1, 1, 1, 1, 3, 2, 3, 2, 1, 1, 3, 1, 3, 2, 3, 2, 2, 2, 2, 1, 2, 2, 4, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 1, 2, 2, 3, 1, 1, 3, 2, 1, 5, 1, 5, 3, 1, 2, 4, 2, 4, 2, 1, 2, 3, 5, 3, 2, 2, 2, 1, 3, 2, 2, 1, 2, 1, 1, 3, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 3, 1, 2, 2, 1, 6, 1, 3, 3, 1, 2, 1, 2, 2, 1, 2, 2, 2, 3, 2, 2, 2, 1, 1, 1, 3, 2, 1, 2, 2, 1, 2, 1, 1, 5, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 4, 1, 3, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 3, 1, 1, 3, 2, 3, 3, 1, 2, 2, 2, 3, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 2, 2, 1, 2, 3, 1, 1, 2, 1, 1, 3, 2, 2, 1, 1, 2, 1, 2, 3, 2, 1, 2, 2, 3, 1, 2, 3, 1, 1, 2, 2, 3, 2, 1, 1, 2, 3, 4, 1, 2, 2, 1, 1, 2, 3, 3, 2, 2, 1, 3, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 3, 2, 2, 1, 1, 1, 1, 3, 3, 4, 1, 2, 1, 1, 1, 2, 3, 2, 2, 2, 1, 2, 1, 1, 1, 1, 3, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 3, 1, 2, 2, 1, 3, 1, 3, 1, 4, 2, 4, 2, 2, 3, 1, 1, 2, 2, 1, 6, 2, 3, 1, 2, 2, 2, 3, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 3, 2, 2, 3, 1, 2, 4, 2, 1, 1, 1, 3, 1, 1, 1, 1, 2, 4, 1, 2, 1, 2, 3, 3, 1, 2, 2, 2, 1, 3, 1, 1, 3, 2, 1, 1, 2, 2, 2, 2, 1, 2, 3, 2, 3, 1, 3, 2, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 4, 1, 1, 1, 3, 1, 3, 3, 1, 2, 2, 3, 2, 2, 2, 2, 4, 1, 1, 1, 2, 2, 2, 1, 1, 3, 1, 3, 1, 2, 1, 1, 1, 1, 2, 2, 3, 1, 1, 3, 1, 1, 1, 1, 1, 3, 2, 2, 2, 1, 1, 1, 1, 5, 2, 1, 3, 1, 2, 1, 4, 1, 1, 2, 2, 2, 2, 1, 2, 4, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 3, 3, 3, 2, 2, 2, 1, 1, 1, 3, 1, 2, 1, 2, 1, 1, 1, 3, 1, 2, 3, 3, 4, 1, 2, 1, 1, 1, 1, 2, 3, 4, 3, 2, 1, 2, 1, 3, 2, 2, 2, 2, 1, 1, 3, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 2, 1, 1, 1, 2, 3, 2, 3, 2, 1, 1, 3, 1, 2, 1, 2, 3, 1, 1, 1, 1, 1, 1, 3, 1, 4, 2, 2, 1, 2, 1, 2, 4, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1]
klasselokale1000sim_hestesko_maxinfected_22TA = [3, 1, 1, 4, 2, 2, 3, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 2, 2, 2, 1, 2, 1, 4, 2, 3, 1, 1, 3, 2, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 3, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 3, 1, 1, 1, 1, 1, 2, 2, 1, 3, 3, 1, 2, 3, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 3, 1, 2, 2, 1, 2, 1, 2, 2, 5, 1, 2, 4, 1, 3, 1, 2, 1, 1, 1, 1, 1, 5, 2, 3, 1, 1, 4, 1, 2, 2, 1, 3, 1, 3, 1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 4, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 3, 1, 1, 1, 2, 1, 2, 1, 1, 3, 3, 3, 2, 3, 1, 1, 4, 2, 1, 1, 2, 1, 2, 1, 1, 3, 2, 1, 1, 3, 1, 1, 2, 3, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 3, 1, 3, 1, 3, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2, 1, 1, 1, 2, 3, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 4, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 4, 1, 2, 1, 3, 2, 2, 2, 4, 2, 2, 1, 1, 2, 1, 3, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 4, 1, 2, 1, 1, 1, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 1, 2, 2, 1, 2, 3, 1, 1, 1, 2, 1, 2, 2, 2, 3, 3, 2, 2, 2, 1, 4, 2, 1, 2, 1, 2, 3, 2, 1, 1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 3, 1, 2, 2, 3, 1, 2, 4, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 3, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 3, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 3, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 4, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 3, 1, 1, 2, 1, 1, 3, 3, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 3, 2, 1, 1, 2, 4, 2, 3, 1, 3, 1, 3, 1, 2, 3, 1, 1, 2, 1, 2, 1, 2, 6, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 3, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 3, 4, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 3, 3, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 1, 1, 3, 1, 3, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 4, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 3, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 3, 2, 2, 1, 3, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 2, 2, 4, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 2, 3, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 3, 1, 1, 2, 4, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 3, 2, 1]
print("22 TA mean,row: ",np.mean(klasselokale1000sim_rows_maxinfected_22TA),"std: ",np.std(klasselokale1000sim_rows_maxinfected_22TA))
print("22 TA mean,group: ",np.mean(klasselokale1000sim_rows_maxinfected_22TA),"std: ",np.std(klasselokale1000sim_rows_maxinfected_22TA))
print("22 TA mean,hest: ",np.mean(klasselokale1000sim_hestesko_maxinfected_22TA),"std: ",np.std(klasselokale1000sim_hestesko_maxinfected_22TA))
'''

klasselokale1000sim_rows_maxinfected_20TA = [1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 4, 2, 1, 3, 2, 1, 2, 1, 1, 3, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 3, 1, 1, 1, 2, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 3, 3, 1, 1, 2, 1, 1, 1, 3, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 2, 3, 2, 1, 1, 1, 3, 1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 3, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 3, 1, 1, 1, 2, 1, 2, 2, 1, 4, 2, 1, 3, 2, 3, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 2, 1, 3, 1, 1, 2, 2, 1, 1, 1, 3, 2, 1, 1, 1, 2, 1, 3, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 3, 1, 1, 1, 1, 2, 5, 1, 2, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 3, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 3, 1, 1, 1, 5, 2, 1, 1, 1, 3, 2, 1, 3, 1, 2, 1, 3, 1, 3, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 2, 2, 1, 4, 2, 1, 3, 2, 3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 3, 1, 1, 1, 1, 2, 1, 1, 2, 2, 4, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 3, 1, 2, 2, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 3, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 3, 1, 1, 3, 1, 1, 3, 3, 2, 1, 2, 1, 1, 2, 1, 5, 2, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 3, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 4, 2, 1, 1, 1, 1, 2, 1, 1, 2, 4, 2, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 2, 1, 2, 1, 2, 4, 1, 2, 1, 3, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 3, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 3, 3, 2, 1, 1, 1, 1, 3, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 3, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 4, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 3, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 2, 3, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 3, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 4, 1, 3, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 1, 1, 2, 3, 3, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1]
klasselokale1000sim_grupper_maxinfected_20TA = [2, 1, 1, 3, 2, 2, 1, 1, 2, 3, 1, 3, 2, 2, 2, 2, 2, 2, 4, 1, 2, 1, 3, 3, 1, 2, 3, 2, 1, 1, 1, 1, 3, 3, 1, 1, 3, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 3, 2, 1, 2, 1, 2, 1, 1, 3, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 3, 2, 3, 2, 1, 1, 1, 3, 1, 4, 1, 1, 1, 2, 1, 2, 2, 1, 1, 4, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 4, 1, 1, 3, 1, 5, 1, 2, 1, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 3, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 3, 1, 2, 1, 3, 3, 1, 3, 4, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 3, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 3, 2, 3, 1, 1, 2, 1, 3, 4, 3, 1, 2, 2, 1, 1, 3, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 4, 1, 1, 4, 1, 1, 4, 1, 2, 2, 1, 2, 2, 5, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 4, 2, 1, 2, 2, 2, 2, 1, 1, 1, 3, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 3, 1, 2, 2, 1, 1, 1, 2, 1, 1, 3, 3, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2, 1, 3, 2, 1, 3, 2, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 3, 2, 1, 3, 2, 1, 1, 2, 3, 1, 2, 1, 3, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 3, 2, 2, 2, 4, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 4, 1, 2, 2, 1, 4, 1, 1, 1, 2, 2, 2, 1, 2, 2, 3, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 3, 1, 2, 1, 1, 2, 1, 2, 3, 3, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 2, 3, 3, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 1, 3, 3, 1, 3, 1, 1, 2, 1, 2, 3, 1, 2, 2, 1, 3, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 3, 3, 1, 2, 1, 2, 2, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 1, 2, 1, 3, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2, 1, 1, 4, 1, 1, 1, 1, 2, 2, 1, 1, 2, 3, 3, 1, 2, 2, 2, 2, 1, 2, 3, 3, 3, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 5, 1, 1, 2, 2, 1, 1, 1, 1, 3, 1, 2, 2, 2, 1, 2, 1, 1, 2, 1, 2, 1, 3, 1, 2, 1, 1, 2, 1, 3, 1, 2, 1, 1, 1, 1, 2, 3, 2, 2, 3, 1, 4, 2, 1, 1, 3, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 2, 1, 2, 1, 2, 1, 4, 1, 2, 2, 1, 1, 1, 1, 4, 1, 2, 1, 3, 2, 1, 1, 3, 2, 2, 1, 1, 1, 1, 2, 1, 3, 1, 2, 1, 1, 2, 1, 3, 2, 3, 2, 2, 1, 1, 1, 3, 1, 1, 1, 2, 3, 1, 2, 1, 1, 1, 1, 2, 1, 3, 3, 2, 1, 2, 1, 1, 1, 2, 2, 3, 1, 3, 1, 2, 1, 1, 3, 1, 4, 2, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2, 3, 1, 1, 1, 1, 1, 2, 3, 3, 1, 2, 2, 2, 3, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 3, 2, 1, 1, 1, 1, 1, 2, 1, 4, 1, 2, 1, 3, 4, 1, 3, 1, 1, 2, 2, 2, 2, 3, 3, 1, 1, 3, 2, 3, 1, 2, 1, 1, 2, 2, 3, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1, 3, 1, 1, 3, 1, 3, 1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 3, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 4, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 3, 1, 1, 2, 1, 3, 1, 2, 2, 1, 3, 1, 1, 1, 2, 2, 2, 2, 1, 2, 3, 2, 1, 1, 2, 1, 3, 3, 2, 2, 1, 2, 1, 2, 2, 1, 2, 3, 2, 4, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 3, 1, 1, 1, 2, 2, 1, 2, 3, 2, 3, 1]
klasselokale1000sim_hestesko_maxinfected_20TA = [1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 3, 4, 1, 1, 3, 2, 4, 1, 2, 1, 2, 1, 1, 2, 3, 1, 2, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 4, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 4, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 3, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 4, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 2, 2, 1, 3, 2, 1, 2, 1, 2, 2, 1, 3, 1, 1, 1, 1, 1, 3, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 3, 1, 1, 3, 3, 2, 1, 3, 3, 3, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 3, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 3, 2, 1, 2, 1, 2, 2, 3, 3, 1, 2, 3, 2, 1, 1, 1, 1, 1, 4, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 4, 1, 1, 1, 2, 2, 1, 2, 1, 4, 2, 2, 1, 2, 1, 2, 2, 1, 3, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 3, 1, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 3, 2, 1, 1, 1, 1, 2, 2, 1, 2, 3, 2, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 4, 3, 1, 1, 1, 2, 2, 3, 1, 2, 1, 1, 1, 2, 2, 1, 3, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 3, 2, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 1, 4, 2, 1, 1, 1, 2, 1, 1, 2, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 1, 2, 3, 1, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 2, 3, 2, 1, 1, 2, 2, 2, 3, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 2, 5, 1, 2, 1, 3, 3, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 3, 1, 2, 3, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 3, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 4, 2, 3, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 3, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 4, 3, 1, 3, 1, 1, 3, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 2, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 2, 1, 3, 1, 1, 1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 2, 3, 1, 1, 2, 1, 1, 1, 1, 3, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 3, 4, 2, 2, 3, 2, 2, 1, 1, 1, 1, 2, 4, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2]
print("20 TA mean,row: ",np.mean(klasselokale1000sim_rows_maxinfected_20TA),"std: ",np.std(klasselokale1000sim_rows_maxinfected_20TA))
print("20 TA mean,group: ",np.mean(klasselokale1000sim_grupper_maxinfected_20TA),"std: ",np.std(klasselokale1000sim_grupper_maxinfected_20TA))
print("20 TA mean,hest: ",np.mean(klasselokale1000sim_hestesko_maxinfected_20TA),"std: ",np.std(klasselokale1000sim_hestesko_maxinfected_20TA))


'''
klasselokale1000sim_rows_maxinfected_18TA = [1, 1, 1, 1, 1, 2, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 4, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 4, 2, 1, 1, 2, 2, 1, 1, 1, 2, 3, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 4, 1, 2, 1, 2, 2, 1, 1, 1, 3, 1, 1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 1, 2, 3, 1, 3, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 3, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 2, 3, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 3, 1, 2, 2, 1, 1, 1, 3, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 3, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 2, 3, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 3, 1, 1, 1, 2, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 2, 3, 1, 1, 1, 2, 2, 3, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 3, 2, 1, 1, 2, 1, 1, 3, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 4, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 4, 2, 2, 2, 1, 1, 2, 1, 1, 4, 1, 1, 1, 3, 2, 3, 1, 1, 2, 3, 1, 1, 1, 2, 1, 1, 3, 1, 2, 2, 1, 2, 1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 5, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 3, 2, 1, 2, 4, 1, 2, 3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 4, 1, 1, 1, 1, 1, 2, 2, 5, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 4, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 1, 4, 2, 1, 2, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 3, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 3, 1, 1, 1, 1, 1, 4, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 3, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 3, 1, 3, 1, 2, 1, 1, 1, 1, 2, 3, 1, 1, 2, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 3, 1, 1, 5, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 3, 2, 2, 1, 1, 1, 1, 2, 1, 1, 2, 3, 2, 2, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 3, 1, 1, 1, 2, 1, 2, 3, 1, 1, 1, 1, 2, 2, 1, 3, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 3, 3, 2, 2, 2, 2, 1, 2, 1, 1, 3, 2, 1, 3, 2, 2, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 3, 2, 1, 2, 3, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1, 1]
klasselokale1000sim_grupper_maxinfected_18TA = [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 1, 2, 2, 1, 2, 2, 3, 1, 1, 1, 2, 4, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 3, 3, 2, 2, 1, 1, 1, 1, 1, 2, 3, 2, 1, 1, 3, 1, 4, 3, 1, 2, 3, 5, 1, 2, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 3, 2, 1, 4, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2, 2, 4, 1, 2, 2, 2, 2, 2, 2, 1, 3, 3, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 3, 1, 1, 1, 1, 1, 2, 1, 2, 1, 3, 2, 1, 1, 1, 3, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 3, 1, 1, 1, 1, 4, 2, 2, 1, 2, 3, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 3, 4, 1, 2, 1, 2, 2, 2, 2, 1, 3, 2, 1, 2, 1, 2, 1, 4, 1, 1, 2, 1, 3, 1, 1, 1, 1, 2, 2, 4, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 4, 2, 1, 2, 1, 1, 2, 2, 3, 1, 2, 3, 1, 1, 2, 5, 1, 1, 1, 1, 3, 1, 3, 1, 2, 1, 3, 5, 3, 3, 1, 2, 1, 2, 1, 1, 2, 1, 3, 1, 2, 1, 1, 1, 1, 1, 2, 4, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 3, 2, 1, 1, 2, 3, 3, 2, 1, 1, 2, 2, 2, 3, 1, 3, 2, 2, 1, 1, 1, 2, 1, 1, 3, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 3, 2, 3, 4, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 4, 2, 3, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 3, 2, 1, 2, 1, 1, 2, 3, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 3, 2, 1, 2, 1, 1, 2, 2, 3, 3, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 3, 2, 2, 1, 2, 1, 2, 4, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 4, 3, 1, 1, 1, 2, 3, 2, 4, 1, 1, 2, 1, 3, 2, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 3, 2, 1, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 3, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 2, 1, 2, 1, 1, 3, 2, 2, 3, 2, 1, 1, 1, 2, 2, 3, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 3, 2, 2, 3, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 3, 2, 1, 1, 1, 3, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 3, 1, 1, 2, 3, 2, 2, 3, 2, 1, 3, 2, 2, 3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 3, 1, 1, 1, 2, 2, 1, 1, 1, 1, 3, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 3, 2, 3, 3, 1, 1, 2, 1, 1, 1, 3, 1, 3, 2, 2, 3, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 3, 1, 1, 1, 1, 1, 3, 2, 2, 3, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 3, 1, 2, 2, 2, 1, 1, 3, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 3, 2, 1, 1, 1, 2, 3, 1, 2, 2, 3, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 3, 3, 1, 1, 1, 1, 2, 1, 4, 2, 1, 2, 1, 1, 3, 2, 3, 1, 2, 1, 1, 2, 1, 2, 2, 3, 1, 1, 3, 1, 2, 2, 1, 3, 1, 2, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 1, 3, 3, 2, 2, 1, 2, 2, 2, 2, 1, 1, 1, 3, 2, 2, 1, 1, 3, 1, 1, 1, 3, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 2, 1, 3, 2, 1, 2, 2, 2, 1, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2, 3, 2, 2, 3, 1, 1, 1, 1, 1, 1, 2, 1, 2, 3, 1, 2, 1, 3, 3, 2, 1, 1, 5, 1, 3, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 3, 2, 1, 1, 1, 3, 1, 2, 1, 2, 3, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 3, 2, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 3, 2, 1, 1, 1, 1, 2, 2, 2, 3, 2, 3, 1, 2, 1, 1, 2, 2, 2, 3, 1, 1, 1, 3, 1, 1, 2, 1, 1, 1, 3]
klasselokale1000sim_hestesko_maxinfected_18TA = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 3, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 3, 1, 2, 2, 1, 2, 1, 1, 1, 3, 1, 2, 2, 3, 1, 1, 1, 2, 1, 3, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 3, 1, 1, 2, 1, 1, 1, 1, 2, 1, 3, 3, 2, 1, 3, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 3, 2, 1, 3, 2, 1, 4, 2, 1, 2, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 1, 4, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 3, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 3, 2, 2, 1, 3, 1, 2, 2, 2, 2, 1, 1, 3, 1, 1, 1, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 1, 3, 1, 2, 1, 1, 1, 2, 2, 1, 1, 3, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 3, 1, 3, 1, 1, 1, 1, 1, 1, 2, 3, 3, 1, 1, 1, 1, 2, 1, 2, 1, 1, 3, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 1, 3, 1, 1, 3, 1, 1, 1, 3, 2, 1, 1, 3, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 3, 1, 2, 2, 1, 2, 2, 2, 1, 3, 1, 1, 1, 3, 2, 1, 3, 1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 2, 2, 3, 3, 2, 2, 2, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 3, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 3, 1, 4, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 4, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 3, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 3, 2, 1, 2, 1, 2, 1, 1, 3, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 4, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 2, 3, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 3, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 2, 2, 2, 1, 1, 4, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 1, 1, 2, 3, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 3, 2, 1, 2, 2, 1, 3, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 3, 2, 1, 1, 2, 1, 1, 2, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 3, 2, 1, 2, 2, 1, 1, 2, 1, 3, 2, 2, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 2, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 3, 2, 1, 2, 2, 1, 2, 1, 1, 1, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 3, 1, 2, 3, 1, 1, 2, 2, 2, 1, 2, 1, 1, 2, 1, 3, 2, 1, 1, 2, 1, 1, 1]
print("18 TA mean,row: ",np.mean(klasselokale1000sim_rows_maxinfected_18TA),"std: ",np.std(klasselokale1000sim_rows_maxinfected_18TA))
print("18 TA mean,group: ",np.mean(klasselokale1000sim_grupper_maxinfected_18TA),"std: ",np.std(klasselokale1000sim_grupper_maxinfected_18TA))
print("18 TA mean,hest: ",np.mean(klasselokale1000sim_hestesko_maxinfected_18TA),"std: ",np.std(klasselokale1000sim_hestesko_maxinfected_18TA))




#x_ = [x for x in range(1,1001)]
#plt.plot(x_,klasselokale1000sim_hestesko_maxinfected_24studerende)
#plt.show()

'''


def calc_mean_imax_std_peak_day(data):
    """ Returns which day infection peaks. Use this with raw data """
    df = pd.read_csv(data)
    df.columns =['timestep','infected','Agent_count','recovered','at_home','l','æ','n_sim']
    Imax, peakday,std = [],[], []
    sustilsidst = []
    d_peak = []
    s_=[]
    for i in range(1,51):
        correct_sim = df.loc[df['n_sim'] == i]
        index_max = correct_sim[correct_sim['infected'] == max(correct_sim.infected)].index.values[0]
        Imax.append(correct_sim.loc[index_max]['infected'])
        sustilsidst.append(index_max)
        s_.append(correct_sim.Agent_count[i*(21000)]-correct_sim.infected[i*(21000)]-correct_sim.recovered[i*(21000)])
        std.append(np.std(correct_sim['infected']))
        d_peak.append(correct_sim.loc[index_max]['timestep']/525)
  #      print(correct_sim.loc[index_max]['timestep']/525)
    print("mean+std of d_peak: mean",np.mean(d_peak), "std",np.std(d_peak))
    print("min(Imax);",min(Imax),"max(Imax);",max(Imax))
    print("Mean of std of all imax: ",np.mean(std))
    print("Mean of I_max:",np.mean(Imax),"Mean of peak day:", np.mean(d_peak))
    print("Std of I_max:",np.std(Imax),"Std of peak day:",np.std(d_peak))
    print("Mean sus når t=slut;",np.mean(s_))


basis_all2_plotted = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_2.csv"
basis_all3_plotted = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_3.csv"
basis_all4_plotted = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_4.csv"

basis_all2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/Basis_2.csv"
basis_all3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/Basis_3.csv"
basis_all4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/100_sim/Basis_4.csv"

studerende20_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/20studerende_2.csv"
studerende20_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/20studerende_3.csv"
studerende20_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/20studerende_4.csv"
studerende16_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/16studerende_2.csv"
studerende16_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/16studerende_3.csv"
studerende16_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/16studerende_4.csv"


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
    plt.title('Udvikling i kontakttal i R med mundbind')
    plt.show()
    return x_values, Re_lists, Std_list

def amalie_true_reproduction_numbers_means(data):
    "TO USE WITH RAW DATA"
    df = pd.read_csv(data)
    df.columns = ['timestep', 'infected', 'Agent_count', 'recovered', 'Home','d','f','Iteration']
    plt.figure()
    Re_lists = []
    for j in range(1,51):
        indx_df = df[df['Iteration'] == j].index.to_numpy()  #list of indexes for the j'th iteration [0,1,..,21000], [21001,21002,..]
      #  print(indx_df)
        mean_list_j = []
        for i in range(min(indx_df),max(indx_df)-524,525): #Fra dag 1 til 40
            mean_list_j.append(np.mean([df.infected[x] for x in range(i,i+525)])) #Get the mean of infected on the i'th day in the j'th simulation
        growth = [] #initalisere med 1 som kontakttal
        for i in range(1,len(mean_list_j)): #Compare day 2 with day 1 , plot as day 1 (day 1 er på i=0)
            if mean_list_j[i-1] != 0:
                growth.append((mean_list_j[i]-mean_list_j[i-1])/mean_list_j[i-1])
            else:
                growth.append(0)
        Re_lists.append([3]+[(i*2.7)+1 for i in growth]) #Plug in 3 = R0
    Std_list = np.std(Re_lists, axis=0)
    Re_lists = np.mean(Re_lists, axis=0)
    print(Re_lists,len(Re_lists),len(growth))
    Re_lists = [max(x,0) for x in Re_lists]
    x_values = [x for x in range(0,len(Re_lists))]
    Re_minus_sd= Re_lists-Std_list
    Re_minus_sd=[max(x,0) for x in Re_minus_sd]
    print(next(x[0] for x in enumerate(Re_lists) if x[1] <= 1)) #prints first index for which R_e < 1
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
    plt.title('Udvikling i kontakttal i G med mundbind')
    plt.show()
    return x_values, Re_lists, Std_list

mundbind70_2 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind70_2.csv"
mundbind70_3 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind70_3.csv"
mundbind70_4 = "/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/csvdata/mundbind70_4.csv"
#amalie_true_reproduction_numbers_means(mundbind70_4)

def reproduction_number_correct(S, r0):
    Re_list = []
    x_val = [x for x in range(len(S))]
    first = True
    for n in range(len(S)):
        re = (S[n]/9700)*r0
        if re < 1 and first:
            print("Rt is below 1 for the first time in timestep:",n)
            first = False
        Re_list.append(re)

    #plt.xticks([x*10080 for x in range(0,9)], [x*7 for x in range(0,9)])
   # plt.ylim(0,2)
    plt.axhline(y=1, color='indianred', linestyle='--')
    plt.plot(x_val,Re_list)
    plt.show()
    return x_val,Re_list

def per(N,n):
    return (N/100)*n
def plot_sveiir_days(N_susceptible,N_inf,percent_vaccinated):
    N_total = N_susceptible + N_inf
    beta = 0.00000003*0.8
    beta2 = 0.00000001
    gamma = 1/14400
    eta = 0.7
    psi = 1/4320
    delta = 0.75
    alpha = 0.00007
    D = 7*8            #8 uger
    N_t = math.floor(D*24*60) #Antallet af minutter på 8 uger (40 dage) - 21000

    print(N_t)
    t = np.linspace(0, N_t, N_t+1)
    S = np.zeros(N_t+1)
    V = np.zeros(N_t+1)
    E = np.zeros(N_t+1)
    I = np.zeros(N_t+1)
    Ia = np.zeros(N_t+1)
    Is = np.zeros(N_t+1)
    R = np.zeros(N_t+1)

    percent_vaccinated = percent_vaccinated
    N_susceptibles = N_susceptible


    S[0] = math.ceil(N_susceptibles*(1-percent_vaccinated))
    V[0] = math.floor(N_susceptibles*percent_vaccinated)
    E[0] = 0
    Ia[0] = N_inf*(1-eta)
    Is[0] = N_inf*(eta)
    I[0] = Ia[0] + Is[0]
    R[0] = 0

    print("Så mange s+v",S[0]+V[0])
    index_max = 0
  #  r0 = np.abs(((beta+beta2)*(delta*(-1+eta)-eta))/gamma)*N_total
    r0 =np.abs(N_total*(((delta + beta2 - 1)*eta - delta - beta2)*beta - beta2*eta)/gamma)
    first = True
    imax_when_st_is = S[0]/r0
    #Euler
    for n in range(N_t):
        S[n+1] = S[n] - beta*S[n]*(delta*Ia[n]+Is[n]) - alpha*S[n]
        V[n+1] = V[n] + alpha*S[n] - beta2*V[n]*(delta*Ia[n]+Is[n])
        E[n+1] = E[n] + beta*S[n]*(delta*Ia[n]+Is[n]) - psi*E[n] + beta2*V[n]*(delta*Ia[n]+Is[n])
        Ia[n+1] = Ia[n] + (1-eta)*psi*E[n] - gamma*Ia[n]
        Is[n+1] = Is[n] + eta*psi*E[n] - gamma*Is[n]
        R[n+1] = R[n] + gamma*(Ia[n]+Is[n])
        if (R[n]+V[n])/N_total> (1-(1/r0)) and first:
            print(n)
            first = False
        if imax_when_st_is - 0.5 < S[n+1] < imax_when_st_is + 0.5:
            index_max = n
         #   print("hejh",index_max,S[n+1])

        I[n+1] = Is[n+1]+Ia[n+1]
    print(I[57330])
 #   print(math.floor(S[N_t]+E[N_t]+Ia[N_t]+Is[N_t]+R[N_t]+V[N_t]))
    print("troede jeg",I[index_max],"rigtig Imax",max(I))
    print("st skal være ",S[0]/r0)
    print("R0 SVEIR",(np.abs((beta+beta2)*(delta*(-1+eta)-eta))/gamma)*N_total)
    print("Other r0 SVIER",np.abs((((delta + beta - 1)*eta - delta - beta2)*beta - eta*beta2)*N_total/gamma))
    print("r0::::",np.abs(N_total*(((delta + beta2 - 1)*eta - delta - beta2)*beta - beta2*eta)/gamma))
    fig = plt.figure()
  #  plt.axvline(x=index_max, color='red', linestyle='dashed',linewidth='0.75')
  #  l1, l2, l3, l4, l5 = plt.plot(t, S, t, E, t, Ia, t, Is, t, R)
   # fig.legend((l1, l2, l3, l4, l5), ('S','E','Ia', 'Is', 'R'))
    l1, l2, l5, l6 = plt.plot(t, S, t, E, t, I, t, R)
    l3, l4 = plt.plot(t,Ia,t,Is,linestyle="dashed")

    fig.legend((l1, l2, l3, l4, l5, l6), ('S','E','Ia','Is','I','R'))
    plt.title("SVE$I_{a}$$I_{s}$R model med " '$\Re_{0}= $'+ "2.5 og $S_{0}$ = 99%")
    plt.xlabel('minutter')
    plt.ylim(0,10000)
    plt.show()
#plot_sveiir_days(9700-per(9700,1),per(9700,1),0.45)

def test_seiir_change_N(N_list,first,second,vaccp):
    "N_list should consist of 0<n<1, where n is the percentage of susceptible."
    plt.figure()

    N=9700
    for i in range(len(N_list)):
        beta = 0.00000003*0.8
        beta2 = 0.00000001
        gamma = 1/14400
        eta = 0.7
        psi = 1/4320
        delta = 0.75
        alpha = 0.00007
        D = 7*8            #8 uger
        N_t = math.floor(D*24*60) #Antallet af minutter på 8 uger (40 dage) - 21000

        t = np.linspace(0, N_t, N_t+1)
        S = np.zeros(N_t+1)
        V = np.zeros(N_t+1)
        E = np.zeros(N_t+1)
        I = np.zeros(N_t+1)
        Ia = np.zeros(N_t+1)
        Is = np.zeros(N_t+1)
        R = np.zeros(N_t+1)

        N_susceptibles = N*N_list[i]
        N_inf = N - N_susceptibles

        S[0] = math.ceil(N_susceptibles*(1-vaccp))
        V[0] = math.floor(N_susceptibles*vaccp)
        E[0] = 0
        Ia[0] = N_inf*(1-eta)
        Is[0] = N_inf*(eta)
        I[0] = Ia[0] + Is[0]
        R[0] = 0
        r0 = np.abs(((beta+beta2)*(delta*(-1+eta)-eta))/gamma)*N

        imax_when_st_is = S[0]/r0
        #Euler
        for n in range(N_t):
            S[n+1] = S[n] - beta*S[n]*(delta*Ia[n]+Is[n]) - alpha*S[n]
            V[n+1] = V[n] + alpha*S[n] - beta2*V[n]*(delta*Ia[n]+Is[n])
            E[n+1] = E[n] + beta*S[n]*(delta*Ia[n]+Is[n]) - psi*E[n] + beta2*V[n]*(delta*Ia[n]+Is[n])
            Ia[n+1] = Ia[n] + (1-eta)*psi*E[n] - gamma*Ia[n]
            Is[n+1] = Is[n] + eta*psi*E[n] - gamma*Is[n]
            R[n+1] = R[n] + gamma*(Ia[n]+Is[n])
            if imax_when_st_is - 0.5 < S[n+1] < imax_when_st_is + 0.5:
                index_max = n
             #   print("hejh",index_max,S[n+1])

            #Just for show/plot
            I[n+1] = Is[n+1]+Ia[n+1]
        choice_list = ['t', 'S', 'I']
        true_choice_list = [t,S,I]
        if first in choice_list:
            indx = choice_list.index(first)
            x = true_choice_list[indx]
        else:
            print('choose first value: t,s,i')
        if second in choice_list:
            indx = choice_list.index(second)
            y = true_choice_list[indx]
        else:
            print('choose second value: t,s,i')
        p = str(N_list[i]*100)
        plt.plot(x,y,label="$S_{0}$ = "+p+"%")
        if first != 't':
   #         add_arrow(plt.plot(x,y)[0])
            plt.xlim(0-N/100,N)
            plt.ylim(0-N/100,N)
            plt.xticks([0,1000,2000,3000,4000,5000,6000,7000,8000,9000])
            plt.yticks([0,1000,2000,3000,4000,5000,6000,7000,8000,9000])
            plt.title("Faseplot for S,I ved "r'$\Re_0$ = 3.1')
            plt.legend()
            plt.grid(True)
        else:
            plt.title('Tidsplot')
            plt.ylim(0,N)
    plt.ylabel("Antal infektiøse, "+second)
    plt.xlabel("Antal modtagelige, "+first)
    print(r0)
    plt.show()
#test_seiir_change_N([0.99], 't','I',0.68)


def test_seiir_change_N_differentVACCpercentages(N_list, first, second, vaccp):
    "N_list should consist of 0<n<1, where n is the percentage of susceptible."
    plt.figure()

    N=9700
    for i in range(len(vaccp)):

        beta2 = 0.00000001
        alpha = 0.00007
        beta = 0.00000003*0.8
        gamma = 1/14400
        eta = 0.7
        psi = 1/4320
        delta = 0.75
        D = 7*8            #8 uger
        N_t = math.floor(D*24*60) #Antallet af minutter på 8 uger (40 dage) - 21000

        t = np.linspace(0, N_t, N_t+1)
        S = np.zeros(N_t+1)
        V = np.zeros(N_t+1)
        E = np.zeros(N_t+1)
        I = np.zeros(N_t+1)
        Ia = np.zeros(N_t+1)
        Is = np.zeros(N_t+1)
        R = np.zeros(N_t+1)

        N_susceptibles = N*N_list
        N_inf = N - N_susceptibles

        S[0] = math.ceil(N_susceptibles*(1-vaccp[i]))
        V[0] = math.floor(N_susceptibles*vaccp[i])
        print(S[0],V[0])
        E[0] = 0
        Ia[0] = N_inf*(1-eta)
        Is[0] = N_inf*(eta)
        I[0] = Ia[0] + Is[0]
        R[0] = 0
        r0 = np.abs(((beta+beta2)*(delta*(-1+eta)-eta))/gamma)*N

        imax_when_st_is = S[0]/r0
        #Euler
        for n in range(N_t):
            S[n+1] = S[n] - beta*S[n]*(delta*Ia[n]+Is[n]) - alpha*S[n]
            V[n+1] = V[n] + alpha*S[n] - beta2*V[n]*(delta*Ia[n]+Is[n])
            E[n+1] = E[n] + beta*S[n]*(delta*Ia[n]+Is[n]) - psi*E[n] + beta2*V[n]*(delta*Ia[n]+Is[n])
            Ia[n+1] = Ia[n] + (1-eta)*psi*E[n] - gamma*Ia[n]
            Is[n+1] = Is[n] + eta*psi*E[n] - gamma*Is[n]
            R[n+1] = R[n] + gamma*(Ia[n]+Is[n])
            if imax_when_st_is - 0.5 < S[n+1] < imax_when_st_is + 0.5:
                index_max = n
             #   print("hejh",index_max,S[n+1])

            #Just for show/plot
            I[n+1] = Is[n+1]+Ia[n+1]
        choice_list = ['t', 'S', 'I','R']
        true_choice_list = [t,S,I,R]
        if first in choice_list:
            indx = choice_list.index(first)
            x = true_choice_list[indx]
        else:
            print('choose first value: t,s,i')
        if second in choice_list:
            indx = choice_list.index(second)
            y = true_choice_list[indx]
        else:
            print('choose second value: t,s,i')

        if first != 't':
   #         add_arrow(plt.plot(x,y)[0])
            plt.xlim(0-N/100,N)
            plt.ylim(0-N/100,N)
            plt.xticks([0,1000,2000,3000,4000,5000,6000,7000,8000,9000])
            plt.yticks([0,1000,2000,3000,4000,5000,6000,7000,8000,9000])
            plt.title("Faseplot for S,I ved "r'$\Re_0$ = 3.1')
            plt.legend()
            plt.grid(True)
        else:
            p = str(vaccp[i]*100)
            plt.plot(x,y,label="$Vaccine$ = "+p+"%")
            plt.title('Tidsplot')
            plt.ylim(0,2000)
            plt.legend()

    plt.ylabel("Antal infektiøse, "+second)
    plt.xlabel("Minutter")
    print(r0)
    plt.show()
#test_seiir_change_N_differentVACCpercentages(0.99, 't', 'I', [0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.9])

def test_seiir_change_N_differentALPHApercentages(N_list, first, second, vaccp, alphas):
    "N_list should consist of 0<n<1, where n is the percentage of susceptible."
    plt.figure()
    S_,I_,V_,R_ = [], [], [], []

    N=9700
    for i in range(len(alphas)):
        if i == 0:
            n_ = 61886
            andelH = 1
        elif i == 1:
            n_ = 58577
            andelH = 1
        elif i == 2:
            n_ = 53182
            andelH = 77212
        elif i == 3:
            n_ = 40141
            andelH = 77212
        elif i == 4:
            n_ = 23440
            andelH = 77212#26533

        beta2 = 0.00000001
        alpha = alphas[i]
        beta = 0.00000003*0.8
        gamma = 1/14400
        eta = 0.7
        psi = 1/4320
        delta = 0.75
        D = 7*8            #8 uger
        N_t = math.floor(D*24*60) #Antallet af minutter på 8 uger (40 dage) - 21000

        t = np.linspace(0, N_t, N_t+1)
        S = np.zeros(N_t+1)
        V = np.zeros(N_t+1)
        E = np.zeros(N_t+1)
        I = np.zeros(N_t+1)
        Ia = np.zeros(N_t+1)
        Is = np.zeros(N_t+1)
        R = np.zeros(N_t+1)

        N_susceptibles = N*N_list
        N_inf = N - N_susceptibles

        S[0] = math.ceil(N_susceptibles*(1-vaccp))
        V[0] = math.floor(N_susceptibles*vaccp)
        print(S[0],V[0])
        E[0] = 0
        Ia[0] = N_inf*(1-eta)
        Is[0] = N_inf*(eta)
        I[0] = Ia[0] + Is[0]
        R[0] = 0
        r0 = np.abs(N*(((delta + beta2 - 1)*eta - delta - beta2)*beta - beta2*eta)/gamma)

        imax_when_st_is = S[0]/r0
        #Euler
        for n in range(N_t):
            S[n+1] = S[n] - beta*S[n]*(delta*Ia[n]+Is[n]) - alpha*S[n]
            V[n+1] = V[n] + alpha*S[n] - beta2*V[n]*(delta*Ia[n]+Is[n])
            E[n+1] = E[n] + beta*S[n]*(delta*Ia[n]+Is[n]) - psi*E[n] + beta2*V[n]*(delta*Ia[n]+Is[n])
            Ia[n+1] = Ia[n] + (1-eta)*psi*E[n] - gamma*Ia[n]
            Is[n+1] = Is[n] + eta*psi*E[n] - gamma*Is[n]
            R[n+1] = R[n] + gamma*(Ia[n]+Is[n])
            I[n+1] = Is[n+1]+Ia[n+1]
            if n == n_:
                print("NU ER RT UNDER 1, hvad er infektionstallet?",I[n_])
            if n == 7*24*60:
                print("beskyttet vaccineret efter 7 dage,",V[n])
        S_.append(S)
        I_.append(I)
        V_.append(V)
        R_.append(R)
        print("I max var faktisk:",max(I),"når andelen er under tærskel da er imax",I[andelH])
        choice_list = ['t', 'S', 'I','R','V']
        true_choice_list = [t,S,I,R,V]
        if first in choice_list:
            indx = choice_list.index(first)
            x = true_choice_list[indx]
        else:
            print('choose first value: t,s,i')
        if second in choice_list:
            indx = choice_list.index(second)
            y = true_choice_list[indx]
        else:
            print('choose second value: t,s,i')

        if first != 't':
   #         add_arrow(plt.plot(x,y)[0])
            plt.xlim(0-N/100,N)
            plt.ylim(0-N/100,N)
            plt.xticks([0,1000,2000,3000,4000,5000,6000,7000,8000,9000])
            plt.yticks([0,1000,2000,3000,4000,5000,6000,7000,8000,9000])
            plt.title("Faseplot for S,I ved "r'$\Re_0$ = 3.1')
            plt.legend()
            plt.grid(True)
        else:
            p = str(alphas[i])
            plt.plot(x,y,label="$\sigma$ = "+p+"")
            plt.title('Modtagelige over tid')
            plt.ylim(0,10000)
            plt.legend()

    plt.ylabel("Antal infektiøse, " + second)
    plt.xlabel('Dage')
    plt.ylim(0,10000)
    plt.xticks([x*10080 for x in range(0,9)], [x*7 for x in range(0,9)])

    plt.show()
    return S_,I_,V_,R_,r0,N
#test_seiir_change_N_differentALPHApercentages(0.99, 't', 'I', 0,[0,0.0000035,0.000007,0.000014,0.000028,0.000056])
#[0,0.0000035,0.000007,0.000014,0.000028,0.000056]
#print(test_seiir_change_N_differentALPHApercentages(0.99, 't', 'I', 0,[0,0.0000035,0.000007,0.000014,0.000028,0.000056]))

def reproduction_number_correct_plot_multiple(S_,r0):
    x_val = [x for x in range(len(S_[0]))]
    for i in range(len(S_)):
        Re_list = []
        first = True
        for n in range(len(S_[i])):
            re = (S_[i][n]/9700)*r0
            if re < 1 and first:
                print("Rt is below 1 for the first time in timestep:",n)
                first = False
            Re_list.append(re)
        plt.plot(x_val,Re_list)

    #plt.xticks([x*10080 for x in range(0,9)], [x*7 for x in range(0,9)])
   # plt.ylim(0,2)
    plt.axhline(y=1, color='indianred', linestyle='--')

    plt.show()
    return x_val,Re_list

def flok_immunitet(S,V,R,N,r0):
    x_val = [x for x in range(len(R[0]))]
    for i in range(len(R)):
        Re_list = []
        first = True
        for n in range(len(R[i])):
            v_ = V[i][n]
            r_ = R[i][n]
            andelH = (r_+v_)/N
            if andelH >= (1-1/r0) and first:
                print("Andelen er >= tærskel:",n,i)
                first = False
    return x_val,Re_list

#S,I,V,R,r0,N = test_seiir_change_N_differentALPHApercentages(0.99, 't', 'I', 0,[0,0.000007,0.000014,0.000028,0.000056])
#reproduction_number_correct_plot_multiple(S,r0)
#flok_immunitet(S,V,R,N,r0)

def plot_seiir_basis(N_susceptible,N_infected):
    dt = 0.001
    N_total = N_susceptible + N_infected
    beta = 0.00000003*0.80
    gamma = 1/14400
    eta = 0.7
    rho = gamma/beta
    psi = 1/4320 #2.7 dage
    delta = 0.75
    D = 7*8    #8 uger
    N_t = math.floor(D*24*60*1/dt) #Antallet af minutter på 8 uger (40 dage) - 21000X

    t = np.linspace(0, N_t, N_t+1)
    S = np.zeros(N_t+1)
    E = np.zeros(N_t+1)
    Ia = np.zeros(N_t+1)
    Is = np.zeros(N_t+1)
    I = np.zeros(N_t+1)
    R = np.zeros(N_t+1)

    S[0] = N_susceptible
    E[0] = 0
    Ia[0] = N_infected*(1-eta)
    Is[0] = N_infected*(eta)
    I[0] = Ia[0] + Is[0]
    R[0] = 0
    r0 = np.abs((beta*(delta*(-1+eta)-eta))/gamma)*N_total
    n_for_imax = []
    first_n = 0
    imax_when_st_is = S[0]/r0
    first = True
    now = datetime.now()
    #Euler
    for n in range(N_t):
        if n in [500000,1000000,2000000,3000000,4000000,5000000,6000000]:
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print("date and time =", dt_string)
        S[n+1] = S[n] - dt*beta*S[n]*(delta*Ia[n]+Is[n])
        E[n+1] = E[n] + dt*beta*S[n]*(delta*Ia[n]+Is[n]) - dt*psi*E[n]
        Ia[n+1] = Ia[n] + dt*(1-eta)*psi*E[n] - dt*gamma*Ia[n]
        Is[n+1] = Is[n] + dt*eta*psi*E[n] - dt*gamma*Is[n]
        I[n+1] = Is[n+1]+Ia[n+1]
        R[n+1] = R[n] + dt*gamma*(Ia[n]+Is[n])
        if imax_when_st_is-0.01 < S[n] < imax_when_st_is+0.01:
            n_for_imax.append(n)
            if first:
                first_n = n
                first = False
    print(first_n)
    print(n_for_imax)
    print(S[n_for_imax[0]])
    df = pd.DataFrame({'S': S, 'E': E, 'Ia': Ia, 'Is': Is, 'I': I, 'R': R})
 #   df.to_csv("csvdata/SEIIR_inddelinger_00001_.csv")
   # S.to_csv('csvdata/A_S.csv')
    fig = plt.figure()

    print("r0 SEIR",r0)
    print("teoretisk indtræffer imax når St=",S[0]/r0)
    print("imax er rent faktisk", max(I),"Ved index:",np.argmax(I))
    print("Ved index",np.argmax(I),"er S faktisk",S[np.argmax(I)])
    l1, l2, l3, l4 = plt.plot(t, S, t, E, t, I, t, R)
    l5, l6 = plt.plot(t,Ia,t,Is,linestyle="dashed")
    fig.legend((l1, l2,l5, l6,l3,l4), ('S','E','Ia', 'Is','I','R'),'center right')
    plt.title("SE$I_{a}$$I_{s}$R model med " '$\Re_{0}= $'+ "2.5 og $S_{0}$ = 99%")
    plt.xlabel('Dage')
    plt.ylim(0,10000)
    plt.xticks([x*10080 for x in range(0,9)], [x*7 for x in range(0,9)])
    plt.ylabel("Antal mennesker")
    print(N_t,"I max", max(I), "I mean", np.mean(I), "I std", np.std(I), "sslut",S[N_t], "islut", I[N_t],"Rslut",R[N_t])
    print("I total efter sim", (I[N_t]+E[N_t]+R[N_t])/N_total)

    plt.show()
    return S,I,R

################WORKING MODELS FOR N=9700#######################
def per(N,n):
    return (N/100)*n
plot_seiir_basis(9700-per(9700,1),per(9700,1))

