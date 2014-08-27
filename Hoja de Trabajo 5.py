# -*- coding: cp1252 -*-
#Alejandro Diaz  Carne: 13082
#Samuel Maldonado Carne: 13153
#Seccion: 30    26/08/14
#HOJA DE TRABAJO 5
#---------------------------------------------------------------------
import simpy
import random
from math import sqrt
cantidadProcesos = 100
intervaloProc = 10
cantidadRAM = 100
RANDOM_SEED=10

#-----NEW-------------------------------------------------------------
def source(env,number,interval,RAM,CPU,WAIT, cantidadRAM, contador):
    for i in range (number):
        instrucciones = random.randint(1,10)
        memoria = random.randint(1,10)
        if contador != 1:
            cantidadRAM = cantidadRAM - memoria
        contador = contador + 1
        c = procesos(env, i, memoria,RAM,CPU,wait1,instrucciones,cantidadRAM)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)

def procesos(env,nombre,memoria,RAM,CPU,wait1,instrucciones,cantidadRAM):
    global promedio    
    global desvEst
    arrive =env.now
    print ('%7.4f %s: NEW (esperando RAM %s), RAM disponible %s' % (arrive, nombre, memoria, cantidadRAM))

#-----READY-----------------------------------------------------------
    with RAM.get(memoria) as req:
        yield req

    espera = env.now - arrive
    print ('%7.4f %s: Espero RAM %6.3f' %(env.now, nombre, espera))
    while instrucciones > 0:
#-----WAITING-----------------------------------------------------------
        with CPU.request() as reqCPU:
            yield reqCPU
#-----RUNNING-----------------------------------------------------------
            print('%7.4f %s: RUNNING instrucciones %6.3f' % (env.now, nombre, instrucciones))
            yield env.timeout(1)

        
            if instrucciones > 3:
                    instrucciones = instrucciones - 3
            else:
                instrucciones = 0

    if instrucciones > 0:
        avanzar = random.choice(["r","w"])
        if avanzar == "w":
            with wait1.request as reqwait:
                yield reqwait
                print('%7.4f %s: esperando' % (env.now, nombre))
                yield env.timeout(1)
        print ('%7.4f %s: listo' % (env.now, nombre))
    tiempoTotal = env.now - arrive
    desvEst=desvEst+((tiempoTotal-4.51)**2)
    promedio=tiempoTotal+promedio

#-----TERMINATED-----------------------------------------------------------
    print ('%7.4f %s: finalizado tiempo total %s' % (env.now, nombre, tiempoTotal))

    with RAM.put(memoria) as reqDevuelve:
        yield reqDevuelve
        print('%7.4f %s: Devolviendo memoria %s' % (env.now, nombre, memoria))
        memoria=memoria+memoria

promedio=0
desvEst=0
random.seed(RANDOM_SEED)
env = simpy.Environment()
CPU = simpy.Resource(env,capacity=1)
RAM = simpy.Container(env,init=100,capacity=100)
wait1 = simpy.Resource(env,capacity=1)
env.process(source(env,cantidadProcesos,intervaloProc,RAM,CPU,wait1,cantidadRAM,1))

env.run()

promedio=promedio/cantidadProcesos
desvEst=desvEst/(cantidadProcesos - 1)
desvEst=sqrt(desvEst)
print ('El promedio es %s' % promedio)
print('La desviacion estandar es %s' %desvEst)
