
from functools import partial

buttons = {}

button_box = Element('buttons')
help_button = Element('help_button')

from blume import magic, farm

import asyncio

def add_button(key=None):

    def send_key(evt=None, key=None):
        print(key)

    buttons[len(buttons)] = key


def show_key(event, key=None):

    q = TheMagicRoundAbout.select('keys')
    q.put_nowait(key)
    
    print('show_key', key)
    
for ix in range(26):
    key = chr(ord('a')+ix)
    print('adding button', key) 
    button = help_button.clone(to=button_box)
    print(dir(button))
    button.element.innerText = key
    button.element.onClick = partial(show_key, key=key)

async def run(fm):

    await farm.start_and_run_farm(fm)

fm = farm.Farm()
    
pyscript.run_until_complete(run(farm))

    
