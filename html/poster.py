import numpy as np
from blume import farm as land
from blume import magic

class Helper(magic.Ball):

    def __init__(self, element, channel=None):

        super().__init__()

        channel = channel or element.id

        self.channel = channel
        self.element = element
        #id(self.radii)
        self.element.write(f'hello from {self.channel} helper')
        self.element.write(f'roundabout id {id(magic.TheMagicRoundAbout)}')

    async def run(self):

        await self.put('HELPER STARTING UP', 'help')

        while True:
            msg = await self.get(self.channel)
            print(f'channel {self.channel} got message')
            self.element.clear()
            for line in msg.split('\n'):
                self.element.write(line, append=True)

def main():

    from blume.examples import legendary

    log = Element('log')
    fig = Element('fig')
    hhh = Element('help')

    helpers = {}
    for channel in channels:
        helpers[channel] = Helper(Element(channel))

    words = [x.strip() for x in legendary.legend.__doc__.split()]
    words = np.array(words)

    #log.write(str(words))

    cols = 5
    words = words[:cols * cols].reshape(cols, cols)

    leg = legendary.Legend(words)

    log.write(str(words), append=True)

    farm = land.Farm()

    #farm.add(Helper(), background=True)

    log.write('got farm', append=True)
    farm.add(leg)

    farm.helpers = helpers

    gotu = True
    if gotu:
        from gotu import dss
        from gotu.spiral import Spiral
        from gotu.wits import SolarSystem, get_args

        ds = dss.Dss()
        farm.add(ds)
        farm.shep.path.append(ds)

        farm.add(Spiral())
        ssargs = get_args()
        ssargs.planets = True
        farm.add(SolarSystem(ssargs))

    farm.carpet.output = fig
    farm.shep.hhh = hhh
    
    global keypress
    def keys(event):
        log.write(f'kkk {event.key}')
        try:
            farm.carpet.keypress(event)
        except Exception as e:
            log.write(f'exception {e}')
    keypress = keys

    return farm

tmra = magic.TheMagicRoundAbout

async def send_key(event):

    await tmra.put(event.key, 'keys')
    

def show_key(event):

    global keypress
    pyscript.write('log', f'key pressed {event}', append=True)
    #pyscript.write('log', dir(event), append=True)
    pyscript.write('log', f'key value {event.key}', append=True)
    #pyscript.write('log', f'{type(keypress)}', append=True)
    keypress(event)
    pyscript.write('log', f'{farm.carpet}', append=True)

channels = ['help', 'interact', 'status']


def key_presser(key, event=None):

    tmra.put_nowait(f'keypress {key}', 'help')
    tmra.put_nowait(key, 'keys')


from functools import partial    
run_current2 = partial(key_presser, 'r')
more_axes = partial(key_presser, '+')
less_axes = partial(key_presser, '-')
interact = partial(key_presser, 'i')
nexti = partial(key_presser, ',')
next_ball = partial(key_presser, 'n')
up_tree = partial(key_presser, 'u')
help_cb = partial(key_presser, 'h')

                    

async def run(farm):

    helpers = {}
    for channel, helper in farm.helpers.items():
        print(channel)
        print(dir(helper))
        try:
            helper.element.write(f'xxx roundabout id {id(magic.TheMagicRoundAbout)}')
        except Exception as e:
            import traceback
            traceback.print_exc()

        task = magic.spawn(helper.run())
        print(dir(task))
        print(task.get_name())
        print('task done:')
        print(task.done())

    #await helpers['help'].put('status', 'time to launch farm')
    #await asyncio.sleep(3)
    #await helpers['help'].put('status', 'launch time...')
    #await asyncio.sleep(3)
    await land.start_and_run(farm)

      
# close the global PyScript pyscript_loader
pyscript_loader.close()
print('about to run farm')
farm = main()
print(farm.helpers.keys())
print('finished main')
for key in farm.nodes.keys():
    print(repr(key))
    print(type(key))


print('launching async farm')
try:
    pyscript.run_until_complete(run(farm))
except:
    print('farm bailed out')

