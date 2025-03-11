# Quantum Interpretations Unified Meta-Model

This repository defines a **unified JSON-based data schema** for quantum mechanical systems that seamlessly accommodates **Copenhagen**, **Many-Worlds**, and **Relational Quantum Mechanics (RQM)** interpretations. Instead of maintaining three entirely separate models, this schema provides shared core entities (e.g., wavefunction, measurement event) and leverages **interpretation-specific policies** to handle differences (collapse vs. branching vs. observer-relative states).

## Overview

The main file, [`unified_quantum_model.json`](./unified_quantum_model.json), contains definitions for entities such as:

- **QuantumState**:  
  Stores wavefunction (amplitude data) or references to density matrices.  
  May include branching references, entanglement measures, decoherence tracking, and more.

- **InterpretationPolicy**:  
  Indicates which interpretation (Copenhagen, Many-Worlds, RQM) applies to a given wavefunction, along with associated behavior (e.g., single-outcome collapse, branching, or observer-relative state updates).

- **MeasurementEvent**:  
  Logs measurement details, possible outcomes, time stamps, and references to observers.  
  The **execute_measurement** lambda uses the assigned `InterpretationPolicy` to decide if measurement collapses to one outcome, branches into multiple outcomes, or remains observer-specific.

- **ObserverFrame**:  
  For **Relational Quantum Mechanics**, each observer can have a vantage-specific wavefunction or partial knowledge.  
  This entity stores **contextual state data**—the slice or perspective of the wavefunction relevant to that observer.

- **BranchRecord**:  
  Represents wavefunction branches (primarily for Many-Worlds, but optionally for partial branching in RQM).  
  Each branch holds its own amplitude data, probability weighting, and coherence factors.

- **Observable**, **DensityMatrixRecord**, **Subsystem**, **DecoherenceChannel**, **QuantumEvolution**, **QuantumEvent**, **ObserverRelationship**, **ConsistencyCheck**, **QuantumCircuit**:  
  Additional entities that handle operators, density matrices, open-system noise channels, unitary evolution, event tracking, consistency checks, etc.  
  They are designed to support a wide range of quantum phenomena, from standard gate-based circuits to decoherence modeling and partial-trace-based entanglement measures.

## Key Features

1. **Interpretation Flexibility**  
   - Use the same core data structure for different quantum interpretations.  
   - The `InterpretationPolicy` entity drives how measurements and outcomes are processed.  
   - Copenhagen, Many-Worlds, and RQM are the primary included policies, but others could be added later.

2. **Common Core Entities**  
   - Regardless of interpretation, wavefunctions, measurements, observers, and branches have consistent definitions.  
   - Ensures that analysis tools, libraries, and GUIs can unify around one data structure.

3. **Observer-Relative Fields** (RQM Integration)  
   - RQM does not typically use a single “global wavefunction.” Instead, each observer sees a partial wavefunction or measurement record.  
   - `ObserverFrame` and `observer_relative_*` rollups handle vantage-dependent states.  
   - `allow_partial_branching` in `InterpretationPolicy` optionally spawns partial branches for RQM events.

4. **Measurement Handling**  
   - `MeasurementEvent` references a `wavefunction_id`, an `observable_operator`, possible outcomes, and the relevant observer.  
   - The `execute_measurement` lambda calls `InterpretationBasedMeasurement`, which checks the wavefunction’s `interpretation_id` to decide how to update state or spawn branches.

5. **Advanced Quantum Mechanics Support**  
   - **Density Matrices**: `DensityMatrixRecord` with Kraus operator updates for open systems.  
   - **Entanglement & Decoherence**: Rollups for entanglement entropy, decoherence mapping, partial traces, etc.  
   - **Quantum Circuits**: `QuantumCircuit` entity for gate-based operations; can generate or apply gate matrices.  
   - **Consistency & Event Logging**: `ConsistencyCheck`, `ObserverRelationship`, `QuantumEvent` let you track agreement across observers, handle event histories, or detect contradictory data.

## Getting Started

1. **Clone or Download** this repository, then locate the `unified_quantum_model.json`.
2. **Load** the JSON into your preferred environment:
   - A custom DSL or no-code platform that reads JSON-based schemas.
   - A knowledge graph or graph database that can interpret structured models.
   - A standard programming language with a JSON parser (Python, TypeScript, etc.).
3. **Initialize Entities**:
   - Start by creating `InterpretationPolicy` records for your chosen interpretation(s).
   - Create one or more `QuantumState` records with amplitude data.
   - Perform or simulate `MeasurementEvent`s to see how states evolve or branch.
   - Create `ObserverFrame` records to represent your RQM observers if needed.

## Usage Example

1. **Define an Interpretation Policy**:

   ```json
   {
     "interpretation_id": "policy_mw_01",
     "interpretation_name": "ManyWorlds",
     "collapse_behavior": "branch",
     "observer_specificity": false,
     "metadata": {
       "branch_weight": "equal"
     },
     "allow_partial_branching": false
   }
   ```

2. **Create a QuantumState**:
   ```json
   {
     "state_id": "wf_001",
     "description": "2-qubit system",
     "amplitude_data": [ /* complex vector data */ ],
     "interpretation_id": "policy_mw_01"
   }
   ```

3. **Perform a Measurement**:
   ```json
   {
     "meas_id": "meas_001",
     "wavefunction_id": "wf_001",
     "measurement_type": "spin_z",
     "observable_operator": { /* operator matrix */ },
     "possible_outcomes": { /* basis projections */ },
     "time_stamp": "2025-03-10T10:00:00Z",
     "observer_id": null,   // Not needed for ManyWorlds
     "selected_outcome": "", // Will be filled after measurement
     "branch_ids_generated": []
   }
   ```
   - Running the `execute_measurement` lambda spawns new `BranchRecord`s.

4. **Track Branches or Collapses**  
   - If **Many-Worlds**: after measurement, multiple `BranchRecord`s reference the parent `wavefunction_id = wf_001`.
   - If **Copenhagen**: the `selected_outcome` is assigned, and amplitude data is collapsed.
   - If **RQM**: partial updates to the observer’s local state in `ObserverFrame.contextual_state_data`.

## Extending the Schema

- **Add New Interpretations**: Just create an `InterpretationPolicy` record with your logic for measurement and branching.  
- **Add Additional Observables**: The `Observable` entity includes a `matrix_representation`; just link it to measurement events.  
- **Create Lambdas or Aggregations**: The JSON allows you to define new formulas (rollups, constraints, or lambdas) for advanced quantum phenomena (e.g., topological qubits, gauge invariants).

## Contributing

1. **Fork or Clone** this repo.  
2. **Branch Off** and add your enhancements to the `unified_quantum_model.json` file:
   - Additional fields, constraints, or lambdas for more specialized quantum effects.
   - Further expansions to the RQM approach, multi-observer entanglement, or advanced HPC integration.
3. **Pull Requests**: Submit a PR describing your changes, test coverage, and rationale.

---

**Thanks for checking out the Quantum Interpretations Unified Meta-Model!** With this schema, you can explore various quantum interpretations in a consistent data structure, pivoting between single-outcome, branching, or observer-relative viewpoints without re-writing your entire system. Feel free to adapt and extend it for your own research or applications.