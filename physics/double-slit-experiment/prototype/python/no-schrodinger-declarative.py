#!/usr/bin/env python3
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
        print(f"Slit1=({self.slit1_xstart}:{self.slit1_xend}),  Slit2=({self.slit2_xstart}:{self.slit2_xend})")


class CoinOperator:
    """
    Stores the NxN (in this case 8x8) matrix for the local coin operation.
    """
    def __init__(self, seed=42):
        self.matrix = self._make_coin_8(seed)

    @staticmethod
    def _make_coin_8(seed):
        rng = np.random.default_rng(seed=seed)
        mat = np.ones((8,8), dtype=np.complex128)
        alpha = 2.0
        for i in range(8):
            mat[i,i] -= alpha
        rnd = 0.05*(rng.random((8,8)) + 1j*rng.random((8,8)))
        mat += rnd
        # Force unitarity via SVD
        U, s, Vh = np.linalg.svd(mat, full_matrices=True)
        return U @ Vh

    def apply(self, spin_in):
        """
        spin_in shape=(8,), returns spin_out shape=(8,)
        """
        return self.matrix @ spin_in


class Wavefunction:
    """
    An immutable snapshot of the wavefunction at a given time:
      psi.shape = (ny, nx, 8)

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

    def __init__(self, grid: Grid, array_psi: np.ndarray):
        """
        array_psi is shape=(ny,nx,8), complex
        """
        self.grid = grid
        self.psi = array_psi  # store the array as immutable
        # no direct assignment to self.psi[...] from outside

    @classmethod
    def initial_condition(cls, grid: Grid):
        """
        Build the wavefunction at t=0, as a Gaussian in y near the bottom,
        wide in x, same amplitude in all directions.
        """
        psi0 = np.zeros((grid.ny, grid.nx, 8), dtype=np.complex128)
        # let's pick a src_y ~ 15% from bottom:
        src_y = int(grid.ny * 0.15)
        sigma_y = 5.0

        for y in range(grid.ny):
            dy = y - src_y
            amp = np.exp(-0.5*(dy/sigma_y)**2)
            for d in range(8):
                psi0[y,:,d] = amp

        return cls(grid, psi0)

    def evolve_one_step(self, coin: CoinOperator, measure_barrier=False):
        """
        Return a NEW Wavefunction at time t+1, applying:
          1) coin step
          2) shift step
          3) barrier or measure (if measure_barrier=True)
        """
        ny, nx, ndir = self.psi.shape
        # 1) Coin step
        psi_coin = np.zeros_like(self.psi, dtype=np.complex128)
        for y in range(ny):
            for x in range(nx):
                spin_in = self.psi[y,x,:]  # shape=(8,)
                spin_out = coin.apply(spin_in)
                psi_coin[y,x,:] = spin_out

        # 2) Shift step
        psi_shift = np.zeros_like(psi_coin, dtype=np.complex128)
        for d, (ofy, ofx) in enumerate(self.DIRECTION_OFFSETS):
            shifted_dir = np.roll(psi_coin[:,:,d], shift=ofy, axis=0)
            shifted_dir = np.roll(shifted_dir, shift=ofx, axis=1)
            psi_shift[:,:,d] = shifted_dir

        # 3) Barrier or measurement
        if measure_barrier:
            # measure_collapse_barrier logic
            psi_out = self._collapse_barrier(psi_shift)
        else:
            # normal barrier
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
        # sum intensities across directions
        row_intens = np.sum(np.abs(psi_in[br,:,:])**2, axis=-1)  # shape=(nx,)

        keep = np.zeros_like(row_intens)
        s1s, s1e = self.grid.slit1_xstart, self.grid.slit1_xend
        s2s, s2e = self.grid.slit2_xstart, self.grid.slit2_xend
        keep[s1s:s1e] = row_intens[s1s:s1e]
        keep[s2s:s2e] = row_intens[s2s:s2e]

        m = np.max(keep)
        if m > 1e-30:
            keep /= m
        amps = np.sqrt(keep)
        psi_out[br,:,:] = 0
        psi_out[br,:,0] = amps  # put amplitude in direction=0
        return psi_out

    def total_norm(self):
        """
        Returns the sum of |psi|^2 over all y,x,d.
        """
        return np.sum(np.abs(self.psi)**2)

    def detector_row_intensity(self):
        """
        Summation over directions at 'detector_row', returns shape=(nx,).
        """
        dr = self.grid.detector_row
        row_amp = self.psi[dr, :, :]  # shape=(nx,8)
        row_intens = np.sum(np.abs(row_amp)**2, axis=-1)  # shape=(nx,)
        return row_intens


class QWalkRunner:
    """
    Orchestrates the layer-by-layer evolution in an immutable, functional style.
    - We keep a list of Wavefunction objects, wave[t].
    - wave[t+1] = wave[t].evolve_one_step(...)

    We can optionally do a measurement collapse at t=steps_to_barrier.
    """
    def __init__(self, grid: Grid, coin: CoinOperator, steps_to_barrier, steps_after_barrier):
        self.grid = grid
        self.coin = coin
        self.steps_to_barrier = steps_to_barrier
        self.steps_after_barrier = steps_after_barrier

    def run_experiment(self, collapse=False):
        """
        Return the final Wavefunction after steps_to_barrier + steps_after_barrier.
        """
        t_final = self.steps_to_barrier + self.steps_after_barrier
        # We'll keep each wavefunction in a list for demonstration
        wave = [None]*(t_final+1)
        wave[0] = Wavefunction.initial_condition(self.grid)

        # Evolve up to barrier
        for t in range(self.steps_to_barrier):
            wave[t+1] = wave[t].evolve_one_step(self.coin, measure_barrier=False)

        # If collapse => measure at t=steps_to_barrier
        if collapse:
            wave[self.steps_to_barrier] = wave[self.steps_to_barrier-1].evolve_one_step(self.coin, measure_barrier=True)
        else:
            # else wave[self.steps_to_barrier] was already created with measure=False above
            pass

        # Evolve remainder
        for t in range(self.steps_to_barrier, t_final):
            wave[t+1] = wave[t].evolve_one_step(self.coin, measure_barrier=False)

        return wave[t_final]  # final wavefunction

##############################################################################
# MAIN
##############################################################################
def main():
    # 1) Build the Grid
    nx = 201
    ny = 201
    Lx, Ly = 16.0, 16.0
    steps_to_barrier = 80
    steps_after_barrier = 200

    barrier_y_phys = -2.0
    detector_y_phys = 5.0
    slit_width = 3
    slit_spacing = 12

    grid = Grid(nx, ny, Lx, Ly, barrier_y_phys, detector_y_phys,
                slit_width, slit_spacing)

    # 2) Create the Coin
    coin = CoinOperator(seed=42)

    # 3) Create a QWalkRunner
    runner = QWalkRunner(grid, coin, steps_to_barrier, steps_after_barrier)

    # 4) Run the "FULL" wave (no measurement)
    print("Running FULL wave (no barrier measurement)...")
    wave_full = runner.run_experiment(collapse=False)
    norm_full = wave_full.total_norm()
    print(f"Final norm (full)={norm_full:.3g}")

    # 5) Run the "COLLAPSED" wave (with measurement)
    print("Running COLLAPSED wave (with barrier measurement)...")
    wave_coll = runner.run_experiment(collapse=True)
    norm_coll = wave_coll.total_norm()
    print(f"Final norm (collapsed)={norm_coll:.3g}")

    # 6) Measure intensity at the detector row => sum over directions => shape=(nx,)
    int_full = wave_full.detector_row_intensity()
    int_coll = wave_coll.detector_row_intensity()

    # 7) Normalize each
    mf = np.max(int_full)
    if mf > 1e-30:
        int_full /= mf
    mc = np.max(int_coll)
    if mc > 1e-30:
        int_coll /= mc

    # 8) Build 2D "screen" => tile 1D intensity
    screen_height = 60
    screen_full = np.tile(int_full, (screen_height,1))
    screen_coll = np.tile(int_coll, (screen_height,1))

    # 9) Plot
    plt.figure(figsize=(8,4))
    plt.imshow(screen_full, origin="lower", aspect="auto", cmap="inferno")
    plt.title("Full Wave – Detector Row (OO, Functional layering)")
    plt.xlabel("x-index")
    plt.ylabel("Screen Height")
    plt.colorbar(label="Normalized Intensity")

    plt.figure(figsize=(8,4))
    plt.plot(int_full, 'o-')
    plt.title("Full Wave – 1D Intensity at Detector")
    plt.xlabel("x-index")
    plt.ylabel("Intensity")

    plt.figure(figsize=(8,4))
    plt.imshow(screen_coll, origin="lower", aspect="auto", cmap="inferno")
    plt.title("Collapsed Wave – Detector Row (OO, Functional layering)")
    plt.xlabel("x-index")
    plt.ylabel("Screen Height")
    plt.colorbar(label="Normalized Intensity")

    plt.figure(figsize=(8,4))
    plt.plot(int_coll, 'o-')
    plt.title("Collapsed Wave – 1D Intensity at Detector")
    plt.xlabel("x-index")
    plt.ylabel("Intensity")

    plt.tight_layout()
    plt.show()


if __name__=="__main__":
    main()
