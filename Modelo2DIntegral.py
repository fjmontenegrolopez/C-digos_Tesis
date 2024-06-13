# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:34:37 2023

@author: FEDERICO
"""
import numpy as np
import pandas as  pd
#%% TEMPERATURAS 
df = pd.read_excel('Datos22al26Agosto22.xlsx') # DATOS CADA 10 MINUTOS
df.Date = pd.to_datetime(df.Date)
df.index = df.Date
df2 = df[['TtuboMuro','TairEX','TairIN','TaguaIN']]
#%%
maxSample = 1022
Tp = np.array(df2.TtuboMuro)[:maxSample] 
TinN = np.array(df2.TairIN)[:maxSample] 
Tout = np.array(df2.TairEX)[:maxSample] 
Tin = np.array(df2.TairIN)[:maxSample]
#%%
TaguaINFalso = np.where(np.isnan(df['TaguaIN']),df['TtuboMuro'],df['TaguaIN']) 
TaguaOut = np.where(np.isnan(df['TaguaOUT']),df['TtuboMuro'],df['TaguaOUT']) 
#%%
#TaguaIN = TaguaINFalso
TaguaIN = (TaguaINFalso + TaguaOut)/2
#TaguaIN = 0.25*TaguaINFalso + 0.75*TaguaOut 
#TaguaIN = 0.30*TaguaINFalso + 0.70*TaguaOut 
#TaguaIN = 0.35*TaguaINFalso + 0.65*TaguaOut 
#TaguaIN = 0.37*TaguaINFalso + 0.63*TaguaOut
#TaguaIN = 0.4*TaguaINFalso + 0.6*TaguaOut
#TaguaIN = 0.6*TaguaINFalso + 0.4*TaguaOut
#TaguaIN = 0.75*TaguaINFalso + 0.25*TaguaOut 
#TaguaIN = TaguaOut
#%% TEMPERATURAS INTERPOLADAS
from scipy.interpolate import interp1d
sample_times = np.arange(len(Tp))
Tinfunc = interp1d(sample_times, TinN, bounds_error=False, fill_value="extrapolate")
Tpfunc = interp1d(sample_times, Tp, bounds_error=False, fill_value="extrapolate")
ToutfuncTABS = interp1d(sample_times, Tout, bounds_error=False, fill_value="extrapolate") # Sol-Aire
TaguaINfunc = interp1d(sample_times, TaguaIN, bounds_error=False, fill_value="extrapolate")
#%% USA EL 2D
tt = np.linspace(0, sample_times.max(),2052)
Taooo = ToutfuncTABS(tt) # AMB OUT
Tao = Tinfunc(tt) # AMB IN
Tait = TaguaINfunc(tt) # AGUA IN
#%% TEMPERATURAS SOL-AIRE
df3 = pd.read_csv('TempSolAire22al29Agosto.csv',delimiter=',') # DATOS CADA 1 HORA 
#%% TEMPERATURAS SOL-AIRE, SIN INTERPOLACION
# USA 1D
ToutTABS = np.array(df3.SolAireParedNorte)#[:maxSample] # Sol-Aire
ToutParedSur = np.array(df3.SolAireParedSur)#[:maxSample] # Sol-Aire
ToutParedEste = np.array(df3.SolAireParedEste)#[:maxSample] # Sol-Aire
ToutParedOeste = np.array(df3.SolAireParedOeste)#[:maxSample] # Sol-Aire
ToutTecho = np.array(df3.SolAireTecho)#[:maxSample] # Sol-Aire
ToutDoor = np.array(df3.SolAireParedOeste)#[:maxSample] # Sol-Aire
ToutVenta = np.array(df3.SolAireParedEste)#[:maxSample] # Sol-Aire
#%% TEMPERATURAS INTERPOLADAS
# USA 1D
TSUB = Tout.mean() 
# Cree interpoladores lineales para Tsefunc(t) y Tsifunc(t).
sample_times = np.arange(len(Tout))
Toutfunc = interp1d(sample_times, Tout, bounds_error=False, fill_value="extrapolate")
# Tinfunc = interp1d(sample_times, Tin, bounds_error=False, fill_value="extrapolate")
Tpfunc = interp1d(sample_times, Tp, bounds_error=False, fill_value="extrapolate")
#%% USA 1D
sample_times2 = np.arange(len(ToutTABS))
ToutfuncTABS = interp1d(sample_times2, ToutTABS, bounds_error=False, fill_value="extrapolate") # Sol-Aire
ToutfuncParedSur = interp1d(sample_times2, ToutParedSur, bounds_error=False, fill_value="extrapolate") # Sol-Aire
ToutfuncParedEste = interp1d(sample_times2, ToutParedEste, bounds_error=False, fill_value="extrapolate") # Sol-Aire
ToutfuncParedOeste = interp1d(sample_times2, ToutParedOeste, bounds_error=False, fill_value="extrapolate") # Sol-Aire
ToutfuncTecho = interp1d(sample_times2, ToutTecho, bounds_error=False, fill_value="extrapolate") # Sol-Aire
ToutfuncDoor = interp1d(sample_times2, ToutDoor, bounds_error=False, fill_value="extrapolate") # Sol-Aire
ToutfuncVentana = interp1d(sample_times2,ToutVenta, bounds_error=False, fill_value="extrapolate") # Sol-Aire

#%% USA 1D
t = np.linspace(0, sample_times2.max(),171*12)
ToutTABSFin = ToutfuncTABS(t) 
ToutEsteFin = ToutfuncParedEste(t)
ToutOesteFin = ToutfuncParedOeste(t)
ToutTechoFin = ToutfuncTecho(t)
ToutDoorFin = ToutfuncDoor(t)
ToutVentanaFin = ToutfuncVentana(t)
ToutFin = Taooo 
ToutSurFin = ToutfuncParedSur(t)
#%%
hi = 2473.87 
ho = 9.7 # ADENTRO DE LA CASA
hoo = 15 # AFUERA DE LA CASA
dx = 0.005
a = 0.3  # ABSORTANCIA PARA LA RADIACION SOLAR 0 - 1
qq = np.empty_like(tt)
q=np.dot(qq,a)
"""Material I (cemento)"""
km=0.9
ro=2300
cp=890
alpha=km/(ro*cp)
dt=300 # SEGUNDOS
fo=(alpha*dt)/dx**2
Bio=ho*dx/km # DENTRO DE LA CASA
Bii=hi*dx/km
ci1=(1+2*fo*(2+Bii))/fo # NODO SUPERFICIE PLANA CONVECCION
ei1=(3/fo)*(1+4*fo*(1+(1/3)*Bii)) # NODO ESQUINA
co1=(1+2*fo*(2+Bio))/fo # NODO SUPERFICIE PLANA CONVECCION
fco2=np.dot(Tao,2*Bio) # <========== DENTRO DE LA CASA
ei3=(1+4*fo*(1+Bii))/fo # NODO VERTICE 
eo1=(1+4*fo*(1+Bio))/fo # NODO VERTICE
# DENTRO DEL TUBO
fci2=np.dot(Tait,2*Bii) # NODO SUPERFICIE PLANA CONVECCION EN f(t)
fei2=np.dot(Tait,4*Bii) # NODO ESQUINA INTERIOR EN f(t) 
"""Material II (ladrillo o cemento)"""
km2=0.9
ro2=2300
cp2=890
alpha2=km2/(ro2*cp2)
fo2=(alpha2*dt)/dx**2
"""Material III aislante o ladrillo o cemento"""
km33=0.05
ro33=30
cp33=1160
alpha33=km33/(ro33*cp33)
fo33=(alpha33*dt)/dx**2
"""Material IV ladrillo """
km44=0.44
ro44=790
cp44=850
alpha44=km44/(ro44*cp44)
fo44=(alpha44*dt)/dx**2
"""Exterior"""
# MATERIAL I
Bioo1=hoo*dx/km #afuera de la casa
co121=(1+2*fo*(2+Bioo1))/fo
fco221=np.dot(Taooo,2*Bioo1) # <==========AFUERA DE LA CASA
# MATERIAL IV
Bioo4=hoo*dx/km44
co4121=(1+2*fo44*(2+Bioo4))/fo44
fco4221=np.dot(ToutTABSFin,2*Bioo4) # <==========AFUERA DE LA CASA
rad=(2*alpha/fo)*q*(dt/(km*dx))
cte1=(2*alpha)/fo
cte2=dt/(km*dx)
cte=cte1*cte2
frad=np.dot(q,cte) * 0
"""Interface"""
km3=2*km*km2/(km+km2)
alpha3=km3/(ro*cp) # MATERIAL I
alpha4=km3/(ro2*cp2) # MATERIAL II
fo3=(alpha3*dt)/dx**2 # MATERIAL I
fo4=(alpha4*dt)/dx**2 # MATERIAL II
"""Interface para el aislante"""
km4=2*km*km33/(km+km33)
alpha5=km4/(ro*cp) # MATERIAL I
alpha6=km4/(ro33*cp33) # MATERIAL III
fo5=(alpha5*dt)/dx**2 # MATERIAL I
fo6=(alpha6*dt)/dx**2 # MATERIAL III
"""Interface ladrillo cemento lado EXTERIOR"""
kmIn44=2*km*km44/(km+km44)
alphaIn44=kmIn44/(ro*cp) # MATERIAL I
alphaIn444=kmIn44/(ro44*cp44) # MATERIAL IV
foIn44=(alphaIn44*dt)/dx**2 # MATERIAL I
foIn444=(alphaIn444*dt)/dx**2 # MATERIAL IV
#%% DIMENSION DE LA MALLA
R=0.01
# ACA DEBO RESTAR UN NODO POR Nx + 1
# PARA ARMAR LA MATRIZ USO UN NODO DE MAS.
Lct=0.195 # DISTANCIA ENTRE LOS CENTRO DE LOS TUBOS
d1=0.02 # MATERIAL I 
d2=0.04 # MATERIAL I
l1=0.02 # MATERIAL II
l2=0.01 # MATERIAL III
z1=0.01 # MATERIAL I AMBIENTE INTERIOR
z2=0.02 # MATERIAL I
z4=0.12 # MATERIAL IV AMBIENTE EXTERIOR 
# NODOS
Z2=int((z2/dx) + (z4/dx))
L2=int((z2/dx) + (z4/dx) + (l2/dx))
D2=int((d2/dx) + (l2/dx) + (z2/dx) + (z4/dx))
D11=int(D2 + 2*(R/dx))
D1=int(D2 + 2*(R/dx) + d1/dx) 
L1=int(D1 + (l1/dx))
Z1=int((z1/dx) + L1)
Nx=int((z2/dx) + (z4/dx) + (l2/dx) + (d2/dx) + (l1/dx) + (d1/dx) + (z1/dx) + 2*(R/dx) + 1)
Ny=int((Lct/dx) + 1)
n=int(4*(R/dx))
Nxy=Nx*Ny-n
u=np.zeros([Nxy,Nxy])
#%%
import FunMatrizCalculo as Fun
Altura = 2.3 
Ancho = 3
Largo = 2.7
AreaVentana = 1
AreaPuerta = 0.84 * 2
AreaTecho = Ancho * Largo
AreaSuelo = Ancho * Largo
AreaParedNorte = Ancho * Altura 
AreaParedOeste = (Largo * Altura) - AreaPuerta
AreaParedSur = Ancho * Altura
AreaParedEste = (Largo * Altura) - AreaVentana
# ADENTRO
hiS = 6 * AreaParedSur
hiE = 6 * AreaParedEste
hiO = 6 * AreaParedOeste
hiTABS = 9.7 * AreaParedNorte
hiT = 6 * AreaTecho
hiV = 6 * AreaVentana
hSuelo = 6 * AreaSuelo
hiD = 6 * AreaPuerta
# AFUERA
hoS = 15 * AreaParedSur
hoE = 15 * AreaParedEste
hoO = 15 * AreaParedOeste
hoTABS = 15 * AreaParedNorte 
hoT = 15 * AreaTecho 
hoV = 15 * AreaVentana
hoD = 15 * AreaPuerta
# RESISTENCIAS CONVECTIVAS
# PARED SUR 
rhiS = 1/hiS
rhoS = 1/hoS
# PARED ESTE
rhiE = 1/hiE
rhoE = 1/hoE
# PARED OESTE
rhiO = 1/hiO
rhoO = 1/hoO
# PARED NORTE (TABS)
rhiTABS = 1/hiTABS
rhoTABS = 1/hoTABS
# TECHO
rhiT = 1/hiT
rhoT = 1/hoT
# SUELO
rhSuelo = 1/hSuelo
# VENTANA
rhiV = 1/hiV
rhoV = 1/hoV
# PUERTA
rhiD = 1/hiD
rhoD = 1/hoD
# PARED SUR
ladrilloS = Fun.ParametrosConcentrados('ladrillo', 0.44, 850, 790, 0.12,AreaParedSur)
revoqueS = Fun.ParametrosConcentrados('morter', 0.85, 850, 1900, 0.015,AreaParedSur) # REVOQUE DEL LADO INTERIOR PAREDES COMUNES 
# PARED ESTE 
ladrilloE = Fun.ParametrosConcentrados('ladrillo', 0.44, 850, 790, 0.12,AreaParedEste)
revoqueE = Fun.ParametrosConcentrados('morter', 0.85, 850, 1900, 0.015,AreaParedEste) # REVOQUE DEL LADO INTERIOR PAREDES COMUNES 
# PARED OESTE
ladrilloO = Fun.ParametrosConcentrados('ladrillo', 0.44, 850, 790, 0.12,AreaParedOeste)
revoqueO = Fun.ParametrosConcentrados('morter', 0.85, 850, 1900, 0.015,AreaParedOeste) # REVOQUE DEL LADO INTERIOR PAREDES COMUNES 
# NODO AIRE 
aire = Fun.ParametrosConcentrados('aire', 0.025, 1006, 1.23, 3, 2.4*2.3)
# PUERTA
pino = Fun.ParametrosConcentrados('pino', 0.12, 2800,500, 0.05, AreaPuerta)
# SUELO
suelo = Fun.ParametrosConcentrados('piso', 1.2, 840, 1750, 0.15, AreaSuelo)
aislacionSuelo = Fun.ParametrosConcentrados('aislacion', 0.05, 1160, 30, 0.04, AreaSuelo)
# TECHO
aire2 = Fun.ParametrosConcentrados('aireTecho', 0.025, 1006, 1.23, 0.15, AreaTecho)
ChapaGalvanizadaC24 = Fun.ParametrosConcentrados('chapaC24', 60, 450, 7900, 0.0007, AreaTecho)
PoliestilenoExpandido = Fun.ParametrosConcentrados('PoliExpan',0.032, 1420, 30, 0.05,AreaTecho)
# VENTANA
pino2 = Fun.ParametrosConcentrados('vidrio', 1.05, 840,2500, 0.003, AreaVentana)
#%% RESISTENCIAS, CAPACITORES Y FLUJOS DE CALORES
# FLUJOS DE CALOR
qin = 0
qout = 0
areain = 1
areaout = 1
# CASUCHA
# AIRE
CIN = aire.Capacitancia()  
# Pared Este
CEI = CEX = ladrilloE.Capacitancia()/2 + revoqueE.Capacitancia()/2
RE  = ladrilloE.Resistencia() + revoqueE.Resistencia()
# Pared Sur
CSI = CSX = ladrilloS.Capacitancia()/2 + revoqueS.Capacitancia()/2
RS = ladrilloS.Resistencia() + revoqueS.Resistencia()
# Pared Oeste
COI = COX = ladrilloO.Capacitancia()/2 + revoqueO.Capacitancia()/2
RO = ladrilloO.Resistencia() + revoqueO.Resistencia()
# Techo
CTI = CTX = aire2.Capacitancia()/2 + PoliestilenoExpandido.Capacitancia()/2 + ChapaGalvanizadaC24.Capacitancia()/2
RT = aire2.Resistencia() + PoliestilenoExpandido.Resistencia() + ChapaGalvanizadaC24.Resistencia()
# Suelo
CSU = suelo.Capacitancia() + aislacionSuelo.Capacitancia()
RSU = suelo.Resistencia() + aislacionSuelo.Resistencia() 
# Puerta
CD = pino.Capacitancia()
RD = pino.Resistencia()/2
# Ventana
areaVentana = 0
Tramitancia = 0.5
qVentana = areaVentana*Tramitancia
CW = pino2.Capacitancia()
RW = pino2.Resistencia()/2
# Flujo de calor por aire
flujoMasico = 0.0002 #0.000548 #0.00068#rmse% 7.67 #0.0002 #rmse% 6.74
mcprhoAire = flujoMasico*aire.calor_esp

#%% 
# DEFINICION DEL SISTEMAS DE EDO
from scipy.integrate import odeint

def f(state,t,TTABS,ToutFin,ToutSur,ToutEste,ToutOeste,ToutDoor,ToutTecho,ToutVentana,CIN,CSI,CSX,CEI,CEX,COI,COX,CTI,CTX,CSU,CD,CW,rhiTABS,rhiS,rhiE,rhiO,rhiT,rhiD,rhiV,rhoTABS,rhoS,rhoE,rhoO,rhoT,rhoD,rhoV,rhSuelo,RS,RE,RO,RT,RSU,RD,RW,TSUB,qin,qout,areain,areaout,qVentana,mcprhoAire):
    
    TIN,TSI,TSX,TEI,TEX,TOI,TOX,TTI,TTX,TSU,TD,TW = state # LOS T dan el orden de las ecuaciones abajo!!!
    
    return [(1/CIN)*((TTABS-TIN)/rhiTABS + (TSI-TIN)/rhiS + (TEI-TIN)/rhiE + (TOI-TIN)/rhiO + (TTI-TIN)/rhiT + (TSU-TIN)/rhSuelo + (TD-TIN)/(rhiD+RD) + (TW-TIN)/(rhiV+RW) + mcprhoAire*(ToutFin - TIN) + qVentana),
            (1/CSI)*((TIN-TSI)/rhiS + (TSX-TSI)/RS),
            (1/CSX)*((TSI-TSX)/RS + (ToutSur-TSX)/rhoS),
            (1/CEI)*((TIN-TEI)/rhiE + (TEX-TEI)/RE),
            (1/CEX)*((TEI-TEX)/RE + (ToutEste-TEX)/rhoE),
            (1/COI)*((TIN-TOI)/rhiO + (TOX-TOI)/RO),
            (1/COX)*((TOI-TOX)/RO + (ToutOeste-TOX)/rhoO),
            (1/CTI)*((TIN-TTI)/rhiT + (TTX-TTI)/RT),
            (1/CTX)*((TTI-TTX)/RT + (ToutTecho-TTX)/rhoT),
            (1/CSU)*((TIN-TSU)/rhSuelo + (TSUB-TSU)/RSU),
            (1/CD)*((TIN-TD)/(rhiD+RD) + (ToutDoor-TD)/(rhoD+RD)),
            (1/CW)*((TIN-TW)/(rhiV+RW) + (ToutVentana-TW)/(rhoV+RW))]
#%% CREACION DE MATRIZ DE COEFICIENTES
u = Fun.CreacionMatrix(u,dx,Nx,Ny,Z2,fo,fo5,fo6,fo3,fo33,L2,D2,co121,ci1,ei1,ei3,D1,D11,fo4,fo2,L1,Z1,co1,fo44,foIn44,foIn444,z4,co4121)
#%% 
TIN = np.empty_like(t)
TSI = np.empty_like(t)
TSX = np.empty_like(t)
TEI = np.empty_like(t)
TEX = np.empty_like(t)
TOI = np.empty_like(t)
TOX = np.empty_like(t)
TTI = np.empty_like(t)
TTX = np.empty_like(t)
TSU = np.empty_like(t)
TD = np.empty_like(t)
TW = np.empty_like(t)
TIN[0] = 20
TSI[0] = 20
TSX[0] = 20
TEI[0] = 20
TEX[0] = 20
TOI[0] = 20
TOX[0] = 20
TTI[0] = 20
TTX[0] = 20
TSU[0] = 20
TD[0] = 20
TW[0] = 20
#%%
state0 = [20,20,20,20,20,20,20,20,20,20,20,20]
TTABS = 16.654 #22
invu=np.linalg.inv(u)
Nitera = len(Taooo)
tWhile = np.linspace(0, 615300,2052)
k=0
w = 0
Nt=Nxy
c=np.zeros([Nt,1])
T=np.zeros([Nt,1])
sumaTempt=0
ssumaTempt=0
p = 18.5  # #Temperatura de inicio
sumaTemp_ = [p]
for i in range(0,Nt):
    T[i]=p
s=-1

QinSuperficie = []
#QoutSuperficie = []
Temp_sup_tubo_ = []

while k<Nitera:# and itera==0:          
      
      k=k+1          
      s=s+1
      w=w+1
    
      co221=fco4221[s]   # AMBIENTE EXERIOR
      cci2=fci2[s]       # AGUA IN 
      cei2=fei2[s]       # AGUA IN 
      rad=frad[s]        # RADIACION
   
      if k == Nitera:
         w = Nitera-1     
         
      tspan = [tWhile[w-1],tWhile[w]]
      
      states2 = odeint(f, state0, tspan,args=(TTABS,ToutFin[w-1],ToutSurFin[w-1],ToutEsteFin[w-1],ToutOesteFin[w-1],ToutDoorFin[w-1],ToutTechoFin[w-1],ToutVentanaFin[w-1],CIN,CSI,CSX,CEI,CEX,COI,COX,CTI,CTX,CSU,CD,CW,rhiTABS,rhiS,rhiE,rhiO,rhiT,rhiD,rhiV,rhoTABS,rhoS,rhoE,rhoO,rhoT,rhoD,rhoV,rhSuelo,RS,RE,RO,RT,RSU,RD,RW,TSUB,qin,qout,areain,areaout,qVentana,mcprhoAire))

      TIN[w] = states2[1][0]
      TSI[w] = states2[1][1]
      TSX[w] = states2[1][2]
      TEI[w] = states2[1][3]
      TEX[w] = states2[1][4]
      TOI[w] = states2[1][5]
      TOX[w] = states2[1][6]
      TTI[w] = states2[1][7]
      TTX[w] = states2[1][8]
      TSU[w] = states2[1][9]
      TD[w] = states2[1][10]
      TW[w] = states2[1][11]
      
      #=== ACA INTERACTUAN LOS MODELOS ===#
      co2=(states2[1][0])*2*Bio  # AMBIENTE INTERIOR
      #===================================#
      
      state0 = states2[-1][:]
      
      """Nodos internos < int(z4/dx), Material IV"""
      for i in range(0,Nx):
          for j in range(0,Ny):
              if i >0 and i<int(z4/dx) and j>0 and j<Ny-1:
                 c[Ny*i+j]=-T[Ny*i+j]/fo44
              #pared izquierda con aislacion        
              if j==0 and i>0 and i<L2:
                 c[Ny*i+j]=-T[Ny*i+j]/fo44
              #pared derecha con aislacion        
              if j==Ny-1 and i>0 and i<L2:      
                 c[Ny*i+j]=-T[Ny*i+j]/fo44   
              """int(z4/dx) < Nodos internos < Z2, Material I"""
              if i >int(z4/dx) and i<Z2 and j>0 and j<Ny-1:
                 c[Ny*i+j]=-T[Ny*i+j]/fo
              #pared izquierda con aislacion        
              if j==0 and i>int(z4/dx) and i<Z2:
                 c[Ny*i+j]=-T[Ny*i+j]/fo
              #pared derecha con aislacion        
              if j==Ny-1 and i>int(z4/dx) and i<Z2:      
                 c[Ny*i+j]=-T[Ny*i+j]/fo   
              """Nodos inferiores con conveccion exterior, Material IV"""
              if i==0  and j>0 and j<Ny-1: 
                 c[Ny*i+j]=-T[Ny*i+j]/fo44 - co221 - rad
             #nodo inferior izquiedo con conveccion exterior        
              if i==0 and j==0:
                 c[Ny*i+j]=-T[Ny*i+j]/fo44 -co221 - rad
             #nodo inferior derecho con conveccion exterior 
              if i==0 and j==Ny-1:      
                 c[Ny*i+j]=-T[Ny*i+j]/fo44 -co221 - rad
              """Interface Material IV y I, en int(z4/dx) y int(z4/dx)+1"""
      #Material IV
      #pared aislado izq arriba de los caños 
              if i==int(z4/dx) and j==0:
                 c[Ny*i+j]=-T[Ny*i+j]/fo44
      #pared aislado izq arriba de los caños 
              if i==int(z4/dx)and j==Ny-1:
                 c[Ny*i+j]=-T[Ny*i+j]/fo44
      #Nodos internos        
              if i==int(z4/dx) and j>0 and j<Ny-1:
                 c[Ny*i+j]=-T[Ny*i+j]/fo44
      #Material I
      #pared aislado izq arriba de los caños 
              if i==int(z4/dx)+1 and j==0:
                c[Ny*i+j]=-T[Ny*i+j]/fo           
      #pared aislado izq arriba de los caños 
              if i==int(z4/dx)+1 and j==Ny-1:
                c[Ny*i+j]=-T[Ny*i+j]/fo      
      #Nodos internos        
              if i==int(z4/dx)+1 and j>0 and j<Ny-1:
                c[Ny*i+j]=-T[Ny*i+j]/fo               
              """Interface Material III y I, en Z2 y Z2+1"""
      #Material I
      #pared aislado izq arriba de los caños 
              if i==Z2 and j==0:
                 c[Ny*i+j]=-T[Ny*i+j]/fo
      #pared aislado izq arriba de los caños 
              if i==Z2 and j==Ny-1:
                 c[Ny*i+j]=-T[Ny*i+j]/fo
      #Nodos internos        
              if i==Z2 and j>0 and j<Ny-1:
                 c[Ny*i+j]=-T[Ny*i+j]/fo
      #Material III
      #pared aislado izq arriba de los caños 
              if i==Z2+1 and j==0:
                c[Ny*i+j]=-T[Ny*i+j]/fo33           
      #pared aislado izq arriba de los caños 
              if i==Z2+1 and j==Ny-1:
                c[Ny*i+j]=-T[Ny*i+j]/fo33      
      #Nodos internos        
              if i==Z2+1 and j>0 and j<Ny-1:
                c[Ny*i+j]=-T[Ny*i+j]/fo33 
              """Z2 +1 <Nodos internos <L2, Material III"""

              if i >Z2+1 and i < L2 and j >0 and j< Ny-1:
                c[Ny*i+j]=-T[Ny*i+j]/fo33 #diagonal principal
              if j==0 and i>Z2+1 and i<L2:
                c[Ny*i+j]=-T[Ny*i+j]/fo33        
              if j==Ny-1 and i>Z2+1 and i<L2: 
                c[Ny*i+j]=-T[Ny*i+j]/fo33 
              """Interface Material II y I,en L2 y L2+1""" 
      #Material III
              if i==L2 and j>0 and j<Ny-1:
                 c[Ny*i+j]=-T[Ny*i+j]/fo33  
      #pared izquierda con aislacion        
              if i==L2 and j==0:
                 c[Ny*i+j]=-T[Ny*i+j]/fo33
      #pared derecha con aislacion        
              if i==L2 and j==Ny-1: 
                 c[Ny*i+j]=-T[Ny*i+j]/fo33
      #Material I
              if i==L2+1 and j>0 and j<Ny-1:
                 c[Ny*i+j]=-T[Ny*i+j]/fo
      #pared izquierda con aislacion        
              if i==L2+1 and j==0:
                 c[Ny*i+j]=-T[Ny*i+j]/fo
      #pared derecha con aislacion        
              if i==L2+1 and j==Ny-1: 
                 c[Ny*i+j]=-T[Ny*i+j]/fo
              """L2 + 1 < Nodos internos < D2"""
              if i > L2 +1 and i<D2 and j>0 and j<Ny-1: 
                 c[Ny*i+j]=-T[Ny*i+j]/fo
      #pared izquierda con aislacion        
              if j==0 and i> L2 +1 and i<D2:
                 c[Ny*i+j]=-T[Ny*i+j]/fo  
      #pared derecha con aislacion        
              if j==Ny-1 and i> L2 +1 and i<D2: 
                 c[Ny*i+j]=-T[Ny*i+j]/fo             
              """inicio de tubos izquierdo y derecho"""
              if i==D2 and j==0:
                  c[Ny*i+j]=-T[Ny*i+j]/fo - cci2
              if i==D2 and j==1:
                  c[Ny*i+j]=-(3/fo)*T[Ny*i+j] - cei2
              if i==D2 and j==Ny-2:
                  c[Ny*i+j]=-(3/fo)*T[Ny*i+j] - cei2
              if i==D2 and j==Ny-1:            
                  c[Ny*i+j]=-T[Ny*i+j]/fo -cci2
              if i==D2+1 and j==1:
                  c[Ny*i+j-1]=-T[Ny*i+j-1]/fo - cei2
              if i==D2+1 and j==2:
                  c[Ny*i+j-1]=-(3/fo)*T[Ny*i+j-1] - cei2
              if i==D2+1 and j==Ny-3:
                  c[Ny*i+j-1]=-(3/fo)*T[Ny*i+j-1] - cei2
              if i==D2+1 and j==Ny-2:
                  c[Ny*i+j-1]=-T[Ny*i+j-1]/fo - cei2
              if i==D2+2 and j==2:
                  c[Ny*i+j-4]=-T[Ny*i+j-4]/fo - cci2
              if i==D2+2 and j==Ny-3:  
                  c[Ny*i+j-4]=-T[Ny*i+j-4]/fo - cci2
              if i==D2+3 and j==1:
                  c[Ny*i+j-7]=-T[Ny*i+j-7]/fo - cei2
              if i==D2+3 and j==2:
                  c[Ny*i+j-7]=-(3/fo)*T[Ny*i+j-7] - cei2
              if i==D2+3  and j==Ny-3:
                  c[Ny*i+j-7]=-(3/fo)*T[Ny*i+j-7] - cei2
              if i==D2+3 and j==Ny-2:
                  c[Ny*i+j-7]=-T[Ny*i+j-7]/fo - cei2
              if i==D2+4 and j==0:
                  c[Ny*i+j-8]=-T[Ny*i+j-8]/fo - cci2
              if i==D2+4 and j==1:
                  c[Ny*i+j-8]=-(3/fo)*T[Ny*i+j-8] - cei2
              if i==D2+4 and j==Ny-2:
                  c[Ny*i+j-8]=-(3/fo)*T[Ny*i+j-8] - cei2
              if i==D2+4 and j==Ny-1:
                  c[Ny*i+j-8]=-T[Ny*i+j-8]/fo - cci2
              """Nodos interiores entre los tubos"""
              if i==D2 and j>1 and j<Ny-2:  
                  c[Ny*i+j]=-T[Ny*i+j]/fo
              if i==D2+1 and j>2 and j<Ny-3:
                  c[Ny*i+j-1]=-T[Ny*i+j-1]/fo
              if i==D2+2 and j>2 and j<Ny-3:
                  c[Ny*i+j-4]=-T[Ny*i+j-4]/fo
              if i==D2+3 and j>2 and j<Ny-3:
                  c[Ny*i+j-7]=-T[Ny*i+j-7]/fo
              if i==D2+4 and j>1 and j<Ny-2:
                  c[Ny*i+j-8]=-T[Ny*i+j-8]/fo   
              """D11<Nodos internos arriba de los caños ,<D1-1,Material I"""
     #pared aislado izq arriba de los caños 
              if i<D1-1 and i>D11 and j==0:
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
     #pared aislado izq arriba de los caños 
              if i<D1-1 and i>D11 and j==Ny-1:
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
     #Nodos internos        
              if i>D11 and i<D1-1 and j>0 and j<Ny-1:
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo   
              """Interface Material II y I, Superior,D1-1 y D1"""
      #Material I
      #pared aislado izq arriba de los caños 
              if i==D1-1 and j==0:
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
      #pared aislado izq arriba de los caños 
              if i==D1-1 and j==Ny-1:
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
      #Nodos internos        
              if i==D1-1 and j>0 and j<Ny-1:
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
      #Material II     
      #pared aislado izq arriba de los caños 
              if i==D1 and j==0:
                c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2           
      #pared aislado izq arriba de los caños 
              if i==D1 and j==Ny-1:
                c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2      
      #Nodos internos        
              if i==D1 and j>0 and j<Ny-1:
                c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2        
              """Interface Material II y I,en L1-1 y L1"""      
      #Material II
              if i==L1-1 and j>0 and j<Ny-1:
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2  
      #pared izquierda con aislacion        
              if i==L1-1 and j==0:
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2
      #pared derecha con aislacion        
              if i==L1-1 and j==Ny-1: 
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2
      #Material I
              if i==L1 and j>0 and j<Ny-1:
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
      #pared izquierda con aislacion        
              if i==L1 and j==0:
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
      #pared derecha con aislacion        
              if i==L1 and j==Ny-1: 
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
              """L1 < Nodos internos < Z1"""
              if i > L1 and i<Z1 and j>0 and j<Ny-1: 
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
      #pared izquierda con aislacion        
              if j==0 and i> L1 and i<Z1:
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo  
      #pared derecha con aislacion        
              if j==Ny-1 and i> L1 and i<Z1: 
                 c[Ny*i+j-8]=-T[Ny*i+j-8]/fo                             
              """Nodos internos arriba de los caños ,Matarial II,>D1,<L1-1"""
      #pared aislado izq arriba de los caños 
              if i>D1 and i<L1-1 and j==0:
                c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2
      #pared aislado izq arriba de los caños 
              if i>D1 and i<L1-1 and j==Ny-1:
                c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2
      #Nodos internos        
              if i>D1 and i<L1-1 and j>0 and j<Ny-1:
                c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2     
              """L1<Nodos internos <Z1, Material I"""
              if i >L1 and i < Z1 and j >0 and j< Ny-1:
                c[Ny*i+j-8]=-T[Ny*i+j-8]/fo                        
      #pared izquierda con aislacion        
              if j==0 and i>L1 and i<Z1:
                c[Ny*i+j-8]=-T[Ny*i+j-8]/fo      
      #pared derecha con aislacion        
              if j==Ny-1 and i>L1 and i<Z1: 
                c[Ny*i+j-8]=-T[Ny*i+j-8]/fo       
              """Nodos superiores con conveccion interior en superficie plana,Material I,==Z1"""
              if i==Z1 and j>0 and j<Ny-1:
                c[Ny*i+j-8]=-T[Ny*i+j-8]/fo - co2
              if i==Z1 and j==0:
                c[Ny*i+j-8]=-T[Ny*i+j-8]/fo - co2
              if i==Z1 and j==Ny-1:
                c[Ny*i+j-8]=-T[Ny*i+j-8]/fo - co2    
       
      T=np.dot(invu,c)
      """calculo de q Superficie interna"""

      mi=int(Ny*Z1+0-8)
      mf=int(Ny*Z1+Ny-1-8) + 1
      m=T[mi:mf] # Distri. de Temperatura en la superficie int.!!!
  
      sumaTemp=np.sum(m)/len(m) # Temp S. int. medio en el espacio para una iteracion!!!          
      
      qTemp=ho*(TIN[w]-sumaTemp)            
                       
      QinSuperficie += [qTemp] 
      sumaTemp_ += [sumaTemp]
      
      #=== ACA INTERACTUAN LOS MODELOS ===#
      TTABS = sumaTemp
      #===================================# 
      
      """ Flujo de calor en la superficie del tubo"""
      Temp_sup_tubo2 = sum([T[Ny*(D2-1)]]+[T[Ny*(D2-1)+1]]+[T[Ny*D2+2]]+[T[Ny*(D2+1)+2]]+[T[Ny*(D2+2)-1]]+[T[Ny*(D2+3)-4]]+[T[Ny*(D2+4)-6]]+[T[Ny*(D2+5)-8]]+[T[Ny*(D2+5)-7]])
      Temp_sup_tubo_ += [Temp_sup_tubo2/9]      

#%%      
TsupINfunc = interp1d(sample_times, np.array(df['TsupIN']), bounds_error=False, fill_value="extrapolate")
TsupIN = TsupINfunc(tt)
QmeanINfunc = interp1d(sample_times, np.array(df['Qmean']), bounds_error=False, fill_value="extrapolate")
QmeanIN = QmeanINfunc(tt)
Q1INfunc = interp1d(sample_times, np.array(df['Flujo1']), bounds_error=False, fill_value="extrapolate")
Q1IN = Q1INfunc(tt)
Q2INfunc = interp1d(sample_times, np.array(df['Flujo2']), bounds_error=False, fill_value="extrapolate")
Q2IN = Q2INfunc(tt)
TempSupTUBOfunc = interp1d(sample_times, np.array(df2['TtuboMuro']), bounds_error=False, fill_value="extrapolate")
TempSupTUBO = TempSupTUBOfunc(tt)
#%%
import matplotlib.pyplot as plt
x = [i for i in np.linspace(0,172,2052)] 
fig,ax = plt.subplots()
ax.plot(x[:],TIN[:],label="TinSimulado")
ax.plot(x[:],Tao[:],label="TinMedido",marker='o',ls='--', markevery=25, mec='0.1')
ax.plot(x[:],sumaTemp_[1:],label='SupInSimulado_2D')
ax.plot(x,TsupIN[:],label='SupInMedido',marker="o",ls="--",markevery=25,mec='0.1')
ax.set_yticks([i for i in range(10,45,5)])
ax.set_xticks(np.array([i for i in range(0,172,5)]))
ax.set_xlim(0,100)
ax.set_ylim(10,45)
ax.set_ylabel('Temperaturas (°C)')
ax.set_xlabel('Tiempo (Hora)')
ax.grid()
ax.legend() 
#%% FLUJO DE CALOR SUPERFICIAL INTERIOR 
fig,ax = plt.subplots()
ax.plot(x,QinSuperficie[:],label='QinSimulado')
ax.plot(x,Q1IN,label='QinMedido',marker="o",ls="--",markevery=25,mec='0.1')
ax.set_yticks([i for i in range(-100,50,10)])
ax.set_xticks(np.array([i for i in range(0,172,5)]))
ax.set_ylim(-100,50)
ax.set_xlim(0,100)
ax.set_ylabel('Flujo de calor $(W/m^2)$')
ax.set_xlabel('Tiempo (Hora)')
ax.grid()
ax.legend() 
#%% TEMPERATURA SUPERFICIAL DEL TUBO
fig,ax = plt.subplots()
ax.plot(x,TempSupTUBO,label='SupTuboMedido',marker="o",ls="--",markevery=25,mec='0.1')
ax.plot(x,Temp_sup_tubo_,label='SupTuboSimulado')
ax.set_yticks([i for i in range(10,50,5)])
ax.set_xticks(np.array([i for i in range(0,172,5)]))
ax.set_ylim(10,50)
ax.set_xlim(0,100)
ax.set_ylabel('Temperatura (°C)')
ax.set_xlabel('Tiempo (Hora)')
ax.grid()
ax.legend() 
#%% TEMPERATURA DE AMBIENTE INTERIOR
from sklearn.metrics import mean_absolute_error,mean_squared_error,mean_absolute_percentage_error,r2_score
TinFin = Tao # MEDiDO
inicio = 0 
fin = 1184 
ErrorMedioAbosuluto = mean_absolute_error(TinFin[inicio:fin],TIN[inicio:fin])
ErrorCuadraticoMedio = mean_squared_error(TinFin[inicio:fin],TIN[inicio:fin])
RaizErrorCuadraticoMedio = mean_squared_error(TinFin[inicio:fin],TIN[inicio:fin],squared=False)
RaizErrorCuadraticoMedioPorcentual = mean_squared_error(TinFin[inicio:fin],TIN[inicio:fin],squared=False)/TinFin[inicio:fin].mean() * 100
ErrorPocentualMedioAbsoluto = mean_absolute_percentage_error(TinFin[inicio:fin],TIN[inicio:fin]) * 100
r2 = r2_score(TinFin[inicio:fin],TIN[inicio:fin])
print('TEMPERATURA DE AMBIENTE INTERIOR')
print(f'ERROR MEDIO ABSOLUTO: {ErrorMedioAbosuluto}')
print(f'ERROR MEDIO ABSOLUTO PORCENTUAL: {ErrorPocentualMedioAbsoluto}')
print(f'ERROR CUADRATICO MEDIO: {ErrorCuadraticoMedio}')
print(f'RAIZ DEL ERROR CUADRATICO MEDIO: {RaizErrorCuadraticoMedio}')
print(f'RAIZ DEL ERROR CUADRATICO MEDIO PORCENTUAL: {RaizErrorCuadraticoMedioPorcentual}')
print(f'R2: {r2}')
np.save('TempAmb_2D',TIN[inicio:fin])
#%% TEMPERATURA SUPERFICIAL INTERIOR 
ErrorMedioAbosuluto = mean_absolute_error(TsupIN[inicio:fin],sumaTemp_[inicio+1:fin+1])
ErrorCuadraticoMedio = mean_squared_error(TsupIN[inicio:fin],sumaTemp_[inicio+1:fin+1])
RaizErrorCuadraticoMedio = mean_squared_error(TsupIN[inicio:fin],sumaTemp_[inicio+1:fin+1],squared=False)
RaizErrorCuadraticoMedioPorcentual = mean_squared_error(TsupIN[inicio:fin],sumaTemp_[inicio+1:fin+1],squared=False)/TsupIN[inicio:fin].mean() * 100
ErrorPocentualMedioAbsoluto = mean_absolute_percentage_error(TsupIN[inicio:fin],sumaTemp_[inicio+1:fin+1]) * 100
r2 = r2_score(TsupIN[inicio:fin],sumaTemp_[inicio+1:fin+1])
print('TEMPERATURA SUPERFICIAL INTERIOR')
print(f'ERROR MEDIO ABSOLUTO: {ErrorMedioAbosuluto}')
print(f'ERROR MEDIO ABSOLUTO PORCENTUAL: {ErrorPocentualMedioAbsoluto}')
print(f'ERROR CUADRATICO MEDIO: {ErrorCuadraticoMedio}')
print(f'RAIZ DEL ERROR CUADRATICO MEDIO: {RaizErrorCuadraticoMedio}')
print(f'RAIZ DEL ERROR CUADRATICO MEDIO PORCENTUAL: {RaizErrorCuadraticoMedioPorcentual}')
print(f'R2: {r2}')
np.save('TempSuperficial_2D',sumaTemp_[inicio+1:fin+1])
#%% FLUJO 1 DE CALOR SUPERFICIAL INTERIOR 
QinSuperficie2 = np.array(QinSuperficie)
ErrorMedioAbosuluto = mean_absolute_error(Q1IN[inicio:fin],QinSuperficie2[inicio:fin])
ErrorCuadraticoMedio = mean_squared_error(Q1IN[inicio:fin],QinSuperficie2[inicio:fin])
RaizErrorCuadraticoMedio = mean_squared_error(Q1IN[inicio:fin],QinSuperficie2[inicio:fin],squared=False)
RaizErrorCuadraticoMedioPorcentual = mean_squared_error(Q1IN[inicio:fin],QinSuperficie2[inicio:fin],squared=False)/Q1IN[inicio:fin].mean()  *  -100
ErrorPocentualMedioAbsoluto = mean_absolute_percentage_error(np.abs(Q1IN[inicio:fin]),np.abs(QinSuperficie2[inicio:fin])) * 100
r2 = r2_score(Q1IN[inicio:fin],QinSuperficie2[inicio:fin])
print('FLUJO 1 DE CALOR SUPERFICIAL INTERIOR ')
print(f'ERROR MEDIO ABSOLUTO: {ErrorMedioAbosuluto}')
print(f'ERROR MEDIO ABSOLUTO PORCENTUAL: {ErrorPocentualMedioAbsoluto}')
print(f'ERROR CUADRATICO MEDIO: {ErrorCuadraticoMedio}')
print(f'RAIZ DEL ERROR CUADRATICO MEDIO: {RaizErrorCuadraticoMedio}')
print(f'RAIZ DEL ERROR CUADRATICO MEDIO PORCENTUAL: {RaizErrorCuadraticoMedioPorcentual}')
print(f'R2: {r2}')
#%% FLUJO MEAN DE CALOR SUPERFICIAL INTERIOR 
ErrorMedioAbosuluto = mean_absolute_error(QmeanIN[inicio:fin],QinSuperficie2[inicio:fin])
ErrorCuadraticoMedio = mean_squared_error(QmeanIN[inicio:fin],QinSuperficie2[inicio:fin])
RaizErrorCuadraticoMedio = mean_squared_error(QmeanIN[inicio:fin],QinSuperficie2[inicio:fin],squared=False)
RaizErrorCuadraticoMedioPorcentual = mean_squared_error(QmeanIN[inicio:fin],QinSuperficie2[inicio:fin],squared=False)/QmeanIN[inicio:fin].mean()  *  -100
ErrorPocentualMedioAbsoluto = mean_absolute_percentage_error(QmeanIN[inicio:fin],QinSuperficie2[inicio:fin]) * 100
r2 = r2_score(QmeanIN[inicio:fin],QinSuperficie2[inicio:fin])
print('FLUJO MEAN DE CALOR SUPERFICIAL INTERIOR ')
print(f'ERROR MEDIO ABSOLUTO: {ErrorMedioAbosuluto}')
print(f'ERROR MEDIO ABSOLUTO PORCENTUAL: {ErrorPocentualMedioAbsoluto}')
print(f'ERROR CUADRATICO MEDIO: {ErrorCuadraticoMedio}')
print(f'RAIZ DEL ERROR CUADRATICO MEDIO: {RaizErrorCuadraticoMedio}')
print(f'RAIZ DEL ERROR CUADRATICO MEDIO PORCENTUAL: {RaizErrorCuadraticoMedioPorcentual}')
print(f'R2: {r2}')
#%% TEMPERATURA SUPERFICIAL INTERIOR DEL TUBO 
ErrorMedioAbosuluto = mean_absolute_error(TempSupTUBO,Temp_sup_tubo_)
ErrorCuadraticoMedio = mean_squared_error(TempSupTUBO,Temp_sup_tubo_)
RaizErrorCuadraticoMedio = mean_squared_error(TempSupTUBO,Temp_sup_tubo_,squared=False)
RaizErrorCuadraticoMedioPorcentual = mean_squared_error(TempSupTUBO,Temp_sup_tubo_,squared=False)/TempSupTUBO.mean() * 100
ErrorPocentualMedioAbsoluto = mean_absolute_percentage_error(TempSupTUBO,Temp_sup_tubo_) * 100
r2 = r2_score(TempSupTUBO,Temp_sup_tubo_)
print('TEMPERATURA SUPERFICIAL INTERIOR DEL TUBO')
print(f'ERROR MEDIO ABSOLUTO: {ErrorMedioAbosuluto}')
print(f'ERROR MEDIO ABSOLUTO PORCENTUAL: {ErrorPocentualMedioAbsoluto}')
print(f'ERROR CUADRATICO MEDIO: {ErrorCuadraticoMedio}')
print(f'RAIZ DEL ERROR CUADRATICO MEDIO: {RaizErrorCuadraticoMedio}')
print(f'RAIZ DEL ERROR CUADRATICO MEDIO PORCENTUAL: {RaizErrorCuadraticoMedioPorcentual}')
print(f'R2: {r2}')

#%%
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 6))
ax1.plot(x[:],TIN[:],label="TinSimulado")
ax1.plot(x[:],Tao[:],label="TinMedido",marker='o',ls='--', markevery=25, mec='0.1')
ax1.plot(x[:],sumaTemp_[1:],label='SupInSimulado_2D')
ax1.plot(x,TsupIN[:],label='SupInMedido',marker="o",ls="--",markevery=25,mec='0.1')
ax1.set_yticks([i for i in range(10,45,5)])
ax1.set_xticks(np.array([i for i in range(0,172,5)]))
ax1.set_xlim(0,100)
ax1.set_ylim(10,45)
ax1.set_ylabel('Temperaturas (°C)',fontsize=14)
ax1.set_xlabel('Tiempo (Hora)',fontsize=14)
ax1.grid()
ax1.legend(fontsize=12)
ax2.plot(x,QinSuperficie[:],label='QinSimulado')
ax2.plot(x,Q1IN,label='QinMedido',marker="o",ls="--",markevery=25,mec='0.1')
ax2.set_yticks([i for i in range(-100,50,10)])
ax2.set_xticks(np.array([i for i in range(0,172,5)]))
ax2.set_ylim(-100,50)
ax2.set_xlim(0,100)
ax2.set_ylabel('Flujo de calor $(W/m^2)$',fontsize=14)
ax2.set_xlabel('Tiempo (Hora)',fontsize=14)
ax2.grid()
ax2.legend(fontsize=12) 
#%%
diccionario  = {'AmbienteOut':ToutFin,'AmbienteIn':TIN,'Techo':TTI,'Piso':TSU,'Norte':sumaTemp_[1:],'Sur':TSI,'Este':TEI,'Oeste':TOI,'Puerta':TD,'Ventana':TW,'Qin':QinSuperficie}
TempSuperficiesInt = pd.DataFrame(diccionario)
TempSuperficiesInt.to_csv('TempSuperficiesInt2D.csv')