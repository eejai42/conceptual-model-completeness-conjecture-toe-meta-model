#!/usr/bin/env python3

import numpy as np
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Grid:
    nx: int
    ny: int
    Lx: float
    Ly: float
    barrier_y_phys: float
    detector_y_phys: float
    slit_width: int
    slit_spacing: int

    @property
    def dy(self): 
        return self.Ly / self.ny
    @property
    def barrier_row(self):
        return int((self.barrier_y_phys + self.Ly/2) / self.dy)
    @property
    def detector_row(self):
        return int((self.detector_y_phys + self.Ly/2) / self.dy)

    @property
    def slit_regions(self):
        cx = self.nx // 2
        half_spacing = self.slit_spacing // 2
        return [
            (cx - half_spacing, cx - half_spacing + self.slit_width),
            (cx + half_spacing, cx + half_spacing + self.slit_width)
        ]

@dataclass(frozen=True)
class CoinOperator:
    matrix: np.ndarray
    seed: int

    @property
    def is_unitary(self):
        return np.allclose(self.matrix @ self.matrix.conj().T, np.eye(8))

@dataclass(frozen=True)
class Timestep:
    grid: Grid
    coin_operator: CoinOperator
    previous: Optional['Timestep']
    timestep: int

    @property
    def psi(self):
        if self.previous is None:
            y = np.arange(self.grid.ny).reshape(-1,1,1)
            sigma_y = 5.0
            amplitude = np.exp(-0.5*((y - 40)/sigma_y)**2)
            return np.tile(amplitude, (1, self.grid.nx, 8))
        else:
            # pure structural reference—no imperative looping here
            return self.barrier * self.shifted

    @property
    def coin_step(self):
        return np.matmul(self.previous.psi, self.coin_operator.matrix.T)

    @property
    def shifted(self):
        offsets = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        return np.stack([
            np.roll(self.coin_step[:,:,d], shift=offsets[d], axis=(0,1))
            for d in range(8)
        ], axis=-1)

    @property
    def barrier(self):
        mask = np.zeros((self.grid.ny, self.grid.nx, 8))
        mask[self.grid.barrier_row, self.grid.slit1_xstart:self.grid.slit1_xend, :] = 1
        mask[self.grid.barrier_row, self.grid.slit2_xstart:self.grid.slit2_xend, :] = 1
        mask[:self.grid.barrier_row, :, :] = 1
        mask[self.grid.barrier_row+1:, :, :] = 1
        return mask

    @property
    def psi_out(self):
        return self.shifted * self.barrier

# ONE main function (structural entry point)
def main():
    grid = Grid(nx=701, ny=701, Lx=16.0, Ly=16.0, barrier_y_phys=-2.0, detector_y_phys=5.0, slit_width=3, slit_spacing=20)
    coin_matrix = np.eye(8, dtype=np.complex128)
    coin_operator = CoinOperator(matrix=coin_matrix, seed=42)

    t0 = Timestep(grid=grid, coin_operator=coin_operator, previous=None, timestep=0)
    t1 = Timestep(grid=grid, coin_operator=coin_operator, previous=timestep0, timestep=1)
    # etc. Add timesteps structurally

    # Example structural query:
    intensity_t1 = t1.psi[grid.detector_row,:,:].sum(axis=-1)
    print(intensity_t1)

if __name__ == "__main__":
    main()
