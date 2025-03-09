"""
Auto-generated Python code from your quantum-walk rulebook.
It includes building-block definitions (SHIFT, BARRIER, EVOLVE, etc.)
and the classes with calculated fields referencing them.
"""
import math
import numpy as np

# ----- Building Block Lambdas (auto-injected) -----

def APPLY_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
    """
    Zero out wavefunction in barrier_row except for the slit columns.
    """
    import numpy as np
    psi_out = psi_in.copy()
    psi_out[barrier_row,:,:] = 0
    psi_out[barrier_row, slit1_xstart:slit1_xend, :] = psi_in[barrier_row, slit1_xstart:slit1_xend, :]
    psi_out[barrier_row, slit2_xstart:slit2_xend, :] = psi_in[barrier_row, slit2_xstart:slit2_xend, :]
    return psi_out

def COLLAPSE_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
    """
    Example barrier measurement: amplitude outside the slits is lost.
    """
    import numpy as np
    psi_out = np.zeros_like(psi_in)
    # sum intensities across directions
    row_intens = np.sum(np.abs(psi_in[barrier_row,:,:])**2, axis=-1)
    keep = np.zeros_like(row_intens)
    keep[slit1_xstart:slit1_xend] = row_intens[slit1_xstart:slit1_xend]
    keep[slit2_xstart:slit2_xend] = row_intens[slit2_xstart:slit2_xend]
    amps = np.sqrt(keep)
    # place them in direction=0 (say "up")
    d_up = 0
    psi_out[barrier_row, :, d_up] = amps
    return psi_out

def EVOLVE(psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier,
           coin_matrix, offsets,
           barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
    """
    Example function to do a quantum-walk evolution with a single time loop.
    coin -> shift -> barrier, repeated 'steps_to_barrier' times,
    optional measurement,
    then repeated 'steps_after_barrier' times.
    """
    import numpy as np

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

def GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(src_y, sigma_y, ny, nx, spin_dim):
    """
    Returns a np array (ny,nx,spin_dim) that is Gaussian in y, uniform in x & directions.
    """
    import numpy as np
    arr = np.zeros((ny, nx, spin_dim), dtype=np.complex128)
    ycoords = np.arange(ny)
    gauss_y = np.exp(-0.5*((ycoords - src_y)/sigma_y)**2)
    # normalize in y
    norm_factor = np.sqrt(np.sum(np.abs(gauss_y)**2))
    gauss_y /= norm_factor

    # fill across x & directions
    for d in range(spin_dim):
        for x in range(nx):
            arr[:, x, d] = gauss_y
    return arr

def SHIFT(psi_in, offsets):
    """
    SHIFT each spin component by the specified (dy,dx).
    psi_in: shape=(ny,nx,8) (or something similar)
    offsets: list of (ofy,ofx)
    """
    import numpy as np
    ny, nx, spin_dim = psi_in.shape
    psi_out = np.zeros_like(psi_in)
    for d,(dy,dx) in enumerate(offsets):
        rolled = np.roll(psi_in[:,:,d], shift=dy, axis=0)
        rolled = np.roll(rolled, shift=dx, axis=1)
        psi_out[:,:,d] = rolled
    return psi_out

# ----- Generated classes below -----

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
        """
        Original formula: DIVIDE(Lx,nx)
        """
        return (self.Lx / self.nx)

    @property
    def dy(self):
        """
        Original formula: DIVIDE(Ly,ny)
        """
        return (self.Ly / self.ny)

    @property
    def barrier_row(self):
        """
        Original formula: FLOOR(DIVIDE(ADD(barrier_y_phys,DIVIDE(Ly,2)),dy))
        """
        return math.floor(((self.barrier_y_phys + (self.Ly / 2)) / self.dy))

    @property
    def detector_row(self):
        """
        Original formula: FLOOR(DIVIDE(ADD(detector_y_phys,DIVIDE(Ly,2)),dy))
        """
        return math.floor(((self.detector_y_phys + (self.Ly / 2)) / self.dy))

    @property
    def center_x(self):
        """
        Original formula: FLOOR(DIVIDE(nx,2))
        """
        return math.floor((self.nx / 2))

    @property
    def slit1_xstart(self):
        """
        Original formula: SUBTRACT(center_x,FLOOR(DIVIDE(slit_spacing,2)))
        """
        return (self.center_x - math.floor((self.slit_spacing / 2)))

    @property
    def slit1_xend(self):
        """
        Original formula: ADD(slit1_xstart,slit_width)
        """
        return (self.slit1_xstart + self.slit_width)

    @property
    def slit2_xstart(self):
        """
        Original formula: ADD(center_x,FLOOR(DIVIDE(slit_spacing,2)))
        """
        return (self.center_x + math.floor((self.slit_spacing / 2)))

    @property
    def slit2_xend(self):
        """
        Original formula: ADD(slit2_xstart,slit_width)
        """
        return (self.slit2_xstart + self.slit_width)

class CoinOperator:
    def __init__(self, **kwargs):
        self.Matrix = kwargs.get('Matrix')
        self.seed = kwargs.get('seed')
        self.construction_method = kwargs.get('construction_method')
        self.construction_params = kwargs.get('construction_params')

    @property
    def UnitarityCheck(self):
        """
        Original formula: EQUAL(MULTIPLY(Matrix,CONJUGATE_TRANSPOSE(Matrix)),IDENTITY(8))
        """
        return np.allclose(np.matmul(self.Matrix, self.Matrix.conj().T), np.eye(8, dtype=np.complex128))

class WavefunctionInitial:
    def __init__(self, **kwargs):
        self.src_y = kwargs.get('src_y')
        self.sigma_y = kwargs.get('sigma_y')
        self.kx = kwargs.get('kx')
        self.ky = kwargs.get('ky')

    @property
    def psi_init(self):
        """
        Original formula: GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(src_y, sigma_y, Grid.ny, Grid.nx, 8)
        """
        return GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(self.src_y, self.sigma_y, self.Grid.ny, self.Grid.nx, 8)

class CoinStep:
    def __init__(self, **kwargs):
        self.psi_in = kwargs.get('psi_in')
        self.coin_matrix = kwargs.get('coin_matrix')

    @property
    def psi_out(self):
        """
        Original formula: MATMUL(psi_in, TRANSPOSE(coin_matrix))
        """
        return np.matmul(self.psi_in, self.coin_matrix.T)

class ShiftStep:
    def __init__(self, **kwargs):
        self.psi_in = kwargs.get('psi_in')
        self.offsets = kwargs.get('offsets')

    @property
    def psi_out(self):
        """
        Original formula: SHIFT(psi_in, offsets)
        """
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
        """
        Original formula: APPLY_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)
        """
        return APPLY_BARRIER(self.psi_in, self.barrier_row, self.slit1_xstart, self.slit1_xend, self.slit2_xstart, self.slit2_xend)

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
        """
        Original formula: COLLAPSE_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)
        """
        return COLLAPSE_BARRIER(self.psi_in, self.barrier_row, self.slit1_xstart, self.slit1_xend, self.slit2_xstart, self.slit2_xend)

class WavefunctionNorm:
    def __init__(self, **kwargs):
        self.psi_in = kwargs.get('psi_in')

    @property
    def total_norm(self):
        """
        Original formula: SUM(ABS(psi_in)^2)
        """
        return np.sum(self.ABS(psi_in)^2)

class DetectorAmplitude:
    def __init__(self, **kwargs):
        self.psi_in = kwargs.get('psi_in')
        self.detector_row = kwargs.get('detector_row')

    @property
    def row_amp(self):
        """
        Original formula: SLICE(psi_in, axis=0, index=detector_row)
        """
        # Parser error for formula: SLICE(psi_in, axis=0, index=detector_row)
        return None

class DetectorIntensity:
    def __init__(self, **kwargs):
        self.row_amp = kwargs.get('row_amp')

    @property
    def intensity_1d(self):
        """
        Original formula: SUM(ABS(row_amp)^2, axis=-1)
        """
        # Parser error for formula: SUM(ABS(row_amp)^2, axis=-1)
        return None

class QWalkRunner:
    def __init__(self, **kwargs):
        self.steps_to_barrier = kwargs.get('steps_to_barrier')
        self.steps_after_barrier = kwargs.get('steps_after_barrier')
        self.collapse_barrier = kwargs.get('collapse_barrier')
        self.step_order = kwargs.get('step_order')

    @property
    def final_wavefunction(self):
        """
        Original formula: EVOLVE(WavefunctionInitial.psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier)
        """
        # Parser error for formula: EVOLVE(WavefunctionInitial.psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier)
        return None

class RandomnessControl:
    def __init__(self, **kwargs):
        self.global_seed = kwargs.get('global_seed')

class DetectorRegion:
    def __init__(self, **kwargs):
        self.y_start = kwargs.get('y_start')
        self.y_end = kwargs.get('y_end')
