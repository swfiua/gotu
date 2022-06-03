import numpy as np
from blume import farm as land

def main():

    from blume.examples import legendary
    from gotu import dss

    log = Element('log')
    fig = Element('fig')
    hhh = Element('help')

    words = [x.strip() for x in legendary.legend.__doc__.split()]
    words = np.array(words)

    #log.write(str(words))

    cols = 5
    words = words[:cols * cols].reshape(cols, cols)

    leg = legendary.Legend(words)

    log.write(str(words), append=True)

    farm = land.Farm()

    log.write('got farm', append=True)
    farm.add(leg)

    ds = dss.Dss()
    
    farm.add(ds)
    farm.carpet.output = fig
    farm.shep.path.append(ds)

    from gotu.spiral import Spiral
    farm.add(Spiral())
    from gotu.wits import SolarSystem, get_args
    ssargs = get_args()
    ssargs.planets = True
    farm.add(SolarSystem(ssargs))
    
    global keypress
    def keys(event):
        log.write(f'kkk {event.key}')
        try:
            farm.carpet.keypress(event)
        except Exception as e:
            log.write(f'exception {e}')
    keypress = keys

    return farm

def show_key(event):

    global keypress
    pyscript.write('log', f'key pressed {event}', append=True)
    #pyscript.write('log', dir(event), append=True)
    pyscript.write('log', f'key value {event.key}', append=True)
    #pyscript.write('log', f'{type(keypress)}', append=True)
    keypress(event)
    pyscript.write('log', f'{farm.carpet}', append=True)
    
      
# close the global PyScript pyscript_loader
pyscript_loader.close()
print('about to run farm')
farm = main()
for key in farm.nodes.keys():
    print(key)
    print(type(key))
pyscript.run_until_complete(land.start_and_run(farm))

