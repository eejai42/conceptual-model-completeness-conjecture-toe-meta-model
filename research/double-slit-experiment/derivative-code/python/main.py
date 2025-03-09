#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

# Import the classes/functions from the auto-generated helper
# (Replace "my_exp_helper" with the actual module name you generated)
from cmcc_helpers import (
    Grid, 
    WavefunctionInitial,
    QWalkRunner,       # assuming your JSON defines QWalkRunner
    DetectorAmplitude, # if your JSON defines these
    DetectorIntensity, # ...
    # etc. if needed
)

def main():
    # 1) Define a 201x201 grid with a barrier at y=0 and a detector at y=50
    grid = Grid(
        nx=201,
        ny=201,
        Lx=201.0,
        Ly=201.0,
        barrier_y_phys=0.0,
        detector_y_phys=50.0,
        slit_width=4,
        slit_spacing=12,
        boundary_conditions="periodic"
    )

    # 2) Build an initial wavefunction. You might have fields like src_y, sigma_y, etc.
    wfi = WavefunctionInitial(
        src_y=-70,
        sigma_y=10,
        kx=0.0,
        ky=0.0
    )
    # If your JSON references Grid.ny / Grid.nx internally, ensure you provide the grid
    # E.g., if your auto-generated code expects wfi.Grid to be set, do:
    wfi.Grid = grid

    # 3) Construct a coin matrix, e.g., a DFT-8
    dft8 = np.fft.fft(np.eye(8)) / np.sqrt(8)

    # 4) Create QWalkRunner or your equivalent class
    #    Suppose your JSON has a final_wavefunction = EVOLVE(...)
    #    and that you supply steps, coin_matrix, offsets, barrier, etc.
    offsets_8dir = [
        (-1,  0),
        (-1, +1),
        ( 0, +1),
        (+1, +1),
        (+1,  0),
        (+1, -1),
        ( 0, -1),
        (-1, -1),
    ]
    runner = QWalkRunner(
        steps_to_barrier=50,
        steps_after_barrier=50,
        collapse_barrier=False,
        coin_matrix=dft8,
        offsets=offsets_8dir,
        barrier_row=grid.barrier_row,
        slit1_xstart=grid.slit1_xstart,
        slit1_xend=grid.slit1_xend,
        slit2_xstart=grid.slit2_xstart,
        slit2_xend=grid.slit2_xend
    )

    # 5) Actually get the wavefunction. If your JSON references something like:
    #    final_wavefunction = EVOLVE(WavefunctionInitial.psi_init, steps_to_barrier, ...)
    #    then we do:
    #
    #    wavefunction = runner.final_wavefunction
    #
    # But you might need to set runner.psi_init = wfi.psi_init, depending on your schema.
    #
    # For example, if your JSON says:
    # "formula": "EVOLVE(WavefunctionInitial.psi_init, steps_to_barrier, steps_after_barrier, ...)"
    # then the auto-generated code might look up wfi.psi_init automatically if it's all wired up.
    # If not, you can assign it manually or pass it as an argument.  Let's assume it's wired:

    psi_init = wfi.psi_init  # an ndarray (201,201,8)
    # If your QWalkRunner references "WavefunctionInitial.psi_init" internally, no direct assignment is needed.
    # Otherwise, you might do runner.psi_init = psi_init.

    # Access the final wavefunction property (which calls EVOLVE behind the scenes)
    final_psi = runner.final_wavefunction  # calls EVOLVE(...) if that's how your JSON is set up

    # 6) Now we can slice the detector row. If your JSON has DetectorAmplitude, you can do:
    #    d_amp = DetectorAmplitude(psi_in=final_psi, detector_row=grid.detector_row)
    #    row_amp = d_amp.row_amp
    #    dint = DetectorIntensity(row_amp=row_amp)
    #    intensity_1d = dint.intensity_1d
    # Otherwise, do it manually:
    row_amp = final_psi[grid.detector_row, :, :]  # shape = (nx,8)
    intensity_1d = np.sum(np.abs(row_amp)**2, axis=-1)

    # 7) Plot or print some results
    print("Final wavefunction shape:", final_psi.shape)
    print("Detector row intensity (first 20 x-points):", intensity_1d[:20])

    # (Optional) Quick matplotlib
    plt.plot(intensity_1d, 'o-')
    plt.title("Detector Row Intensity")
    plt.xlabel("x-index")
    plt.ylabel("Intensity")
    plt.show()

if __name__ == "__main__":
    main()
