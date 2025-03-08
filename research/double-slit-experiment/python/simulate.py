import cupy as cp
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
#                             SPLIT OPERATOR 2D                              #
##############################################################################

# ---------------------------
# Simulation Parameters
# ---------------------------
nx, ny = 128, 128     # grid size in x and y
Lx, Ly = 20.0, 20.0   # physical size of the region (for wavevectors)
dx = Lx / nx
dy = Ly / ny

xvals = cp.linspace(-Lx/2, Lx/2 - dx, nx)
yvals = cp.linspace(-Ly/2, Ly/2 - dy, ny)
X, Y = cp.meshgrid(xvals, yvals)  # shape (ny, nx)

# Times
dt = 0.02
# total steps for the entire simulation
# We'll just break them into "to barrier" and "to detector" below
nsteps = 2000

# "m = 1/2 => kinetic operator is -1/2 * laplacian" => wave eq is i d/dt psi = -1/2 nabla^2 psi + V psi
# We'll incorporate that factor 1/2 in the exponent for the free propagation step.

# ---------------------------
# Potential: A 2D double-slit
# ---------------------------
barrier_y_min = -0.2
barrier_y_max =  0.2
barrier_height = 100.0  # large but finite

slit_width   = 0.3
slit_spacing = 1.2
slit1_center = -slit_spacing / 2
slit2_center =  slit_spacing / 2

def make_potential():
    V = cp.zeros((ny, nx), dtype=cp.float64)

    # Horizontal barrier near y=0
    mask_barrier = (Y >= barrier_y_min) & (Y <= barrier_y_max)
    V[mask_barrier] = barrier_height

    # Carve out 2 slits
    half_w = slit_width / 2
    # slit1 region in x
    slit1_left, slit1_right = (slit1_center - half_w), (slit1_center + half_w)
    slit1_mask = (X >= slit1_left) & (X < slit1_right) & mask_barrier
    # slit2 region in x
    slit2_left, slit2_right = (slit2_center - half_w), (slit2_center + half_w)
    slit2_mask = (X >= slit2_left) & (X < slit2_right) & mask_barrier

    # zero potential in slit areas
    V[slit1_mask] = 0.0
    V[slit2_mask] = 0.0

    return V

V = make_potential()

# ---------------------------
# FFT wave vectors (kx, ky)
# ---------------------------
kx_vals = 2.0 * np.pi * np.fft.fftfreq(nx, d=dx)
ky_vals = 2.0 * np.pi * np.fft.fftfreq(ny, d=dy)

kx_vals = cp.array(kx_vals)
ky_vals = cp.array(ky_vals)

KX, KY = cp.meshgrid(kx_vals, ky_vals)  # shape (ny, nx)
k2 = (KX**2 + KY**2)

# Exponential factor for the free propagation step: e^{- i (1/2) k^2 dt}
def kinetic_phase(k2, dt):
    return cp.exp(-0.5j * k2 * dt)

# ---------------------------
# Initialize wavefunction
# ---------------------------
def make_initial_wave():
    """
    A Gaussian wave packet near y=-5 with upward momentum.
    """
    sigma = 1.0
    y0 = -5.0
    k0 = 2.0  # initial upward wave number

    # Make a float array, then cast to complex
    psi = cp.exp(-((X)**2 + (Y - y0)**2) / (2*sigma**2)).astype(cp.complex128)
    
    # Multiply by plane-wave factor
    plane_factor = cp.exp(1j * k0 * (Y - y0))
    psi *= plane_factor

    # Normalize
    norm = cp.sqrt(cp.sum(cp.abs(psi)**2))
    psi /= norm
    return psi

# ---------------------------
# SPLIT STEP: one time step
# ---------------------------
def split_step(psi, V, dt):
    """
    i d/dt Psi = -1/2 laplacian(Psi) + V Psi
    => Psi_{new} ~ e^{-i V dt/2} FFT -> e^{-i (k^2/2) dt} -> IFFT -> e^{-i V dt/2}
    """
    # 1) half-step in potential
    psi *= cp.exp(-0.5j * V * dt)

    # 2) full-step in kinetic
    psi_k = cp.fft.fft2(psi)
    psi_k *= kinetic_phase(k2, dt)
    psi = cp.fft.ifft2(psi_k)

    # 3) half-step in potential
    psi *= cp.exp(-0.5j * V * dt)

    return psi

# ---------------------------
# Collapse at Slits
# ---------------------------
def collapse_wave_at_slits(psi, V):
    """
    We measure the wave in the barrier region (barrier_y_min..barrier_y_max),
    but only keep the amplitude in the slits (where V=0). Everything else zeroed.
    We'll also normalize that amplitude within the slit region.
    """
    psi_host = psi.get()  # move to CPU to handle masking easily
    V_host = V.get()

    # barrier region
    mask_barrier = (Y.get() >= barrier_y_min) & (Y.get() <= barrier_y_max)
    # slit region is where V=0 in that barrier
    mask_slit = (mask_barrier) & (np.abs(V_host) < 1e-12)

    intensities = np.abs(psi_host)**2
    slit_vals = intensities[mask_slit]
    if slit_vals.size == 0:
        # no slit region found, just return zeros
        new_host = np.zeros_like(psi_host, dtype=np.complex128)
        return cp.array(new_host)

    max_val = slit_vals.max()
    new_host = np.zeros_like(psi_host, dtype=np.complex128)
    if max_val > 1e-30:
        # put normalized intensities only in the slit region
        new_host[mask_slit] = intensities[mask_slit] / max_val

    return cp.array(new_host)

# ---------------------------
# MAIN RUN
# ---------------------------
def run_experiment(collapse_at_slits=False):
    print(f"\n=== Running Experiment: collapse={collapse_at_slits} ===")
    psi = make_initial_wave()

    # Evolve until wave reaches barrier
    print("Evolving to barrier...")
    nsteps_to_barrier = 400
    for step in range(nsteps_to_barrier):
        psi = split_step(psi, V, dt)
        if step % 100 == 0:
            amp = cp.sum(cp.abs(psi)**2).item()
            print(f"  step {step:4d}  total |psi|^2 = {amp:.2e}")

    if collapse_at_slits:
        print("Collapsing (measuring) at barrier row...")
        psi = collapse_wave_at_slits(psi, V)

    # Continue from barrier to top
    print("Continuing from barrier to detector...")
    nsteps_to_detector = 600
    for step in range(nsteps_to_detector):
        psi = split_step(psi, V, dt)
        if step % 100 == 0:
            amp = cp.sum(cp.abs(psi)**2).item()
            print(f"  step {step:4d}  total |psi|^2 = {amp:.2e}")

    # Suppose we detect around y = +5
    detector_y = 5.0
    idx_det = int((detector_y + Ly/2.0)/dy)

    row_psi = psi[idx_det, :]
    intensity = cp.abs(row_psi)**2
    intensity_np = intensity.get()
    intensity_max = intensity_np.max()
    if intensity_max < 1e-30:
        intensity_max = 1.0
    norm_intensity = intensity_np / intensity_max

    # 2D screen
    screen_height = 80
    screen_image = np.tile(norm_intensity, (screen_height, 1))

    return {
        "psi": psi.get(),
        "intensity": intensity_np,
        "screen_image": screen_image,
        "detector_index": idx_det
    }


##############################################################################
# Run and Visualize
##############################################################################
res_wave = run_experiment(collapse_at_slits=False)
res_collapse = run_experiment(collapse_at_slits=True)

plt.figure(figsize=(8,4))
plt.imshow(res_wave["screen_image"], origin="lower", aspect="auto", cmap="inferno")
plt.title("Full Wave – Detector Row Visualization")
plt.colorbar(label="Normalized Intensity")
plt.xlabel("x-index")
plt.ylabel("Screen 'height'")
plt.show()

plt.figure(figsize=(8,4))
plt.plot(res_wave["intensity"], 'o-')
plt.title("Full Wave – Detector Row 1D Intensity")
plt.xlabel("x-index")
plt.ylabel("Intensity")
plt.show()

plt.figure(figsize=(8,4))
plt.imshow(res_collapse["screen_image"], origin="lower", aspect="auto", cmap="inferno")
plt.title("Collapsed Wave – Detector Row Visualization")
plt.colorbar(label="Normalized Intensity")
plt.xlabel("x-index")
plt.ylabel("Screen 'height'")
plt.show()

plt.figure(figsize=(8,4))
plt.plot(res_collapse["intensity"], 'o-')
plt.title("Collapsed Wave – Detector Row 1D Intensity")
plt.xlabel("x-index")
plt.ylabel("Intensity")
plt.show()
