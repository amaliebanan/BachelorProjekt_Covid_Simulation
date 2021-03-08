import AgentClass as ac
from Model import covid_Model, find_status
import numpy as np
from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt
import multiprocessing as mp
from multiprocessing import Pool


fixed_params = {"width": 20, "height": 33, "setUpType": [2,2,2]}
variable_params = {"N": range(25,26,1)} # 25 students
iterationer = 100
skridt = 520*1



"Below is to plot infected vs timestep for a single set up type"

def plot_infected(fix_par, var_par, model, iter, steps):
    """
    :param iter: number of iterations to run
    :param steps: number of timesteps
    :return: returns a plot of mean number of infected by timesteps
    """
    batch_run = BatchRunner(model,
    variable_parameters=var_par,
    fixed_parameters=fix_par,
    iterations=iter,
    max_steps=steps,
    model_reporters={"infected": lambda m: find_status(m,"infected")})
    batch_run.run_all() #run batchrunner

    data_list = list(batch_run.get_collector_model().values()) # saves batchrunner data in a list

    sum_of_infected = [0]*(steps+1) #makes list for y-values
    for i in range(len(data_list)):
        for j in range(len(data_list[i]["infected"])):
            sum_of_infected[j]+=data_list[i]["infected"][j] #at the right index add number of infected
    sum_of_infected =[number / iter for number in sum_of_infected] #divide list with number of iterations to get avg
    time = [i for i in range(0,steps+1)] #makes list of x-values for plotting
    plt.plot(time, sum_of_infected)
    plt.xlabel('Tidsskridt')
    plt.ylabel('Gennemsnit antal smittede')
    plt.title('Klasselokaleopstilling %s '%fix_par['setUpType']+ ' ved %s simulationer' %iter)
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
    model_reporters={"infected": lambda m: find_status(m,"infected")})
    batch_run.run_all() #run batchrunner

    data_list = list(batch_run.get_collector_model().values()) # saves batchrunner data in a list
    max_number_of_infected = []
    for i in range(len(data_list)):
        temp_list = []
        for j in range(len(data_list[i]["infected"])):
            temp_list.append(data_list[i]["infected"][j]) #appends number of infected
        max_number_of_infected.append(max(temp_list)) #saves max of temp_list
    return max_number_of_infected

"uncomment below to get avg max number of infected. Change setup type by changing fixed_params at line 10"
#print("Gennemsnitligt er antallet af max antal smittede: \t", np.mean(max_infected(fixed_params, variable_params, covid_Model, iterationer, skridt)))


"Below is to compare setup type [2,2,2], [3,3,3], [4,4,4]"
def list_of_infected(j):
    """
    :param j: j is the setup type. eg j=2 => setup type [2,2,2]
    :return: returns a list of y-values for plotting
    """
    batch_run = BatchRunner(covid_Model,
        variable_parameters=variable_params,
        fixed_parameters={"width": 20, "height": 33, "setUpType": [j,j,j]},
        iterations=iterationer,
        max_steps=skridt,
        model_reporters={"infected": lambda m: find_status(m,"infected")})
    batch_run.run_all() #run batchrunner
    data_list = list(batch_run.get_collector_model().values()) #saves batchrunner data in list

    sum_of_infected = [0]*(skridt+1) #makes list for y-values
    for i in range(len(data_list)):
        for j in range(len(data_list[i]["infected"])):
            sum_of_infected[j]+=data_list[i]["infected"][j]
    avg_infected =[number / iterationer for number in sum_of_infected] #avg number of infected
    return avg_infected


"uncomment below to run list_of_infected function with different set up types. Change line 12 and 13 to change number of iterations and timesteps"
pool = mp.Pool(mp.cpu_count()) #opens pools for running parallel programs
results=pool.map(list_of_infected, [2,3,4]) #runs the list_of_infected function for j={2,3,4}
pool.close() #closes the pools

"Uncomment below for plotting the three plots for comparing"
time = [i for i in range(0,skridt+1)] #makes a list of x-values for plotting
for i in range(1,4,1):
    plt.plot(time, results[i-1], label= [i+1,i+1,i+1]) #makes the three different plots
plt.xlabel('Tidsskridt')
plt.ylabel('Gennemsnit antal smittede')
plt.title('%s simulationer' %iterationer)
plt.legend()

plt.show()
