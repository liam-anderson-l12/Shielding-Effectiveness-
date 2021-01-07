import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import cmath
import math

root = tkinter.Tk()
root.wm_title("Sheilding Effectiveness")
root.configure(background='#DAF7A6')

f = np.array([1.7**x for x in range(50)])
SE = 0*f

fig = Figure(figsize=(5, 4), dpi=100,facecolor=(.229, .158, .86, 0.4), edgecolor=(0.001, 0.03, 0.2,1))
a = fig.add_subplot(111)
fig.subplots_adjust(left=0.2,bottom=0.2)
a.plot(f,SE,'C0',label='SE')
a.legend(loc='best')
a.set_xlabel('Frequency (Hz)')
a.set_ylabel('Sheilding Effectiveness (Db)')
a.set_xscale('log')
#a.set_title('Sheilding Effectiveness')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1,column=4,columnspan=9,rowspan=20, sticky='se')
canvas.draw()

    ###############    TOOLBAR    ###############
toolbarFrame = tkinter.Frame(master=root,bg='#DAF7A6')
toolbarFrame.grid(row=22,column=4)
toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
def proces():
    permittivity = tkinter.Entry.get(E1)
    permeability = tkinter.Entry.get(E2)
    conductivity = tkinter.Entry.get(E3)
  
    epsilon = float(permittivity)
    mu = float(permeability)
    sigma = float(conductivity)

#######SHIELDING EFFECTIVENESS##############################
    muvac = 4*math.pi*10**-7 ### permeabilitty of vac
    epsilonvac = 8.85418782*10**-12  #### permitivitty of vac
    sigmavac = 0 ### conductivity of vac
    muair = 1.00000037*(muvac) ### permeabilitty of air 
    epsilonair = 8.85418782*10**-12  #### permitivitty of air
    sigmaair = 0 ### conductivity of air
   
    

    i = cmath.sqrt(-1) 
    f = np.array([1.7**x for x in range(50)]) ### frequency of incident wave (Hz)
    omega = 2*np.pi*f ### frequency of incident wave (rad)

    Sthick = tkinter.Entry.get(E4)  #5*10**(-2) #Shield Thickness 
    Sthick = float(Sthick)

    Bair = omega*np.sqrt(muair*epsilonair)

    Gamma = np.sqrt((i*omega*mu*(sigma + i*omega*epsilon)))

 
    Nair = np.sqrt(muair/epsilonair) 

    N = np.sqrt((i*omega*mu)/(sigma + i*omega*epsilon)) 

####Gamma*lamb is large number, this a an exponent is too large for python##### an exponent by squaring method is employed #####


    def R(f):
      return 20*np.log10(abs((Nair+N)**2/(4*Nair*N))) ####Reflection
    R = R(f)
      
    def A(f):
      return 20*np.log10(abs((np.exp(-i*Bair*Sthick))*(np.exp(Gamma*Sthick))))
    A = A(f)

    def M(f):
      return 20*np.log10(abs(1-(np.exp(-2*Sthick*Gamma))*((Nair - N)/(Nair + N))**2)) #### Multiple scattering
    M = M(f)

    SE = R + A + M 
    fig = Figure(figsize=(5, 4), dpi=100,facecolor=(0.001, 0.03, 0.3,0.2), edgecolor=(0.001, 0.03, 0.2,1))
    a = fig.add_subplot(111)
    fig.subplots_adjust(left=0.2,bottom=0.2)
    a.plot(f,SE,'C0',label='SE')
    a.plot(f,R,'C1--',label='Reflection')
    a.plot(f,A,'C2--',label='Absorption')
    a.plot(f,M,'C3--',label='Mutiple reflection')
    a.legend(loc='best')
    a.set_xlabel('Frequency (Hz)')
    a.set_ylabel('Db')
    a.set_xscale('log')
    a.set_title('Sheilding Effectiveness')
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=1,column=4,columnspan=9,rowspan=20, sticky='se')
    canvas.draw()

    ###############    TOOLBAR    ###############
    toolbarFrame = tkinter.Frame(master=root,bg='#DAF7A6')
    toolbarFrame.grid(row=22,column=4)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)

    print(SE)

button = tkinter.Button(master=root, text="QUIT", command=_quit)
button.grid(row=6,column=2)

button = tkinter.Button(master=root, text="PLOT", command=proces)
button.grid(row=5,column=2)

#L1 = tkinter.Label(master=root, text="Material Properties",).grid(row=0,column=1)
L2 = tkinter.Label(master=root, text="Permittivity [F/m]", font=('verdana',11),bg='#DAF7A6').grid(row=1,column=1)
L3 = tkinter.Label(master=root, text="Permeability [H/m]",font=('verdana',11),bg='#DAF7A6').grid(row=1,column=2)
L4 = tkinter.Label(master=root, text="Conductivity [S/m]",font=('verdana',11),bg='#DAF7A6').grid(row=1,column=3)
L5 = tkinter.Label(master=root, text="Thickness [m]",font=('verdana',11),bg='#DAF7A6').grid(row=3,column=2)

E1 = tkinter.Entry(master=root, bd =5)
E1.grid(row=2,column=1)
E2 = tkinter.Entry(master=root, bd =5)
E2.grid(row=2,column=2)
E3 = tkinter.Entry(master=root, bd =5)
E3.grid(row=2,column=3)
E4 = tkinter.Entry(master=root, bd = 5)
E4.grid(row=4,column=2)
#B=Button(top, text ="Submit",command= proces).grid(row=5,column=1)

tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
