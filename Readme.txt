#Covid simulation on HCØ Institute, Copenhagen University

A mesa-ABM model of the spread of corona virus on HCØ Institute at Copenhagen University.

It is necessary to have python3 installed to run the project.

1. Download and install an IDÉ (Fx Pycharm, Visual Studio Code, IntelliJ, etc.)
2. From your terminal or your IDÉ clone the project

Needed libraries:

- MESA
- Numpy
- Matplotlib
- math
- scipy
- random


Run the project:
1. Open the project in your IDÉ
2. Run run.py. A local browser will open and you can run the simulation. 
3. Add restriction in top of Model.py file by changing the following: 
  - Close the common area by setting go_home_in_break == True                    (Line 36)
  - Implement family groups in the classroom by setting family_groups == True    (Line 37)
  - Put masks on people when they walk or stand by setting with_mask == True     (Line 38)
        - Change how much masks decrease the probability of infection others by changing the infection_decrease_with_mask_pct-parameter (Line 33)
        
