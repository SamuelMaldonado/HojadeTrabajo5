import random
import simpy

randomSeed =10

def proceso(env,name,CPU,RAM,tiempoDeEspera,tiempoDeEjecucion):
    yield env.timeout(tiempoDeEspera)
    arrive =env.now

    print ('%s Llego Procese en %d' % (name,env.now))

    with RAM.request() as req:
        yield req

    
        
