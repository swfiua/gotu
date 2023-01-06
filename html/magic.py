            from collections import deque
            from js import document
            from pyodide import create_proxy

            import matplotlib
            matplotlib.use("module://matplotlib_pyodide.html5_canvas_backend")

            from blume import farm, magic
            from gotu import spiral

            ss = spiral.Spiral()
            land = farm.Farm()
            land.add(ss)
            
            history = deque()
            
            tmra = magic.TheMagicRoundAbout

            stdin = document.getElementById("input")

            def keydown(event, *args):

                if event.key == 'Enter':
                    tmra.put_nowait(stdin.value, 'stdin')
                    history.appendleft(stdin.value)
                    stdin.value = ''
                    return True

                elif event.key == 'Tab':
                    completion = land.shell.complete(stdin.value)
                    if completion:
                       stdin.value = completion
                    event.preventDefault()
                    return True
                elif event.key == "ArrowUp":
                    # Up pressed
                    stdin.value = history[0]
                    history.rotate(-1)

                elif event.key == "ArrowDown":
                    history.rotate(1)
                    # Down pressed
                    stdin.value = history[0]

                return False

            stdin.addEventListener("keydown", create_proxy(keydown))


            await farm.start_and_run(land)
