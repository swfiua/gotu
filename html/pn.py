import panel as pn

#print(dir(pn))
#print(dir(pn.widgets))
#print(pn.widgets.Button.__doc__)

buttons = [pn.widgets.Button(name=chr(ord('a') + x)) for x in range(26)]
print(f'number of buttons {len(buttons)}')
pn.Row(*buttons).servable(target='buttons')

print('matplotlib time')
from matplotlib import pyplot
fig, ax = pyplot.subplots()
ax.plot(range(10))

foo =pn.pane.Matplotlib(fig).servable(target='fig')

bar = pn.pane.Markdown("""
Pretty *please* show this for me.
""").servable(target='help')

print('done')
