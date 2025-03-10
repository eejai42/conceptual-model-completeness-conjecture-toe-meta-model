#!/usr/bin/env python3
"""
A single Python script that matches your JSON rulebook, but uses a 4-argument
EVOLVE(...) function. This ensures final_wavefunction won't return None.

Make sure your QWalkRunner JSON formula is:
"formula": "EVOLVE(WavefunctionInitial.psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier)"
"""

import math
import numpy as np

###############################
# 1) BUILDING-BLOCK FUNCTIONS #
###############################

def SHIFT(psi_in, offsets):
    """
    SHIFT each spin component by the specified (dy,dx).
    Offsets is a list of length=8, e.g. for an 8D walk.
    """
    ny, nx, spin_dim = psi_in.shape
    psi_out = np.zeros_like(psi_in)
    for d, (dy, dx) in enumerate(offsets):
        rolled = np.roll(psi_in[:, :, d], shift=dy, axis=0)
        rolled = np.roll(rolled, shift=dx, axis=1)
        psi_out[:, :, d] = rolled
    return psi_out

def APPLY_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
    """
    Zero out wavefunction in 'barrier_row' except for the columns in slit ranges.
    """
    psi_out = psi_in.copy()
    psi_out[barrier_row, :, :] = 0
    psi_out[barrier_row, slit1_xstart:slit1_xend, :] = psi_in[barrier_row, slit1_xstart:slit1_xend, :]
    psi_out[barrier_row, slit2_xstart:slit2_xend, :] = psi_in[barrier_row, slit2_xstart:slit2_xend, :]
    return psi_out

def COLLAPSE_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
    """
    Example measurement-based barrier: amplitude outside slits is lost.
    For demonstration, we place collapsed amplitude in direction=0.
    """
    psi_out = np.zeros_like(psi_in)
    row_intens = np.sum(np.abs(psi_in[barrier_row, :, :])**2, axis=-1)
    keep = np.zeros_like(row_intens)
    keep[slit1_xstart:slit1_xend] = row_intens[slit1_xstart:slit1_xend]
    keep[slit2_xstart:slit2_xend] = row_intens[slit2_xstart:slit2_xend]
    amps = np.sqrt(keep)
    psi_out[barrier_row, :, 0] = amps
    return psi_out

def GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(src_y, sigma_y, ny, nx, spin_dim):
    """
    Returns shape=(ny,nx,spin_dim), Gaussian in y, uniform in x & spin.
    """
    arr = np.zeros((ny, nx, spin_dim), dtype=np.complex128)
    ycoords = np.arange(ny)
    gauss_y = np.exp(-0.5 * ((ycoords - src_y)/sigma_y)**2)
    norm = np.sqrt(np.sum(np.abs(gauss_y)**2))
    gauss_y /= norm

    for d in range(spin_dim):
        for x in range(nx):
            arr[:, x, d] = gauss_y
    return arr

###############################
# THE 4-ARG EVOLVE FUNCTION
###############################
def EVOLVE(psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier):
    """
    4-argument time evolution that references some global or fixed coin/op/offsets/barrier logic.
    We'll just define them here for demonstration. 
    If you want them from QWalkRunner fields, do so inside this function or pass them in.

    Steps:
      1) 8D coin + SHIFT + barrier for steps_to_barrier
      2) optional collapse
      3) 8D coin + SHIFT + barrier for steps_after_barrier
    """
    # Hard-code an 8D DFT coin
    coin_matrix = np.fft.fft(np.eye(8)) / np.sqrt(8)
    # Hard-code offsets
    offsets = [
        (-1,  0), 
        (-1, +1), 
        ( 0, +1), 
        (+1, +1),
        (+1,  0), 
        (+1, -1), 
        ( 0, -1), 
        (-1, -1),
    ]
    # Hard-code a barrier row, slits, etc. 
    # For demonstration, let's place them at row=100, with 2 slits each 5 wide
    # (You can replace these with global references or keep them consistent with your Grid)
    barrier_row = 100
    slit1_xstart = 90
    slit1_xend   = 95
    slit2_xstart = 105
    slit2_xend   = 110

    psi = psi_init
    for _ in range(steps_to_barrier):
        # coin step
        ny, nx, spin_dim = psi.shape
        psi_flat = psi.reshape(ny*nx, spin_dim)
        out_flat = psi_flat @ coin_matrix.T
        psi_coin = out_flat.reshape((ny,nx,spin_dim))

        # shift step
        psi_shift = SHIFT(psi_coin, offsets)

        # barrier step
        psi = APPLY_BARRIER(psi_shift, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)

    if collapse_barrier:
        psi = COLLAPSE_BARRIER(psi, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)

    for _ in range(steps_after_barrier):
        ny, nx, spin_dim = psi.shape
        psi_flat = psi.reshape(ny*nx, spin_dim)
        out_flat = psi_flat @ coin_matrix.T
        psi_coin = out_flat.reshape((ny,nx,spin_dim))

        psi_shift = SHIFT(psi_coin, offsets)
        psi = APPLY_BARRIER(psi_shift, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)

    return psi

###############################
# 2) AUTO-GENERATED CLASSES
###############################

class Grid:
    def __init__(self, **kwargs):
        self.nx = kwargs.get('nx')
        self.ny = kwargs.get('ny')
        self.Lx = kwargs.get('Lx')
        self.Ly = kwargs.get('Ly')
        self.barrier_y_phys = kwargs.get('barrier_y_phys')
        self.detector_y_phys = kwargs.get('detector_y_phys')
        self.slit_width = kwargs.get('slit_width')
        self.slit_spacing = kwargs.get('slit_spacing')
        self.boundary_conditions = kwargs.get('boundary_conditions')

    @property
    def dx(self):
        # formula: DIVIDE(Lx,nx)
        return (self.Lx / self.nx)

    @property
    def dy(self):
        # formula: DIVIDE(Ly,ny)
        return (self.Ly / self.ny)

    @property
    def barrier_row(self):
        # formula: FLOOR(DIVIDE(ADD(barrier_y_phys,DIVIDE(Ly,2)),dy))
        return math.floor(((self.barrier_y_phys + (self.Ly / 2)) / self.dy))

    @property
    def detector_row(self):
        # formula: FLOOR(DIVIDE(ADD(detector_y_phys,DIVIDE(Ly,2)),dy))
        return math.floor(((self.detector_y_phys + (self.Ly / 2)) / self.dy))

    @property
    def center_x(self):
        # formula: FLOOR(DIVIDE(nx,2))
        return math.floor((self.nx / 2))

    @property
    def slit1_xstart(self):
        # formula: SUBTRACT(center_x,FLOOR(DIVIDE(slit_spacing,2)))
        return (self.center_x - math.floor((self.slit_spacing / 2)))

    @property
    def slit1_xend(self):
        # formula: ADD(slit1_xstart,slit_width)
        return (self.slit1_xstart + self.slit_width)

    @property
    def slit2_xstart(self):
        # formula: ADD(center_x,FLOOR(DIVIDE(slit_spacing,2)))
        return (self.center_x + math.floor((self.slit_spacing / 2)))

    @property
    def slit2_xend(self):
        # formula: ADD(slit2_xstart,slit_width)
        return (self.slit2_xstart + self.slit_width)

class CoinOperator:
    def __init__(self, **kwargs):
        self.Matrix = kwargs.get('Matrix')
        self.seed = kwargs.get('seed')
        self.construction_method = kwargs.get('construction_method')
        self.construction_params = kwargs.get('construction_params')

    @property
    def UnitarityCheck(self):
        # formula: EQUAL(MULTIPLY(Matrix,CONJUGATE_TRANSPOSE(Matrix)),IDENTITY(8))
        return np.allclose(np.matmul(self.Matrix, self.Matrix.conj().T), np.eye(8))

class WavefunctionInitial:
    def __init__(self, **kwargs):
        self.src_y = kwargs.get('src_y')
        self.sigma_y = kwargs.get('sigma_y')
        self.kx = kwargs.get('kx')
        self.ky = kwargs.get('ky')
        self.Grid = None  # set externally if needed

    @property
    def psi_init(self):
        # formula: GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(src_y, sigma_y, Grid.ny, Grid.nx, 8)
        if not self.Grid:
            raise ValueError("WavefunctionInitial: must set self.Grid before calling psi_init.")
        return GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(self.src_y, self.sigma_y, self.Grid.ny, self.Grid.nx, 8)

class CoinStep:
    def __init__(self, **kwargs):
        self.psi_in = kwargs.get('psi_in')
        self.coin_matrix = kwargs.get('coin_matrix')

    @property
    def psi_out(self):
        # formula: MATMUL(psi_in, TRANSPOSE(coin_matrix))
        return np.matmul(self.psi_in, self.coin_matrix.T)

class ShiftStep:
    def __init__(self, **kwargs):
        self.psi_in = kwargs.get('psi_in')
        self.offsets = kwargs.get('offsets')

    @property
    def psi_out(self):
        # formula: SHIFT(psi_in, offsets)
        return SHIFT(self.psi_in, self.offsets)

class BarrierStep:
    def __init__(self, **kwargs):
        self.psi_in = kwargs.get('psi_in')
        self.barrier_row = kwargs.get('barrier_row')
        self.slit1_xstart = kwargs.get('slit1_xstart')
        self.slit1_xend = kwargs.get('slit1_xend')
        self.slit2_xstart = kwargs.get('slit2_xstart')
        self.slit2_xend = kwargs.get('slit2_xend')

    @property
    def psi_out(self):
        # formula: APPLY_BARRIER(...)
        return APPLY_BARRIER(self.psi_in, self.barrier_row,
                             self.slit1_xstart, self.slit1_xend,
                             self.slit2_xstart, self.slit2_xend)

class CollapseBarrierStep:
    def __init__(self, **kwargs):
        self.psi_in = kwargs.get('psi_in')
        self.barrier_row = kwargs.get('barrier_row')
        self.slit1_xstart = kwargs.get('slit1_xstart')
        self.slit1_xend = kwargs.get('slit1_xend')
        self.slit2_xstart = kwargs.get('slit2_xstart')
        self.slit2_xend = kwargs.get('slit2_xend')
        self.collapse_method = kwargs.get('collapse_method')

    @property
    def psi_out(self):
        # formula: COLLAPSE_BARRIER(...)
        return COLLAPSE_BARRIER(self.psi_in,
                                self.barrier_row,
                                self.slit1_xstart,
                                self.slit1_xend,
                                self.slit2_xstart,
                                self.slit2_xend)

class WavefunctionNorm:
    def __init__(self, **kwargs):
        self.psi_in = kwargs.get('psi_in')

    @property
    def total_norm(self):
        # formula: SUM(ABS(psi_in)^2)
        return np.sum(np.abs(self.psi_in)**2)

class DetectorAmplitude:
    def __init__(self, **kwargs):
        self.psi_in = kwargs.get('psi_in')
        self.detector_row = kwargs.get('detector_row')

    @property
    def row_amp(self):
        # formula: SLICE(psi_in, axis=0, index=detector_row)
        # we do a direct slice
        return self.psi_in[self.detector_row, :, :]

class DetectorIntensity:
    def __init__(self, **kwargs):
        self.row_amp = kwargs.get('row_amp')

    @property
    def intensity_1d(self):
        # formula: SUM(ABS(row_amp)^2, axis=-1)
        return np.sum(np.abs(self.row_amp)**2, axis=-1)

class QWalkRunner:
    def __init__(self, **kwargs):
        self.steps_to_barrier = kwargs.get('steps_to_barrier')
        self.steps_after_barrier = kwargs.get('steps_after_barrier')
        self.collapse_barrier = kwargs.get('collapse_barrier')
        self.step_order = kwargs.get('step_order')  # not used here, but stored

    @property
    def final_wavefunction(self):
        """
        Original formula: EVOLVE(WavefunctionInitial.psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier)
        """
        # Actually call our 4-arg EVOLVE function
        # We do need a reference to "WavefunctionInitial.psi_init". For demonstration, we'll
        # assume it is some global or stored reference. Typically you'd wire this up or pass it in.
        # For now, let's just raise an error if we haven't set it:

        if not hasattr(self, 'psi_init'):
            # In many setups, you'd store a reference:
            #   self.psi_init = wfi.psi_init
            # from your main code or define a way to link them automatically
            raise ValueError("QWalkRunner: please set runner.psi_init = wavefunction_array.")
        
        return EVOLVE(self.psi_init,
                      self.steps_to_barrier,
                      self.steps_after_barrier,
                      self.collapse_barrier)

####################################
# END OF FILE
####################################
