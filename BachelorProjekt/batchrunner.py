import AgentClass as ac
from Model import covid_Model,is_human, get_home_sick,get_infected,get_recovered, with_mask, family_groups, go_home_in_breaks, percentages_of_vaccinated
import numpy as np
from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt
import multiprocessing as mp
from multiprocessing import Pool
import pandas as pd
import csv


fixed_params = {"width":26, "height": 38, "setUpType": [2,4,5]}
variable_params = {"N": range(24,25,1)} # 24 students
iterationer = 50
skridt = 525*40



"Below is to plot infected vs timestep and susceptible vs timestep for a single set up type"

def plot_infected(fix_par, var_par, model, iter, steps):
    """
    :param iter: number of iterations to run
    :param steps: number of timesteps
    :return: returns a plot of mean number of infected by timesteps and mean number of susceptible by timesteps
    """
    batch_run = BatchRunner(model,
    variable_parameters=var_par,
    fixed_parameters=fix_par,
    iterations=iter,
    max_steps=steps,
    model_reporters={"infected": lambda m: get_infected(m)}, )
    batch_run.run_all() #run batchrunner

    data_list = list(batch_run.get_collector_model().values()) # saves batchrunner data in a list

    sum_of_infected = [0]*(steps+1) #makes list for y-values
    num_of_susceptible = [0]*(steps+1)



    for i in range(len(data_list)):
        for j in range(len(data_list[i]["infected"])):
            sum_of_infected[j]+=data_list[i]["infected"][j] #at the right index add number of infected
            num_of_susceptible[j] += data_list[i]["Agent_count"][j]-data_list[i]["infected"][j] #number of susceptible at each time step
    sum_of_infected =[number / iter for number in sum_of_infected] #divide list with number of iterations to get avg
   # num_of_susceptible = [number / iter for number in num_of_susceptible]
    time = [i for i in range(0,steps+1)] #makes list of x-values for plotting
    plt.plot(time, sum_of_infected, label= 'Number of Infected', color = 'Green')
  #  plt.plot(time, num_of_susceptible, label= 'Number of Susceptible', color = 'Green', linestyle='dashed')
    plt.xlabel('Tidsskridt')
    plt.ylabel('Gennemsnit antal smittede')
    plt.title('Klasselokaleopstilling %s '%fix_par['setUpType']+ ' ved %s simulationer' %iter)
    plt.legend()
    return


"uncomment below to see a plot of a single setup type. Change setup type by changing fixed_params at line 10"
#plot_infected(fixed_params, variable_params, covid_Model, iterationer, skridt)
#plt.show()


def max_infected(fix_par, var_par, model, iter, steps):
    """
    :param iter: number of iterations
    :param steps: number of timesteps
    :return: returns a list of maximum number of infected pr iteration
    """
    batch_run = BatchRunner(model,
    variable_parameters=var_par,
    fixed_parameters=fix_par,
    iterations=iter,
    max_steps=steps,
    model_reporters={"infected": lambda m: get_infected(m)})
    batch_run.run_all() #run batchrunner

    data_list = list(batch_run.get_collector_model().values()) # saves batchrunner data in a list
    max_number_of_infected = []
    for i in range(len(data_list)):
        temp_list = []
        for j in range(len(data_list[i]["infected"])):
            temp_list.append(data_list[i]["infected"][j]) #appends number of infected
        max_number_of_infected.append(max(temp_list)) #saves max of temp_list
    return max_number_of_infected #this is now a list of max number of infected for each iteration

#print("Gennemsnitligt er antallet af max antal smittede: \t", np.mean(max_infected(fixed_params, variable_params, covid_Model, iterationer, skridt)))




"Below is to compare setup type [2,2,2], [3,3,3], [4,4,4]"
def list_of_infected(j):
    """
    :param j: j is the setup type. eg j=2 => setup type [2,2,2]
    :return: returns a list of y-values for plotting
    """
    batch_run = BatchRunner(covid_Model,
        variable_parameters=variable_params,
        fixed_parameters={"width": 26, "height": 38, "setUpType": [j,j,j]},
        iterations=iterationer,
        max_steps=skridt,
        model_reporters={"infected": lambda m: get_infected(m)})
    batch_run.run_all() #run batchrunner

    ordered_df = batch_run.get_collector_model()
    data_list = list(ordered_df.values()) #saves batchrunner data in list
    for i in range(len(data_list)):
        data_list[i]['Iteration'] = i+1
    pd.concat(data_list).to_csv('csvdata/all_data_Mundbind50_'+str(j)+'.csv')

    #next 5 lines is to determine reproduction number
    #list_reproduction = []
    #for i in range(0, iterationer):
    #    list_reproduction.append(sum(data_list[i]["Reproduction"][skridt]))
    #print(list_reproduction)
    #print(sum(list_reproduction)/iterationer)


    #next 7 lines is to determine max number of infected
    max_number_of_infected = []
    for i in range(len(data_list)):
        temp_list = []
        for k in range(len(data_list[i]["infected"])):
            temp_list.append(data_list[i]["infected"][k]) #appends number of infected
        max_number_of_infected.append(max(temp_list)) #saves max of temp_list
    #print("Gennemsnitligt er antallet af max smittede for setup type %s " %[j,j,j], "er: ", np.mean(max_number_of_infected))
    #rest of code is to get y-values for the plot
    num_of_infected = [0]*(skridt+1) #makes list for y-values for Infected
    num_of_susceptible = [0]*(skridt+1) #makes list for y-values for Susceptible
    num_of_recovered = [0]*(skridt+1) #makes list for y-values for Recovered
    for i in range(len(data_list)):
        for j in range(len(data_list[i]["infected"])):
            num_of_infected[j]+=data_list[i]["infected"][j]
            num_of_susceptible[j] += data_list[i]["Agent_count"][j]-(data_list[i]["infected"][j]+data_list[i]["recovered"][j]) #number of susceptible at each time step
            num_of_recovered[j] += data_list[i]["recovered"][j]
    num_of_infected =[number / iterationer for number in num_of_infected] #avg number of infected
    num_of_susceptible = [number / iterationer for number in num_of_susceptible]
    num_of_recovered = [number / iterationer for number in num_of_recovered]

    return num_of_infected, num_of_susceptible, num_of_recovered

"uncomment below to run list_of_infected function with different set up types. Change line 12 and 13 to change number of iterations and timesteps"
pool = mp.Pool(mp.cpu_count()) #opens pools for running parallel programs
results=pool.map(list_of_infected, [2,3,4]) #runs the list_of_infected function for j={2,3,4}
pool.close() #closes the pools
resultsinfected2 = results[0][0]
resultsinfected3 = results[1][0]
resultsinfected4 = results[2][0]
resultssusceptible2 = results[0][1]
resultssusceptible3 = results[1][1]
resultssusceptible4 = results[2][1]
resultsrecovered2 = results[0][2]
resultsrecovered3 = results[1][2]
resultsrecovered4 = results[2][2]
#print(results[0])

for i in range(len(results)):
    samlet = []
    for j in range(len(results[i])):
        samlet.append(results[i][j])
        if j == 0:
            print("MAX SMITTEDE VED:" ,i+2,max(results[i][j]))
    df = pd.DataFrame(samlet)
    dff = df.T
    dff.to_csv('csvdata/plotted_data_Mundbind50_'+str(i+2)+'.csv')

"Uncomment below for plotting the three plots for comparing"
time = [i for i in range(0,skridt+1)] #makes a list of x-values for plotting
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
Legends = ['Hestesko', 'Rækker', 'Grupper']
plt.figure(0,figsize=(10,6)) #size of the plot-figure
for i in range(1,3,1):
    plt.plot(time, results[i-1][0], label= Legends[i-1], color=colors[i-1]) #makes the three different plots
    plt.plot(time, results[i-1][1], color=colors[i-1], linestyle='dashed')
    plt.plot(time, results[i-1][2], color=colors[i-1], linestyle='dotted')
plt.xlabel('Tidsskridt')
plt.plot([], color='Black', label='Infected')
plt.plot([], color='Black', label='Susceptible', linestyle='dashed')
plt.plot([], color='Black', label='Recovered', linestyle='dotted')
plt.ylabel('Gennemsnit antal smittede')
plt.suptitle('%s simulationer' %iterationer, fontsize=20)
plt.title('Masker=%s' %with_mask + ', Familiegrupper=%s' %family_groups +', Hjemme i pauser= %s' %go_home_in_breaks + ', Procent vaccinerede=%s' %percentages_of_vaccinated,fontsize=10)
plt.tight_layout(rect=[0,0,0.75,1]) #placement of legend
plt.legend(bbox_to_anchor=(1.04, 0.5), loc='upper left') #placement of legend

plt.figure(1,figsize=(10,6)) #size of the plot-figure
for i in range(1,4,1):
    plt.plot(time, results[i-1][0], label= Legends[i-1], color=colors[i-1]) #makes the three different plots
    plt.plot(time, results[i-1][1], color=colors[i-1], linestyle='dashed')
    plt.plot(time, results[i-1][2], color=colors[i-1], linestyle='dotted')
plt.xlabel('Tidsskridt')
plt.plot([], color='Black', label='Infected')
plt.plot([], color='Black', label='Susceptible', linestyle='dashed')
plt.plot([], color='Black', label='Recovered', linestyle='dotted')
plt.ylabel('Gennemsnit antal smittede')
plt.suptitle('%s simulation(er)' %iterationer, fontsize=20)
plt.title('Masker=%s' %with_mask + ', Familiegrupper=%s' %family_groups +', Hjemme i pauser= %s' %go_home_in_breaks + ', Procent vaccinerede=%s' %percentages_of_vaccinated,fontsize=10)
plt.tight_layout(rect=[0,0,0.75,1]) #placement of legend
plt.legend(bbox_to_anchor=(1.04, 0.5), loc='upper left') #placement of legend
plt.show()


'''
def list_of_infected_in_classroom(j):
    batch_run = BatchRunner(covid_Model,
        variable_parameters=variable_params,
        fixed_parameters={"width": 11, "height": 11, "setUpType": [j]},
        iterations=iterationer,
        max_steps=skridt)
    batch_run.run_all() #run batchrunner
    data_list = list(batch_run.get_collector_model().values()) #saves batchrunner data in list

    #next 7 lines is to determine max number of infected
    max_number_of_infected = []
    #rest of code is to get y-values for the plot
    num_of_infected = [0]*(skridt+1) #makes list # for y-values for Infected
    for i in range(len(data_list)):
        temp_list = []
        for k in range(len(data_list[i]["infected"])):
            num_of_infected[k]+=data_list[i]["infected"][k]
            temp_list.append(data_list[i]["infected"][k])
        max_number_of_infected.append(max(temp_list))
    num_of_infected = [number / iterationer for number in num_of_infected] #avg number of infected

    print(j,"Gennemsnitligt er antallet af max smittede for setup type %s " %j, "er: ", np.mean(max_number_of_infected))
    print(j,"Std er antallet af max smittede for setup type %s " %j, "er: ", np.std(max_number_of_infected))

    #max_number_of_infected.append(j)
    print(max_number_of_infected)
    return num_of_infected


"uncomment below to run list_of_infected function with different set up types. Change line 12 and 13 to change number of iterations and timesteps"
pool = mp.Pool(mp.cpu_count()) #opens pools for running parallel programs
results=pool.map(list_of_infected_in_classroom, [2,3,4]) #runs the list_of_infected function for j={2,3,4}
pool.close() #closes the pools
"Uncomment below for plotting three plots without susceptible and recovered. Use this for One Classroom"
time = [i for i in range(0,skridt+1)] #makes a list of x-values for plotting
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
Legends = ['Hestesko', 'Rækker', 'Grupper']
for i in range(1,4):
    plt.plot(time, results[i-1], label= Legends[i-1], color=colors[i-1]) #makes the three different plots
plt.xlabel('Tidsskridt')
plt.ylabel('Gennemsnit antal smittede')
plt.ylim(1,2)
plt.suptitle('%s simulationer af 105 minutters undervisning' %iterationer,fontsize=15)
plt.title("Initialiseret med én studerende smittet, 18 studerende i alt")
plt.tight_layout() #placement of legend
plt.legend() #placement of legend

plt.show()
'''
