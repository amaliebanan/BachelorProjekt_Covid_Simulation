from mesa import Agent, Model
from mesa.space import MultiGrid
import numpy as np


class covid_Agent(Agent):
    def __init__(self, id, model):
        super().__init__(id, model)
        self.infected = 0 #0 for False, 1 for True
        self.recovered = 0 #0 for False, 1 for True
        self.infection_period = 9
        self.id = id


    #Go through neighbors and find one to infect.
    def infectNewAgent(self):
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if isinstance(neighbor,covid_Agent):
                if neighbor.recovered == 1:
                    continue
                if neighbor.infected == 0:
                    neighbor.infected = 1
                    return

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos,moore=True,include_center=False)
        possible_empty_steps = []
        for position in possible_steps:
            if self.model.grid.is_cell_empty(position):
                possible_empty_steps.append(position)
        next_move = self.random.choice(possible_empty_steps)
        self.model.grid.move_agent(self, next_move)
    #from wolf_sheep RandomWalker


    #The step method is the action the agent takes when it is activated by the model schedule.
    def step(self):
        self.move()

        #Infect another agent random
        if self.infected == 0:
            return

        #Generate random int and infect a new agent if int = 1.
        #
        randomInt = np.random.poisson(1/5)
        if randomInt == 1:
            self.infectNewAgent()

        #Subtract 1 from infection period. Reset infection period if == 0 and make agent not infected anymore
        # (not yet immun)
        self.infection_period -= 1
        if self.infection_period == 0:
            self.infected = 0
            if np.random.poisson(1/100) == 0:
                self.recovered = 1
            else:
                self.infection_period = 9
        else: self.infected = 1



