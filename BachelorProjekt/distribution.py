#To be main of program
from numpy import random
import math
import matplotlib.pyplot as plt
from scipy.stats import geom
import matplotlib.pyplot as plt
from sympy import symbols, solve,Eq
import seaborn as sns
import numpy as np


#Covid infektionen er geometrisk fordelt. Sandsynligheden for at blive smittet akkumulerer over tid.

#Sandsynligheden for at få succes (= blive smittet) er 0.0025:
pTA = 0.025 #TA står meget tæt og snakker højt
p = 0.0025 #Indenfor 1 meters afstand
p1 = 0.0022450 #Mellem 1 og 2 meters afstand
p2 = 0.002199651 #Over 2 meters afstand


def cdf(n,p):
    x = [i for i in range(1,n)]
    y = [1-(1-p)**n for n in range(1,n)]

    plt.ylabel("Cumulative probability")
    plt.xlabel("Time steps")
    plt.plot(x,y)
   # plt.show()

    return x,y

#Calculate and plot Cumulative Distribution Function for geometrisk fordeling med vores p-værdi
x,y = cdf(120,p)

#x,y = cdf(120,p1)

#x,y = cdf(120,p2)

#https://blogs.sas.com/content/iml/2020/04/08/reducing-spread-of-coronavirus.html
#https://blogs.sas.com/content/iml/2020/04/06/geometric-distribution-sas.html

print("ssh for at blive smittet i løbet af timen",1-(1-p)**120)

#sns.distplot(x, hist=False)

#plt.show()
expected = 1/p  #Expected number of trails until success(infection) happens
std = math.sqrt((1-p)/p**2)


fig, ax = plt.subplots(1, 1)
mean, var, skew, kurt = geom.stats(p, moments='mvsk')

x = np.arange(geom.ppf(0.01, p),geom.ppf(0.99, p))
ax.plot(x, geom.pmf(x, p), 'bo', ms=8, label='geom pmf')
ax.vlines(x, 0, geom.pmf(x, p), colors='b', lw=5, alpha=0.5)
#plt.show()



