import numpy as np

async def main():

    from blume.examples import legendary
    #from gotu import dss

    log = Element('log')
    fig = Element('fig')
    aid = Element('help')

    words = [x.strip() for x in legendary.legend.__doc__.split()]
    words = np.array(words)

    log.write(str(words))

    cols = 5
    words = words[:cols * cols].reshape(cols, cols)

    leg = legendary.Legend(words)

    log.write(str(words), append=True)

    from blume import farm as land
    farm = land.Farm()

    log.write('got farm', append=True)
    farm.add(leg)
    #ds = dss.Dss()
    #farm.add(ds)
    farm.carpet.output = fig
    farm.shep.path.append(leg)
    
    await farm.start()
    global keypress
    def keys(event):
        log.write(f'kkk {event.key}')
        try:
            farm.carpet.keypress(event)
        except Exception as e:
            log.write(f'exception {e}')
    keypress = keys

    aid.write('xxxstarting up farm for dss no leg')
    await farm.run()

      
# close the global PyScript pyscript_loader
pyscript_loader.close()
print('about to run farm')
pyscript.run_until_complete(main())

