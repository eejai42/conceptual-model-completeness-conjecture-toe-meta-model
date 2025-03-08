#!/usr/bin/env python3

import cupy as cp
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
# CLASSES
##############################################################################

class Grid:
    """
    Holds geometry info: nx, ny, domain size, barrier row, slit geometry, etc.
    """
    def __init__(self, nx, ny, Lx, Ly, barrier_y_phys, detector_y_phys,
                 slit_width, slit_spacing):
        self.nx = nx
        self.ny = ny
        self.Lx = Lx
        self.Ly = Ly
        self.dx = Lx / nx
        self.dy = Ly / ny

        # Convert physical coords to grid indices
        self.barrier_row = int((barrier_y_phys + Ly/2) / self.dy)
        self.detector_row = int((detector_y_phys + Ly/2) / self.dy)

        # Slit geometry
        center_x = nx // 2
        self.slit_width = slit_width
        self.slit_spacing = slit_spacing
        self.slit1_xstart = center_x - slit_spacing // 2
        self.slit1_xend   = self.slit1_xstart + slit_width
        self.slit2_xstart = center_x + slit_spacing // 2
        self.slit2_xend   = self.slit2_xstart + slit_width

        # For logging/demonstration
        print(f"Barrier row={self.barrier_row}, Detector row={self.detector_row}")
        print(f"Slit1=({self.slit1_xstart}:{self.slit1_xend}), "
              f"Slit2=({self.slit2_xstart}:{self.slit2_xend})")


class CoinOperator:
    """
    Stores the 8x8 matrix for the local coin operation on the GPU.
    We replicate the 'make_coin_8()' approach from the first script (CPU-based
    random seed + SVD => unify), then store the result as a CuPy array.
    """
    def __init__(self, seed=42):
        self.matrix = self._make_coin_8_cpu_then_gpu(seed)

    @staticmethod
    def _make_coin_8_cpu_then_gpu(seed):
        """
        Exactly replicate the steps from the first script:
          1. np.random.seed(42)
          2. mat = np.ones(...) - alpha on the diagonal
          3. small random
          4. svd => unitarize
          5. convert to cp array
        """
        np.random.seed(seed)
        mat = np.ones((8,8), dtype=np.complex128)
        alpha = 2.0
        for i in range(8):
            mat[i,i] -= alpha
        # small random perturbation
        rnd = 0.05*(np.random.rand(8,8) + 1j*np.random.rand(8,8))
        mat += rnd
        # Force unitarity via SVD
        U, s, Vh = np.linalg.svd(mat, full_matrices=True)
        coin_cpu = U @ Vh
        # Now store on GPU
        return cp.array(coin_cpu, dtype=cp.complex128)

    def apply(self, spin_in):
        """
        spin_in shape=(8,) [on GPU], returns spin_out shape=(8,) [on GPU].
        """
        return self.matrix @ spin_in


class Wavefunction:
    """
    An immutable snapshot of the wavefunction at a given time:
      psi.shape = (ny, nx, 8), stored on the GPU (cp.complex128).

    We'll have a method evolve_one_step(...) that returns a NEW Wavefunction.
    """
    DIRECTION_OFFSETS = [
        (-1,  0),  # up
        (+1,  0),  # down
        ( 0, -1),  # left
        ( 0, +1),  # right
        (-1, -1),  # up-left
        (-1, +1),  # up-right
        (+1, -1),  # down-left
        (+1, +1),  # down-right
    ]

    def __init__(self, grid: Grid, array_psi: cp.ndarray):
        """
        array_psi is shape=(ny,nx,8), dtype=cp.complex128
        """
        self.grid = grid
        # We'll store a reference, but treat as immutable outside
        self.psi = array_psi

    @classmethod
    def initial_condition(cls, grid: Grid):
        """
        Build the wavefunction at t=0, exactly as in the first script:
          - src_y=40, sigma_y=5
          - wide in x, same amplitude in all directions
        """
        psi0 = cp.zeros((grid.ny, grid.nx, 8), dtype=cp.complex128)
        src_y = 40
        sigma_y = 5.0

        # We do it in pure CuPy:
        for y in range(grid.ny):
            dy = y - src_y
            amp = cp.exp(-0.5*(dy/sigma_y)**2)
            # wide in x => fill entire row for all directions
            for d in range(8):
                psi0[y, :, d] = amp

        return cls(grid, psi0)

    def evolve_one_step(self, coin: CoinOperator, measure_barrier=False):
        """
        Return a NEW Wavefunction at time t+1, applying:
          1) coin step
          2) shift step
          3) barrier or measure (if measure_barrier=True)
        """
        ny, nx, ndir = self.psi.shape

        # 1) Coin step (vectorized approach on GPU)
        #    spin_out = coin_matrix @ spin_in, for each (y,x).
        # A direct python loop over y,x is slow. We'll do a reshape -> matmul -> reshape
        # (Same approach as the first script's "coin_step".)

        # flatten (ny*nx, 8)
        psi_flat = self.psi.reshape((-1, 8))
        # multiply from the left by coin.matrix => shape stays (ny*nx, 8)
        psi_coin_flat = psi_flat @ coin.matrix.T
        psi_coin = psi_coin_flat.reshape((ny, nx, 8))

        # 2) Shift step
        psi_shift = cp.zeros_like(psi_coin)
        for d, (ofy, ofx) in enumerate(self.DIRECTION_OFFSETS):
            shifted_dir = cp.roll(psi_coin[:,:,d], shift=ofy, axis=0)
            shifted_dir = cp.roll(shifted_dir, shift=ofx, axis=1)
            psi_shift[:,:,d] = shifted_dir

        # 3) Barrier or measurement
        if measure_barrier:
            psi_out = self._collapse_barrier(psi_shift)
        else:
            psi_out = self._apply_barrier(psi_shift)

        return Wavefunction(self.grid, psi_out)

    def _apply_barrier(self, psi_in):
        """
        Normal barrier => zero out barrier row except slit columns.
        """
        psi_out = psi_in.copy()
        br = self.grid.barrier_row
        psi_out[br,:,:] = 0
        s1s, s1e = self.grid.slit1_xstart, self.grid.slit1_xend
        s2s, s2e = self.grid.slit2_xstart, self.grid.slit2_xend

        psi_out[br, s1s:s1e, :] = psi_in[br, s1s:s1e, :]
        psi_out[br, s2s:s2e, :] = psi_in[br, s2s:s2e, :]
        return psi_out

    def _collapse_barrier(self, psi_in):
        """
        Collapsing amplitude in barrier row => sum intensities across directions,
        keep only slit columns, sqrt(keep / max), put in direction=0
        """
        psi_out = psi_in.copy()
        ny, nx, ndir = psi_in.shape
        br = self.grid.barrier_row

        # sum intensities across directions for that row
        row_intens = cp.sum(cp.abs(psi_in[br,:,:])**2, axis=-1)  # shape=(nx,)

        keep = cp.zeros_like(row_intens)
        s1s, s1e = self.grid.slit1_xstart, self.grid.slit1_xend
        s2s, s2e = self.grid.slit2_xstart, self.grid.slit2_xend
        keep[s1s:s1e] = row_intens[s1s:s1e]
        keep[s2s:s2e] = row_intens[s2s:s2e]

        m = cp.max(keep)
        if m > 1e-30:
            keep /= m
        amps = cp.sqrt(keep)

        psi_out[br,:,:] = 0
        # direction=0 is "up" – just put amplitude there
        psi_out[br,:,0] = amps
        return psi_out

    def total_norm(self):
        """
        Returns the sum of |psi|^2 over all y,x,d (on GPU).
        """
        return cp.sum(cp.abs(self.psi)**2)

    def detector_row_intensity(self):
        """
        Summation over directions at 'detector_row', returns shape=(nx,) on GPU
        """
        dr = self.grid.detector_row
        row_amp = self.psi[dr, :, :]  # shape=(nx,8)
        row_intens = cp.sum(cp.abs(row_amp)**2, axis=-1)  # shape=(nx,)
        return row_intens


class QWalkRunner:
    """
    Orchestrates the evolution in an immutable, functional style.
    We keep wave[t+1] = wave[t].evolve_one_step(...)

    We can optionally do a measurement collapse at t=steps_to_barrier.
    """
    def __init__(self, grid: Grid, coin: CoinOperator,
                 steps_to_barrier, steps_after_barrier):
        self.grid = grid
        self.coin = coin
        self.steps_to_barrier = steps_to_barrier
        self.steps_after_barrier = steps_after_barrier

    def run_experiment(self, collapse=False):
        """
        Return the final Wavefunction after steps_to_barrier + steps_after_barrier,
        without storing intermediate wavefunctions.
        """
        # Initialize once
        wave_current = Wavefunction.initial_condition(self.grid)

        # Evolve up to barrier
        for _ in range(self.steps_to_barrier):
            wave_current = wave_current.evolve_one_step(self.coin, measure_barrier=False)

        # If collapse => measure at the barrier
        if collapse:
            wave_current = wave_current.evolve_one_step(self.coin, measure_barrier=True)

        # Evolve remainder
        for _ in range(self.steps_after_barrier):
            wave_current = wave_current.evolve_one_step(self.coin, measure_barrier=False)

        return wave_current


##############################################################################
# MAIN
##############################################################################
def main():
    # Match the first script's parameters exactly:
    nx = 701
    ny = 701
    Lx, Ly = 16.0, 16.0
    steps_to_barrier = 400
    steps_after_barrier = 1000

    barrier_y_phys = -2.0
    detector_y_phys = 5.0
    slit_width = 3
    slit_spacing = 20

    # 1) Build the Grid
    grid = Grid(nx, ny, Lx, Ly, barrier_y_phys, detector_y_phys,
                slit_width, slit_spacing)

    # 2) Create the Coin
    coin = CoinOperator(seed=42)

    # 3) Create a QWalkRunner
    runner = QWalkRunner(grid, coin, steps_to_barrier, steps_after_barrier)

    # 4) Run the "FULL" wave (no measurement)
    print("Running FULL wave (no barrier measurement)...")
    wave_full = runner.run_experiment(collapse=False)
    norm_full = wave_full.total_norm().item()  # .item() to pull scalar to CPU
    print(f"Final norm (full)={norm_full:.3g}")

    # 5) Run the "COLLAPSED" wave (with measurement)
    print("Running COLLAPSED wave (with barrier measurement)...")
    wave_coll = runner.run_experiment(collapse=True)
    norm_coll = wave_coll.total_norm().item()
    print(f"Final norm (collapsed)={norm_coll:.3g}")

    # 6) Measure intensity at the detector row => sum over directions => shape=(nx,)
    int_full = wave_full.detector_row_intensity()
    int_coll = wave_coll.detector_row_intensity()

    # 7) Normalize each (on GPU), then bring to CPU
    mf = cp.max(int_full)
    if mf > 1e-30:
        int_full /= mf
    mc = cp.max(int_coll)
    if mc > 1e-30:
        int_coll /= mc

    int_full_cpu = int_full.get()
    int_coll_cpu = int_coll.get()

    # 8) Build 2D "screen" => tile 1D intensity. For plotting we can do it in NumPy:
    screen_height = 60
    screen_full = np.tile(int_full_cpu, (screen_height,1))
    screen_coll = np.tile(int_coll_cpu, (screen_height,1))

    # 9) Plot
    plt.figure(figsize=(8,4))
    plt.imshow(screen_full, origin="lower", aspect="auto", cmap="inferno")
    plt.title("Full Wave – Detector Row (GPU OO style)")
    plt.xlabel("x-index")
    plt.ylabel("Screen Height")
    plt.colorbar(label="Normalized Intensity")

    plt.figure(figsize=(8,4))
    plt.plot(int_full_cpu, 'o-')
    plt.title("Full Wave – 1D Intensity at Detector")
    plt.xlabel("x-index")
    plt.ylabel("Intensity")

    plt.figure(figsize=(8,4))
    plt.imshow(screen_coll, origin="lower", aspect="auto", cmap="inferno")
    plt.title("Collapsed Wave – Detector Row (GPU OO style)")
    plt.xlabel("x-index")
    plt.ylabel("Screen Height")
    plt.colorbar(label="Normalized Intensity")

    plt.figure(figsize=(8,4))
    plt.plot(int_coll_cpu, 'o-')
    plt.title("Collapsed Wave – 1D Intensity at Detector")
    plt.xlabel("x-index")
    plt.ylabel("Intensity")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()