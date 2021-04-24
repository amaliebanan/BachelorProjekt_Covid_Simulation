#To be main of program
from numpy import random
import math
import matplotlib.pyplot as plt
from scipy.stats import geom
import matplotlib.pyplot as plt
from sympy import symbols, solve,Eq
import seaborn as sns
import numpy as np
from scipy.stats import truncnorm,norm,poisson
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

#Covid infektionen er geometrisk fordelt. Sandsynligheden for at blive smittet akkumulerer over tid.

#Sandsynligheden for at få succes (= blive smittet) er 0.0025:
pTA = 0.025 #TA står meget tæt og snakker højt
p = 0.00035 #Indenfor 1 meters afstand
p1 = 0.0022450 #Mellem 1 og 2 meters afstand
p2 = 0.002199651 #Over 2 meters afstand


def cdf(n,p):
    x = [i for i in range(0,n)]
    y = [1-(1-p)**n for n in range(0,n)]
    y2 = [((1-p)**(n-1))*p for n in range (0,n)]


    plt.ylabel("Sandsynlighed")
    plt.xlabel("# forsøg")
    plt.plot(x,y2,label= 'Sandsynlighed')
    #plt.plot(x,y2)
   # plt.legend()
    plt.xlim(1,n+10)
  #  plt.ylim(0,1)
    plt.title("P(X=k), geometrisk fordeling for p = 0.00035")
  #  plt.show()

    return x,y

#Calculate and plot Cumulative Distribution Function for geometrisk fordeling med vores p-værdi
#x,y = cdf(10000,p)

#x,y = cdf(120,p1)

#x,y = cdf(120,p2)

#https://blogs.sas.com/content/iml/2020/04/08/reducing-spread-of-coronavirus.html
#https://blogs.sas.com/content/iml/2020/04/06/geometric-distribution-sas.html

print("ssh for at blive smittet i løbet af timen",1-(1-p)**105)

#sns.distplot(x, hist=False)

#plt.show()
expected = 1/p  #Expected number of trails until success(infection) happens
std = math.sqrt((1-p)/p**2)


#fig, ax = plt.subplots(1, 1)
#mean, var, skew, kurt = geom.stats(p, moments='mvsk')

#x = np.arange(geom.ppf(0.01, p),geom.ppf(0.99, p))
#ax.plot(x, geom.pmf(x, p), 'bo', ms=8, label='geom pmf')
#ax.vlines(x, 0, geom.pmf(x, p), colors='b', lw=5, alpha=0.5)
#plt.show()


def truncnorm_(a,b,mu,sigma):
        alpha, beta = (a-mu)/sigma, (b-mu)/sigma
        return truncnorm.rvs(alpha,beta,loc=mu,scale=sigma)


myclip_a = 6
myclip_b = 21
my_mean = 10
my_std = 2

a, b = (myclip_a - my_mean) / my_std, (myclip_b - my_mean) / my_std
x_range = np.linspace(5,25,1000)
plt.axvline(6, 0, 1, color="red")
plt.axvline(21, 0, 1, color="red")
plt.title("Trunkeret normalfordeling med mu = 10 og sigma = 2")
plt.ylabel("Sandsynlighed")
y = truncnorm.pdf(x_range, a, b, loc = my_mean, scale = my_std)
plt.plot(x_range,y)
plt.show()
y2 = norm.pdf(x_range, loc = my_mean, scale = my_std)
plt.plot(x_range,y2)
plt.title("Normalfordeling med mu = 10 og sigma = 2")
plt.ylabel("Sandsynlighed")
plt.axvline(6, 0, 1, color="red")
plt.axvline(21, 0, 1, color="red")
plt.show()

mu = 1/2
xx = np.linspace(0,3,1000)
y3 = poisson.pmf(xx, mu = mu, loc=0)
plt.plot(xx,y3)
plt.show()
