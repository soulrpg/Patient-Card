import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk

import math

import numpy as np

import warnings
warnings.filterwarnings("ignore")



window = tk.Tk()
window.title("Rzut Poziomy")
window.iconbitmap( default="clienticon4.ico")
window.geometry('1280x720')


def oblicz(m,r,h,Vx0,ro,Tp,Tsym,opcja):
    Cd = 0.47
    g = 9.80665
    Vx = []
    Vy = []
    y = []
    x = []
    k = (Cd*ro*math.pi*r*r)/(2*m)
    Vx.append(Vx0)
   
    Vy.append(0)
    y.append(h)
    x.append(0)
    B = k/m
    N = int(Tsym/Tp)
    ostatniaIteracja=0
    for n in range(N-1):
        Vx.append(Vx[n] - B*Vx[n]*Tp)
        Vy.append(-Tp * g - B * Vy[n]*Tp + Vy[n])
        if(y[n]+Vy[n]*Tp-(1/2)*g*Tp*Tp+(k/2*m)*Vy[n]*Tp*Tp)>0:
            x.append(x[n]+Vx[n]*Tp-(k/2*m)*Vx[n]*Tp*Tp)
            y.append(y[n]+Vy[n]*Tp-(1/2)*g*Tp*Tp+(k/2*m)*Vy[n]*Tp*Tp)
        else:
            #x.append(x[n]+(x[n]-x[n-1])/2)
            #y.append(0)
            x.append(x[n]+Vx[n]*Tp-(k/2*m)*Vx[n]*Tp*Tp)
            y.append(y[n]+Vy[n]*Tp-(1/2)*g*Tp*Tp+(k/2*m)*Vy[n]*Tp*Tp)
            ostatniaIteracja=n
            break   
    if(ostatniaIteracja==0):
        ostatniaIteracja=N-2
    N= np.arange(0,ostatniaIteracja+2,1)
    X = []
    for i in range(len(N)):
        X.append(i*Tp)
  
   

    if(opcja==3):
        
        f.clear()
        a4 = f.add_subplot(111)
        
        a4.set_title("Tor ruchu obiektu")
        a4.set_xlabel("współrzędna x [m]")
        a4.set_ylabel("współrzędna y [m]")
        a4.grid()
        a4.axis('equal')
        
        a4.plot(x,y,"o-",markersize=1)
        
    else:
        
        f.clear()
        a = f.add_subplot(212)
        a2 = f.add_subplot(221)
        a3 = f.add_subplot(222)
        f.tight_layout(pad=5)
       
        
        

        a.set_title("Zależność wysokości od drogi przebytej w poziomie")
        a.set_xlabel("współrzędna x [m]")
        a.set_ylabel("współrzędna y [m]")
        a.axis('auto')
        a.grid()
        a.plot(x,y,"mo-",markersize=1)

    
        if(opcja==1):
            a2.set_title('Wartośc predkości Vx w funkcji czasu')
            a2.set_xlabel("Czas [s]")
            a2.set_ylabel("Vx [m/s]")
   
            a2.grid()
            a2.plot(X,Vx,"g")

            a3.set_title('Wartośc predkości Vy w funkcji czasu')
            a3.set_xlabel("Czas [s]")
            a3.set_ylabel("Vy [m/s]")
   
            a3.grid()
            a3.plot(X,Vy,"g")
        else:
            a2.set_title('Położenie X w funkcji czasu')
            a2.set_xlabel("Czas [s]")
            a2.set_ylabel("x [m]")
   
            a2.grid()
            a2.plot(X,x)

            a3.set_title('Położenie Y w funkcji czasu')
            a3.set_xlabel("Czas [s]")
            a3.set_ylabel("y [m]")
   
            a3.grid()
            a3.plot(X,y)

    fd = open("wyniki.txt","a+")
    fd.write("Wynik symulacji dla danych:\nMasa: ")
    fd.write(str(m))
    fd.write("\nWysokosc: ")
    fd.write(str(h))
    fd.write("\nPromien: ")
    fd.write(str(r))
    fd.write("\nPredkosc poczatkowa: ")
    fd.write(str(Vx0))
    fd.write("\nGestosc powietrza: ")
    fd.write(str(ro))
    fd.write("\nWspolczynnik \"k\": ")
    fd.write(str(k))
    fd.write("\nMaksymalny czas symulacji: ")
    fd.write(str(Tsym))
    fd.write("\nOkres probkowania: ")
    fd.write(str(Tp))
    fd.write("\nLiczba przebiegow: ")
    fd.write(str(ostatniaIteracja+2))
    fd.write("\nWartosci X:\n")
    for i in range(ostatniaIteracja+2):
        fd.write(str(x[i]))
        fd.write(" ")
    fd.write("\nWartosci Y:\n")
    for i in range(ostatniaIteracja+2):
        fd.write(str(y[i]))
        fd.write(" ")
    fd.write("\nWartosci Vx:\n")
    for i in range(ostatniaIteracja+2):
        fd.write(str(Vx[i]))
        fd.write(" ")
    fd.write("\nWartosci Vy:\n")
    for i in range(ostatniaIteracja+2):
        fd.write(str(Vy[i]))
        fd.write(" ")
  
    fd.write("\n\n")

    fd.close()


def wykres(frame3,m,r,h,Vx0,ro,Tp,Tsym,opcja):
    m2=float(m)
    r2=float(r)
    h2=float(h)
    Vx02=float(Vx0)
    ro2=float(ro)
    Tp2=float(Tp)
    Tsym2=float(Tsym)
    if(m2>0 and r2 >0 and h2 >0 and Vx02>0 and ro2>0 and Tp2>0 and Tsym2>0):
        oblicz(m2,r2,h2,Vx02,ro2,Tp2,Tsym2,opcja)   
        frame3.update()
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


f = Figure(figsize=(12,6), dpi=100)
f.tight_layout(pad=5)


frame3=tk.Frame(window)

canvas = FigureCanvasTkAgg(f, frame3)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
toolbar = NavigationToolbar2Tk(canvas, frame3)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)




frame1=tk.Frame(window)
frame1.pack()

tk.Label(frame1, text="Masa [kg]:").pack(side=tk.LEFT, anchor=tk.W, expand=True)
entry = tk.Entry(frame1)
entry.pack(side=tk.LEFT,anchor=tk.W, expand=True)
        
tk.Label(frame1, text="Promień kuli [m]:").pack(side=tk.LEFT, anchor=tk.W, expand=True)
entry2 = tk.Entry(frame1)
entry2.pack(side=tk.LEFT,anchor=tk.W, expand=True)

tk.Label(frame1, text="Prędkość początkowa [m/s]:").pack(side=tk.LEFT, anchor=tk.W, expand=True)
entry3 = tk.Entry(frame1)
entry3.pack(side=tk.LEFT,anchor=tk.W, expand=True)

tk.Label(frame1, text="Wysokość [m]:").pack(side=tk.LEFT, anchor=tk.W, expand=True)
entry4 = tk.Entry(frame1)
entry4.pack(side=tk.LEFT,anchor=tk.W, expand=True)

tk.Label(frame1, text="Gęstość powietrza [kg/m^3]:").pack(side=tk.LEFT, anchor=tk.W, expand=True)
entry5 = tk.Entry(frame1)
entry5.pack(side=tk.LEFT,anchor=tk.W, expand=True)


frame2=tk.Frame(window)
frame2.pack()

tk.Label(frame2, text="Maksymalny czas symulacji [s]:").pack(side=tk.LEFT, anchor=tk.W, expand=True)
entry6 = tk.Entry(frame2)
entry6.pack(side=tk.LEFT,anchor=tk.W, expand=True)


tk.Label(frame2, text="Okres próbkowania [s]:").pack(side=tk.LEFT, anchor=tk.W, expand=True)
entry7 = tk.Entry(frame2)
entry7.pack(side=tk.LEFT,anchor=tk.W, expand=True)

frame3.pack()


btn = ttk.Button(frame2, text="Wyświetl wykresy Vx(t) Vy(t)",command=lambda: wykres(frame3,entry.get(),entry2.get(),entry4.get(),entry3.get(),entry5.get(),entry7.get(),entry6.get(),1))
btn.pack(padx=18,side=tk.LEFT,anchor=tk.W)

btn = ttk.Button(frame2, text="Wyświetl wykresy x(t) y(t)",command=lambda: wykres(frame3,entry.get(),entry2.get(),entry4.get(),entry3.get(),entry5.get(),entry7.get(),entry6.get(),2))
btn.pack(padx=18,side=tk.LEFT,anchor=tk.W)

btn = ttk.Button(frame2, text="Wyświetl tor ruchu",command=lambda: wykres(frame3,entry.get(),entry2.get(),entry4.get(),entry3.get(),entry5.get(),entry7.get(),entry6.get(),3))
btn.pack(padx=18,side=tk.LEFT,anchor=tk.W)

window.mainloop()

 

 