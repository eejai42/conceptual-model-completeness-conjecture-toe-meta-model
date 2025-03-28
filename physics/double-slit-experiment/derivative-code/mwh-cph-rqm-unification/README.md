# Quantum Interpretations Unified Meta-Model

This repository defines a **unified JSON-based data schema** for quantum mechanical systems that seamlessly accommodates **Copenhagen**, **Many-Worlds**, and **Relational Quantum Mechanics (RQM)** interpretations. Instead of maintaining three entirely separate models, this schema provides shared core entities (e.g., wavefunction, measurement event) and leverages **interpretation-specific policies** to handle differences (collapse vs. branching vs. observer-relative states). It also integrates **multi-observer** scenarios (RQM), advanced **entanglement** and **decoherence** tracking, and **foundational inequality** checks (Bell, GHZ/Mermin, Hardy’s paradox, etc.) via a variety of aggregator formulas.

## Overview

The main file, [`unified_quantum_model.json`](./unified_quantum_model.json), defines several entities, each with fields, **rollups** (aggregations), **lambdas** (computed functions), and **constraints**. Some of the major entities:

- **QuantumState**  
  Stores wavefunction (amplitude data) or references to density matrices.  
  Includes optional branching references, coherence/decoherence monitoring, subsystem partitions for entanglement measures, partial‐trace features, and more.  
  Key aggregator examples include:
  - **`history_decoherence_check`**: Evaluates whether the wavefunction’s measurement events and branches remain consistent with “decohered histories” (Many‐Worlds) or partial‐collapse logic.  
  - **`ghz_mermin_violation_indicator`**, **`bell_inequality_check`**, **`hardys_paradox_indicator`**, etc.: Standard quantum‐foundational tests that detect nonlocal or contextual behavior in measurement outcomes referencing this wavefunction.  
  - **`multi_partition_entanglement_map`**: Evaluates entanglement across all bipartitions (or tripartitions) to classify the global state structure.  
  - **`interpretation_usage_summary`**: Summarizes how measurement events on this wavefunction have been handled (single‐outcome, branching, or observer‐relative).

- **InterpretationPolicy**  
  Indicates which interpretation (Copenhagen, Many-Worlds, RQM) applies to a given wavefunction, along with associated behavior (e.g., single-outcome collapse, branching, or observer-relative updates).  
  - Supports **`allow_partial_branching`** (for specialized or RQM scenarios).  
  - Includes aggregator checks like **`interpretation_consistency_check`** to ensure the chosen policy settings (collapse_behavior, observer_specificity) are coherent.

- **MeasurementEvent**  
  Logs measurement details, possible outcomes, time stamps, and references to observers.  
  - The **`execute_measurement`** lambda uses the `InterpretationPolicy` of the targeted wavefunction to decide if measurement collapses to a single outcome, spawns multiple branches, or updates only observer-relative data.  
  - Aggregators like **`interpretation_inference`** and **`policy_vs_outcome_consistency`** detect mismatches between expected and actual measurement behavior.

- **ObserverFrame**  
  Manages vantage-specific wavefunction data (especially for **Relational Quantum Mechanics**).  
  - Each observer can hold partial wavefunction snapshots or local “knowledge states.”  
  - Aggregators include **`quantum_darwinism_index`**, **`self_vs_external_consistency`** (checks the observer’s internal timeline vs. how other observers record them), and **`darwinist_redundancy_curve`** (to analyze environment‐assisted classicality from the perspective of this observer).

- **BranchRecord**  
  Represents wavefunction branches (particularly for Many-Worlds, but optionally for partial branching in RQM).  
  - Stores branch‐specific amplitude data, probability weight, coherence/interference factors, references to parent branches, and observer scope in partial branching scenarios.  
  - Aggregators include **`branch_interference_inference`**, **`branch_reunion_check`**, and **`branch_merge_probability`** that let you detect potential re‐interference or partial merges in RQM contexts.

- **Observable**, **DensityMatrixRecord**, **Subsystem**, **DecoherenceChannel**, **QuantumEvolution**, **QuantumEvent**, **ObserverRelationship**, **ConsistencyCheck**, **QuantumCircuit**  
  Various supporting entities handle:
  - **Operators / Observables** (Hermitian checks, eigenvalues, etc.).  
  - **Density Matrices** (Kraus updates, partial trace, tomography checks).  
  - **Subsystems** (IDs and dimensional data).  
  - **Decoherence / Noise Channels** (Kraus operators, validation of completeness).  
  - **Time Evolution** (Hamiltonian references, unitary or Trotter steps).  
  - **Event Logging** (QuantumEvents for broader actions than just measurements).  
  - **Observer Relationships** (cross‐observer consistency checks, Wigner’s friend paradox indicators).  
  - **Consistency Checks** (general logs of warnings/errors).  
  - **Quantum Circuits** (gate lists, circuit‐matrix generation, a convenient aggregator to apply and measure gates in one shot).

- **IntersubjectiveRecord**  
  Aggregates how multiple observers come to (or fail to reach) a mutual outcome in RQM contexts.  
  - Tracks a list of participants, final state agreement, and aggregator fields for multi‐observer discrepancy and paradox detection (e.g., multi‐level nested Wigner’s friend scenarios).  

---

## Key Features

1. **Interpretation Flexibility**  
   - Use the same core data structure for Copenhagen, Many-Worlds, or RQM.  
   - The `InterpretationPolicy` drives how measurements and outcomes are processed.  
   - Built‐in checks ensure that a wavefunction’s assigned policy matches how measurements actually unfold.

2. **Common Core Entities**  
   - Regardless of interpretation, wavefunctions, measurements, observers, and branches share consistent definitions.  
   - Tools or GUIs can unify around one data structure and selectively rely on interpretation-specific aggregator logic where needed.

3. **Observer-Relative Integration** (RQM)  
   - **`ObserverFrame`** and aggregator fields like **`observer_relative_outcomes`** handle vantage‐dependent states and partial branching.  
   - **`ObserverRelationship`** helps detect Wigner’s friend‐type paradoxes or cyclical measurement loops.

4. **Measurement Handling**  
   - **`MeasurementEvent`** references a wavefunction plus an observable and possible outcomes.  
   - **`execute_measurement`** calls an interpretation‐based routine (Copenhagen collapse, Many‐Worlds branching, or RQM observer‐update).

5. **Advanced Quantum Mechanics Support**  
   - **Density Matrices**: `DensityMatrixRecord` with Kraus operator updates for open systems, purity checks, tomography aggregator.  
   - **Entanglement & Decoherence**: partial‐trace entanglement measures, decoherence mapping, branching orthogonality checks, consistent histories (Many‐Worlds).  
   - **Quantum Circuits**: `QuantumCircuit` entity for gate‐based operations; aggregator to apply gates and measure.  
   - **Foundational Tests**: CHSH/Bell, GHZ/Mermin, Hardy’s paradox, Leggett‐Garg, Kochen‐Specker checks built into aggregator formulas on wavefunctions.  
   - **Multi-Observer** consistency checks (RQM) and **Wigner’s Friend** detection in `ObserverRelationship`.

---

## Getting Started

1. **Clone or Download** this repository, then locate the `unified_quantum_model.json`.
2. **Load** the JSON into your environment of choice:
   - A custom DSL or no-code platform that reads JSON-based schemas.
   - A knowledge graph or graph database that interprets structured models.
   - A general programming language (Python, TypeScript, etc.) with JSON parsing.
3. **Initialize Entities**:
   - **InterpretationPolicy**: Create or select a record for your target interpretation approach.
   - **QuantumState**: Instantiate one or more wavefunction records (or link to a density matrix).
   - **MeasurementEvent**: Simulate or record measurements, letting each event update or spawn branches per the wavefunction’s `interpretation_policy_id`.
   - **ObserverFrame**: For RQM, define vantage‐specific frames that track partial wavefunction data.

---

## Example Workflow

1. **Define an Interpretation Policy**  
   ```json
   {
     "interpretation_policy_id": "policy_mw_01",
     "interpretation_name": "ManyWorlds",
     "collapse_behavior": "branch",
     "observer_specificity": false,
     "metadata": {
       "branch_weight": "equal"
     },
     "allow_partial_branching": false
   }
   ```

2. **Create a QuantumState**  
   ```json
   {
     "state_id": "wf_001",
     "description": "2-qubit system",
     "amplitude_data": [ /* complex amplitude vector */ ],
     "interpretation_policy_id": "policy_mw_01"
   }
   ```

3. **Perform a Measurement**  
   ```json
   {
     "meas_id": "meas_001",
     "wavefunction_id": "wf_001",
     "measurement_type": "spin_z",
     "observable_operator": { /* matrix or operator definition */ },
     "possible_outcomes": { /* outcome labels, projection operators */ },
     "time_stamp": "2025-03-10T10:00:00Z",
     "observer_id": null,   // Not needed for ManyWorlds
     "selected_outcome": "", // Will be set after measurement
     "branch_ids_generated": []
   }
   ```
   - Calling the **`execute_measurement`** lambda spawns new `BranchRecord`s (in Many-Worlds).

4. **Track Branches or Collapses**  
   - **Many-Worlds**: You’ll see multiple `BranchRecord`s referencing `wavefunction_id = wf_001`.  
   - **Copenhagen**: The `selected_outcome` is assigned; amplitude data is collapsed.  
   - **RQM**: Partial updates appear in each observer’s `ObserverFrame.contextual_state_data`.

5. **Leverage Aggregator Checks**  
   - For **Bell** or **GHZ** tests, you can define more measurement events in different bases and consult e.g. `QuantumState.bell_inequality_check`.  
   - For **RQM** vantage checks, compare `ObserverFrame.self_vs_external_consistency` or `ObserverRelationship.wigners_friend_paradox_indicator`.

---

## **Extended Aggregators & Inferences**

In addition to the existing aggregator fields, we have introduced several new rollups that leverage the references and relationships already in the schema. They provide extra scenario‐wide or circuit‐level analysis, including:

**For `GlobalScenarioRecord`:**
- **`scenario_measurement_count`** – Counts how many MeasurementEvents are linked to this scenario.  
- **`interpretation_distribution`** – Tally of how many wavefunctions use each interpretation.  
- **`scenario_active_observers_count`** – How many ObserverFrames are active in this scenario.  
- **`scenario_interpretation_mismatch_events`** – Lists measurement events that conflict with their wavefunction’s assigned interpretation policy (e.g., branching in a Copenhagen wavefunction).

**For `QuantumCircuit`:**
- **`gate_count`** – Tallies the total number of gates in the `gates` array.  
- **`circuit_depth`** – Computes the number of sequential “layers” in the circuit (user-defined logic).  
- **`controlled_gate_count`** – Counts how many gates have a non-null `control` field (e.g. CNOT).

**For `QuantumEvolution`:**
- **`unitarity_deviation`** – Estimates numerical deviation from perfect unitarity under the chosen evolution method (e.g., Trotter or exact exponentiation).  

A short snippet to add these fields (for your convenience) is shown below. You can copy this directly into your `unified_quantum_model.json`, appending the new aggregations to each respective entity:

```jsonc
{
  "entities": [
    {
      "name": "GlobalScenarioRecord",
      "aggregations": [
        {
          "name": "scenario_measurement_count",
          "type": "rollup",
          "formula": "COUNT(linked_measurements)",
          "description": "Counts how many MeasurementEvents are linked to this scenario."
        },
        {
          "name": "interpretation_distribution",
          "type": "rollup",
          "formula": "ComputeInterpretationDistribution(linked_wavefunctions)",
          "description": "Returns a JSON object tallying how many wavefunctions use each interpretation policy (e.g. { 'Copenhagen': 2, 'ManyWorlds': 3, 'RQM': 1 })."
        },
        {
          "name": "scenario_active_observers_count",
          "type": "rollup",
          "formula": "COUNT(linked_observers)",
          "description": "Counts how many ObserverFrames are active in this scenario."
        },
        {
          "name": "scenario_interpretation_mismatch_events",
          "type": "rollup",
          "formula": "ListInterpretationMismatches(linked_wavefunctions, linked_measurements)",
          "description": "Returns a list of measurement events that conflict with their wavefunction’s assigned interpretation."
        }
      ]
    },
    {
      "name": "QuantumCircuit",
      "aggregations": [
        {
          "name": "gate_count",
          "type": "rollup",
          "formula": "LENGTH(gates)",
          "description": "Simple aggregator that returns the total number of gates in this circuit."
        },
        {
          "name": "circuit_depth",
          "type": "rollup",
          "formula": "ComputeCircuitDepth(gates)",
          "description": "A user-defined aggregator that calculates circuit depth based on how gates can be grouped into layers."
        },
        {
          "name": "controlled_gate_count",
          "type": "rollup",
          "formula": "COUNT(gates WHERE gates.control IS NOT NULL)",
          "description": "Counts how many gates specify a 'control' field (e.g. CNOT, Toffoli)."
        }
      ]
    },
    {
      "name": "QuantumEvolution",
      "aggregations": [
        {
          "name": "unitarity_deviation",
          "type": "rollup",
          "formula": "ComputeUnitarityDeviation(hamiltonian_ref, time_step, evolution_method)",
          "description": "Estimates non-unitary error from approximate or noisy time evolution. Returns 0 if fully unitary."
        }
      ]
    }
  ]
}
```

Feel free to adapt the aggregator **formulas** to your environment or aggregator library (e.g., define or import `ComputeInterpretationDistribution()`, `ComputeCircuitDepth()`, etc.).

---

## Extending the Schema

1. **Add New Interpretations**: Define an `InterpretationPolicy` record with your custom measurement or branching logic.  
2. **Add Observables**: Use the `Observable` entity’s matrix fields and link them to measurements.  
3. **Create Lambdas & Aggregators**: The JSON allows you to embed new formulas, constraints, or advanced aggregator logic for specialized quantum effects (topological qubits, gauge invariants, etc.).  
4. **Add “Aggregator of Aggregators”**: For multi‐wavefunction or multi‐observer scenario analyses, you can introduce an entity (e.g. `GlobalScenarioRecord`) that references multiple wavefunctions and observer frames, then run top‐level consistency checks or summarizations across them.  
5. **Adopt Additional Rollups**: The schema is flexible—feel free to attach new aggregator fields like the ones shown above to retrieve or summarize data (e.g. scenario-wide gate usage, or detection of interpretation mismatches).

---

## Contributing

1. **Fork or Clone** this repo.  
2. **Branch Off** to add enhancements to the `unified_quantum_model.json`:
   - New fields, constraints, or lambdas for more specialized quantum effects.  
   - Expanded multi-observer or HPC integration, partial branching logic, etc.  
3. **Pull Requests**: Submit a PR explaining your changes, test coverage, and rationale.

---

**Thank you for exploring the Quantum Interpretations Unified Meta-Model!**  
With these new aggregator fields, you gain additional vantage points on your quantum data—spanning scenario-level measurement distributions, circuit resource metrics, and evolution unitarity checks. As before, everything coexists in **one** consistent data structure, bridging single-outcome collapses, coherent many-worlds branching, and observer-relative RQM updates.  

Feel free to customize or extend it further for your research or applications!