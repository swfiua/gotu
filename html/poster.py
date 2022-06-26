import matplotlib
matplotlib.use("module://matplotlib.backends.html5_canvas_backend")

import numpy as np
from blume import farm as land
from blume import magic

from functools import partial
import inspect
import traceback

tmra = magic.TheMagicRoundAbout
relay = magic.relay

def show_key(event, key=None):

    tmra.put_nowait(key, key)
    
    print('show_key', key)
    tmra.put_nowait('help', f'show_key {key}')

def set_up_buttons(shepherd):
    print('SETTING UP BUTTONS')

    button_box = Element('buttons')

    stdout = Element('stdout')
    stdout.clear()
    
    background = '#00ff00'
    bbe = button_box.element
    print(f'Number of CHILDREN before removal {len(bbe.children)}')
    for child in list(bbe.children):
        #bbe.removeChild(child)
        child.remove()
    print(f'Number of CHILDREN after removal {len(bbe.children)}')

    lastsheep = None
    for sheep, key, callback in shepherd.generate_key_bindings():
        if sheep != lastsheep:
            print(f'processing bindings for {sheep} {key}')
            div = document.createElement('div')
            div.className = 'evenly'

            button_box.element.appendChild(div)
            
        lastsheep = sheep

            
        button = document.createElement('Button')

        button.innerHTML = key
        button.style.background = background
        if key == ' ':
            button.innerHTML = 'Space'
        else:
            button.innerHTML = key * 4
        button.id = key
        button.className = 'cb'
        button.onclick = partial(show_key, key=key)
        div.appendChild(button)



async def run():

    from blume.examples import legendary

    log = Element('log')
    status = Element('status')


    words = [x.strip() for x in legendary.legend.__doc__.split()]
    words = np.array(words)

    #log.write(str(words))

    cols = 5
    words = words[:cols * cols].reshape(cols, cols)

    leg = legendary.Legend(words)

    #log.write(str(words), append=True)

    farm = land.Farm()

    status.write('got farm', append=True)

    status.write('adding legendary legend to farm', append=True)
    farm.add(leg)

    gotu = True
    if gotu:
        from gotu import dss
        from gotu.spiral import Spiral
        from gotu.wits import SolarSystem, get_args

        ds = dss.Dss()
        farm.add(ds)

        farm.add(Spiral())
        ssargs = get_args()
        ssargs.planets = True
        farm.add(SolarSystem(ssargs))

        
    button_relay = magic.spawn(relay(
        'oldgrey',
        partial(set_up_buttons, shepherd=farm.shep)))
    #set_up_buttons(shepherd=farm.shep)
    print('launching the farm')
    await land.start_and_run(farm)

      
# close the global PyScript pyscript_loader
pyscript_loader.close()
print('about to run farm')


print('launching async farm')
try:
    pyscript.run_until_complete(run())
except:
    traceback.print_exc()
    print('farm bailed out')

