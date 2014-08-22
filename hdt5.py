import random

import simpy

randomSeed = 10
procesos=25
intervalo=10
RAM=100

def source(env,number,intervalo,contador):
    for i in range(number):
        p = proceso(env,'Proceso%02d' % i, contador,tiempoProceso=1)
        env.process(p)
        t = random.expovariate(1.0 / intervalo)
        yield env.timeout(t)

def proceso(env,name,counter,tiempoProceso):
    arrive =env.now
    print ('%7.4f %s: Proceso' % (arrive,name))

    with counter.request() as req:
        instrucciones = random.uniform(1,10)
        results = yield req | env.timeout(instrucciones)

        wait = env.now - arrive

        if req in results:
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0/tiempoProceso)
            yield env.timeout(tib)
            print('%7.4f %s: Finished' % (env.now, name))
        else:
             print('%7.4f %s: ESPERANDO %6.3f' % (env.now, name, wait))

print ('Computadora')
random.seed(randomSeed)
env = simpy.Environment()

counter = simpy.Resource(env,capacity=1)
env.process(source(env,procesos,intervalo,counter))
env.run()
