# quantum_walk_blocks.py

import numpy as np

def SHIFT(psi_in, offsets):
    """
    SHIFT each spin component by the specified (dy, dx).
    psi_in: shape = (ny, nx, spin_dim)
    offsets: list of (ofy, ofx), e.g. for an 8D walk
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
    Zero out wavefunction in barrier_row except for the slit columns.
    """
    psi_out = psi_in.copy()
    psi_out[barrier_row, :, :] = 0
    psi_out[barrier_row, slit1_xstart:slit1_xend, :] = psi_in[barrier_row, slit1_xstart:slit1_xend, :]
    psi_out[barrier_row, slit2_xstart:slit2_xend, :] = psi_in[barrier_row, slit2_xstart:slit2_xend, :]
    return psi_out

def COLLAPSE_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
    """
    Example barrier measurement: amplitude outside the slits is lost.
    """
    psi_out = np.zeros_like(psi_in)
    # Sum intensities across directions
    row_intens = np.sum(np.abs(psi_in[barrier_row, :, :])**2, axis=-1)
    keep = np.zeros_like(row_intens)
    keep[slit1_xstart:slit1_xend] = row_intens[slit1_xstart:slit1_xend]
    keep[slit2_xstart:slit2_xend] = row_intens[slit2_xstart:slit2_xend]
    amps = np.sqrt(keep)
    # Place them in direction=0 (say "up")
    d_up = 0
    psi_out[barrier_row, :, d_up] = amps
    return psi_out

def GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(src_y, sigma_y, ny, nx, spin_dim):
    """
    Returns a np array (ny, nx, spin_dim) that is Gaussian in y
    but uniform in x & directions.
    """
    arr = np.zeros((ny, nx, spin_dim), dtype=np.complex128)
    ycoords = np.arange(ny)
    gauss_y = np.exp(-0.5*((ycoords - src_y)/sigma_y)**2)
    # Normalize in y
    norm_factor = np.sqrt(np.sum(np.abs(gauss_y)**2))
    gauss_y /= norm_factor

    # Fill across x & directions
    for d in range(spin_dim):
        for x in range(nx):
            arr[:, x, d] = gauss_y
    return arr


def EVOLVE(psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier,
           coin_matrix=None, offsets=None,
           barrier_row=None, slit1_xstart=None, slit1_xend=None,
           slit2_xstart=None, slit2_xend=None):
    """
    EVOLVE can be called with 4 or up to 11 arguments. The last 7 can be None,
    in which case we define defaults or skip them.
    """
    # Example defaults if not provided:
    if coin_matrix is None:
        # e.g. 8D DFT coin
        coin_matrix = np.fft.fft(np.eye(8)) / np.sqrt(8)
    if offsets is None:
        offsets = [
            (-1,0), (-1,1), (0,1), (1,1),
            (1,0), (1,-1), (0,-1), (-1,-1)
        ]
    if barrier_row is None:
        barrier_row = 100
    if slit1_xstart is None:
        slit1_xstart = 90
    if slit1_xend is None:
        slit1_xend = 95
    if slit2_xstart is None:
        slit2_xstart = 105
    if slit2_xend is None:
        slit2_xend = 110

    psi = psi_init
    # same logic as your original EVOLVE
    for _ in range(steps_to_barrier):
        # coin step
        ny, nx, spin_dim = psi.shape
        psi_flat = psi.reshape(ny*nx, spin_dim)
        out_flat = psi_flat @ coin_matrix.T
        psi_coin = out_flat.reshape((ny,nx,spin_dim))

        psi_shift = SHIFT(psi_coin, offsets)
        psi = APPLY_BARRIER(psi_shift, barrier_row,
                            slit1_xstart, slit1_xend,
                            slit2_xstart, slit2_xend)

    if collapse_barrier:
        psi = COLLAPSE_BARRIER(psi, barrier_row,
                               slit1_xstart, slit1_xend,
                               slit2_xstart, slit2_xend)

    for _ in range(steps_after_barrier):
        ny, nx, spin_dim = psi.shape
        psi_flat = psi.reshape(ny*nx, spin_dim)
        out_flat = psi_flat @ coin_matrix.T
        psi_coin = out_flat.reshape((ny,nx,spin_dim))

        psi_shift = SHIFT(psi_coin, offsets)
        psi = APPLY_BARRIER(psi_shift, barrier_row,
                            slit1_xstart, slit1_xend,
                            slit2_xstart, slit2_xend)

    return psi