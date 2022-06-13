import numpy as np
from blume import farm as land
from blume import magic

from functools import partial
import inspect
import traceback

class Helper(magic.Ball):

    def __init__(self, element, channel=None):

        super().__init__()

        channel = channel or element

        self.channel = channel
        self.element = element

    async def run(self):

        await self.put('HELPER STARTING UP', 'help')

        while True:
            msg = await self.get(self.channel)
            print(f'channel {self.channel} got message')
            element = Element(self.element)
            element.clear()
            for line in msg.split('\n'):
                element.write(line, append=True)

async def relay(channel, callback):

    print(f'listening for messages from {channel}')
    while True:
        print(f'RELAY WAITING FOR MESSAGE FROM {channel}')
        msg = await magic.TheMagicRoundAbout.get(channel)
        print(f'message from {channel}: {msg}')
        try:
            result = callback()
            print(f'{callback} RETURNED SUCCESSFULLY')
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f'{channel} relay exception for {callback}')
            
        if inspect.iscoroutine(result):
            try:
                print(f'awaiting {result}')
                await result
            except:
                print(f'{channel} relay exception awaiting {result}')
        
                
tmra = magic.TheMagicRoundAbout

async def send_key(event):

    await tmra.put(event.key, 'keys')
    


channels = ['interact', 'status', 'help']


def show_key(event, key=None):

    tmra.put_nowait(key, 'keys')
    
    print('show_key', key)
    tmra.put_nowait('help', f'show_key{key}')

def set_up_buttons(shepherd):
    print('SETTING UP BUTTONS')
    button_box = Element('buttons')
    help_button = Element('help_button')

    background = '#00ff00'
    bbe = button_box.element
    print(f'Number of CHILDREN before removal {len(bbe.children)}')
    for child in list(bbe.children):
        #bbe.removeChild(child)
        child.remove()
    print(f'Number of CHILDREN after removal {len(bbe.children)}')

    help_button.element.onclick = partial(show_key, key='h')

    lastsheep = None
    for sheep, key, callback in shepherd.generate_key_bindings():
        if sheep != lastsheep:
            print(f'processing bindings for {sheep} {key}')
            #bb = button_box.element.append(Element('div').element)
            
        lastsheep = sheep

            
        button = document.createElement('Button')

        print(f'bbbbbbbbbbbbbbbbbbbbbbbb {button}')
        button.innerHTML = key
        button.style.background = background
        if key == ' ':
            button.innerHTML = 'Space'
        else:
            button.innerHTML = key
        button.id = key
        button.onclick = partial(show_key, key=key)
        button_box.element.appendChild(button)



async def run():

    from blume.examples import legendary

    log = Element('log')
    status = Element('status')
    fig = Element('fig')


    words = [x.strip() for x in legendary.legend.__doc__.split()]
    words = np.array(words)

    #log.write(str(words))

    cols = 5
    words = words[:cols * cols].reshape(cols, cols)

    leg = legendary.Legend(words)

    #log.write(str(words), append=True)

    farm = land.Farm()

    #farm.add(Helper(), background=True)

    status.write('got farm', append=True)

    for channel in channels:
        status.write(f'adding helper for {channel}', append=True)
        helper = Helper(channel)
        farm.add_node(helper, background=True)

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

    farm.carpet.output = fig

        
    button_relay = magic.spawn(relay(
        'oldgrey',
        partial(set_up_buttons, shepherd=farm.shep)))
    #set_up_buttons(shepherd=farm.shep)
    print('launching the farm')
    await land.start_and_run(farm)

      
# close the global PyScript pyscript_loader
pyscript_loader.close()
print('about to run farm')

# connect temporary butts that actually work
from functools import partial    
run_current2 = partial(show_key, key='r')
more_axes = partial(show_key, key='+')
less_axes = partial(show_key, key='-')
interact = partial(show_key, key='i')
nexti = partial(show_key, key=',')
next_ball = partial(show_key, key='n')
up_tree = partial(show_key, key='u')
help_cb = partial(show_key, key='h')


print('launching async farm')
try:
    pyscript.run_until_complete(run())
except:
    traceback.print_exc()
    print('farm bailed out')

