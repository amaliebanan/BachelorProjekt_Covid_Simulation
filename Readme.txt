#Covid simulation on HCØ Institute, Copenhagen University

A mesa-ABM model of the spread of corona virus on HCØ Institute at Copenhagen University.

It is necessary to have python3 installed to run the project.

1. Download and install your favorite IDÉ (Fx Pycharm, Visual Studio Code, IntelliJ, etc.)
2. From your terminal or your IDÉ clone the project

Needed libraries:

- MESA
- Numpy
- Matplotlib
- math
- scipy
- random


Run the project:
1. Open the project in your favorite IDÉ
2. If you want to add a restriction, do it in top of Model.py file by changing one or more of the following: 
  - Close the common area by setting go_home_in_break == True                    (Line 40)
  - Implement family groups in the classroom by setting family_groups == True    (Line 41)
  - Put masks on people when they walk or stand by setting with_mask == True     (Line 42)
        - Change how much masks decrease the probability of infection others by changing the infection_decrease_with_mask_pct-parameter (Line 37)
  - Vaccinate parts of the population by changing the percentages_of_vaccinated-parameter to a number between in range [0,1]. (Line 43)      
3. Start the simulation by running run.py. This will open a local browser, where you can run the simulation. 
