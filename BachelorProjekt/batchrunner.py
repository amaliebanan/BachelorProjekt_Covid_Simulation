import AgentClass as ac
from Model import covid_Model, find_status
import numpy as np
from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt

fixed_params = {"width": 20, "height": 32, "setUpType": [4,4]}
variable_params = {"N": range(25,26,1)} # 25 students


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

    data_list = list(batch_run.get_collector_model().values())

    sum_of_infected = [0]*(steps+1) #makes list for y-values
    for i in range(len(data_list)):
        for j in range(len(data_list[i]["infected"])):
            sum_of_infected[j]+=data_list[i]["infected"][j]
    sum_of_infected =[number / iter for number in sum_of_infected]
    time = [i for i in range(0,steps+1)]
    plt.plot(time, sum_of_infected)
    plt.xlabel('Tidsskridt')
    plt.ylabel('Gennemsnit antal smittede')
    plt.title('Klasselokale med 25 elever')
    return


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

    data_list = list(batch_run.get_collector_model().values())
    max_number_of_infected = []
    for i in range(len(data_list)):
        temp_list = []
        for j in range(len(data_list[i]["infected"])):
            temp_list.append(data_list[i]["infected"][j])
        max_number_of_infected.append(max(temp_list))
    return max_number_of_infected

#print(np.mean(max_infected(fixed_params, variable_params, covid_Model, 50, 120)))

plot_infected(fixed_params, variable_params, covid_Model, 50, 120)
plt.show()

