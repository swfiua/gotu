
from matplotlib import pyplot, patches
plt = pyplot

fig = pyplot.figure()
ax = fig.add_axes((0,0,1,1))

patch = patches.Rectangle(
    (0, 0), 0.5, 0.5,
    facecolor='red')

ax.add_artist(patch)

# show the figure, image is not scaled as I would expect
plt.show()

# save as a png, image is scaled as I would expect
fig.savefig('foo.png')

# save as an svg, image matches the one in the FigureCanvas window.
fig.savefig('foo.svg')

# NB reversing the order of the two savefig calls produces images
# matching the FigureCanvas version.
