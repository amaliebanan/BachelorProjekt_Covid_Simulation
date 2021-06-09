import AgentClass as ac
from Model import covid_Model,is_human, get_home_sick_count,get_infected_count,get_recovered_count, with_mask, family_groups, go_home_in_breaks, percentages_of_vaccinated, number_of_vaccinated
from mesa.batchrunner import BatchRunner
import multiprocessing as mp
import pandas as pd


'''
Module responsible for collecting data for various simulations at the same time.
'''
antal_iterationer = 1
antal_tidsskridt_per_simulation = 525*2


def batch_run(j):
    """
     Helper function.
    The function containing the batchrunner for the full simulations.
    :param j: j is the setup type. eg j=2 => setup type [2,2,2]
    :return: Returns lists of average number of Infected, Susceptible, Recovered for every timestep.
    Saves the raw data from the datacollector into a csv file.
    """
    batch_run = BatchRunner(covid_Model,
                            variable_parameters={"N": range(24,25,1)},
                            fixed_parameters={"width": 26, "height": 38, "setUpType": [j,j,j]},
                            iterations=antal_iterationer,
                            max_steps=antal_tidsskridt_per_simulation,
                            model_reporters={"infected": lambda m: get_infected_count(m)})
    batch_run.run_all() #run batchrunner

    ordered_df = batch_run.get_collector_model()
    data_list = list(ordered_df.values()) #saves batchrunner data in list
    for i in range(len(data_list)):
        data_list[i]['Iteration'] = i+1
    pd.concat(data_list).to_csv('csvdata/rawdata'+str(j)+'.csv')
    num_of_infected = [0]*(antal_tidsskridt_per_simulation+1)
    num_of_susceptible = [0]*(antal_tidsskridt_per_simulation+1)
    num_of_recovered = [0]*(antal_tidsskridt_per_simulation+1)

    for i in range(len(data_list)):
        for j in range(len(data_list[i]["infected"])):
            num_of_infected[j]+=data_list[i]["infected"][j]
            num_of_susceptible[j] += data_list[i]["Agent_count"][j]-(data_list[i]["infected"][j]+data_list[i]["recovered"][j]+number_of_vaccinated) #number of susceptible at each time step
            num_of_recovered[j] += data_list[i]["recovered"][j]
    num_of_infected =[number / antal_iterationer for number in num_of_infected] #avg number of infected
    num_of_susceptible = [number / antal_iterationer for number in num_of_susceptible]
    num_of_recovered = [number / antal_iterationer for number in num_of_recovered]

    return num_of_infected, num_of_susceptible, num_of_recovered


def batch_run_in_pool():
    """
    This function runs the BatchRunner for table setting 2,3 and 4.
    :return None:
    The function saves the data for average number of Infected, Susceptible, Recovered for every timestep in a csv file.
    """
    pool = mp.Pool(mp.cpu_count())
    results=pool.map(batch_run, [2,3,4]) #runs the batch_run function for j={2,3,4}
    pool.close()
    for i in range(len(results)):
        samlet = []
        for j in range(len(results[i])):
            samlet.append(results[i][j])
        df = pd.DataFrame(samlet)
        dff = df.T
        dff.to_csv('csvdata/plotted_data_'+str(i+2)+'.csv')


def batch_run_classroom(j):
    """
    Helper function.
    The function containing the batchrunner for the classroom simulations.
    :param j: j is the setup type. eg j=2 => setup type [2,2,2]
    :return: Returns lists of average number of infected for every timestep.
    Saves the raw data from the datacollector into a csv file.
    """
    batch_run = BatchRunner(covid_Model,
        variable_parameters={"N": range(24,25,1)},
        fixed_parameters={"width": 11, "height": 11, "setUpType": [j]},
        iterations=antal_iterationer,
        max_steps=antal_tidsskridt_per_simulation)
    batch_run.run_all() #run batchrunner
    ordered_df = batch_run.get_collector_model()
    data_list = list(ordered_df.values()) #saves batchrunner data in list
    for i in range(len(data_list)):
        data_list[i]['Iteration'] = i+1
    pd.concat(data_list).to_csv('csvdata/classroom_test'+str(j)+'.csv')


    num_of_infected = [0]*(antal_tidsskridt_per_simulation+1)
    for i in range(len(data_list)):
        temp_list = []
        for k in range(len(data_list[i]["infected"])):
            num_of_infected[k]+=data_list[i]["infected"][k]
            temp_list.append(data_list[i]["infected"][k])
    num_of_infected = [number / antal_iterationer for number in num_of_infected] #avg number of infected
    return num_of_infected


def batch_run_classroom_in_pool():
    """
    This function runs the BatchRunner for table setting 2,3 and 4 for the classroom simulations.
    :return None:
    The function saves the data for average number of Infected, Susceptible, Recovered for every timestep in a csv file.
    """
    pool = mp.Pool(mp.cpu_count()) #opens pools for running parallel programs
    results=pool.map(batch_run, [2,3,4]) #runs the list_of_infected function for j={2,3,4}
    pool.close() #closes the pools

    for i in range(len(results)):
        samlet = []
        for j in range(len(results[i])):
            samlet.append(results[i][j])
        df = pd.DataFrame(samlet)
        dff = df.T
        dff.to_csv('csvdata/plotted_data_test_'+str(i+2)+'.csv')

