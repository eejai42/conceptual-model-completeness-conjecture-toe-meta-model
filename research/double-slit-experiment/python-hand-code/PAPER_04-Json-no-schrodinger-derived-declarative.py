#!/usr/bin/env python3
import math
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Dummy implementations for DSL helper functions
# -----------------------------------------------------------------------------
def GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(src_y, sigma_y, ny, nx, ndir):
    """Return an array of shape (ny, nx, ndir) with a Gaussian in y and uniform in x/direction."""
    psi = np.zeros((ny, nx, ndir), dtype=np.complex128)
    for y in range(ny):
        amp = np.exp(-0.5 * ((y - src_y) / sigma_y) ** 2)
        psi[y, :, :] = amp
    return psi

def SHIFT(psi, offsets):
    """Apply a directional shift to psi. Dummy implementation."""
    return psi

def APPLY_BARRIER(psi, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
    """Zero out the barrier row except for the slit columns."""
    psi_out = psi.copy()
    psi_out[barrier_row, :] = 0
    psi_out[barrier_row, slit1_xstart:slit1_xend] = psi[barrier_row, slit1_xstart:slit1_xend]
    psi_out[barrier_row, slit2_xstart:slit2_xend] = psi[barrier_row, slit2_xstart:slit2_xend]
    return psi_out

def COLLAPSE_BARRIER(psi, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
    """Collapse the barrier row amplitude outside of the slits. Dummy implementation."""
    psi_out = psi.copy()
    psi_out[barrier_row, :] = 0
    psi_out[barrier_row, slit1_xstart:slit1_xend] = psi[barrier_row, slit1_xstart:slit1_xend]
    psi_out[barrier_row, slit2_xstart:slit2_xend] = psi[barrier_row, slit2_xstart:slit2_xend]
    return psi_out

def EVOLVE(initial_psi, steps_to_barrier, steps_after_barrier, collapse_barrier):
    """Advance the simulation. For now, simply return the initial state."""
    return initial_psi.copy()

def SLICE(psi, axis, index):
    """Slice the tensor psi along the specified axis at the given index."""
    if axis == 0:
        return psi[index, ...]
    else:
        raise NotImplementedError("Only slicing along axis=0 is implemented.")

# -----------------------------------------------------------------------------
# Generated Python classes from JSON
# -----------------------------------------------------------------------------
class Grid:
    def __init__(self, nx, ny, Lx, Ly, barrier_y_phys, detector_y_phys, slit_width, slit_spacing):
        self.nx = nx
        self.ny = ny
        self.Lx = Lx
        self.Ly = Ly
        self.barrier_y_phys = barrier_y_phys
        self.detector_y_phys = detector_y_phys
        self.slit_width = slit_width
        self.slit_spacing = slit_spacing

    @property
    def dx(self):
        return self.Lx / self.nx  # DIVIDE(Lx, nx)

    @property
    def dy(self):
        return self.Ly / self.ny  # DIVIDE(Ly, ny)

    @property
    def barrier_row(self):
        # FLOOR(DIVIDE(ADD(barrier_y_phys, DIVIDE(Ly,2)), dy))
        return math.floor((self.barrier_y_phys + (self.Ly / 2)) / self.dy)

    @property
    def detector_row(self):
        # FLOOR(DIVIDE(ADD(detector_y_phys, DIVIDE(Ly,2)), dy))
        return math.floor((self.detector_y_phys + (self.Ly / 2)) / self.dy)

    @property
    def center_x(self):
        # FLOOR(DIVIDE(nx,2))
        return math.floor(self.nx / 2)

    @property
    def slit1_xstart(self):
        # SUBTRACT(center_x, FLOOR(DIVIDE(slit_spacing,2)))
        return self.center_x - math.floor(self.slit_spacing / 2)

    @property
    def slit1_xend(self):
        # ADD(slit1_xstart, slit_width)
        return self.slit1_xstart + self.slit_width

    @property
    def slit2_xstart(self):
        # ADD(center_x, FLOOR(DIVIDE(slit_spacing,2)))
        return self.center_x + math.floor(self.slit_spacing / 2)

    @property
    def slit2_xend(self):
        # ADD(slit2_xstart, slit_width)
        return self.slit2_xstart + self.slit_width


class CoinOperator:
    def __init__(self, Matrix, seed):
        self.Matrix = Matrix  # Expected shape (8,8)
        self.seed = seed

    @property
    def UnitarityCheck(self):
        # EQUAL(MULTIPLY(Matrix, CONJUGATE_TRANSPOSE(Matrix)), IDENTITY(8))
        return np.allclose(np.dot(self.Matrix, self.Matrix.conjugate().T), np.eye(8))


class WavefunctionInitial:
    def __init__(self, src_y, sigma_y, grid: Grid):
        self.src_y = src_y
        self.sigma_y = sigma_y
        self.grid = grid

    @property
    def psi_init(self):
        # GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(src_y, sigma_y, Grid.ny, Grid.nx, 8)
        return GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(
            self.src_y, self.sigma_y, self.grid.ny, self.grid.nx, 8
        )


class CoinStep:
    def __init__(self, psi_in, coin_matrix):
        self.psi_in = psi_in  # Tensor of shape (ny, nx, 8)
        self.coin_matrix = coin_matrix  # Tensor of shape (8,8)

    @property
    def psi_out(self):
        # MATMUL(psi_in, TRANSPOSE(coin_matrix))
        return np.matmul(self.psi_in, self.coin_matrix.T)


class ShiftStep:
    def __init__(self, psi_in, offsets):
        self.psi_in = psi_in  # Tensor of shape (ny, nx, 8)
        self.offsets = offsets  # List of (dy, dx) tuples

    @property
    def psi_out(self):
        # SHIFT(psi_in, offsets)
        return SHIFT(self.psi_in, self.offsets)


class BarrierStep:
    def __init__(self, psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
        self.psi_in = psi_in
        self.barrier_row = barrier_row
        self.slit1_xstart = slit1_xstart
        self.slit1_xend = slit1_xend
        self.slit2_xstart = slit2_xstart
        self.slit2_xend = slit2_xend

    @property
    def psi_out(self):
        # APPLY_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)
        return APPLY_BARRIER(
            self.psi_in,
            self.barrier_row,
            self.slit1_xstart,
            self.slit1_xend,
            self.slit2_xstart,
            self.slit2_xend,
        )


class CollapseBarrierStep:
    def __init__(self, psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
        self.psi_in = psi_in
        self.barrier_row = barrier_row
        self.slit1_xstart = slit1_xstart
        self.slit1_xend = slit1_xend
        self.slit2_xstart = slit2_xstart
        self.slit2_xend = slit2_xend

    @property
    def psi_out(self):
        # COLLAPSE_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)
        return COLLAPSE_BARRIER(
            self.psi_in,
            self.barrier_row,
            self.slit1_xstart,
            self.slit1_xend,
            self.slit2_xstart,
            self.slit2_xend,
        )


class WavefunctionNorm:
    def __init__(self, psi_in):
        self.psi_in = psi_in  # Tensor of shape (ny, nx, 8)

    @property
    def total_norm(self):
        # SUM(ABS(psi_in)^2)
        return np.sum(np.abs(self.psi_in) ** 2)


class DetectorAmplitude:
    def __init__(self, psi_in, detector_row):
        self.psi_in = psi_in  # Tensor of shape (ny, nx, 8)
        self.detector_row = detector_row

    @property
    def row_amp(self):
        # SLICE(psi_in, axis=0, index=detector_row)
        return SLICE(self.psi_in, axis=0, index=self.detector_row)


class DetectorIntensity:
    def __init__(self, row_amp):
        self.row_amp = row_amp  # Tensor of shape (nx, 8)

    @property
    def intensity_1d(self):
        # SUM(ABS(row_amp)^2, axis=-1)
        return np.sum(np.abs(self.row_amp) ** 2, axis=-1)


class QWalkRunner:
    def __init__(self, steps_to_barrier, steps_after_barrier, collapse_barrier, initial_wavefunction):
        self.steps_to_barrier = steps_to_barrier
        self.steps_after_barrier = steps_after_barrier
        self.collapse_barrier = collapse_barrier
        self.initial_wavefunction = initial_wavefunction

    @property
    def final_wavefunction(self):
        # EVOLVE(WavefunctionInitial.psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier)
        return EVOLVE(
            self.initial_wavefunction,
            self.steps_to_barrier,
            self.steps_after_barrier,
            self.collapse_barrier,
        )

# -----------------------------------------------------------------------------
# Main script: advancing time and plotting results
# -----------------------------------------------------------------------------
def main():
    # 1. Build the Grid
    grid = Grid(
        nx=701,
        ny=701,
        Lx=16.0,
        Ly=16.0,
        barrier_y_phys=-2.0,
        detector_y_phys=5.0,
        slit_width=3,
        slit_spacing=20,
    )

    # 2. Create the CoinOperator (using a dummy unitary 8x8 matrix)
    Matrix = np.eye(8, dtype=np.complex128)
    coin_operator = CoinOperator(Matrix, seed=42)
    print("CoinOperator UnitarityCheck:", coin_operator.UnitarityCheck)

    # 3. Initialize the wavefunction
    wf_init_obj = WavefunctionInitial(src_y=40, sigma_y=5.0, grid=grid)
    psi_init = wf_init_obj.psi_init

    # 4. Run the experiment via QWalkRunner
    runner = QWalkRunner(
        steps_to_barrier=400,
        steps_after_barrier=1000,
        collapse_barrier=False,
        initial_wavefunction=psi_init,
    )
    final_psi = runner.final_wavefunction

    # 5. Compute the total norm of the final wavefunction
    norm_obj = WavefunctionNorm(final_psi)
    total_norm = norm_obj.total_norm
    print("Final wavefunction norm:", total_norm)

    # 6. Extract detector amplitude and compute intensity
    det_amp_obj = DetectorAmplitude(final_psi, grid.detector_row)
    row_amp = det_amp_obj.row_amp
    det_intensity_obj = DetectorIntensity(row_amp)
    intensity_1d = det_intensity_obj.intensity_1d
    print("Detector intensity shape:", intensity_1d.shape)

    # 7. Plot the detector intensity
    plt.figure(figsize=(8,4))
    plt.plot(intensity_1d, 'o-')
    plt.title("Detector Intensity")
    plt.xlabel("x-index")
    plt.ylabel("Intensity")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()