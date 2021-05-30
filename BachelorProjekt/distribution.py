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
from scipy.interpolate import interp2d
from control.phaseplot import phase_plot


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

def SIR_BASIS(beta_, gamma_,N_susceptible,N_infected):
    eta = 0.7
    psi = 1/1575 #Tre dage
    delta = 0.75

    s_,i_,r_ = [],[],[]

    D = 5*8                   #8 uger (hverdage)
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
    Is[0] = N_infected
    I[0] = Ia[0] + Is[0]
    R[0] = 0

    for i in range(len(beta_)):
        rho = gamma_[i]/beta_[i]
        r0 = (beta_[i]/gamma_[i])*N_susceptible
        iMax = N_susceptible/r0
        print("Values R0, Imax and S(inf)",r0,iMax,S[N_t-1])
        #Euler
        for n in range(N_t):
            S[n+1] = S[n] - beta_[i]*S[n]*I[n]
            I[n+1] = I[n] + beta_[i]*S[n]*I[n] - gamma_[i]*I[n]
            R[n+1] = R[n] + gamma_[i]*I[n]
            if S[n]-0.1 <= np.floor(iMax) <= S[n+1]+0.1:
                print(n)

        fig = plt.figure()
        l1, l2, l3 = plt.plot(t, S, t, I, t, R)
        fig.legend((l1, l2, l3), ('S','I', 'R'),'center right')
        s_.append(S)
        i_.append(I)
        r_.append(R)

 #   plt.axvline(x=8591, color='red', linestyle='dashed',linewidth='0.75')

    plt.title("SIR epidemi model")
    plt.xlabel('minutter')
    plt.show()
    return s_,i_,r_
#SIR_BASIS([1/800000],[1/10000],9699,1)
def norm(data):
    return (data)/(max(data)-min(data))
def phaseplot():
    S_basis1, I_basis1, R_basis1 = SIR_BASIS([0.000025], [1/6037],156,1)
    S_basis2, I_basis2, R_basis2 = SIR_BASIS([0.000025], [1/6037],150,7)
    S_basis3, I_basis3, R_basis3 = SIR_BASIS([0.000025], [1/6037],143,14)
    S_basis4, I_basis4, R_basis4 = SIR_BASIS([0.000025], [1/6037],135,21)
 #   S_basis2, I_basis2, R_basis2 = SIR_BASIS([1/1000], [1/1000],900,100)
 #   S_basis3, I_basis3, R_basis3 = SIR_BASIS([1/900000], [1/6500],950,50)
 #   S_basis4, I_basis4, R_basis4 = SIR_BASIS([1/70000], [1/6700],500,500)
    sy1 = norm(S_basis1[0])
    ix1 = norm(I_basis1[0])
    sy2 = norm(S_basis2[0])
    ix2 = norm(I_basis2[0])
    sy3 = norm(S_basis3[0])
    ix3 = norm(I_basis3[0])
    sy4 = norm(S_basis4[0])
    ix4 = norm(I_basis4[0])

    plt.plot(ix1*1000, sy1*1000,ix2*1000, sy2*1000,ix3*1000, sy3*1000,ix4*1000, sy4*1000)

    plt.xlabel("I")
    plt.ylabel("S")
    plt.title("Faseplot for I og S")

    plt.show()
#phaseplot()
"Denne kan er basis. Den skal kopieres, hvis du vil lave modifikationer"

def phaseplot_seiir():
    S_basis1, I_basis1, R_basis1 = plot_seiir_basis(120,37)
    S_basis2, I_basis2, R_basis2 = plot_seiir_basis(37,120)
    S_basis3, I_basis3, R_basis3 = plot_seiir_basis(156.5,0.5)
    S_basis4, I_basis4, R_basis4 = plot_seiir_basis(150,7)

    print(S_basis2)
 #   S_basis2, I_basis2, R_basis2 = SIR_BASIS([1/1000], [1/1000],900,100)
 #   S_basis3, I_basis3, R_basis3 = SIR_BASIS([1/900000], [1/6500],950,50)
 #   S_basis4, I_basis4, R_basis4 = SIR_BASIS([1/70000], [1/6700],500,500)
    iy1 = norm(I_basis1)
    sx1 = norm(S_basis1)
    iy2 = norm(I_basis2)
    sx2 = norm(S_basis2)
    iy3 = norm(I_basis3)
    sx3 = norm(S_basis3)
    iy4 = norm(I_basis4)
    sx4 = norm(S_basis4)

    print(sx2)
    plt.plot(sx1,iy1, sx2, iy2, sx3,iy3, sx4,iy4)

    plt.xlabel("S")
    plt.ylabel("I")
    plt.title("Faseplot for I og S")

    plt.show()
#phaseplot_seiir()


#http://hplgit.github.io/prog4comp/doc/pub/._p4c-solarized-Python021.html
def plot_sir():
    beta = 0.02
    gamma = 1/(8*24)
    eta = 0.7
    psi = 1/(6*24)


    dt = 1/60        # 1 minut
    D = 40          # 8 uger (med weekend)
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
    S[0] = 999
    E[0] = 0
    I[0] = 1
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
    plt.show()
#plot_sir()

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
def add_arrow(line, position=None, direction='right', size=15, color=None):
    """
    add an arrow to a line.

    line:       Line2D object
    position:   x-position of the arrow. If None, mean of xdata is taken
    direction:  'left' or 'right'
    size:       size of the arrow in fontsize points
    color:      if None, line color is taken.
    """
    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if position is None:
        position = xdata.mean()+xdata.std()
    # find closest index
    start_ind = np.argmin(np.absolute(xdata - position))
    if direction == 'right':
        end_ind = start_ind + 1
    else:
        end_ind = start_ind - 1
    line.axes.annotate('',
        xytext=(xdata[start_ind], ydata[start_ind]),
        xy=(xdata[end_ind], ydata[end_ind]),
        arrowprops=dict(arrowstyle="->", color=color),
        size=size
    )
def reproduction_number1(S,beta,gamma):
    Re_list = []
    x_val = [x for x in range(len(S))]
    for n in range(len(S)):
        Re_list.append(beta*(S[n])/157*gamma)
    #plt.xticks([x*10080 for x in range(0,9)], [x*7 for x in range(0,9)])
   # plt.ylim(0,2)
    plt.plot(x_val,Re_list)
def reproduction_number_correct(S, r0):
    Re_list = []
    x_val = [x for x in range(len(S))]
    first = True
    for n in range(len(S)):
        re = (S[n]/9700)*r0
        if re < 1 and first:
            print("Rt is below 1 for the first time in timestep:",n)
            first = False
        Re_list.append(re)

    #plt.xticks([x*10080 for x in range(0,9)], [x*7 for x in range(0,9)])
   # plt.ylim(0,2)
    plt.axhline(y=1, color='indianred', linestyle='--')
    plt.plot(x_val,Re_list)
    return x_val,Re_list

def plot_seiir_basis(N_susceptible,N_infected):
    N_total = N_susceptible + N_infected
    beta = 0.00000003*0.65
    gamma = 1/14400
    eta = 0.7
    rho = gamma/beta
    psi = 1/4320 #2.7 dage
    delta = 0.75
    dt = 1
    D = 7*8    #8 uger
    N_t = math.floor(D*24*60*dt) #Antallet af minutter på 8 uger (40 dage) - 21000X

    t = np.linspace(0, N_t, N_t+1)
    S = np.zeros(N_t+1)
    E = np.zeros(N_t+1)
    Ia = np.zeros(N_t+1)
    Is = np.zeros(N_t+1)
    I = np.zeros(N_t+1)
    R = np.zeros(N_t+1)

    S[0] = N_susceptible
    E[0] = 0
    Ia[0] = N_infected*(1-eta)
    Is[0] = N_infected*(eta)
    I[0] = Ia[0] + Is[0]
    R[0] = 0
    r0 = np.abs((beta*((-1+eta)*delta-eta))/gamma)*N_total
    first = True
    #Euler
    for n in range(N_t):
        S[n+1] = dt*S[n] - dt*beta*S[n]*(delta*Ia[n]+Is[n])
        E[n+1] = dt*E[n] + dt*beta*S[n]*(delta*Ia[n]+Is[n]) - dt*psi*E[n]
        Ia[n+1] = dt*Ia[n] + dt*(1-eta)*psi*E[n] - dt*gamma*Ia[n]
        Is[n+1] = dt*Is[n] + dt*eta*psi*E[n] - dt*gamma*Is[n]
        I[n+1] = dt*Is[n+1]+Ia[n+1]
        R[n+1] = dt*R[n] + dt*gamma*(Ia[n]+Is[n])

    fig = plt.figure()
   # print(r0,iMax)
   # print("dette er r0 pangdang",(N_susceptible+N_infected)*gamma/beta)
    r0 = np.abs((beta*(delta*(-1+eta)-eta))/gamma)*N_total
    print("r0 SEIR",r0)
    print()

    print("teoretisk indtræffer imax når St=",S[0]/r0)
    print("imax er rent faktisk", max(I),"Ved index:",np.argmax(I))
    print("Ved index",np.argmax(I),"er S faktisk",S[np.argmax(I)])
    print(S[69408],I[69408])
    l1, l2, l3, l4 = plt.plot(t, S, t, E, t, I, t, R)
    l5, l6 = plt.plot(t,Ia,t,Is,linestyle="dashed")
    fig.legend((l1, l2,l5, l6,l3,l4), ('S','E','Ia', 'Is','I','R'),'center right')
    plt.title("SE$I_{a}$$I_{s}$R model med " '$\Re_{0}= $'+ "2.5 og $S_{0}$ = 99%")
    plt.xlabel('Dage')
    plt.ylim(0,10000)
    plt.xticks([x*10080 for x in range(0,9)], [x*7 for x in range(0,9)])
    plt.ylabel("Antal mennesker")
    print(N_t,"I max", max(I), "I mean", np.mean(I), "I std", np.std(I), "sslut",S[N_t], "islut", I[N_t],"Rslut",R[N_t])
    print("I total efter sim", (I[N_t]+E[N_t]+R[N_t])/N_total)

    plt.show()
    return S,I,R



################WORKING MODELS FOR N=9700#######################
def per(N,n):
    return (N/100)*n
plot_seiir_basis(9700-per(9700,1),per(9700,1))
print(9700-per(9700,2),per(9700,2))
def plot_seiir_basis(N_susceptible,N_infected):
    N_total = N_susceptible + N_infected
    beta = 0.00000003*0.65
    gamma = 1/14400
    eta = 0.7
    rho = gamma/beta
    psi = 1/4320 #2.7 dage
    delta = 0.75
    D = 7*8    #8 uger
    N_t = math.floor(D*24*60) #Antallet af minutter på 8 uger (40 dage) - 21000X

    t = np.linspace(0, N_t, N_t+1)
    S = np.zeros(N_t+1)
    E = np.zeros(N_t+1)
    Ia = np.zeros(N_t+1)
    Is = np.zeros(N_t+1)
    I = np.zeros(N_t+1)
    R = np.zeros(N_t+1)

    S[0] = N_susceptible
    E[0] = 0
    Ia[0] = N_infected*(1-eta)
    Is[0] = N_infected*(eta)
    I[0] = Ia[0] + Is[0]
    R[0] = 0
    index_max = 0
    r0 = np.abs((beta*((-1+eta)*delta-eta))/gamma)*N_total
    imax_when_st_is = S[0]/r0
    first = False

    ismax = (gamma*Is)/(eta*psi) #E skal være dette
    iamax = -((-1 + eta)*psi*E)/gamma #Ia skal være dette
    first = True
    #Euler
    for n in range(N_t):
        S[n+1] = S[n] - beta*S[n]*(delta*Ia[n]+Is[n])
        E[n+1] = E[n] + beta*S[n]*(delta*Ia[n]+Is[n]) - psi*E[n]
     #   if gamma*Is[n]/(eta*psi)-0.01 < E[n] <gamma*Is[n]/(eta*psi)+0.01:
           # print("HEJEHEJ",gamma*Is[n]/(eta*psi))
        Ia[n+1] = Ia[n] + (1-eta)*psi*E[n] - gamma*Ia[n]
       # if -((-1 + eta)*psi*E[n])/gamma-0.1 < Ia[n] < -((-1 + eta)*psi*E[n])/gamma+0.1:
      #      print("HEJ", -((-1 + eta)*psi*E[n])/gamma)
        Is[n+1] = Is[n] + eta*psi*E[n] - gamma*Is[n]
        I[n+1] = Is[n+1]+Ia[n+1]
        R[n+1] = R[n] + gamma*(Ia[n]+Is[n])
        if imax_when_st_is - 2 < S[n+1] < imax_when_st_is + 2:
            index_max = n
      #  if n>100 and I[n+1] < I[n] and first:
      #      first = False
      #      print("max er her",n)
  # print(S[index_max],E[index_max], Ia[index_max],Is[index_max],R[index_max])
   # print(max(I),"hejehj")
   # reproduction_number1(S,beta,gamma)
    x_rt, y_rt = reproduction_number_correct(S, r0)
    fig = plt.figure()
   # print(r0,iMax)
   # print("dette er r0 pangdang",(N_susceptible+N_infected)*gamma/beta)
    r0 = np.abs((beta*(delta*(-1+eta)-eta))/gamma)*N_total
    print("r0 SEIR",r0)
    print()

    print("teoretisk indtræffer imax når St=",S[0]/r0)
    print("imax er rent faktisk", max(I),"Ved index:",np.argmax(I))
    print("Ved index",np.argmax(I),"er S faktisk",S[np.argmax(I)])
    print(S[69408],I[69408])
    l1, l2, l3, l4 = plt.plot(t, S, t, E, t, I, t, R)
    l5, l6 = plt.plot(t,Ia,t,Is,linestyle="dashed")
    fig.legend((l1, l2,l5, l6,l3,l4), ('S','E','Ia', 'Is','I','R'),'center right')
    plt.title("SE$I_{a}$$I_{s}$R model med " '$\Re_{0}= $'+ "2.5 og $S_{0}$ = 99%")
    plt.xlabel('Dage')
    plt.ylim(0,10000)
    plt.xticks([x*10080 for x in range(0,9)], [x*7 for x in range(0,9)])
    plt.ylabel("Antal mennesker")
    print(N_t,"I max", max(I), "I mean", np.mean(I), "I std", np.std(I), "sslut",S[N_t], "islut", I[N_t],"Rslut",R[N_t])
    print("I total efter sim", (I[N_t]+E[N_t]+R[N_t])/N_total)

    plt.show()
    return S,I,R
#plot_seiir_basis(9700-per(9700,1),per(9700,1))


def plot_sveiir_days(N_susceptible,N_inf,percent_vaccinated):
    N_total = N_susceptible + N_inf
    beta = 0.00000003*0.8
    beta2 = 0.0000000001
    gamma = 1/14400
    eta = 0.7
    rho = gamma/beta
    psi = 1/4320
    delta = 0.75
    alpha = 0.0000001
    D = 7*8            #8 uger
    N_t = math.floor(D*24*60) #Antallet af minutter på 8 uger (40 dage) - 21000

    print(N_t)
    t = np.linspace(0, N_t, N_t+1)
    S = np.zeros(N_t+1)
    V = np.zeros(N_t+1)
    E = np.zeros(N_t+1)
    I = np.zeros(N_t+1)
    Ia = np.zeros(N_t+1)
    Is = np.zeros(N_t+1)
    R = np.zeros(N_t+1)

    percent_vaccinated = percent_vaccinated
    N_susceptibles = N_susceptible


    S[0] = math.ceil(N_susceptibles*(1-percent_vaccinated))
    V[0] = math.floor(N_susceptibles*percent_vaccinated)
    E[0] = 0
    Ia[0] = N_inf*(1-eta)
    Is[0] = N_inf*(eta)
    I[0] = Ia[0] + Is[0]
    R[0] = 0

    print("Så mange s+v",S[0]+V[0])
    index_max = 0
    r0 = np.abs(((beta+beta2)*(delta*(-1+eta)-eta))/gamma)*N_total

    imax_when_st_is = S[0]/r0
    #Euler
    for n in range(N_t):
        S[n+1] = S[n] - beta*S[n]*(delta*Ia[n]+Is[n]) - alpha*S[n]
        V[n+1] = V[n] + alpha*S[n] - beta2*V[n]*(delta*Ia[n]+Is[n])
        E[n+1] = E[n] + beta*S[n]*(delta*Ia[n]+Is[n]) - psi*E[n] + beta2*V[n]*(delta*Ia[n]+Is[n])
        Ia[n+1] = Ia[n] + (1-eta)*psi*E[n] - gamma*Ia[n]
        Is[n+1] = Is[n] + eta*psi*E[n] - gamma*Is[n]
        R[n+1] = R[n] + gamma*(Ia[n]+Is[n])
        if imax_when_st_is - 0.5 < S[n+1] < imax_when_st_is + 0.5:
            index_max = n
         #   print("hejh",index_max,S[n+1])

        #Just for show/plot
        I[n+1] = Is[n+1]+Ia[n+1]
 #   print(math.floor(S[N_t]+E[N_t]+Ia[N_t]+Is[N_t]+R[N_t]+V[N_t]))
    print("troede jeg",I[index_max],"rigtig Imax",max(I))
    print("st skal være ",S[0]/r0)
    print("R0 SVEIR",(np.abs((beta+beta2)*(delta*(-1+eta)-eta))/gamma)*N_total)
    print("Other r0 SVIER",np.abs((((delta + beta - 1)*eta - delta - beta2)*beta - eta*beta2)*N_total/gamma))
    fig = plt.figure()
  #  plt.axvline(x=index_max, color='red', linestyle='dashed',linewidth='0.75')
  #  l1, l2, l3, l4, l5 = plt.plot(t, S, t, E, t, Ia, t, Is, t, R)
   # fig.legend((l1, l2, l3, l4, l5), ('S','E','Ia', 'Is', 'R'))
    l1, l2, l5, l6 = plt.plot(t, S, t, E, t, I, t, R)
    l3, l4 = plt.plot(t,Ia,t,Is,linestyle="dashed")

    fig.legend((l1, l2, l3, l4, l5, l6), ('S','E','Ia','Is','I','R'))
    plt.title("SVE$I_{a}$$I_{s}$R model med " '$\Re_{0}= $'+ "2.5 og $S_{0}$ = 99%")
    plt.xlabel('minutter')
    plt.ylim(0,10000)
    plt.show()
#plot_sveiir_days(9700-per(9700,10),per(9700,10),0.67)

def test_seiir_change_N(N_list,first,second):
    "N_list should consist of 0<n<1, where n is the percentage of susceptible."
    plt.figure()

    N=9700
    for i in range(len(N_list)):
        beta = 0.00000003*0.8
        gamma = 1/14400
        eta = 0.7
        rho = gamma/beta
        psi = 1/4320 #2.7 dage
        delta = 0.75
        D = 7*16          #8 uger
        N_t = math.floor(D*24*60) #Antallet af minutter på 8 uger (40 dage) - 21000X
        r0 = np.abs((beta*((-1+eta)*delta-eta))/gamma)*N


        t = np.linspace(0, N_t, N_t+1)
        S = np.zeros(N_t+1)
        E = np.zeros(N_t+1)
        Ia = np.zeros(N_t+1)
        Is = np.zeros(N_t+1)
        I = np.zeros(N_t+1)
        R = np.zeros(N_t+1)

        S[0] = np.floor(N*N_list[i])+1
        E[0] = 0
        Ia[0] = 0
        Is[0] = N-S[0]
        I[0] = Ia[0] + Is[0]
        R[0] = 0

        #Euler
        for n in range(N_t):
            S[n+1] = S[n] - beta*S[n]*(Ia[n]*delta+Is[n])
            E[n+1] = E[n] + beta*S[n]*(Ia[n]*delta+Is[n]) - psi*E[n]
            Ia[n+1] = Ia[n] + (1-eta)*psi*E[n] - gamma*Ia[n]
            Is[n+1] = Is[n] + eta*psi*E[n] - gamma*Is[n]
            I[n+1] = Is[n+1]+Ia[n+1]
            R[n+1] = R[n] + gamma*(Ia[n]+Is[n])
        choice_list = ['t', 'S', 'I']
        true_choice_list = [t,S,I]
        if first in choice_list:
            indx = choice_list.index(first)
            x = true_choice_list[indx]
        else:
            print('choose first value: t,s,i')
        if second in choice_list:
            indx = choice_list.index(second)
            y = true_choice_list[indx]
        else:
            print('choose second value: t,s,i')
        p = str(N_list[i]*100)
        plt.plot(x,y,label="$S_{0}$ = "+p+"%")
        if first != 't':
            add_arrow(plt.plot(x,y)[0])
            plt.xlim(0-N/100,N)
            plt.ylim(0-N/100,N)
            plt.xticks([0,1000,2000,3000,4000,5000,6000,7000,8000,9000])
            plt.yticks([0,1000,2000,3000,4000,5000,6000,7000,8000,9000])
            plt.title("Faseplot for S,I ved "r'$\Re_0$ = 2.5')
            plt.legend()
            plt.grid(True)
        else:
            plt.title('Tidsplot')
            plt.ylim(0,N)
    plt.ylabel("Antal infektiøse, "+second)
    plt.xlabel("Antal modtagelige, "+first)
    print(r0)
    plt.show()
#test_seiir_change_N([0.99,0.95,0.90,0.80,0.70,0.60,0.50,0.40], 'S','I')

