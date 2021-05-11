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
import pandas as pd
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


def truncnorm_():
    myclip_a = 3
    myclip_b = 11.5
    my_mean = 5
    my_std = 1

    a, b = (myclip_a - my_mean) / my_std, (myclip_b - my_mean) / my_std
    x_range = np.linspace(1,15,1000)
    plt.axvline(3, 0, 1, color="red")
    plt.axvline(11.5, 0, 1, color="red")
    plt.title("Trunkeret normalfordeling med a = 3, b = 11.5, $\mu$ = 5,$\sigma$ = 1")
    plt.ylabel("Sandsynlighed")
    y = truncnorm.pdf(x_range, a, b, loc = my_mean, scale = my_std)

    xx=math.floor((1000/15)*5)
    print(xx,y[xx])

  #  xpos = y.index(ymax)

    fill_x = np.linspace(3,11.5,1000)
    fill_y = truncnorm.pdf(fill_x, a, b, loc = my_mean, scale = my_std)

    plt.fill_between(fill_x,fill_y,0)
   # plt.plot(xpos,ymax, 'ro')
    plt.show()
    y2 = norm.pdf(x_range, loc = my_mean, scale = my_std)
    #y2max = max(y2)
    #xpos2 = y2.index(y2max)
   # plt.plot(xpos2,y2max, 'ro')
    plt.plot(x_range,y2)
    plt.title("Normalfordeling med $\mu$ = 5,$\sigma$ = 1")
    plt.ylabel("Sandsynlighed")
    #plt.axvline(3, 0, 1, color="red")
   # plt.axvline(11.5, 0, 1, color="red")
    plt.show()

    #mu = 1/2
    #xx = np.linspace(0,3,1000)

#truncnorm_()


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


"Denne kan er basis. Den skal kopieres, hvis du vil lave modifikationer"
def plot_seiir_basis(N_susceptible):
    beta = 0.0000240
    gamma = 1/6037 #11.5 dage syg
    eta = 0.7
    rho = gamma/beta
    psi = 1/1575 #Tre dage

    D = 40                      #8 uger (hverdage)
    N_t = math.floor(D*8.75*60) #Antallet af minutter på 8 uger (40 dage) - 21000

    t = np.linspace(0, N_t, N_t+1)
    S = np.zeros(N_t+1)
    E = np.zeros(N_t+1)
    Ia = np.zeros(N_t+1)
    Is = np.zeros(N_t+1)
    I = np.zeros(N_t+1)
    R = np.zeros(N_t+1)

    S[0] = N_susceptible
    E[0] = 0
    Ia[0] = 0
    Is[0] = 1
    I[0] = Ia[0] + Is[0]
    R[0] = 0

    #Euler
    for n in range(N_t):
        S[n+1] = S[n] - beta*S[n]*(Ia[n]+Is[n])
        E[n+1] = E[n] + beta*S[n]*(Ia[n]+Is[n]) - psi*E[n]
        Ia[n+1] = Ia[n] + (1-eta)*psi*E[n] - gamma*Ia[n]
        Is[n+1] = Is[n] + eta*psi*E[n] - gamma*Is[n]
        I[n+1] = Is[n+1]+Ia[n+1]
        R[n+1] = R[n] + gamma*(Ia[n]+Is[n])
    fig = plt.figure()
  #  l1, l2, l3, l4, l5 = plt.plot(t, S, t, E, t, Ia, t, Is, t, R)
   # fig.legend((l1, l2, l3, l4, l5), ('S','E', 'Ia', 'Is', 'R'))
    l1, l2, l3, l4, l5 = plt.plot(t, S, t, I, t, Ia, t, Is, t, R)
    fig.legend((l1, l2, l3, l4, l5), ('S','I', 'Ia', 'Is', 'R'))
    plt.title("SEIR med asymptomatiske og symptomatiske")
    plt.xlabel('minutter')
    plt.show()
plot_seiir_basis(156)


#http://hplgit.github.io/prog4comp/doc/pub/._p4c-solarized-Python021.html

def plot_sir():
    beta = 0.02
    gamma = 1/(8*24)
    eta = 0.7
    psi = 1/(6*24)


    dt = 1/60        # 1 minut
    D = 56           # 8 uger (med weekend)
    N_t = int(D*24/dt)  #Antallet af minutter på 8 uger - 56x24x60 = 80640 minutter = 1344 timer

    print(N_t)
    t = np.linspace(0, N_t*dt, N_t+1)
    S = np.zeros(N_t+1)
    E = np.zeros(N_t+1)
    I = np.zeros(N_t+1)
    Ia = np.zeros(N_t+1)
    Is = np.zeros(N_t+1)
    R = np.zeros(N_t+1)

    N = 1000
    S[0] = 0.99
    E[0] = 0
    I[0] = 0.01
    Ia[0] = 0
    Is[0] = 1
    R[0] = 0

    #Euler
    for n in range(N_t):
        S[n+1] = S[n] - dt*beta*S[n]*I[n]
        I[n+1] = I[n] + dt*beta*S[n]*I[n] - dt*gamma*I[n]
        R[n+1] = R[n] + dt*gamma*I[n]

    beta1 = 0.02
    gamma1 = 1/49
    print(beta1/gamma1)
    fig = plt.figure()
    l1, l2, l3 = plt.plot(t, S, t, I, t, R)
    fig.legend((l1, l2, l3), ('S','I', 'R'),'center right')
    plt.title("SIR epidemi model")
    plt.xlabel('timer')
    plt.ylabel('Andel af befolkningen')
   # plt.show()
#plot_sir()


def plot_sveiir_days():
    beta = 0.00001
    gamma = 1/(9*24)
    eta = 0.7
    psi = 1/(6*24)
    alpha = 0.00001
    sigma = 0.0000001


    dt = 1       # 1 minut
    D = 56          # 8 uger (med weekend)
    N_t = int(D*24)  #Antallet af minutter på 8 uger - 56x24x60 = 80640 minutter = 1344 timer

    print(N_t)
    t = np.linspace(0, N_t*dt, N_t+1)
    S = np.zeros(N_t+1)
    V = np.zeros(N_t+1)
    E = np.zeros(N_t+1)
    I = np.zeros(N_t+1)
    Ia = np.zeros(N_t+1)
    Is = np.zeros(N_t+1)
    R = np.zeros(N_t+1)

    percent_vaccinated = 0.5
    N_susceptibles = 9699

    S[0] = math.ceil(N_susceptibles*(1-percent_vaccinated))
    V[0] = math.floor(N_susceptibles*percent_vaccinated)
    E[0] = 0
    I[0] = 0
    Ia[0] = 0
    Is[0] = 1
    R[0] = 0

    print(S[0]+V[0]+Is[0])

    #Euler
    for n in range(N_t):
        S[n+1] = S[n] - dt*beta*S[n]*(Ia[n]+Is[n]) - alpha*S[n]
        V[n+1] = V[n] + alpha*S[n]
        E[n+1] = E[n] + dt*beta*S[n]*(Ia[n]+Is[n]) - dt*psi*E[n] + sigma*(Ia[n]+Is[n])*V[n]
        Ia[n+1] = Ia[n] + dt*(1-eta)*psi*E[n] - dt*gamma*Ia[n]
        Is[n+1] = Is[n] + dt*eta*psi*E[n] - dt*gamma*Is[n]
        R[n+1] = R[n] + dt*gamma*(Ia[n]+Is[n]) - sigma*(Ia[n]+Is[n])*V[n]


        #Just for show/plot
        I[n+1] = Is[n+1]+Ia[n+1]
 #   print(math.floor(S[N_t]+E[N_t]+Ia[N_t]+Is[N_t]+R[N_t]+V[N_t]))
    print(max(I))
    fig = plt.figure()
  #  l1, l2, l3, l4, l5 = plt.plot(t, S, t, E, t, Ia, t, Is, t, R)
   # fig.legend((l1, l2, l3, l4, l5), ('S','E','Ia', 'Is', 'R'))
    l1, l2, l3, l4, l5, l6 = plt.plot(t, S, t, E, t, I, t, Ia, t, Is, t, R)
    fig.legend((l1, l2, l3, l4, l5, l6), ('S','E','I','Ia', 'Is', 'R'))
    plt.title("Med vaccinationer ")
    plt.xlabel('timer')
    plt.ylim(0,N_susceptibles)
    plt.show()
#plot_sveiir_days()

def plot_loss_immunity_seiir_days():
    beta = 0.00001
    gamma = 1/(9*24)
    eta = 0.7
    psi = 1/(6*24)
    alpha = 0.00001
    sigma = 0.01


    dt = 1/60        # 1 minut
    D = 56           # 8 uger (med weekend)
    N_t = int(D*24/dt)  #Antallet af minutter på 8 uger - 56x24x60 = 80640 minutter = 1344 timer

    print(N_t)
    t = np.linspace(0, N_t*dt, N_t+1)
    S = np.zeros(N_t+1)
    V = np.zeros(N_t+1)
    E = np.zeros(N_t+1)
    I = np.zeros(N_t+1)
    Ia = np.zeros(N_t+1)
    Is = np.zeros(N_t+1)
    R = np.zeros(N_t+1)

    S[0] = 9700
    V[0] = 0
    E[0] = 0
    I[0] = 0
    Ia[0] = 0
    Is[0] = 1
    R[0] = 0

    #Euler
    for n in range(N_t):
        S[n+1] = S[n] - dt*beta*S[n]*(Ia[n]+Is[n]) + alpha*R[n]
     #   V[n+1] = alpha*S[n]-sigma*beta*S[n]*(Ia[n]+Is[n])
        E[n+1] = E[n] + dt*beta*S[n]*(Ia[n]+Is[n]) - dt*psi*E[n]
        Ia[n+1] = Ia[n] + dt*(1-eta)*psi*E[n] - dt*gamma*Ia[n]
        Is[n+1] = Is[n] + dt*eta*psi*E[n] - dt*gamma*Is[n]
        I[n+1] = Is[n+1]+Ia[n+1]
        R[n+1] = R[n] + dt*gamma*(Ia[n]+Is[n]) - alpha*R[n]
    print((beta/gamma)*S[0])
    fig = plt.figure()
  #  l1, l2, l3, l4, l5 = plt.plot(t, S, t, E, t, Ia, t, Is, t, R)
   # fig.legend((l1, l2, l3, l4, l5), ('S','E','Ia', 'Is', 'R'))
    l1, l2, l3, l4, l5, l6 = plt.plot(t, S, t, E, t, I, t, Ia, t, Is, t, R)
    fig.legend((l1, l2, l3, l4, l5, l6), ('S','E','I','Ia', 'Is', 'R'))
    plt.title("SEIR med asymptomatiske og symptomatiske")
    plt.xlabel('minutter')
    plt.show()
#plot_loss_immunity_seiir_days()

def plot_vaccine_decrease():
    x2 = [90.14,70.3,53.6,44.1,26.2,14.78,4.24]
    x3 = [93.88,73.2,60.5,41.6,29.8,15.3,3.96]
    x4 = [104.78,82.1,67.8,52,38.2,20.7,6.1]

    y = [0,10,20,30,40,50,70]
    plt.plot(y,x2)
    plt.plot(y,x3)
    plt.plot(y,x4)
    plt.show()
#plot_vaccine_decrease()

def parse_datafile_infected(data):
    df = pd.read_csv(data)
    list_of_infected = list(df.iloc[:,1])
    return list_of_infected

#print("PARSE",len(parse_datafile_infected("/Users/amaliepalmund/Documents/Bachelor/1_B/BachelorProjekt/Data_amalie/plotted_data_Basis_4.csv")))
