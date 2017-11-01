def showMap(figure, axes, lenx, leny, X, Y, slice, cm, lines):
    axes.cla()
    im = axes.imshow(slice, cmap = cm)
    if lines:
        axes.plot(range(0,leny), X, color = 'red')
        axes.plot(Y, range(0,lenx), color = 'red')
    figure.show()


def plotSpectrum(figure, axes, wavenumber, counts, point, lines):
    axes.cla()
    axes.plot(wavenumber, counts)
    if lines:
        axes.plot([wavenumber[point], wavenumber[point]], [0, 100 + max(counts)])
    axes.axis([min(wavenumber), max(wavenumber), 0, 100 + max(counts)])
    figure.show()
