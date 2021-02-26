import AgentClass as ac
from Model import covid_Model, find_status
import numpy as np
from mesa.batchrunner import BatchRunner
import matplotlib.pyplot as plt

 ###collect data #####
model = covid_Model(25,10,9,3)
for i in range(500):
    model.step()
test = model.datacollector.get_model_vars_dataframe()
#test.plot()

#plt.show()

fixed_params = {"width": 9, "height": 10, "setUpType": 3}
variable_params = {"N": range(2,25,1)}
batch_run = BatchRunner(covid_Model,
variable_parameters=variable_params,
fixed_parameters=fixed_params,
iterations=5,
max_steps=100,
model_reporters={"infected": lambda m: find_status(m,"infected")})
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.N, run_data.infected)
#plt.show()
