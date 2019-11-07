from .plot_crt import plotLine
from astropy.coordinates import Distance, Galactocentric, ICRS, SkyCoord
from astropy.units as u
import numpy as np


# Spiral arm information dictionary
# Format: {name: [R_ref, beta_ref, width, psi, beta_min, beta_max, color],}
# 2014ApJ...783..130R
sa_reid2014 = {'Scutum': [5.0, 27.6, 0.17, 19.8, 3.0, 101.0, '#00FFFFFF'],
               'Sgr': [6.6, 25.6, 0.26, 6.9, -2.0, 68.0, '#FF00FFFF'],
               'Local': [8.4, 8.9, 0.33, 12.8, -8.0, 27.0, '#0000FFFF'],
               'Persus': [9.9, 14.2, 0.38, 9.4, -21.0, 88.0, '#000000FF'],
               'Outer': [13.0, 18.6, 0.63, 13.8, -6.0, 56.0, '#FF0000FF']}


def saHelper(r_ref, beta_ref, width, psi, beta_min, beta_max):
    '''
    Helper function for plotting spiral arm.

    Assume astropy galactocentric corrdinate convension.

    Parameters
    ----------
    All parameters are parameters of spiral arm

    Returns
    -------
    x, y: the center of the spiral arm
    x_i, y_i: the inner limit of the spiral arm
    x_o. y_o: the outer limit of the spiral arm
    '''
    beta = np.linspace(beta_min, beta_max, 500)
    psi_rad = psi * np.pi / 180.0
    r_sp = r_ref * np.exp(-(beta - beta_ref) * np.tan(psi_rad) * np.pi / 180.0)
    theta = (180.0 - beta) * np.pi / 180.0
    x = r_sp * np.cos(theta)
    y = r_sp * np.sin(theta)
    x_i = (r_sp - width) * np.cos(theta)
    y_i = (r_sp - width) * np.sin(theta)
    x_o = (r_sp + width) * np.cos(theta)
    y_o = (r_sp + width) * np.sin(theta)
    return x, y, x_i, y_i, x_o, y_o
    

def plotSArmXY(ax, sa_dict):
    '''
    Plot spiral arm for X-Y plot.

    Assume astropy.coordinates.galactocentric convension

    Parameters
    ----------
    ax: matplotlib.axes, the axes to plot on
    sa_dict: dict, the dictionary containing spiral arm information

    Returns
    -------
    None
    '''
    for each in sa_dict.keys():
        v = sa_dict[each]
        x, y, xi, yi, xo, yo = saHelper(v[0], v[1], v[2], v[3], v[4], v[5])
        ax.plot(x, y, '-', color=v[6], lw=2, label=each)
        ax.plot(xi, yi, '--', color=v[6], lw=0.5)
        ax.plot(xo, yo, '--', color=v[6], lw=0.5)


def plotSArm(ax, xunit='L_Z'):
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


def helio2galacto(ra, dec, parallax, pmra, pmdec, rv, dist=None, 
                  gc=(266.4051, -28.936175), r_sun=8.30, z_sun=27.0,
                  v_sun=(11.1, 232.24, 7.25)):
    '''
    Heliocentric coordinates to galactocentric coordinates. Please add units
    before feeding them in the function.

    Cartesian system: GC at (0, 0), Sun at (-r_sun, 0), right-handed
    Cylindrical system: GC at (0, 0), Sun at (r_sun, +/-180), left-handed

    Parameters
    ----------
    ra, dec: numpy.ndarray. RA and Dec in degrees
    parallax: numpy.ndarray. Parallax in mas
    pmra, pmdec: numpy.ndarray. Proper motion in mas/yr
    rv: numpy.ndarray. Radial velocity in km/s
    dist: numpy.ndarray, default None. Helio-distance with units in kpc
    gc: 2-tuple of float, default (266.4051, -28.936175). RA and Dec of 
        Galactic Center in ICRS with units in degrees
    r_sun: float, default 8.30. Distance from Sun to GC in kpc
    z_sun: float, default 27.0. Distance from Sun to Galactic plane in pc
    v_sun: 3-tuple of loat, default (11.1, 232.24, 7.25). UVW of the velocity
           of the Sun wrt GC in km/s

    Returns
    -------
    X, Y, Z: numpy.ndarray. Galactocentric cartesian coordinates in kpc
    V_X, V_Y, V_Z: numpy.ndarray. Galactocentric cartesian velocity in km/s
    R, PHI: numpy.ndarray. Galactocentric cylindrical coordinates in (kpc, deg)
    V_R, V_PHI: numpy.ndarray. Galactocentric cylindrical velocity in km/s
    '''
    if dist is not None:
        d = dist
    else:
        d = Distance(parallax=parallax, allow_negative=True).to(u.kpc)
    sc = SkyCoord(ra=ra, dec=dec, distance=d, pm_ra_cosdec=pmra,
                  pm_dec=pmdec, radial_velocity=rv)
    galc = sc.transform_to(Galactocentric)
    # Save to file
    X = galc.x
    Y = galc.y
    Z = galc.z
    V_X = galc.v_x
    V_Y = galc.v_y
    V_Z = galc.v_z
    # Transform to cylindrical
    galc.representation_type = 'cylindrical'
    R = galc.rho
    PHI = galc.phi.to(u.deg)
    V_R = galc.d_rho.to(u.km / u.s)
    V_PHI = -galc.d_phi.to(u.rad / u.s) * galc.rho.to(u.km) / u.rad
    return X, Y, Z, V_X, V_Y, V_Z, R, PHI, V_R, V_PHI
