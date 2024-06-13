# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 11:28:44 2023

@author: FEDE
"""
import numpy as np
#%%
class ParametrosConcentrados():
    """
    Rconductivo = (T2-T1)/Q = espesor/area*conductividad
    Rconvectivo = (T2-T1)/Q = 1/area*hconvectivo
    Rradiativa = ver carpeta FuenteBajaEntalpia
    C = cp*masa = cp*rho*area*espesor
    """    
    def __init__(self,nombre,conductividad,calor_esp,densidad,espesor,area):
        self.nombre = nombre
        self.conductividad = conductividad
        self.calor_esp = calor_esp
        self.densidad = densidad
        self.espesor = espesor
        self.area = area
        
    def Resistencia(self):
        return self.espesor / (self.conductividad * self.area)
    
    def Capacitancia(self):
        return self.densidad * self.calor_esp * self.espesor * self.area
    
    def DifusividadTermica(self):
        return self.conductividad / (self.densidad * self.calor_esp)
    
    def __str__(self): 
        res = f'nombre:{self.nombre}\n conductividad: {self.conductividad}\n calor especifico: {self.calor_esp}\
                        \n densidad: {self.densidad} \n espesor: {self.espesor}\
                        \n area: {self.area}'
        return res 

#%% 
def CreacionMatrix(u,dx,Nx,Ny,Z2,fo,fo5,fo6,fo3,fo33,L2,D2,co121,ci1,ei1,ei3,D1,D11,fo4,fo2,L1,Z1,co1,fo44,foIn44,foIn444,z4,co4121):
    
    """Nodos internos < int(z4/dx), Material IV"""

    for i in range(0,Nx):
        for j in range(0,Ny):

            if i >0 and i < int(z4/dx) and j >0 and j< Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo44)/fo44 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=1 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=1 #node de la der.            
    #pared izquierda con aislacion        
            if j==0 and i>0 and i < int(z4/dx):
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo44)/fo44 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
    #pared derecha con aislacion        
            if j==Ny-1 and i>0 and i < int(z4/dx): 
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo44)/fo44 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.
                 
            """int(z4/dx) < Nodos internos < Z2, Material I"""

            if i >int(z4/dx) and i < Z2 and j >0 and j< Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=1 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=1 #node de la der.            
    #pared izquierda con aislacion        
            if j==0 and i>int(z4/dx) and i<Z2:
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
    #pared derecha con aislacion        
            if j==Ny-1 and i>int(z4/dx) and i<Z2: 
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.             
    
            """Interface Material IV y I,int(z4/dx) y int(z4/dx) + 1"""
    
    #Material IV
    
    #pared aislado izq arriba de los caños 
            if i==int(z4/dx) and j==0:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo44+foIn444)/fo44 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=foIn444/fo44 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
    #pared aislado izq arriba de los caños 
            if i==int(z4/dx) and j==Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo44+foIn444)/fo44 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=foIn444/fo44 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.
    #Nodos internos        
            if i==int(z4/dx) and j>0 and j<Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo44+foIn444)/fo44 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=foIn444/fo44 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=1 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=1 #node de la der.
    #Material I

    #pared aislado izq arriba de los caños 
            if i==int(z4/dx)+1 and j==0:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo+foIn44)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=foIn44/fo #nodo de abajo
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
    #pared aislado izq arriba de los caños 
            if i==int(z4/dx)+1 and j==Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo+foIn44)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=foIn44/fo  #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.
    #Nodos internos        
            if i==int(z4/dx)+1 and j>0 and j<Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo+foIn44)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=foIn44/fo #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=1 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=1 #node de la der.    
    
            """Interface Material I y III,Z2 y Z2 + 1"""
    
    #Material I

    #pared aislado izq arriba de los caños 
            if i==Z2 and j==0:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo+fo5)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=fo5/fo #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
    #pared aislado izq arriba de los caños 
            if i==Z2 and j==Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo+fo5)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=fo5/fo #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.
    #Nodos internos        
            if i==Z2 and j>0 and j<Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo+fo5)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=fo5/fo #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=1 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=1 #node de la der.
    #Material III

    #pared aislado izq arriba de los caños 
            if i==Z2+1 and j==0:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo33+fo6)/fo33 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=fo6/fo33 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
    #pared aislado izq arriba de los caños 
            if i==Z2+1 and j==Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo33+fo6)/fo33 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=fo6/fo33 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.
    #Nodos internos        
            if i==Z2+1 and j>0 and j<Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo33+fo6)/fo33 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=fo6/fo33 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=1 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=1 #node de la der.
   
            """Z2 +1 <Nodos internos <L2, Material III"""

            if i >Z2+1 and i < L2 and j >0 and j< Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo33)/fo33 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=1 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=1 #node de la der.            
    #pared izquierda con aislacion        
            if j==0 and i>Z2+1 and i<L2:
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo33)/fo33 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
    #pared derecha con aislacion        
            if j==Ny-1 and i>Z2+1 and i<L2: 
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo33)/fo33 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.
    
            """Interface Material III y I, inferior,L2 y L2+1"""
    
    #Material III

            if i==L2 and j>0 and j<Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo33+fo6)/fo33 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=fo6/fo33 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=1 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=1 #node de la der.
    #pared izquierda con aislacion        
            if i==L2 and j==0:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo33+fo6)/fo33 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=fo6/fo33 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
    #pared derecha con aislacion        
            if i==L2 and j==Ny-1: 
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo33+fo6)/fo33 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=fo6/fo33 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.
    #Material I
            if i==L2+1 and j>0 and j<Ny-1:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo+fo5)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=fo5/fo #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=1 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=1 #node de la der.
    #pared izquierda con aislacion        
            if i==L2+1 and j==0:
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo+fo5)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=fo5/fo #nodo de abajo
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
    #pared derecha con aislacion        
            if i==L2+1 and j==Ny-1: 
                 u[Ny*i+j][Ny*i+j]=-(1+3*fo+fo5)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=fo5/fo #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.
    
            """L2 + 1 < Nodos internos < D2, Material I""" 

            if i > L2 +1 and i<D2 and j>0 and j<Ny-1: #j <Nx and j>0 #and i<Nx:
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=1 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=1 #node de la der.
    #pared izquierda con aislacion        
            if j==0 and i> L2 +1 and i<D2:
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
    #pared derecha con aislacion        
            if j==Ny-1 and i> L2 +1 and i<D2: 
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.
        
            """Nodos inferiores con conveccio exterior,Material IV"""

            if i==0 and j>0 and j<Ny-1:
                 u[Ny*i+j][Ny*i+j]=-co4121#-co121
                 u[Ny*i+j][Ny*(i+1)+j]=2 #nodo de arriba
                 u[Ny*i+j][Ny*i+(j-1)]=1 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=1 #node de la der.
            if i==0 and j==0:
                 u[Ny*i+j][Ny*i+j]=-co4121#-co121
                 u[Ny*i+j][Ny*(i+1)+j]=2 #nodo de arriba
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
            if i==0 and j==Ny-1:
                 u[Ny*i+j][Ny*i+j]=-co4121#-co121
                 u[Ny*i+j][Ny*(i+1)+j]=2 #nodo de arriba
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.
    
            """Nodos interiores entre los tubos"""

            if i==D2 and j>1 and j<Ny-2:
                 u[Ny*i+j][Ny*i+j]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j-1]=1 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=1 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=1 #node de la der.
            if i==D2+1 and j>2 and j<Ny-3:
                 u[Ny*i+j-1][Ny*i+j-1]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j-1][Ny*(i+1)+j-4]=1 #nodo de arriba
                 u[Ny*i+j-1][Ny*(i-1)+j]=1 #nodo de abajo
                 u[Ny*i+j-1][Ny*i+(j-1)-1]=1 #nodo de la izq.
                 u[Ny*i+j-1][Ny*i+(j+1)-1]=1 #node de la der.
            if i==D2+2 and j>2 and j<Ny-3:
                 u[Ny*i+j-4][Ny*i+j-4]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j-4][Ny*(i+1)+j-7]=1 #nodo de arriba
                 u[Ny*i+j-4][Ny*(i-1)+j-1]=1 #nodo de abajo
                 u[Ny*i+j-4][Ny*i+(j-1)-4]=1 #nodo de la izq.
                 u[Ny*i+j-4][Ny*i+(j+1)-4]=1 #node de la der.
            if i==D2+3 and j>2 and j<Ny-3:
                 u[Ny*i+j-7][Ny*i+j-7]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j-7][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-7][Ny*(i-1)+j-4]=1 #nodo de abajo
                 u[Ny*i+j-7][Ny*i+(j-1)-7]=1 #nodo de la izq.
                 u[Ny*i+j-7][Ny*i+(j+1)-7]=1 #node de la der.
            if i==D2+4 and j>1 and j<Ny-2:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-7]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=1 #nodo de la izq.
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=1 #node de la der.
            
            """inicio de tubos izquierdo y derecho"""

            if i==D2 and j==0:
                 u[Ny*i+j][Ny*i+j]=-ci1 #diagonal principal
                 u[Ny*i+j][Ny*(i-1)+j]=2 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
            if i==D2 and j==1:
                 u[Ny*i+j][Ny*i+j]=-ei1 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j-1]=2 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=4 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=4 #node de la der.
            if i==D2 and j==Ny-2:
                 u[Ny*i+j][Ny*i+j]=-ei1 #diagonal principal
                 u[Ny*i+j][Ny*(i+1)+j-1]=2 #nodo de arriba
                 u[Ny*i+j][Ny*(i-1)+j]=4 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=4 #nodo de la izq.
                 u[Ny*i+j][Ny*i+(j+1)]=2 #node de la der.
            if i==D2 and j==Ny-1:            
                 u[Ny*i+j][Ny*i+j]=-ci1 #diagonal principal
                 u[Ny*i+j][Ny*(i-1)+j]=2 #nodo de abajo
                 u[Ny*i+j][Ny*i+(j-1)]=2 #nodo de la izq.
    
            if i==D2+1 and j==1:
                 u[Ny*i+j-1][Ny*i+j-1]=-ei3          
                 u[Ny*i+j-1][Ny*(i-1)+j]=2 #nodo de abajo
                 u[Ny*i+j-1][Ny*i+(j+1)-1]=2 #node de la der.
    
            if i==D2+1 and j==2:
                 u[Ny*i+j-1][Ny*i+j-1]=-ei1 #diagonal principal
                 u[Ny*i+j-1][Ny*(i+1)+j-4]=2 #nodo de arriba
                 u[Ny*i+j-1][Ny*(i-1)+j]=4 #nodo de abajo
                 u[Ny*i+j-1][Ny*i+(j-1)-1]=2 #nodo de la izq.
                 u[Ny*i+j-1][Ny*i+(j+1)-1]=4 #node de la der.
    
            if i==D2+1 and j==Ny-3:
                 u[Ny*i+j-1][Ny*i+j-1]=-ei1 #diagonal principal
                 u[Ny*i+j-1][Ny*(i+1)+j-4]=2 #nodo de arriba
                 u[Ny*i+j-1][Ny*(i-1)+j]=4 #nodo de abajo
                 u[Ny*i+j-1][Ny*i+(j-1)-1]=4 #nodo de la izq.
                 u[Ny*i+j-1][Ny*i+(j+1)-1]=2 #node de la der.
            if i==D2+1 and j==Ny-2:
                 u[Ny*i+j-1][Ny*i+j-1]=-ei3          
                 u[Ny*i+j-1][Ny*(i-1)+j]=2 #nodo de abajo
                 u[Ny*i+j-1][Ny*i+(j-1)-1]=2 #nodo de la izq.
    
            if i==D2+2 and j==2:
                 u[Ny*i+j-4][Ny*i+j-4]=-ci1
                 u[Ny*i+j-4][Ny*(i+1)+j-7]=1 #nodo de arriba, tiene 7 nodos menos acumulados
                 u[Ny*i+j-4][Ny*(i-1)+j-1]=1 #nodo de abajo,tiene 1 nodo menos en esa fila
                 u[Ny*i+j-4][Ny*i+(j+1)-4]=2 #node de la der.
    
            if i==D2+2 and j==Ny-3:
                 u[Ny*i+j-4][Ny*i+j-4]=-ci1
                 u[Ny*i+j-4][Ny*(i+1)+j-7]=1 #nodo de arriba
                 u[Ny*i+j-4][Ny*(i-1)+j-1]=1 #nodo de abajo
                 u[Ny*i+j-4][Ny*i+(j-1)-4]=2 #nodo de la izq.
    
            if i==D2+3 and j==1:
                 u[Ny*i+j-7][Ny*i+j-7]=-ei3
                 u[Ny*i+j-7][Ny*(i+1)+j-8]=2 #nodo de arriba
                 u[Ny*i+j-7][Ny*i+(j+1)-7]=2 #node de la der.
            if i==D2+3 and j==2:
                 u[Ny*i+j-7][Ny*i+j-7]=-ei1
                 u[Ny*i+j-7][Ny*(i+1)+j-8]=4 #nodo de arriba
                 u[Ny*i+j-7][Ny*i+(j+1)-7]=4 #node de la der.
                 u[Ny*i+j-7][Ny*(i-1)+j-4]=2 #nodo de abajo
                 u[Ny*i+j-7][Ny*i+(j-1)-7]=2 #nodo de la izq.
            if i==D2+3  and j==Ny-3:
                 u[Ny*i+j-7][Ny*i+j-7]=-ei1
                 u[Ny*i+j-7][Ny*(i+1)+j-8]=4 #nodo de arriba
                 u[Ny*i+j-7][Ny*i+(j+1)-7]=2 #node de la der.
                 u[Ny*i+j-7][Ny*(i-1)+j-4]=2 #nodo de abajo
                 u[Ny*i+j-7][Ny*i+(j-1)-7]=4 #nodo de la izq.
            if i==D2+3 and j==Ny-2:
                 u[Ny*i+j-7][Ny*i+j-7]=-ei3
                 u[Ny*i+j-7][Ny*(i+1)+j-8]=2 #nodo de arriba
                 u[Ny*i+j-7][Ny*i+(j-1)-7]=2 #nodo de la izq
            if i==D2+4 and j==0:
                 u[Ny*i+j-8][Ny*i+j-8]=-ci1
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=2 #nodo de arriba
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=2 #node de la der.
            if i==D2+4 and j==1:
                 u[Ny*i+j-8][Ny*i+j-8]=-ei1
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=4 #nodo de arriba
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=4 #node de la der.
                 u[Ny*i+j-8][Ny*(i-1)+j-7]=2 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=2 #nodo de la izq.
            if i==D2+4 and j==Ny-2:
                 u[Ny*i+j-8][Ny*i+j-8]=-ei1
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=4 #nodo de arriba
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=2 #node de la der.
                 u[Ny*i+j-8][Ny*(i-1)+j-7]=2 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=4 #nodo de la izq.
            if i==D2+4 and j==Ny-1:
                 u[Ny*i+j-8][Ny*i+j-8]=-ci1
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=2 #nodo de arriba
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=2 #nodo de la izq.
    
            """D11<Nodos internos arriba de los caños ,<D1-1"""

    #pared aislado izq arriba de los caños 
            if i<D1-1 and i>D11 and j==0:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=2 #node de la der.
    #pared aislado izq arriba de los caños 
            if i<D1-1 and i>D11 and j==Ny-1:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=2 #nodo de la izq.
    #Nodos internos        
            if i>D11 and i<D1-1 and j>0 and j<Ny-1:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=1 #nodo de la izq.
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=1 #node de la der.
            
            """Interface Material II y I, Superior,D1-1 y D1"""
    
    #Material I

    #pared aislado izq arriba de los caños 
            if i==D1-1 and j==0:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+3*fo+fo3)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=fo3/fo #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=2 #node de la der.
    #pared aislado derecha arriba de los caños 
            if i==D1-1 and j==Ny-1:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+3*fo+fo3)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=fo3/fo #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=2 #nodo de la izq.
    #Nodos internos        
            if i==D1-1 and j>0 and j<Ny-1:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+3*fo+fo3)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=fo3/fo #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=1 #nodo de la izq.
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=1 #node de la der.
    #Material II

    #pared aislado izq arriba de los caños 
            if i==D1 and j==0:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+3*fo2+fo4)/fo2 #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=fo4/fo2 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=2 #node de la der.
    #pared aislado derecha arriba de los caños 
            if i==D1 and j==Ny-1:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+3*fo2+fo4)/fo2 #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=fo4/fo2 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=2 #nodo de la izq.
    #Nodos internos        
            if i==D1 and j>0 and j<Ny-1:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+3*fo2+fo4)/fo2 #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=fo4/fo2 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=1 #nodo de la izq.
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=1 #node de la der.
    
            """Nodos superiores Material II,>D1,<L1-1"""

            if i>D1 and i<L1-1 and j>0 and j<Ny-1:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+4*fo2)/fo2 #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=1 #nodo de la izq.
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=1 #node de la der. 
    #pared izquierda con aislacion        
            if j==0 and i>D1 and i<L1-1:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+4*fo2)/fo2 #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=2 #node de la der.
    #pared derecha con aislacion        
            if j==Ny-1 and i>D1 and i<L1-1: 
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+4*fo2)/fo2 #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=2 #nodo de la izq.
    
            """Interface Material II y I, inferior,L1-1 y L1"""
    
    #Material II

            if i==L1-1 and j>0 and j<Ny-1:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+3*fo2+fo4)/fo2 #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=fo4/fo2 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=1 #nodo de la izq.
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=1 #node de la der.
    #pared izquierda con aislacion        
            if i==L1-1 and j==0:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+3*fo2+fo4)/fo2 #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=fo4/fo2 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=2 #node de la der.
    #pared derecha con aislacion        
            if i==L1-1 and j==Ny-1: 
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+3*fo2+fo4)/fo2 #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=fo4/fo2 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=2 #nodo de la izq.
    #Material I
            if i==L1 and j>0 and j<Ny-1:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+3*fo+fo3)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=fo3/fo #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=1 #nodo de la izq.
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=1 #node de la der.
    #pared izquierda con aislacion        
            if i==L1 and j==0:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+3*fo+fo3)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=fo3/fo #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=2 #node de la der.
    #pared derecha con aislacion        
            if i==L1 and j==Ny-1: 
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+3*fo+fo3)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=fo3/fo #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=2 #nodo de la izq.
    
            """L1<Nodos internos <Z1, Material I"""

            if i >L1 and i < Z1 and j >0 and j< Ny-1:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=1 #nodo de la izq.
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=1 #node de la der.            
    #pared izquierda con aislacion        
            if j==0 and i>L1 and i<Z1:
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j+1)-8]=2 #node de la der.
    #pared derecha con aislacion            
            if j==Ny-1 and i>L1 and i<Z1: 
                 u[Ny*i+j-8][Ny*i+j-8]=-(1+4*fo)/fo #diagonal principal
                 u[Ny*i+j-8][Ny*(i+1)+j-8]=1 #nodo de arriba
                 u[Ny*i+j-8][Ny*(i-1)+j-8]=1 #nodo de abajo
                 u[Ny*i+j-8][Ny*i+(j-1)-8]=2 #nodo de la izq.
    
            """Nodos superiores con conveccion en superficie plana,==Z1, Material I"""

            if i==Z1 and j>0 and j<Ny-1:
                u[Ny*i+j-8][Ny*i+j-8]=-co1
                u[Ny*i+j-8][Ny*(i-1)+j-8]=2 #nodo de abajo,
                u[Ny*i+j-8][Ny*i+(j-1)-8]=1 #nodo de la izq.
                u[Ny*i+j-8][Ny*i+(j+1)-8]=1 #node de la der.
            if i==Z1 and j==0:
                u[Ny*i+j-8][Ny*i+j-8]=-co1
                u[Ny*i+j-8][Ny*(i-1)+j-8]=2 #nodo de abajo,
                u[Ny*i+j-8][Ny*i+(j+1)-8]=2 #node de la der.
            if i==Z1 and j==Ny-1:
                u[Ny*i+j-8][Ny*i+j-8]=-co1
                u[Ny*i+j-8][Ny*(i-1)+j-8]=2 #nodo de abajo,
                u[Ny*i+j-8][Ny*i+(j-1)-8]=2 #nodo de la izq.
    
    return u

#%%

def Calculos(u,Nx,Ny,Nxy,fco221,fco2,fci2,fei2,frad,Z2,fo,L2,fo33,D2,L1,fo2,D1,D11,Z1,ho,Tao,hoo,Taooo):
    
    invu=np.linalg.inv(u)
    Nitera = 2#2052
    #numitera = 2052# len(Taooo) -120 #numero de iteraciones 
    k=0
    itera=0
    Nt=Nxy
    c=np.zeros([Nt,1])
    T=np.zeros([Nt,1])
    sumaTempt=0
    ssumaTempt=0
    p=25+273.15 #Temperatura de inicio
    sumaTemp_ = [p-273.15]
    for i in range(0,Nt):
        T[i]=p
    s=-1
    
    QinSuperficie = []
    QoutSuperficie = []
    
    while k<Nitera and itera==0:          
          
          k=k+1          
          s=s+1
          
          co221=fco221[s]   # AMBIENTE EXERIOR
          co2=fco2[s]       # AMBIENTE INTERIOR
          cci2=fci2[s]       # AGUA IN 
          cei2=fei2[s]        # AGUA IN 
          rad=frad[s]
          
          """Nodos internos < Z2, Material I"""
          for i in range(0,Nx):
              for j in range(0,Ny):
                  if i >0 and i<Z2 and j>0 and j<Ny-1:
                     c[Ny*i+j]=-T[Ny*i+j]/fo
                  #pared izquierda con aislacion        
                  elif j==0 and i>0 and i<L2:
                     c[Ny*i+j]=-T[Ny*i+j]/fo
                  #pared derecha con aislacion        
                  elif j==Ny-1 and i>0 and i<L2:      
                     c[Ny*i+j]=-T[Ny*i+j]/fo   
          """Nodos inferiores con aislacion"""            

          """Nodos inferiores con conveccion exterior, Material I"""
          for i in range(0,Nx):
              for j in range(0,Ny):
                 if i==0  and j>0 and j<Ny-1: 
                    c[Ny*i+j]=-T[Ny*i+j]/fo - co221 - rad
                 #nodo inferior izquiedo con conveccion exterior        
                 elif i==0 and j==0:
                     c[Ny*i+j]=-T[Ny*i+j]/fo -co221 - rad
                 #nodo inferior derecho con conveccion exterior 
                 elif i==0 and j==Ny-1:      
                     c[Ny*i+j]=-T[Ny*i+j]/fo -co221 - rad
          
          """Interface Material III y I, en Z2 y Z2+1"""
          #Material I
          for i in range(0,Nx):
              for j in range(0,Ny):
          #pared aislado izq arriba de los caños 
                  if i==Z2 and j==0:
                     c[Ny*i+j]=-T[Ny*i+j]/fo
          #pared aislado izq arriba de los caños 
                  elif i==Z2 and j==Ny-1:
                     c[Ny*i+j]=-T[Ny*i+j]/fo
          #Nodos internos        
                  elif i==Z2 and j>0 and j<Ny-1:
                     c[Ny*i+j]=-T[Ny*i+j]/fo
          #Material III
          for i in range(0,Nx):
              for j in range(0,Ny):
          #pared aislado izq arriba de los caños 
                 if i==Z2+1 and j==0:
                    c[Ny*i+j]=-T[Ny*i+j]/fo33           
          #pared aislado izq arriba de los caños 
                 elif i==Z2+1 and j==Ny-1:
                    c[Ny*i+j]=-T[Ny*i+j]/fo33      
          #Nodos internos        
                 elif i==Z2+1 and j>0 and j<Ny-1:
                    c[Ny*i+j]=-T[Ny*i+j]/fo33 
          """Z2 +1 <Nodos internos <L2, Material III"""
          for i in range(0,Nx):
              for j in range(0,Ny):
                 if i >Z2+1 and i < L2 and j >0 and j< Ny-1:
                    c[Ny*i+j]=-T[Ny*i+j]/fo33 #diagonal principal
                 elif j==0 and i>Z2+1 and i<L2:
                    c[Ny*i+j]=-T[Ny*i+j]/fo33        
                 elif j==Ny-1 and i>Z2+1 and i<L2: 
                    c[Ny*i+j]=-T[Ny*i+j]/fo33 
          """Interface Material II y I,en L2 y L2+1"""
          
          #Material III
          for i in range(0,Nx):
              for j in range(0,Ny):
                  if i==L2 and j>0 and j<Ny-1:
                     c[Ny*i+j]=-T[Ny*i+j]/fo33  
          #pared izquierda con aislacion        
                  elif i==L2 and j==0:
                     c[Ny*i+j]=-T[Ny*i+j]/fo33
          #pared derecha con aislacion        
                  elif i==L2 and j==Ny-1: 
                     c[Ny*i+j]=-T[Ny*i+j]/fo33
          #Material I
                  elif i==L2+1 and j>0 and j<Ny-1:
                     c[Ny*i+j]=-T[Ny*i+j]/fo
          #pared izquierda con aislacion        
                  elif i==L2+1 and j==0:
                     c[Ny*i+j]=-T[Ny*i+j]/fo
          #pared derecha con aislacion        
                  elif i==L2+1 and j==Ny-1: 
                     c[Ny*i+j]=-T[Ny*i+j]/fo
          """L2 + 1 < Nodos internos < D2"""
          for i in range(0,Nx):
              for j in range(0,Ny):
                  if i > L2 +1 and i<D2 and j>0 and j<Ny-1: #j <Nx and j>0 #and i<Nx:
                     c[Ny*i+j]=-T[Ny*i+j]/fo
          #pared izquierda con aislacion        
                  elif j==0 and i> L2 +1 and i<D2:
                     c[Ny*i+j]=-T[Ny*i+j]/fo  
          #pared derecha con aislacion        
                  elif j==Ny-1 and i> L2 +1 and i<D2: 
                     c[Ny*i+j]=-T[Ny*i+j]/fo             
          """inicio de tubos izquierdo y derecho"""
          for i in range(0,Nx):
               for j in range(0,Ny):
                   if i==D2 and j==0:
                      c[Ny*i+j]=-T[Ny*i+j]/fo - cci2#ci2
                   elif i==D2 and j==1:
                      c[Ny*i+j]=-(3/fo)*T[Ny*i+j] - cei2#ei2
                   elif i==D2 and j==Ny-2:
                      c[Ny*i+j]=-(3/fo)*T[Ny*i+j] - cei2#ei2
                   elif i==D2 and j==Ny-1:            
                      c[Ny*i+j]=-T[Ny*i+j]/fo -cci2#ci2
                   elif i==D2+1 and j==1:
                      c[Ny*i+j-1]=-T[Ny*i+j-1]/fo - cei2#ei2
                   elif i==D2+1 and j==2:
                      c[Ny*i+j-1]=-(3/fo)*T[Ny*i+j-1] -cei2#ei2
                   elif i==D2+1 and j==Ny-3:
                      c[Ny*i+j-1]=-(3/fo)*T[Ny*i+j-1] -cei2#ei2
                   elif i==D2+1 and j==Ny-2:
                      c[Ny*i+j-1]=-T[Ny*i+j-1]/fo - cei2#ei2
                   elif i==D2+2 and j==2:
                      c[Ny*i+j-4]=-T[Ny*i+j-4]/fo - cci2#ci2
                   elif i==D2+2 and j==Ny-3:  
                      c[Ny*i+j-4]=-T[Ny*i+j-4]/fo - cci2#ci2
                   elif i==D2+3 and j==1:
                      c[Ny*i+j-7]=-T[Ny*i+j-7]/fo - cei2#ei2
                   elif i==D2+3 and j==2:
                      c[Ny*i+j-7]=-(3/fo)*T[Ny*i+j-7] - cei2#ei2
                   elif i==D2+3  and j==Ny-3:
                      c[Ny*i+j-7]=-(3/fo)*T[Ny*i+j-7] - cei2#ei2
                   elif i==D2+3 and j==Ny-2:
                      c[Ny*i+j-7]=-T[Ny*i+j-7]/fo - cei2#ei2
                   elif i==D2+4 and j==0:
                      c[Ny*i+j-8]=-T[Ny*i+j-8]/fo - cci2#ci2
                   elif i==D2+4 and j==1:
                      c[Ny*i+j-8]=-(3/fo)*T[Ny*i+j-8] - cei2#ei2
                   elif i==D2+4 and j==Ny-2:
                      c[Ny*i+j-8]=-(3/fo)*T[Ny*i+j-8] - cei2#ei2
                   elif i==D2+4 and j==Ny-1:
                      c[Ny*i+j-8]=-T[Ny*i+j-8]/fo - cci2#ci2
          """Nodos interiores entre los tubos"""
          for i in range(0,Nx):
               for j in range(0,Ny):
                   if i==D2 and j>1 and j<Ny-2:  
                      c[Ny*i+j]=-T[Ny*i+j]/fo
                   elif i==D2+1 and j>2 and j<Ny-3:
                      c[Ny*i+j-1]=-T[Ny*i+j-1]/fo
                   elif i==D2+2 and j>2 and j<Ny-3:
                      c[Ny*i+j-4]=-T[Ny*i+j-4]/fo
                   elif i==D2+3 and j>2 and j<Ny-3:
                      c[Ny*i+j-7]=-T[Ny*i+j-7]/fo
                   elif i==D2+4 and j>1 and j<Ny-2:
                      c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
        
          """D11<Nodos internos arriba de los caños ,<D1-1,Material I"""
          for i in range(0,Nx):
              for j in range(0,Ny):
         #pared aislado izq arriba de los caños 
                  if i<D1-1 and i>D11 and j==0:
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
         #pared aislado izq arriba de los caños 
                  elif i<D1-1 and i>D11 and j==Ny-1:
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
         #Nodos internos        
                  elif i>D11 and i<D1-1 and j>0 and j<Ny-1:
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo   
          """Interface Material II y I, Superior,D1-1 y D1"""
          #Material I
          for i in range(0,Nx):
              for j in range(0,Ny):
          #pared aislado izq arriba de los caños 
                  if i==D1-1 and j==0:
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
          #pared aislado izq arriba de los caños 
                  elif i==D1-1 and j==Ny-1:
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
          #Nodos internos        
                  elif i==D1-1 and j>0 and j<Ny-1:
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
          #Material II
          for i in range(0,Nx):
              for j in range(0,Ny):
          #pared aislado izq arriba de los caños 
                 if i==D1 and j==0:
                    c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2           
          #pared aislado izq arriba de los caños 
                 elif i==D1 and j==Ny-1:
                    c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2      
          #Nodos internos        
                 elif i==D1 and j>0 and j<Ny-1:
                    c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2    
          
          """Interface Material II y I,en L1-1 y L1"""
          
          #Material II
          for i in range(0,Nx):
              for j in range(0,Ny):
                  if i==L1-1 and j>0 and j<Ny-1:
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2  
          #pared izquierda con aislacion        
                  elif i==L1-1 and j==0:
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2
          #pared derecha con aislacion        
                  elif i==L1-1 and j==Ny-1: 
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2
          #Material I
                  elif i==L1 and j>0 and j<Ny-1:
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
          #pared izquierda con aislacion        
                  elif i==L1 and j==0:
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
          #pared derecha con aislacion        
                  elif i==L1 and j==Ny-1: 
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
          """L1 < Nodos internos < Z1"""
          for i in range(0,Nx):
              for j in range(0,Ny):
                  if i > L1 and i<Z1 and j>0 and j<Ny-1: #j <Nx and j>0 #and i<Nx:
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
          #pared izquierda con aislacion        
                  elif j==0 and i> L1 and i<Z1:
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo  
          #pared derecha con aislacion        
                  elif j==Ny-1 and i> L1 and i<Z1: 
                     c[Ny*i+j-8]=-T[Ny*i+j-8]/fo             
                     
          """Nodos internos arriba de los caños ,Matarial II,>D1,<L1-1"""
          for i in range(0,Nx):
              for j in range(0,Ny):
                 #pared aislado izq arriba de los caños 
                 if i>D1 and i<L1-1 and j==0:
                    c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2
                 #pared aislado izq arriba de los caños 
                 elif i>D1 and i<L1-1 and j==Ny-1:
                    c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2
                 #Nodos internos        
                 elif i>D1 and i<L1-1 and j>0 and j<Ny-1:
                    c[Ny*i+j-8]=-T[Ny*i+j-8]/fo2     
          """L1<Nodos internos <Z1, Material I"""
          for i in range(0,Nx):
              for j in range(0,Ny):
                  if i >L1 and i < Z1 and j >0 and j< Ny-1:
                    c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
                             
    #pared izquierda con aislacion        
                  elif j==0 and i>L1 and i<Z1:
                    c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
                 
    #pared derecha con aislacion        
                  elif j==Ny-1 and i>L1 and i<Z1: 
                    c[Ny*i+j-8]=-T[Ny*i+j-8]/fo
                 
          """Nodos superiores con conveccion interior en superficie plana,Material I,==Z1"""
          for i in range(0,Nx):
              for j in range(0,Ny):
                 if i==Z1 and j>0 and j<Ny-1:
                    c[Ny*i+j-8]=-T[Ny*i+j-8]/fo - co2
                 elif i==Z1 and j==0:
                    c[Ny*i+j-8]=-T[Ny*i+j-8]/fo - co2
                 elif i==Z1 and j==Ny-1:
                    c[Ny*i+j-8]=-T[Ny*i+j-8]/fo - co2    
          
          T=np.dot(invu,c)
          """calculo de q Superficie interna"""
    
          mi=int(Ny*Z1+0-8)
          mf=int(Ny*Z1+Ny-1-8) + 1
          m=T[mi:mf] -273.15 # Distri. de Temperatura en la superficie int.!!!
          
          sumaTemp=np.sum(m)/len(m) # Temp S. int. medio en el espacio para una iteracion!!!          
          qTemp=ho*((Tao[s]-273.15)-sumaTemp)          
          sumaTempt=np.sum(m)/len(m) + sumaTempt # Suma de Tmp.S.int para cada iteracion (acumula)!!!
                     
          QinSuperficie += [qTemp] 
          sumaTemp_ += [sumaTemp]
          
          """calculo de q Superficie exterior""" 
          
          mii=int(Ny*0+0)
          mff=int(Ny*0+Ny-1) + 1
          mm=T[mii:mff] -273.15 # Distri. de Temperatura en la superficie out.!!!
          
          ssumaTemp=np.sum(mm)/len(mm) # Temp S. ext. medio en el espacio para una iteracion!!!          
          qqTemp=hoo*((Taooo[s]-273.15)-ssumaTemp)          
          ssumaTempt=np.sum(mm)/len(mm) + ssumaTempt # Suma de Tmp.S.int para cada iteracion (acumula)!!!
                    
          QoutSuperficie += [qqTemp]
             
    return sumaTemp_,QinSuperficie 