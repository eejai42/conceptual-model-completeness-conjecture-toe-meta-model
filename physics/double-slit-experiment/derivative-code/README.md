# README

## Grid

- **nx** - Number of grid points in the x-direction.
  - **Type:** number  

- **ny** - Number of grid points in the y-direction.
  - **Type:** number  

- **Lx** - Physical domain size in x.
  - **Type:** number  

- **Ly** - Physical domain size in y.
  - **Type:** number  

- **dx** - Spatial step in x (Lx / nx).
  - **Type:** calculated  
  - **Formula:** `DIVIDE(Lx,nx)`

- **dy** - Spatial step in y (Ly / ny).
  - **Type:** calculated  
  - **Formula:** `DIVIDE(Ly,ny)`

- **barrier_y_phys** - Physical y-coordinate where barrier is placed.
  - **Type:** number  

- **detector_y_phys** - Physical y-coordinate of the detector row.
  - **Type:** number  

- **barrier_row** - Barrier row index, computed from physical coordinate.
  - **Type:** calculated  
  - **Formula:** `FLOOR(DIVIDE(ADD(barrier_y_phys,DIVIDE(Ly,2)),dy))`

- **detector_row** - Detector row index, computed from physical coordinate.
  - **Type:** calculated  
  - **Formula:** `FLOOR(DIVIDE(ADD(detector_y_phys,DIVIDE(Ly,2)),dy))`

- **slit_width** - Number of grid columns spanned by each slit.
  - **Type:** number  

- **slit_spacing** - Distance (in columns) between the two slits.
  - **Type:** number  

- **center_x** - The x-center column index (middle of the domain).
  - **Type:** calculated  
  - **Formula:** `FLOOR(DIVIDE(nx,2))`

- **slit1_xstart** - Left edge of slit #1.
  - **Type:** calculated  
  - **Formula:** `SUBTRACT(center_x,FLOOR(DIVIDE(slit_spacing,2)))`

- **slit1_xend** - Right edge of slit #1.
  - **Type:** calculated  
  - **Formula:** `ADD(slit1_xstart,slit_width)`

- **slit2_xstart** - Left edge of slit #2.
  - **Type:** calculated  
  - **Formula:** `ADD(center_x,FLOOR(DIVIDE(slit_spacing,2)))`

- **slit2_xend** - Right edge of slit #2.
  - **Type:** calculated  
  - **Formula:** `ADD(slit2_xstart,slit_width)`

## CoinOperator

- **Matrix** - 8x8 unitary coin operator matrix.
  - **Type:** tensor  
  - **Tensor Shape:** (8,8)

- **seed** - Random seed for reproducibility.
  - **Type:** number  

- **UnitarityCheck** - Checks if Matrix * Matrix^† = I (tests unitarity).
  - **Type:** calculated  
  - **Formula:** `EQUAL(MULTIPLY(Matrix,CONJUGATE_TRANSPOSE(Matrix)),IDENTITY(8))`

## WavefunctionInitial

- **src_y** - Y-center of the initial Gaussian wave packet.
  - **Type:** number  

- **sigma_y** - Std. dev. of the Gaussian in y.
  - **Type:** number  

- **psi_init** - Initial wavefunction: Gaussian in y, uniform across x and spin directions.
  - **Type:** calculated  
  - **Tensor Shape:** (ny,nx,8)
  - **Formula:** `GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(src_y, sigma_y, Grid.ny, Grid.nx, 8)`

## CoinStep

- **psi_in** - Input wavefunction for the coin step.
  - **Type:** tensor  
  - **Tensor Shape:** (ny,nx,8)

- **coin_matrix** - Coin operator to be applied.
  - **Type:** tensor  
  - **Tensor Shape:** (8,8)

- **psi_out** - Applies the coin operator to each spin component.
  - **Type:** calculated  
  - **Tensor Shape:** (ny,nx,8)
  - **Formula:** `MATMUL(psi_in, TRANSPOSE(coin_matrix))`

## ShiftStep

- **psi_in** - Input wavefunction for the spatial shift.
  - **Type:** tensor  
  - **Tensor Shape:** (ny,nx,8)

- **offsets** - List of (dy,dx) offsets for each direction index (0..7).
  - **Type:** array  

- **psi_out** - Rolls each direction's amplitude by the specified (dy,dx) offsets.
  - **Type:** calculated  
  - **Tensor Shape:** (ny,nx,8)
  - **Formula:** `SHIFT(psi_in, offsets)`

## BarrierStep

- **psi_in** - Input wavefunction before barrier is applied.
  - **Type:** tensor  
  - **Tensor Shape:** (ny,nx,8)

- **barrier_row** - Row index of the barrier.
  - **Type:** number  

- **slit1_xstart** - Slit #1 start column.
  - **Type:** number  

- **slit1_xend** - Slit #1 end column.
  - **Type:** number  

- **slit2_xstart** - Slit #2 start column.
  - **Type:** number  

- **slit2_xend** - Slit #2 end column.
  - **Type:** number  

- **psi_out** - Zero out barrier row except in the slit columns.
  - **Type:** calculated  
  - **Tensor Shape:** (ny,nx,8)
  - **Formula:** `APPLY_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)`

## CollapseBarrierStep

- **psi_in** - Input wavefunction before measurement collapse at barrier.
  - **Type:** tensor  
  - **Tensor Shape:** (ny,nx,8)

- **barrier_row** - Barrier row index (where measurement occurs).
  - **Type:** number  

- **slit1_xstart** - Slit #1 start column.
  - **Type:** number  

- **slit1_xend** - Slit #1 end column.
  - **Type:** number  

- **slit2_xstart** - Slit #2 start column.
  - **Type:** number  

- **slit2_xend** - Slit #2 end column.
  - **Type:** number  

- **psi_out** - Implements a barrier measurement collapse: amplitude outside slits is lost.
  - **Type:** calculated  
  - **Tensor Shape:** (ny,nx,8)
  - **Formula:** `COLLAPSE_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)`

## WavefunctionNorm

- **psi_in** - Wavefunction whose norm we want to compute.
  - **Type:** tensor  
  - **Tensor Shape:** (ny,nx,8)

- **total_norm** - Computes the total probability norm: sum(|psi|^2).
  - **Type:** calculated  
  - **Formula:** `SUM(ABS(psi_in)^2)`

## DetectorAmplitude

- **psi_in** - Wavefunction to extract the detector row from.
  - **Type:** tensor  
  - **Tensor Shape:** (ny,nx,8)

- **detector_row** - Row index where the detector is located.
  - **Type:** number  

- **row_amp** - Extracts the wavefunction's amplitude at the detector row.
  - **Type:** calculated  
  - **Tensor Shape:** (nx,8)
  - **Formula:** `SLICE(psi_in, axis=0, index=detector_row)`

## DetectorIntensity

- **row_amp** - Detector row amplitude over x, with 8 spin directions.
  - **Type:** tensor  
  - **Tensor Shape:** (nx,8)

- **intensity_1d** - Sums |amplitude|^2 over spin directions, yielding intensity profile vs. x.
  - **Type:** calculated  
  - **Formula:** `SUM(ABS(row_amp)^2, axis=-1)`

## QWalkRunner

- **steps_to_barrier** - Number of steps taken before potentially measuring at the barrier.
  - **Type:** number  

- **steps_after_barrier** - Number of steps taken after the barrier event.
  - **Type:** number  

- **collapse_barrier** - If true, measure/collapse at the barrier; otherwise let the wave pass.
  - **Type:** boolean  

- **final_wavefunction** - Resulting wavefunction after the prescribed sequence of steps and optional barrier collapse.
  - **Type:** calculated  
  - **Formula:** `EVOLVE(WavefunctionInitial.psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier)`


