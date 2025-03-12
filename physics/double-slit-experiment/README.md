# Conceptual Model Completeness Conjecture (CMCC) Quantum Walk Experiment

This project explore the double slit experiment from first principals.  It does not reference the Schrodinger equations direction, and does not have an impereative (procedural) function that propagates the wave.  Instead, entire experiment is a self describing data structure that contains all of the parameters for the entire experiment, tip to tail.

## DevOps

The repository expects the runtime environment to be Google Notebook (Colab) - this avoids build/runtime problems, as one of our main goals is to make this work easily reproducible/updateable.

When copying code from this repo into a new Colab document, you will need to set the `Runtime Type` to be a **GPU** rather than a **CPU** architecture.  You can choose `Change Runtime type`

When cupy is operational, you should be able to run the: `PAPER_Json-gpu-test.py` and see output something like this:

```CuPy version: 13.3.0
CUDA runtime version: 12060
Test Array Operation (should output a cupy array): [ 0  2  4  6  8 10 12 14 16 18]
```

## Experiments

There are a few different experiments that approach this from different angles.  To begin with, there is just a python "hand written" implementation.

### Hand-Code Experiments

These are hand code that follow a CMCC implementation strategy (i.e. functional and self describing) but they were written "by-hand" which means that any time the parameters of the experiment change, that hand-code will need to be udpated by-hand.

**NOTE:** This does *not* mean Human hands, it just means manually - human, ai, human+ai - it just has to be someone, and then that work has to be checked, by someone else, all of this has to be coordinated and orchested over time.  It's like an enterprise level game of telephone.

`PAPER_Json-no-schrodinger-functional-not-cmcc.ipynb`

This does not directly "follow" the CMCC ToE Meta-Model as the main code does.  

### CMCC Model of the Quantum Walk

#### 1. Grid Definition

- **GridID** *(Primary, Text)*: Unique grid identifier.
- **nx, ny** *(Integer)*: Grid resolution in x and y directions.
- **Lx, Ly** *(Float, 2 decimals, meters)*: Physical domain sizes.
- **dx, dy** *(Computed)*: Spatial steps calculated as Lx/nx and Ly/ny.
- **barrier_y_phys, detector_y_phys** *(Decimal, 2 places)*: Physical positions of barrier and detector.
- **barrier_row, detector_row** *(Computed)*: Grid indices computed from physical coordinates.
- **slit_width, slit_spacing** *(Integer)*: Defines geometry of double slits in grid points.
- **center_x, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend** *(Computed)*: Precisely determine slit placement.

#### 2. Coin Operator
- **CoinID** *(Primary, Text)*: Unique identifier.
- **seed** *(Integer)*: Initialization seed for reproducible coin generation.
- **Matrix** *(Tensor [8×8], Unitary)*: Defines local quantum state evolution.
- **Unitarity** *(Computed Boolean)*: Validates that `Matrix` is unitary.

#### 2. Wavefunction Snapshots
- **WaveID** *(Primary, Text)*: Unique snapshot identifier.
- **Grid** *(Link to Grid)*: Associates wavefunction with spatial domain.
- **Time** *(Integer)*: Discrete evolution time step.
- **psi** *(Complex Tensor [ny, nx, 8], Immutable)*: Quantum state amplitudes across grid points.
- **TotalNorm** *(Computed Real)*: Ensures wavefunction normalization.

#### 3. Quantum Evolution Steps
- **EvolutionID** *(Primary, Text)*: Identifier for evolution timestep.
- **InitialWave** *(Link to Wavefunction)*: State at time `t`.
- **EvolvedWave** *(Link to Wavefunction)*: Resulting state at time `t+1`.
- **CoinStep** *(Computed)*: Application of coin operator.
- **ShiftStep** *(Computed)*: Spatial redistribution according to quantum rules.
- **BarrierInteraction** *(Conditional Computed)*:
  - *No measurement:* Zero amplitudes outside slits at barrier.
  - *Measurement triggered:* Collapse wavefunction at barrier slits, aggregating and renormalizing amplitudes.

#### 4. Measurement Results
- **MeasurementID** *(Primary, Text)*: Unique measurement snapshot.
- **Wavefunction** *(Link to Wavefunction)*: Wavefunction snapshot for measurement.
- **DetectorIntensity** *(Computed Real Array)*: Probability intensity at detector, summing |ψ|².
- **ScreenOutput** *(Computed Visualization Array)*: Intensity tiled for visualization on screen output.

#### 5. Quantum Walk Run Management
- **RunnerID** *(Primary, Text)*: Tracks entire quantum walk run.
- **Grid, CoinOperator** *(Linked References)*: Defines grid and coin parameters.
- **StepsBeforeBarrier, StepsAfterBarrier** *(Integer)*: Evolution durations before and after barrier interaction.
- **CollapseTriggered** *(Boolean)*: Records whether collapse measurement occurred.
- **FinalWave** *(Link to Wavefunction)*: State after full quantum walk evolution.

### Emergent Meaning & Interpretation
- **First-order (Raw Data)**: Captures foundational parameters and quantum state amplitudes.
- **Second-Order (Computed Relationships)**: Spatial discretization, coin transformations, wavefunction evolution, barrier interactions.
- **Third-Order (Emergent Phenomena)**: Interference and diffraction patterns, probability distributions, measurement outcomes, and quantum behavioral insights dynamically inferred from computational processing rather than static linguistic description.

This schema enables a computationally-driven, non-linguistic representation of quantum phenomena, with meanings emerging dynamically through structured numerical transformations rather than static linguistic encoding.

