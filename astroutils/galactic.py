from .plot_crt import plotLine
import numpy as np


def plot_sarm(ax, xunit='L_Z'):
    '''
    Plot spiral arms for 1-d plot. Data from Reid 2014

    Parameters
    ----------
    ax: matplotlib.axes, the axes to plot on
    xunit: str, default 'L_Z'. The unit of x axis

    Returns
    -------
    None

    Raises
    ------
    NotImplementedError
    '''
    if xunit == 'L_Z':
        plotLine(ax, x=1012.389, c='#008000FF', label='Scutum')
        plotLine(ax, x=1540.291, c='#FF00FFFF', label='Sgr')
        plotLine(ax, x=1945.641, c='#0000FFFF', label='Local')
        plotLine(ax, x=2148.064, c='#FF0000FF', label='Persus')
        plotLine(ax, x=2800.568, c='#CCCC00FF', label='Outer')
        plotLine(ax, x=1451.189, c='#00BFFFFF', label='Bar corration', ls='-.')
    else:
        raise NotImplementedError('Can only draw spiral arms in Lz')


def drawGalacticBeaconXY(ax, sun=8.34, glon=4, gc=True, glon_r=2.0):
    '''
    Draw the positon of the following "beacons" in X-Y place
    The Sun, Galactic longitude lines, and/or galactic center

    Assume astropy galacticocentric coordinate system (Sun at -x)

    Parameters
    ----------
    ax: matplotlib.Axes instance, the axes to draw on
    sun: float, default 8.34. Sun to GC in kpc. If None, skip drawing sun
    glon: int, default 4. How many equal galactic longitude lines to draw
    gc: boolean, default True. Draw galactic center or not
    glon_r, float, default 2.0. How far the glon label be placed from Sun

    Returns
    -------
    None
    '''
    if sun is not None:
        ts = 0.0 - sun
        ax.plot([ts], [0.0], marker='o', markersize=12, color='k')
    else:
        ts = -8.34
    if glon > 0 and glon_r > 0.0:
        tmp = np.linspace(0.0, 1.0, glon, endpoint=False)
        for i in range(len(tmp)):
            each= tmp[i]
            ax.plot([ts + 9999.0 * np.cos(each * 2.0 * np.pi), ts],
                    [9999.0 * np.sin(each * 2.0 * np.pi), 0.0], 'k--')
            if glon < 6 or i % (int(glon / 4)) == 0:
                ax.text(ts + glon_r * np.cos(each * 2.0 * np.pi), 
                        glon_r * np.sin(each * 2.0 * np.pi),
                        r'l=%(l)d$^\circ$' % {'l': int(each * 360.0)}, 
                        fontsize=20)
    if gc:
        ax.plot([0.0], [0.0], marker='X', markersize=12, color='k')
