import matplotlib.pyplot as plt
import numpy as np


def initPlot(mn, labels, lim, figSize=(16, 9), share=('none', 'none'),
        spkw=None, gskw=None):
    '''
    Initialize a plot with both axis label and tick shown

    Parameters
    ----------
    mn: 2-tuple, (number of rows, number of columns)
    labels: list of 2-tuple str, string for x and y axis. Allow latex.
    lim: list of 2-tuple, limit for x and y axis.
    figSize: 2-tuple, default (16, 9). Size of the figure in inch. DPI is fixed
             at 300.
    share: 2-tuple, default ('none', 'none'). Whether to share x or y axis.
    spkw: dict, keywords to pass to add_subplot
    gskw: dict, keywords to pass to GridSpec

    Returns
    -------
    fig: matplotlib.pyplot.Figure, the figure itself
    ax: matplotlib.pyplot.axes, the axes in 2D array
    '''
    # Set up the Figure and axes
    fig, ax = plt.subplots(nrows=mn[0], ncols=mn[1], sharex=share[0],
            sharey=share[1], squeeze=False, subplot_kw=spkw, gridspec_kw=gskw,
            figsize=figSize, dpi=300)
    # Set up the limit and labels for each axes
    for i in range(mn[0]):
        for j in range(mn[1]):
            num = i * mn[1] + j
            ax[i][j].set_xlabel(labels[num][0], fontsize=24)
            ax[i][j].set_xlim(lim[num][0])
            ax[i][j].set_ylabel(labels[num][1], fontsize=24)
            ax[i][j].set_ylim(lim[num][1])
            ax[i][j].tick_params(axis='both', which='major', labelsize=20)
    return fig, ax


def plotLine(ax, x=None, y=None, lw=2, ls='--', c='#000000FF', label=None):
    '''
    Plot a line

    Parameters
    ----------
    ax: matplotlib.pyplot.axes, the axes to plot on
    x: int/float, default None. x coord
    y: int/float, default None. y coord
    lw: int, default 2. Width of the line
    ls: str, default '--'. String for linestyle
    c: str, default '#000000FF'. Hex colorcode with transparency.
    label: str, default None. Legend

    Returns
    -------
    None
    '''
    if x is not None:
        ax.plot([x, x], [-65535.0, 65535.0], ls=ls, c=c, label=label,
                marker='None', lw=lw)
    if y is not None:
        ax.plot([-65535.0, 65535.0], [y, y], ls=ls, c=c, label=label,
                marker='None', lw=lw)


def plot_sarm(ax, xunit='L_Z'):
    if xunit == 'L_Z':
        plotLine(ax, x=1012.389, c='#008000FF', label='Scutum')
        plotLine(ax, x=1540.291, c='#FF00FFFF', label='Sgr')
        plotLine(ax, x=1945.641, c='#0000FFFF', label='Local')
        plotLine(ax, x=2148.064, c='#FF0000FF', label='Persus')
        plotLine(ax, x=2800.568, c='#CCCC00FF', label='Outer')
        plotLine(ax, x=1451.189, c='#00BFFFFF', label='Bar corration', ls='-.')
    else:
        raise NotImplementedError('Can only draw spiral arms in Lz')


def formatColorBar(cb, cblabel):
    '''
    Format the color bar by adding a fontsize=24 label and changing the tick
    label to size 20.

    Parameters
    ----------
    cb: matplolib.colorbar intance, the color bar to modify
    cblabel: str, label for the color bar
    '''
    cb.set_label(cblabel, fontsize=24)
    cb.ax.tick_params(labelsize=20)


def drawGalacticBeaconXY(ax, sun=True, glon=4, gc=True, glon_r=2.0):
    '''
    Draw the positon of the following "beacons" in X-Y place
    The Sun, Galactic longitude lines, and/or galactic center

    Parameters
    ----------
    ax: matplotlib.Axes instance, the axes to draw on
    sun: boolean, default True. Draw sun or not
    glon: int, default 4. How many equal galactic longitude lines to draw
    gc: boolean, default True. Draw galactic center or not
    glon_r, float, default 2.0. How far the glon label be placed from Sun

    Returns
    -------
    None
    '''
    if sun:
        ax.plot([-8.34], [0.0], marker='o', markersize=12, color='k')
    if glon > 0 and glon_r > 0.0:
        tmp = np.linspace(0.0, 1.0, glon, endpoint=False)
        for i in range(len(tmp)):
            each= tmp[i]
            ax.plot([-8.34 + 9999.0 * np.cos(each * 2.0 * np.pi), -8.34],
                    [9999.0 * np.sin(each * 2.0 * np.pi), 0.0], 'k--')
            if glon < 6 or i % (int(glon / 4)) == 0:
                ax.text(-8.34 + glon_r * np.cos(each * 2.0 * np.pi), 
                        glon_r * np.sin(each * 2.0 * np.pi),
                        r'l=%(l)d$^\circ$' % {'l': int(each * 360.0)}, 
                        fontsize=20)
    if gc:
        ax.plot([0.0], [0.0], marker='X', markersize=12, color='k')
