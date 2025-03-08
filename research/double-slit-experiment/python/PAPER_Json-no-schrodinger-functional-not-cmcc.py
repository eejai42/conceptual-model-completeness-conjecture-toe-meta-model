#!/usr/bin/env python3

import cupy as cp
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
# 8-DIRECTION QUANTUM WALK (GPU) WITH LOCAL UNITARY COIN
# Produces 4 plots: Full Wave (2D & 1D) vs. Collapsed Wave (2D & 1D)
##############################################################################

# ---------------------------
# Grid Size, Domain
# ---------------------------
nx = 701
ny = 701

# We'll conceptually treat x,y in [-8..+8] => total 16
Lx, Ly = 16.0, 16.0
dx = Lx/nx
dy = Ly/ny

# Steps for time evolution
steps_to_barrier = 400
steps_after_barrier = 1000

# Barrier row near y = -2 => index ...
barrier_y_phys = -2.0
barrier_row = int((barrier_y_phys + Ly/2)/dy)

# Detector row near y = +5 => index ...
detector_y_phys = 5.0
detector_row = int((detector_y_phys + Ly/2)/dy)

# Slit geometry
slit_width = 3
slit_spacing = 20
center_x = nx//2

slit1_xstart = center_x - slit_spacing//2
slit1_xend   = slit1_xstart + slit_width
slit2_xstart = center_x + slit_spacing//2
slit2_xend   = slit2_xstart + slit_width

print(f"Barrier row={barrier_row}, Detector row={detector_row}")
print(f"Slit1=({slit1_xstart}:{slit1_xend}),  Slit2=({slit2_xstart}:{slit2_xend})")

##############################################################################
# psi shape=(ny, nx, 8) => directions:
#   0=up,1=down,2=left,3=right,4=up-left,5=up-right,6=down-left,7=down-right
##############################################################################

# ---------------------------
# Build a random 8x8 coin that is unitary
# ---------------------------
def make_coin_8():
    """
    Creates a random 8x8 matrix, does an SVD, and reprojects it to be unitary.
    This ensures we have a local coin operator that won't destroy norm or cause blowups.
    """
    np.random.seed(42)  # reproducible
    mat = np.ones((8,8), dtype=np.complex128)
    alpha = 2.0
    for i in range(8):
        mat[i,i] -= alpha
    # small random perturbation
    rnd = 0.05*(np.random.rand(8,8) + 1j*np.random.rand(8,8))
    mat += rnd
    # SVD => force unitarity
    U, s, Vh = np.linalg.svd(mat, full_matrices=True)
    coin = U @ Vh
    return cp.array(coin, dtype=cp.complex128)

coin_8 = make_coin_8()  # global coin

# direction offsets
direction_offsets = [
    (-1,  0),  # up
    (+1,  0),  # down
    ( 0, -1),  # left
    ( 0, +1),  # right
    (-1, -1),  # up-left
    (-1, +1),  # up-right
    (+1, -1),  # down-left
    (+1, +1),  # down-right
]

##############################################################################
# COIN STEP => spin_out = coin_8 @ spin_in
##############################################################################
def coin_step(psi_in):
    ny_, nx_, _ = psi_in.shape
    # flatten => (ny*nx, 8)
    flat_in = psi_in.reshape((ny_*nx_, 8))
    # spin_out = spin_in @ coin_8.T  (or coin_8 @ spin_in, depending on your definition)
    flat_out = flat_in @ coin_8.T
    return flat_out.reshape((ny_, nx_, 8))

##############################################################################
# SHIFT STEP => move amplitude from (y,x,d) to (y+dy, x+dx, d)
##############################################################################
def shift_step(psi_in):
    ny_, nx_, _ = psi_in.shape
    psi_out = cp.zeros_like(psi_in)
    for d, (ofy, ofx) in enumerate(direction_offsets):
        shifted = cp.roll(psi_in[:,:,d], shift=ofy, axis=0)
        shifted = cp.roll(shifted, shift=ofx, axis=1)
        psi_out[:,:,d] = shifted
    return psi_out

##############################################################################
# BARRIER => zero out barrier row except slit columns
##############################################################################
def barrier_step(psi_in):
    psi_out = psi_in.copy()
    psi_out[barrier_row,:,:] = 0
    psi_out[barrier_row, slit1_xstart:slit1_xend, :] = psi_in[barrier_row, slit1_xstart:slit1_xend, :]
    psi_out[barrier_row, slit2_xstart:slit2_xend, :] = psi_in[barrier_row, slit2_xstart:slit2_xend, :]
    return psi_out

##############################################################################
# SINGLE TIMESTEP (Full wave => no measurement)
##############################################################################
def one_timestep(psi_in):
    after_coin = coin_step(psi_in)
    after_shift = shift_step(after_coin)
    after_barrier = barrier_step(after_shift)
    return after_barrier

##############################################################################
# MEASUREMENT AT BARRIER => collapse amplitude in barrier row
##############################################################################
def measure_collapse_barrier(psi_in):
    psi_out = cp.zeros_like(psi_in)
    # sum intensities across directions
    row_intens = cp.sum(cp.abs(psi_in[barrier_row,:,:])**2, axis=-1)
    keep = cp.zeros_like(row_intens)
    keep[slit1_xstart:slit1_xend] = row_intens[slit1_xstart:slit1_xend]
    keep[slit2_xstart:slit2_xend] = row_intens[slit2_xstart:slit2_xend]
    m = cp.max(keep)
    if m>1e-30:
        keep /= m
    amps = cp.sqrt(keep)
    # Instead of distributing amps among all directions => only put it in direction=0 (say "up")
    # direction=0 is the up channel, for example:
    d_up = 0
    psi_out[barrier_row, :, d_up] = amps
    return psi_out

##############################################################################
# UTILS
##############################################################################
def norm_sq(psi_in):
    return cp.sum(cp.abs(psi_in)**2)

##############################################################################
# MAIN RUN
##############################################################################
def run_experiment(collapse=False):
    """
    1) Build initial wave near bottom
    2) Evolve 'steps_to_barrier' steps
    3) Optionally measure at barrier row
    4) Evolve 'steps_after_barrier' steps
    """
    # Initial wave
    psi0 = cp.zeros((ny,nx,8), dtype=cp.complex128)
    src_y = 40  # near bottom
    sigma_y = 5.0
    for y in range(ny):
        dy = y - src_y
        amp = cp.exp(-0.5*(dy/sigma_y)**2)
        # wide in x => fill entire row in all directions
        for d in range(8):
            psi0[y,:,d] = amp

    psi = psi0.copy()
    # Evolve to barrier
    for _ in range(steps_to_barrier):
        psi = one_timestep(psi)
    # collapse if requested
    if collapse:
        psi = measure_collapse_barrier(psi)
    # Evolve more
    for _ in range(steps_after_barrier):
        psi = one_timestep(psi)
    return psi

def main():
    print("Running FULL wave (no barrier measurement)...")
    psi_full = run_experiment(collapse=False)
    print(f"Final norm (full)={norm_sq(psi_full).item():.3g}")

    print("Running COLLAPSED wave (with barrier measurement)...")
    psi_coll = run_experiment(collapse=True)
    print(f"Final norm (collapsed)={norm_sq(psi_coll).item():.3g}")

    # measure intensity at the detector row => sum over directions => shape=(nx,)
    int_full = cp.sum(cp.abs(psi_full[detector_row,:,:])**2, axis=-1)
    int_coll= cp.sum(cp.abs(psi_coll[detector_row,:,:])**2, axis=-1)

    # normalize each
    int_full /= cp.max(int_full)
    int_coll /= cp.max(int_coll)
    int_full_np = int_full.get()
    int_coll_np = int_coll.get()

    # BUILD 2D "SCREEN" => tile 1D intensity
    screen_height = 60
    screen_full = cp.tile(int_full, (screen_height,1)).get()
    screen_coll = cp.tile(int_coll, (screen_height,1)).get()

    # Now produce the 4 plots:
    # (1) Full Wave - 2D screen
    # (2) Full Wave - 1D profile
    # (3) Collapsed - 2D screen
    # (4) Collapsed - 1D profile

    plt.figure(figsize=(8,4))
    plt.imshow(screen_full, origin="lower", aspect="auto", cmap="inferno")
    plt.title("Full Wave – Detector Row (8-dir QWalk)")
    plt.xlabel("x-index")
    plt.ylabel("Screen Height")
    plt.colorbar(label="Normalized Intensity")

    plt.figure(figsize=(8,4))
    plt.plot(int_full_np, 'o-')
    plt.title("Full Wave – 1D Intensity at Detector")
    plt.xlabel("x-index")
    plt.ylabel("Intensity")

    plt.figure(figsize=(8,4))
    plt.imshow(screen_coll, origin="lower", aspect="auto", cmap="inferno")
    plt.title("Collapsed Wave – Detector Row (8-dir QWalk)")
    plt.xlabel("x-index")
    plt.ylabel("Screen Height")
    plt.colorbar(label="Normalized Intensity")

    plt.figure(figsize=(8,4))
    plt.plot(int_coll_np, 'o-')
    plt.title("Collapsed Wave – 1D Intensity at Detector")
    plt.xlabel("x-index")
    plt.ylabel("Intensity")

    plt.tight_layout()
    plt.show()

if __name__=="__main__":
    main()