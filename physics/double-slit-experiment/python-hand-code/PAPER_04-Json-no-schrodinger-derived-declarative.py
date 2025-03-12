import math
import numpy as np

###############################################################################
# Placeholder "physics" or "utility" functions corresponding to JSON formulas #
###############################################################################

def GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(src_y, sigma_y, ny, nx, spin_dim):
    """
    Example: returns a 3D array (ny, nx, spin_dim) that is
    Gaussian in y, uniform in x and spin directions.
    Replace with real physics code if needed.
    """
    # Minimal placeholder example:
    psi = np.zeros((ny, nx, spin_dim), dtype=np.complex128)
    y_coords = np.arange(ny) - (ny // 2)
    gauss = np.exp(-0.5 * ((y_coords - src_y) / sigma_y)**2)
    gauss /= np.sqrt(np.sum(np.abs(gauss)**2))  # normalize 1D in y

    for x in range(nx):
        for s in range(spin_dim):
            for y_index in range(ny):
                psi[y_index, x, s] = gauss[y_index]
    return psi

def MATMUL(psi_in, coin_matrix):
    """
    Placeholder for matrix multiplication:
    psi_in shape: (ny, nx, 8), coin_matrix shape: (8,8).
    We apply coin_matrix^T to each (ny,nx) site if that's the convention.
    """
    ny, nx, spin_dim = psi_in.shape
    out = np.zeros_like(psi_in)
    # Apply coin_matrix^T to the spin dimension
    for y_idx in range(ny):
        for x_idx in range(nx):
            out[y_idx, x_idx, :] = coin_matrix.T @ psi_in[y_idx, x_idx, :]
    return out

def SHIFT(psi_in, offsets):
    """
    SHIFT each spin component by its (dy, dx).
    offsets is a list of length 8: offsets[d] = (dy, dx).
    """
    ny, nx, spin_dim = psi_in.shape
    psi_out = np.zeros_like(psi_in)
    for d in range(spin_dim):
        dy, dx = offsets[d]
        # Use np.roll for each direction
        psi_out[:, :, d] = np.roll(np.roll(psi_in[:, :, d], dy, axis=0), dx, axis=1)
    return psi_out

def APPLY_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend,
                  slit2_xstart, slit2_xend):
    """
    Zero out wavefunction in the barrier_row except within the two slit ranges.
    """
    psi_out = np.copy(psi_in)
    ny, nx, spin_dim = psi_out.shape
    for x in range(nx):
        in_slit1 = (slit1_xstart <= x < slit1_xend)
        in_slit2 = (slit2_xstart <= x < slit2_xend)
        if not (in_slit1 or in_slit2):
            # Zero out at barrier row
            psi_out[barrier_row, x, :] = 0
    return psi_out

def COLLAPSE_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend,
                     slit2_xstart, slit2_xend):
    """
    "Measurement" at the barrier row: amplitude outside the slits is lost.
    This is similar to APPLY_BARRIER, but semantically it implies a partial or
    projective measurement event. We just do the same zeroing, but interpret it as a collapse.
    """
    # Could do partial or amplitude damping if needed, but here's a simple zero:
    return APPLY_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend,
                         slit2_xstart, slit2_xend)

def SUM_ABS_SQUARED(psi_in):
    return np.sum(np.abs(psi_in)**2)

def SLICE_ROW(psi_in, axis, index):
    """
    Ex: SLICE(psi_in, axis=0, index=detector_row) => psi_in[detector_row, :, :]
    """
    if axis == 0:
        return psi_in[index, :, :]
    # Extend for other axes as needed
    raise ValueError(f"Slicing along axis={axis} not implemented.")

def EVOLVE(psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier):
    """
    Placeholder for the overall quantum walk evolution from t=0 to final.
    In a real system, you might do repeated calls to coin/shift/etc.
    Here, we just echo back psi_init for demonstration.
    """
    # NOTE: In a real scenario, we'd do:
    #   1. for i in range(steps_to_barrier): coin+shift...
    #   2. if collapse_barrier: measure/collapse...
    #   3. for j in range(steps_after_barrier): coin+shift...
    # Return final wavefunction
    return np.copy(psi_init)

def is_unitary(m):
    """
    Check if m * m^† ~ I for an 8x8 matrix
    """
    return np.allclose(m @ m.conj().T, np.eye(m.shape[0]))


###############################################################################
#                        AUTO-GENERATED CLASSES FROM JSON                     #
###############################################################################

class Grid:
    def __init__(self,
                 nx=None,
                 ny=None,
                 Lx=None,
                 Ly=None,
                 barrier_y_phys=None,
                 detector_y_phys=None,
                 slit_width=None,
                 slit_spacing=None,
                 boundary_conditions=None):
        self.nx = nx
        self.ny = ny
        self.Lx = Lx
        self.Ly = Ly
        self.barrier_y_phys = barrier_y_phys
        self.detector_y_phys = detector_y_phys
        self.slit_width = slit_width
        self.slit_spacing = slit_spacing
        self.boundary_conditions = boundary_conditions

    @property
    def dx(self):
        # formula: DIVIDE(Lx,nx)
        return self.Lx / self.nx

    @property
    def dy(self):
        # formula: DIVIDE(Ly,ny)
        return self.Ly / self.ny

    @property
    def barrier_row(self):
        # formula: FLOOR(DIVIDE(ADD(barrier_y_phys,DIVIDE(Ly,2)),dy))
        return math.floor((self.barrier_y_phys + (self.Ly / 2.0)) / self.dy)

    @property
    def detector_row(self):
        # formula: FLOOR(DIVIDE(ADD(detector_y_phys,DIVIDE(Ly,2)),dy))
        return math.floor((self.detector_y_phys + (self.Ly / 2.0)) / self.dy)

    @property
    def center_x(self):
        # formula: FLOOR(DIVIDE(nx,2))
        return self.nx // 2

    @property
    def slit1_xstart(self):
        # formula: SUBTRACT(center_x,FLOOR(DIVIDE(slit_spacing,2)))
        return self.center_x - (self.slit_spacing // 2)

    @property
    def slit1_xend(self):
        # formula: ADD(slit1_xstart,slit_width)
        return self.slit1_xstart + self.slit_width

    @property
    def slit2_xstart(self):
        # formula: ADD(center_x,FLOOR(DIVIDE(slit_spacing,2)))
        return self.center_x + (self.slit_spacing // 2)

    @property
    def slit2_xend(self):
        # formula: ADD(slit2_xstart,slit_width)
        return self.slit2_xstart + self.slit_width


class CoinOperator:
    def __init__(self,
                 Matrix=None,
                 seed=None,
                 construction_method=None,
                 construction_params=None):
        self.Matrix = Matrix
        self.seed = seed
        self.construction_method = construction_method
        self.construction_params = construction_params

    @property
    def UnitarityCheck(self):
        # formula: EQUAL(MULTIPLY(Matrix,CONJUGATE_TRANSPOSE(Matrix)),IDENTITY(8))
        # We'll interpret it as "is the matrix unitary?"
        if self.Matrix is None:
            return False
        return is_unitary(self.Matrix)


class WavefunctionInitial:
    def __init__(self,
                 src_y=None,
                 sigma_y=None,
                 kx=None,
                 ky=None,
                 grid=None):
        """
        The JSON schema references Grid.ny and Grid.nx.
        So we expect a 'grid' object to be passed, or we can store them directly.
        """
        self.src_y = src_y
        self.sigma_y = sigma_y
        self.kx = kx
        self.ky = ky
        self.grid = grid

    @property
    def psi_init(self):
        # formula: GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(src_y, sigma_y, Grid.ny, Grid.nx, 8)
        if not self.grid:
            return None
        return GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(
            self.src_y,
            self.sigma_y,
            self.grid.ny,
            self.grid.nx,
            8
        )


class CoinStep:
    def __init__(self, psi_in=None, coin_matrix=None):
        self.psi_in = psi_in
        self.coin_matrix = coin_matrix

    @property
    def psi_out(self):
        # formula: MATMUL(psi_in, TRANSPOSE(coin_matrix))
        if self.psi_in is None or self.coin_matrix is None:
            return None
        return MATMUL(self.psi_in, self.coin_matrix)


class ShiftStep:
    def __init__(self, psi_in=None, offsets=None):
        self.psi_in = psi_in
        self.offsets = offsets

    @property
    def psi_out(self):
        # formula: SHIFT(psi_in, offsets)
        if self.psi_in is None or self.offsets is None:
            return None
        return SHIFT(self.psi_in, self.offsets)


class BarrierStep:
    def __init__(self,
                 psi_in=None,
                 barrier_row=None,
                 slit1_xstart=None,
                 slit1_xend=None,
                 slit2_xstart=None,
                 slit2_xend=None):
        self.psi_in = psi_in
        self.barrier_row = barrier_row
        self.slit1_xstart = slit1_xstart
        self.slit1_xend = slit1_xend
        self.slit2_xstart = slit2_xstart
        self.slit2_xend = slit2_xend

    @property
    def psi_out(self):
        # formula: APPLY_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)
        if self.psi_in is None:
            return None
        return APPLY_BARRIER(self.psi_in,
                             self.barrier_row,
                             self.slit1_xstart,
                             self.slit1_xend,
                             self.slit2_xstart,
                             self.slit2_xend)


class CollapseBarrierStep:
    def __init__(self,
                 psi_in=None,
                 barrier_row=None,
                 slit1_xstart=None,
                 slit1_xend=None,
                 slit2_xstart=None,
                 slit2_xend=None,
                 collapse_method=None):
        self.psi_in = psi_in
        self.barrier_row = barrier_row
        self.slit1_xstart = slit1_xstart
        self.slit1_xend = slit1_xend
        self.slit2_xstart = slit2_xstart
        self.slit2_xend = slit2_xend
        self.collapse_method = collapse_method  # projective, partial_transmission, amplitude_damping

    @property
    def psi_out(self):
        # formula: COLLAPSE_BARRIER(...)
        if self.psi_in is None:
            return None
        # We ignore 'collapse_method' for now
        return COLLAPSE_BARRIER(self.psi_in,
                                self.barrier_row,
                                self.slit1_xstart,
                                self.slit1_xend,
                                self.slit2_xstart,
                                self.slit2_xend)


class WavefunctionNorm:
    def __init__(self, psi_in=None):
        self.psi_in = psi_in

    @property
    def total_norm(self):
        # formula: SUM(ABS(psi_in)^2)
        if self.psi_in is None:
            return None
        return SUM_ABS_SQUARED(self.psi_in)


class DetectorAmplitude:
    def __init__(self, psi_in=None, detector_row=None):
        self.psi_in = psi_in
        self.detector_row = detector_row

    @property
    def row_amp(self):
        # formula: SLICE(psi_in, axis=0, index=detector_row)
        if self.psi_in is None or self.detector_row is None:
            return None
        return SLICE_ROW(self.psi_in, axis=0, index=self.detector_row)


class DetectorIntensity:
    def __init__(self, row_amp=None):
        self.row_amp = row_amp

    @property
    def intensity_1d(self):
        # formula: SUM(ABS(row_amp)^2, axis=-1)
        if self.row_amp is None:
            return None
        return np.sum(np.abs(self.row_amp)**2, axis=-1)


class QWalkRunner:
    def __init__(self,
                 steps_to_barrier=None,
                 steps_after_barrier=None,
                 collapse_barrier=None):
        self.steps_to_barrier = steps_to_barrier
        self.steps_after_barrier = steps_after_barrier
        self.collapse_barrier = collapse_barrier

    @property
    def final_wavefunction(self):
        # formula: EVOLVE(WavefunctionInitial.psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier)
        # We'll assume you pass the initial wavefunction separately or store it globally.
        # For demonstration, let's just show a usage example:
        if self._initial_psi is None:
            return None
        return EVOLVE(self._initial_psi,
                      self.steps_to_barrier,
                      self.steps_after_barrier,
                      self.collapse_barrier)

    def set_initial_psi(self, psi):
        """
        A helper so we can specify which wavefunction is used as the input to EVOLVE.
        In a real system, you might pass WavefunctionInitial or store it in init.
        """
        self._initial_psi = psi


class RandomnessControl:
    def __init__(self, global_seed=None):
        self.global_seed = global_seed


class DetectorRegion:
    def __init__(self, y_start=None, y_end=None):
        self.y_start = y_start
        self.y_end = y_end
