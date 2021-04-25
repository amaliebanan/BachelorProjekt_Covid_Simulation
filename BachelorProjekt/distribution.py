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

    mu = 1/2
    xx = np.linspace(0,3,1000)
    y3 = poisson.pmf(xx, mu = mu, loc=0)
    plt.plot(xx,y3)



def plot_sir():
    # Time unit: 1 minute
    beta = 0.001
    gamma = 0.015
    dt = 1/60            # 6 min
    D = 40             # Simulate for D days
    N_t = int((D*7)/dt)   # Corresponding no of minutes
    print(N_t)
    t = np.linspace(0, N_t, N_t+1)
    print(len(t))
    S = np.zeros(N_t+1)
    I = np.zeros(N_t+1)
    R = np.zeros(N_t+1)

    # Initial condition
    S[0] = 157
    I[0] = 1
    R[0] = 0

    # Step equations forward in time
    for n in range(N_t):
        S[n+1] = S[n] - dt*beta*S[n]*I[n]
        I[n+1] = I[n] + dt*beta*S[n]*I[n] - dt*gamma*I[n]
        R[n+1] = R[n] + dt*gamma*I[n]

    fig = plt.figure()
    l1, l2, l3 = plt.plot(t, S, t, I, t, R)
    fig.legend((l1, l2, l3), ('S', 'I', 'R'), 'upper left')
    plt.xlabel('minutes')
    plt.show()


def plot_seiir():
    # Time unit: 1 minute
    beta = 0.001
    gamma = 0.015
    eta = 0.7
    psi = 0.1
    dt = 1/60            # 1 minut
    D = 56             # 8 uger (med weekend)
    N_t = D*7*60  #Antallet af minutter på 8 uger - 56 dage

    print(N_t)
    t = np.linspace(0, N_t, N_t+1)
    S = np.zeros(N_t+1)
    E = np.zeros(N_t+1)
    Ia = np.zeros(N_t+1)
    Is = np.zeros(N_t+1)
    R = np.zeros(N_t+1)

    S[0] = 156
    E[0] = 0
    Ia[0] = 0
    Is[0] = 1
    R[0] = 0

    #Euler
    for n in range(N_t):
        S[n+1] = S[n] - dt*beta*S[n]*(Ia[n]+Is[n])
        E[n+1] = E[n] + dt*beta*S[n]*(Ia[n]+Is[n]) - dt*psi*E[n]
        Ia[n+1] = Ia[n] + (1-eta)*psi*E[n]*dt - dt*gamma*Ia[n]
        Is[n+1] = Is[n] + eta*psi*E[n]*dt - dt*gamma*Is[n]
        R[n+1] = R[n] + dt*gamma*(Ia[n]+Is[n])

    fig = plt.figure()
    l1, l2, l3, l4, l5 = plt.plot(t, S, t, E, t, Ia, t, Is, t, R)
    fig.legend((l1, l2, l3, l4, l5), ('S','E', 'Ia', 'Is', 'R'))
    plt.title("SEIR med asymptomatiske og symptomatiske")
    plt.xlabel('minutes')
    plt.show()
plot_seiir()
