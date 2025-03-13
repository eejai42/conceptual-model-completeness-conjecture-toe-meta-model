# All-In-One CMCC Physics Model

A unified data+rule schema capturing classical mechanics, quantum wavefunctions, gauge fields, density matrices, multiway branching, black holes, spin-statistics, etc. Aggregators/lambdas are fully declarative and can reference each other in any order.


## Metadata

**Title**: CMCC Complete Physics ToE Meta-Model  
**Subtitle**: A Comprehensive ACID-Based Data Architecture for Classical, Quantum, and Relativistic Theories  
**Date**: March 2025
**Domain Identifier**: CMCC_ToEMM_Physics

### Authors
- **EJ Alexandra** <start@anabstractlevel.com>  
  Affiliations: SSoT.me, EffortlessAPI.com

### Abstract
This Physics extension of the CMCC (Conceptual Model Completeness Conjecture) unifies classical mechanics, quantum wavefunctions, relativistic effects, and multiway branching under one coherent, ACID-compliant schema. By leveraging the same five fundamental primitives—Schema, Data, Lookups, Aggregations, and Lambda formulas—it provides a purely declarative framework capable of modeling everything from basic Newtonian systems to Many-Worlds quantum branching events, seamlessly integrating with the broader CMCC environment.

### Key Points
- Captures both classical and quantum physics entities (particles, wavefunctions, measurement events) within the same structural model.
- Demonstrates universal coverage: from gravitational orbits to entangled states and multi-observer Wigner’s friend scenarios.
- Scales across microscopic, relativistic, and cosmic domains via aggregator-based rules and constraints.
- Aligns naturally with Wolfram’s multiway systems and Turing-complete formalisms, bridging theoretical and computational physics.

### Implications
- Offers a unified data substrate for cross-domain queries, enabling advanced analyses that tie together quantum states, cosmic evolution, or classical mechanics.
- Enhances reproducibility: each theorem, measurement event, or wavefunction is stored as data, eliminating the friction of specialized scripts.
- Lowers barriers to adding new physics theories or phenomena, since aggregator formula definitions are updated purely as data, not code.

### Narrative
#### CMCC Physics Extension
Traditional physics modeling often separates each domain—classical mechanics, quantum mechanics, relativity—into bespoke toolchains and file formats. This isolation complicates integrated analyses, such as bridging quantum wavefunctions with large-scale relativistic frames or observer-based paradoxes.
The CMCC Physics Model solves this by encoding all relevant physics concepts—like quantum states, measurements, observer frames, cosmic structures, or classical bodies—in the same ACID-compliant environment. Observables, wavefunction amplitudes, gauge fields, and branching structures appear as aggregator-driven records, decoupled from any one programming or simulation language. Even advanced, multi-observer paradox scenarios are captured via relationships and aggregator constraints.
This data-first approach, shared across the entire CMCC ecosystem, encourages cross-domain synergy. For instance, a single aggregator can check both quantum entanglement measures and classical gravitational parameters in the same query. The result is a single coherent data architecture that scales smoothly from fundamental quantum processes up to cosmic evolution, all while remaining Turing-complete and interpretation-agnostic.


---

# Schema Overview

## Entity: GlobalScenarioRecord

**Description**: Captures a top-level scenario or experiment context that aggregates wavefunctions, observers, measurements, and classical/cosmic data. Supports scenario-wide checks such as no-signalling, classical limit analyses, multi-observer reconstructions, etc.

### Fields
- **scenario_id**  
  *Type:* scalar, *Datatype:* string  
  
- **scenario_description**  
  *Type:* scalar, *Datatype:* string  
  
- **scenario_metadata**  
  *Type:* scalar, *Datatype:* json  
  

### Lookups
- **linked_wavefunctions**  
  *Target Entity:* ScenarioWavefunctionLink, *Type:* one_to_many  
    
  (Join condition: **ScenarioWavefunctionLink.scenario_id = this.scenario_id**)  
  *Description:* Points to a linking entity that associates this scenario with its included QuantumState records.
- **linked_observers**  
  *Target Entity:* ScenarioObserverLink, *Type:* one_to_many  
    
  (Join condition: **ScenarioObserverLink.scenario_id = this.scenario_id**)  
  *Description:* Points to a linking entity that associates this scenario with the relevant ObserverFrames.
- **linked_measurements**  
  *Target Entity:* ScenarioMeasurementLink, *Type:* one_to_many  
    
  (Join condition: **ScenarioMeasurementLink.scenario_id = this.scenario_id**)  
  *Description:* Points to a linking entity that associates this scenario with its MeasurementEvents.
- **linked_relationships**  
  *Target Entity:* ScenarioRelationshipLink, *Type:* one_to_many  
    
  (Join condition: **ScenarioRelationshipLink.scenario_id = this.scenario_id**)  
  *Description:* Points to a linking entity that associates this scenario with ObserverRelationships.
- **linked_classical_systems**  
  *Target Entity:* ClassicalSystemRecord, *Type:* one_to_many  
    
  (Join condition: **Some bridging record or scenario_id if desired**)  
  *Description:* Points to classical systems relevant for the scenario (optional extension).
- **linked_particles**  
  *Target Entity:* ParticleRecord, *Type:* one_to_many  
    
  (Join condition: **Possibly ScenarioParticleLink if we want the same pattern as wavefunctions.**)  
  *Description:* If the scenario includes classical or hybrid ParticleRecords.
- **scenario_dark_matter_inferences**  
  *Target Entity:* DarkMatterInferenceRecord, *Type:* one_to_many  
    
  (Join condition: **DarkMatterInferenceRecord.scenario_id = this.scenario_id**)  
  *Description:* Points to DM inference records relevant to this scenario, each referencing this scenario_id.
- **scenario_halo_structures**  
  *Target Entity:* HaloSubstructureRecord, *Type:* one_to_many  
    
  (Join condition: **HaloSubstructureRecord.scenario_id = this.scenario_id**)  
  *Description:* Points to halo substructure records. The 'scenario_id' field in HaloSubstructureRecord enables this link.
- **scenario_cosmic_evolutions**  
  *Target Entity:* CosmicEvolutionRecord, *Type:* one_to_many  
    
  (Join condition: **CosmicEvolutionRecord.scenario_id = this.scenario_id**)  
  *Description:* Links cosmic-evolution snapshots (by redshift/time) to this scenario. 'scenario_id' in CosmicEvolutionRecord references this scenario.

### Aggregations
- **scenario_wavefunction_count**  
  *Description:* Counts how many QuantumStates are linked to this scenario via the ScenarioWavefunctionLink entity.  
  *Formula:* `COUNT(linked_wavefunctions)`
- **global_no_signalling_check**  
  *Description:* Evaluates measurement data and wavefunction references across this scenario to detect any no-signalling violations.  
  *Formula:* `CheckGlobalNoSignalling(linked_measurements, linked_wavefunctions)`
- **global_classical_limit_analysis**  
  *Description:* Analyzes whether wavefunctions in this scenario exhibit minimal interference, suggesting an overall classical limit.  
  *Formula:* `AssessClassicalLimitAcrossWavefunctions(linked_wavefunctions)`
- **interpretation_consistency_across_wavefunctions**  
  *Description:* Verifies that each wavefunction's assigned interpretation policy is consistent with the observed measurement behavior within this scenario.  
  *Formula:* `CheckGlobalInterpretationConsistency(linked_wavefunctions, linked_measurements)`
- **global_observer_agreement_score**  
  *Description:* Produces a scenario-wide measure of how consistently observers (and relationships among them) record outcomes or states.  
  *Formula:* `AggregateObserverAgreements(linked_observers, linked_relationships)`
- **global_darwinism_index**  
  *Description:* Combines each observer’s quantum_darwinism_index to see if consistent pointer states emerge across the entire scenario.  
  *Formula:* `ComputeAggregateDarwinismIndex(linked_observers)`
- **multi_wavefunction_coherence_map**  
  *Description:* Aggregates coherence or decoherence data from each wavefunction in the scenario, producing a combined map of quantum interference levels.  
  *Formula:* `CombineAllDecoherenceMaps(linked_wavefunctions)`
- **multi_system_bell_violations**  
  *Description:* Examines relevant wavefunction-measurement combos in this scenario for any CHSH/Bell-type inequality violations.  
  *Formula:* `ScanAllBellInequalityChecks(linked_wavefunctions, linked_measurements)`
- **top_level_paradox_score**  
  *Description:* Generates a consolidated 'paradox score' for Wigner’s friend or Hardy’s paradox events across wavefunctions, observers, and relationships in this scenario.  
  *Formula:* `AnalyzeOverallWignersFriendAndHardysParadox(linked_wavefunctions, linked_observers, linked_relationships, linked_measurements)`
- **heisenberg_cut_placement**  
  *Description:* Assesses pointer-basis stability, decoherence measures, and Darwinism indices to locate a plausible quantum–classical boundary within the scenario.  
  *Formula:* `InferHeisenbergCutPlacement(linked_wavefunctions, linked_observers)`
- **global_causality_violations**  
  *Description:* Scans measurement events and observer relationships for cyclical or paradoxical loops that violate standard causality assumptions.  
  *Formula:* `DetectGlobalCausalLoops(linked_measurements, linked_relationships)`
- **multi_observer_rqm_reconstruction**  
  *Description:* Attempts to reconcile partial observer-dependent wavefunctions in RQM into a single global state, if possible. Flags inconsistencies if no single global state can represent every observer’s vantage.  
  *Formula:* `AttemptGlobalStateReconstruction(linked_observers, linked_wavefunctions)`
- **scenario_interpretation_conflict_check**  
  *Description:* Summarizes measurement events that contradict their wavefunction's assigned interpretation policy (e.g., single-outcome vs branching mismatch).  
  *Formula:* `EvaluateScenarioInterpretationConflicts(linked_measurements, linked_wavefunctions)`
- **scenario_wigner_friend_paradox_count**  
  *Description:* Tallies the number of observer relationship records that contain a Wigner’s friend paradox or nested friend scenario in this scenario.  
  *Formula:* `CountAllWignerFriendParadoxes(linked_relationships)`
- **scenario_hardys_paradox_occurrences**  
  *Description:* Counts how many wavefunctions exhibit a non-zero hardys_paradox_indicator, indicating the presence of Hardy's paradox in the scenario.  
  *Formula:* `CountAllHardyParadoxFlags(linked_wavefunctions)`
- **max_branch_depth_across_scenario**  
  *Description:* Scans all wavefunctions linked to this scenario and returns the maximum branch depth encountered.  
  *Formula:* `FindMaxBranchDepth(linked_wavefunctions)`
- **scenario_average_entanglement**  
  *Description:* Averages the entanglement measure across all wavefunctions in this scenario.  
  *Formula:* `AVERAGE(linked_wavefunctions.entanglement_measure)`
- **scenario_measurement_count**  
  *Description:* Counts how many MeasurementEvents are linked to this scenario.  
  *Formula:* `COUNT(linked_measurements)`
- **interpretation_distribution**  
  *Description:* Returns a JSON object tallying how many wavefunctions use each interpretation policy, e.g. { 'Copenhagen': 2, 'ManyWorlds': 3, 'RQM': 1 }.  
  *Formula:* `ComputeInterpretationDistribution(linked_wavefunctions)`
- **scenario_active_observers_count**  
  *Description:* Counts how many ObserverFrames are active in this scenario.  
  *Formula:* `COUNT(linked_observers)`
- **scenario_interpretation_mismatch_events**  
  *Description:* Returns a list of measurement events that conflict with their wavefunction’s assigned interpretation (e.g., ManyWorlds wavefunction storing single outcomes).  
  *Formula:* `ListInterpretationMismatches(linked_wavefunctions, linked_measurements)`
- **interpretation_mismatch_density**  
  *Description:* Aggregates the ratio or percentage of mismatch measurement events over total measurement count. A scenario-level metric of how often interpretation policies are violated.  
  *Formula:* `ComputeInterpretationMismatchDensity(linked_wavefunctions, linked_measurements)`
- **persistent_branch_overlap_ratio**  
  *Description:* Quantifies how many wavefunction branches remain partially overlapping (coherent) instead of fully decohering, providing a measure of re-interference potential.  
  *Formula:* `EvaluatePersistentBranchOverlap(linked_wavefunctions)`
- **heisenberg_cut_inference**  
  *Description:* Computes the effective quantum–classical boundary by integrating decoherence metrics with observer Darwinism indices and reference frame data.  
  *Formula:* `InferHeisenbergCut(decoherence_map, ObserverFrame.quantum_darwinism_index, ObserverFrame.reference_frame_transform)`
- **scenario_total_classical_mass**  
  *Description:* Aggregates the total mass of classical systems linked to this scenario.  
  *Formula:* `SUM(linked_classical_systems.total_system_mass)`
- **scenario_classical_system_count**  
  *Description:* Counts how many ClassicalSystemRecords are included in this scenario.  
  *Formula:* `COUNT(linked_classical_systems)`
- **branch_to_classical_boundary_analysis**  
  *Description:* Synthesizes wavefunction coherence data with scenario-level classical limit analysis to locate partial quantum/classical boundaries in this scenario.  
  *Formula:* `AnalyzeBranchToClassicalBoundary(multi_wavefunction_coherence_map, global_classical_limit_analysis)`
- **cosmological_observer_paradox_scan**  
  *Description:* Correlates RQM or Wigner’s friend paradox indicators among observers with large-scale cosmic structures, such as dark matter subhalos or cosmic evolution.  
  *Formula:* `ScanObserverParadoxesInCosmicContext(linked_relationships, scenario_dark_matter_inferences, scenario_halo_structures, scenario_cosmic_evolutions)`
- **interpretation_mismatch_summary**  
  *Description:* Aggregates mismatch events (branch vs collapse, etc.) into a user-friendly summary grouped by wavefunction or measurement type.  
  *Formula:* `SummarizeInterpretationMismatches(scenario_interpretation_mismatch_events)`
- **pointer_states_cosmic_evolution**  
  *Description:* Tracks whether pointer states remain stable across cosmic time by comparing quantum_darwinism_index from observers with cosmic time data.  
  *Formula:* `CorrelatePointerDarwinismWithCosmicEvolution(linked_observers, scenario_cosmic_evolutions)`
- **global_pointer_state_stability**  
  *Description:* Analyzes observer Darwinism indices and decoherence data across wavefunctions to yield a global pointer-state stability score.  
  *Formula:* `AssessOverallPointerStateStability(linked_wavefunctions, linked_observers)`
- **inferred_classical_boundary**  
  *Description:* Automatically locates a plausible quantum–classical boundary using decoherence thresholds, branching structure, and classical system parameters.  
  *Formula:* `DeriveEffectiveClassicalBoundary(linked_wavefunctions, linked_classical_systems)`
- **dark_matter_entanglement_correlation**  
  *Description:* Searches for correlations between quantum entanglement measures and the presence of large missing mass in dark-matter inference records.  
  *Formula:* `ComputeDMEntanglementCorrelation(linked_wavefunctions, linked_classical_systems, linked_particles, DarkMatterInferenceRecord.*)`
- **cross_interpretation_probability_flow**  
  *Description:* Traces outcome probabilities in wavefunctions marked with different interpretations (Copenhagen vs. ManyWorlds) to see if the sum of branch weights matches single-outcome probabilities.  
  *Formula:* `CompareSingleOutcomeVsMWBranchWeights(linked_measurements, linked_wavefunctions)`
- **multi_level_observer_paradox_scan**  
  *Description:* Examines observer relationships for nested/cyclical Wigner’s friend setups, generating a multi-tier paradox score.  
  *Formula:* `RecursiveParadoxSearch(linked_relationships)`
- **quantum_classical_coupling_entropy**  
  *Description:* Blends wavefunction decoherence metrics with classical system mass or environment parameters to yield an effective quantum–classical coupling entropy.  
  *Formula:* `ComputeCouplingEntropy(linked_wavefunctions, linked_classical_systems)`
- **multi_interpretation_branch_probability_divergence**  
  *Description:* Compares actual single-outcome frequencies vs Many-Worlds branch weights. Identifies wavefunctions flagged as Copenhagen but displaying repeated multi-branch measurements, or vice versa.  
  *Formula:* `ComputeBranchProbabilityDivergence(linked_wavefunctions, linked_measurements)`
- **nested_observer_observer_paradox_score**  
  *Description:* Detects cyclical or deeply nested Wigner’s friend (observer A measures B while B measures A, etc.), producing a multi-level paradox severity score.  
  *Formula:* `ComputeMultiLevelObserverParadox(linked_relationships)`
- **entanglement_decoherence_boundaries**  
  *Description:* Finds the boundary between quantum subsystems (non-negligible entanglement) and effectively classical subsystems (decohered) within large composite scenarios.  
  *Formula:* `IdentifyEntanglementDecoherenceBoundaries(linked_wavefunctions, linked_classical_systems)`
- **interpretation_mismatch_vs_branch_depth**  
  *Description:* Examines whether interpretation mismatch events (e.g. single-outcome logs in a Many-Worlds-labeled wavefunction) correlate with higher branch depth or advanced decoherence stages.  
  *Formula:* `CorrelateMismatchEventsWithBranchDepth(linked_wavefunctions, linked_measurements)`
- **quantum_classical_coupling_entropy**  
  *Description:* Blends wavefunction decoherence metrics with classical environment properties to yield an effective coupling entropy, indicating how strongly the environment drives wavefunction collapse.  
  *Formula:* `ComputeQuantumClassicalCouplingEntropy(linked_wavefunctions, linked_classical_systems)`
- **nested_observer_paradox_depth**  
  *Description:* Determines how many levels of 'observer measuring observer' can be stacked before a paradox arises.  
  *Formula:* `ComputeNestedObserverParadoxDepth(linked_observers, linked_relationships)`
- **multi_wavefunction_interference_matrix**  
  *Description:* Constructs a matrix of cross-interference or orthogonality measures among all wavefunctions in this scenario.  
  *Formula:* `BuildInterferenceMatrixAcrossWavefunctions(linked_wavefunctions)`
- **entanglement_graph_among_observers**  
  *Description:* Examines correlated outcomes among different ObserverFrames to form a graph of intersubjective entanglement or correlation.  
  *Formula:* `GenerateObserverEntanglementGraph(linked_observers, linked_measurements)`
- **cross_validation_partialtrace_branch**  
  *Description:* Checks consistency between partial-trace density matrices and branch-based (Many-Worlds) decompositions for the same system.  
  *Formula:* `CompareDensityMatrixPartialTraceWithBranchRecords(linked_wavefunctions, DensityMatrixRecord.*)`
- **environment_assisted_classicality_spread**  
  *Description:* Evaluates how quickly pointer states replicate across multiple environment fragments (Quantum Darwinism) in the entire scenario.  
  *Formula:* `ComputeDarwinismSpreadRate(linked_observers, linked_wavefunctions)`
- **mw_vs_objective_collapse_diagnostics**  
  *Description:* Flags wavefunctions labeled 'ManyWorlds' that show effectively single-outcome data, or 'Copenhagen' wavefunctions that spawn branches.  
  *Formula:* `ContrastBranchingDepthAgainstSingleOutcomePatterns(linked_wavefunctions, linked_measurements)`
- **macro_scale_interference_revival_prob**  
  *Description:* Computes the small but non-zero chance that large systems might re-interfere (revival) if there's residual coherence.  
  *Formula:* `EstimateMacroRevivalProbability(linked_wavefunctions, BranchRecord.*, classical_systems)`

### Lambdas
- **run_global_analysis**
    
  *Formula:* `PerformAllGlobalScenarioChecks(this.scenario_id)`

### Constraints
- **copenhagen_no_branches**  
  *Formula:* `EnforceNoBranchingForCopenhagen(this.scenario_id)`  
  *Error Message:* Wavefunctions marked with a Copenhagen policy must not produce branching measurement events in this scenario.

---

## Entity: QuantumState

**Description**: Represents a wavefunction or amplitude distribution for a quantum system across different interpretations (Copenhagen, Many-Worlds, RQM). In RQM, it may be observer-dependent or partially global.

### Fields
- **state_id**  
  *Type:* scalar, *Datatype:* string  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **amplitude_data**  
  *Type:* scalar, *Datatype:* json  
  
- **normalization**  
  *Type:* calculated, *Datatype:*   
  
- **interpretation_policy_id**  
  *Type:* lookup, *Datatype:*   
  
- **coherence_time**  
  *Type:* scalar, *Datatype:* float  
  
- **dynamic_phase**  
  *Type:* scalar, *Datatype:* float  
  
- **decoherence_environment_params**  
  *Type:* scalar, *Datatype:* json  
  
- **subsystem_spec**  
  *Type:* scalar, *Datatype:* json  
  
- **dimensionality**  
  *Type:* scalar, *Datatype:* int  
  
- **num_particles**  
  *Type:* scalar, *Datatype:* int  
  
- **spin_states**  
  *Type:* scalar, *Datatype:* json  
  
- **wavefunction_symmetry**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **branches**  
  *Target Entity:* BranchRecord, *Type:* one_to_many  
    
  (Join condition: **BranchRecord.wavefunction_id = this.state_id**)  
  *Description:* References zero or more BranchRecords for Many-Worlds or partial branching.
- **amplitude_algebraic_structure_id**  
  *Target Entity:* AlgebraicStructure, *Type:* lookup  
    
    
  *Description:* An optional reference indicating the complex vector space structure for these amplitudes.
- **reference_frame_id**  
  *Target Entity:* ReferenceFrameRecord, *Type:* lookup  
    
    
  *Description:* If needed, identifies which reference frame the wavefunction is expressed in.

### Aggregations
- **entanglement_measure**  
  *Description:* Computes entanglement entropy (or a similar measure) by partially tracing out subsystems as defined by subsystem_spec.  
  *Formula:* `ComputeEntanglementEntropy(amplitude_data, subsystem_spec)`
- **decoherence_map**  
  *Description:* Evaluates how orthogonal or non-interfering different branches are, indicating the degree of decoherence.  
  *Formula:* `AssessDecoherenceAcrossBranches(this.state_id)`
- **branch_count**  
  *Description:* Number of BranchRecord entries linked to this wavefunction.  
  *Formula:* `COUNT(branches)`
- **global_collapse_metric**  
  *Description:* A user-defined aggregator that scores how 'collapsed' the wavefunction is, based on branch structure.  
  *Formula:* `ComputeGlobalCollapseMetric(branch_count, branches)`
- **time_evolution**  
  *Description:* Applies a time-evolution operator (e.g. e^-iHt) to amplitude_data based on dynamic_phase or a stored Hamiltonian reference.  
  *Formula:* `ApplyTimeEvolution(amplitude_data, dynamic_phase)`
- **causal_branch_graph**  
  *Description:* Builds a directed graph of branching events for analyzing causal/time-order structure in Many-Worlds or partial branching contexts.  
  *Formula:* `ConstructBranchCausalityGraph(branches)`
- **macro_distinct_branches**  
  *Description:* Distinguishes which branches have become macroscopically distinct (orthogonal). 'some_threshold' is a user-defined or global parameter.  
  *Formula:* `IdentifyMacroscopicBranches(decoherence_map, branches, some_threshold)`
- **observer_relative_wavefunction**  
  *Description:* Generates a vantage-specific wavefunction for RQM, factoring in partial knowledge or partial branching for the given observer.  
  *Formula:* `ComputeObserverRelativeWavefunction(amplitude_data, parameters.observer_id)`
- **entanglement_classification**  
  *Description:* Labels the state as 'Product' if entanglement_measure is negligible, else 'Entangled'.  
  *Formula:* `IF(entanglement_measure < 1e-6, 'Product state', 'Entangled')`
- **branch_probability_sum**  
  *Description:* Accumulates total branch probability across all branches. Ideally ~1 in Many-Worlds if the Born rule is followed.  
  *Formula:* `SUM(BranchRecord.prob_weight WHERE wavefunction_id = this.state_id)`
- **global_probability_mismatch_flag**  
  *Description:* Flags if the sum of branch probabilities deviates significantly from 1, suggesting an inconsistency or incomplete branching data.  
  *Formula:* `IF( ABS(branch_probability_sum - 1) > 0.001, 'WARNING: total branch probability != 1', 'OK' )`
- **bell_inequality_check**  
  *Description:* Checks for CHSH or Bell inequality violations by scanning all relevant measurement events referencing this wavefunction.  
  *Formula:* `ComputeCHSHCorrelators(this.state_id, MeasurementEvent.*)`
- **chsh_local_check**  
  *Description:* An alternative aggregator for CHSH correlators on a subset of measurement events, if needed.  
  *Formula:* `ComputeCHSHCorrelatorsForSpecificMeas(this.state_id, MeasurementEvent.*)`
- **wigner_distribution**  
  *Description:* Generates a (quasi-)probability distribution in phase space for continuous-variable quantum states.  
  *Formula:* `ComputeWignerFunction(amplitude_data)`
- **leggett_garg_inequality**  
  *Description:* Tests time-ordered measurements for Leggett-Garg inequality violations, indicating non-classical temporal correlations.  
  *Formula:* `ComputeLeggettGargCorrelations(this.state_id, MeasurementEvent.*)`
- **quantum_fisher_info**  
  *Description:* Calculates quantum Fisher information, requiring a known or assumed Hamiltonian reference for metrological use.  
  *Formula:* `ComputeQuantumFisherInformation(amplitude_data, hamiltonian_ref)`
- **kochen_specker_contextuality_check**  
  *Description:* Scans associated measurement events for Kochen-Specker style contextuality constraints. Flags violations of non-contextual hidden-variable theories.  
  *Formula:* `ComputeContextualityViolations(this.state_id, MeasurementEvent.*)`
- **ghz_mermin_violation_indicator**  
  *Description:* Checks multi-qubit GHZ or Mermin inequalities for measurement events referencing this wavefunction. Returns a numeric violation measure.  
  *Formula:* `ComputeGHZOrMerminInequalityViolations(this.state_id, MeasurementEvent.*)`
- **hardys_paradox_indicator**  
  *Description:* Evaluates Hardy's paradox conditions for measurement outcomes on this wavefunction, returning a contradiction measure under local realism.  
  *Formula:* `ComputeHardyParadoxProbability(this.state_id, MeasurementEvent.*)`
- **interpretation_usage_summary**  
  *Description:* Surveys how measurement events referencing this wavefunction were handled (single-outcome, branching, observer-relative). Detects mismatches with the assigned InterpretationPolicy.  
  *Formula:* `CollectInterpretationEvidence(this.state_id, MeasurementEvent.*)`
- **multi_partition_entanglement_map**  
  *Description:* Computes entanglement entropies for all bipartitions (and optionally tripartitions) to classify GHZ, W-state, or product structure.  
  *Formula:* `EvaluateAllBipartitionsForEntanglement(this.state_id)`
- **global_pointer_basis_inference**  
  *Description:* Combines pointer basis candidates with observer data to see if a stable pointer basis emerges from multiple vantage points.  
  *Formula:* `InferPointerBasisStability(this.state_id, pointer_basis_candidates, ObserverFrame.*)`
- **history_decoherence_check**  
  *Description:* Analyzes measurement and branch records to ensure distinct histories remain decohered. Flags re-appearance of interference among separated branches.  
  *Formula:* `CheckConsistencyOfHistoriesAcrossBranches(this.state_id)`
- **classical_limit_indicator**  
  *Description:* Examines whether off-diagonal interference is negligible, indicating an effectively classical wavefunction in pointer basis terms.  
  *Formula:* `CheckClassicalLimit(pointer_basis_candidates, amplitude_data)`
- **time_until_decoherence_dynamic**  
  *Description:* Estimates remaining coherence time by combining amplitude data, decoherence map, and environment parameters.  
  *Formula:* `ComputeDynamicDecoherenceTime(amplitude_data, decoherence_map, this.decoherence_environment_params)`
- **resource_theory_magic_measure**  
  *Description:* Evaluates 'magic' resourcefulness by measuring distance from the nearest stabilizer state, relevant to fault-tolerant quantum computing.  
  *Formula:* `ComputeMagicStabilizerDistance(amplitude_data)`
- **branch_frequency_vs_amplitude_check**  
  *Description:* In Many-Worlds, compares measured frequencies of branch outcomes to the Born-rule amplitude squares. Flags deviations from expected ratios.  
  *Formula:* `CompareBranchWeightFrequencies(this.state_id, repeated_measurements)`
- **macro_cat_indicator**  
  *Description:* Checks for macroscopically distinct superpositions (Schrödinger cat states), using thresholds on amplitude separation and decoherence times.  
  *Formula:* `DetectMacroscopicSuperposition(this.state_id, amplitude_data, decoherence_map)`
- **freedman_clauser_inequality_check**  
  *Description:* Performs Freedman–Clauser or Clauser–Horne inequality tests, similar to CHSH but with different measurement settings.  
  *Formula:* `ComputeFreedmanClauserCorrelations(this.state_id, MeasurementEvent.*)`
- **max_branch_depth**  
  *Description:* Finds the maximum branch depth among all branches linked to this wavefunction.  
  *Formula:* `MAX(branches.branch_depth)`
- **non_adiabaticity_measure**  
  *Description:* Estimates how quickly the wavefunction departs from an instantaneous eigenstate during time evolution. Helps check adiabatic approximations.  
  *Formula:* `ComputeNonAdiabaticity(this.state_id, time_evolution, amplitude_data)`
- **branching_regime_classifier**  
  *Description:* Classifies branching as partial (RQM-style) or full (Many-Worlds) based on average overlap of observer scopes across branches.  
  *Formula:* `IF(AVERAGE(branches.observer_scope_overlap) > threshold, 'Partial Branching', 'Full Branching')`
- **re_interference_windows**  
  *Description:* Identifies wavefunction sectors that have not fully decohered and can still interfere.  
  *Formula:* `DetectReInterferencePossibility(amplitude_data, decoherence_map)`
- **correlation_branch_depth_classical_limit**  
  *Description:* Checks if deeper branching reliably corresponds to a near-classical wavefunction or if interference persists.  
  *Formula:* `CorrelateBranchDepthWithClassicalLimit(branch_count, classical_limit_indicator)`
- **pointer_basis_drift_analysis**  
  *Description:* Analyzes whether the stable pointer basis changes under environment interactions or time evolution.  
  *Formula:* `TrackPointerBasisShiftOverTime(this.state_id)`
- **macro_vs_micro_entanglement_boundary**  
  *Description:* Determines if large 'classical-scale' subsystems remain unentangled while microscopic ones are significantly entangled.  
  *Formula:* `CheckEntanglementBetweenMacroscopicSubsystemsAndMicroscopicOnes(subsystem_spec, amplitude_data)`
- **cross_interpretation_probability_flow**  
  *Description:* Traces outcome probabilities vs. the sum of branch weights, revealing potential interpretation mismatch or confirmation.  
  *Formula:* `CompareBornRuleFrequenciesToManyWorldsBranchWeights(this.state_id, MeasurementEvent.*)`
- **time_dependent_classical_emergence_rate**  
  *Description:* Estimates how quickly a wavefunction becomes effectively classical under time evolution or repeated measurements.  
  *Formula:* `ComputeClassicalEmergenceRateOverTime(this.state_id, decoherence_map, QuantumEvolution.*)`

### Lambdas
- **normalize_wavefunction**
    
  *Formula:* `amplitude_data / SQRT(normalization)`
- **merge_with_another_state**
  (Parameters: target_state_id, entangling_params)  
  *Formula:* `CreateNewEntangledState(this.state_id, target_state_id, entangling_params)`

### Constraints
- **normalization_check**  
  *Formula:* `ABS(normalization - 1) <= 0.0001`  
  *Error Message:* Wavefunction must be normalized (sum of squared amplitudes ~ 1).

---

## Entity: InterpretationPolicy

**Description**: Defines how measurements on a wavefunction are interpreted (Copenhagen, Many-Worlds, RQM). Enforces rules about collapse behavior, observer specificity, and partial branching.

### Fields
- **interpretation_policy_id**  
  *Type:* scalar, *Datatype:* string  
  
- **interpretation_name**  
  *Type:* scalar, *Datatype:* enum  
  
- **collapse_behavior**  
  *Type:* scalar, *Datatype:* enum  
  
- **observer_specificity**  
  *Type:* scalar, *Datatype:* boolean  
  
- **metadata**  
  *Type:* scalar, *Datatype:* json  
  
- **allow_partial_branching**  
  *Type:* scalar, *Datatype:* boolean  
  
- **observer_hierarchy_model**  
  *Type:* scalar, *Datatype:* enum  
  

### Lookups
- **applied_wavefunctions**  
  *Target Entity:* QuantumState, *Type:* one_to_many  
    
  (Join condition: **QuantumState.interpretation_policy_id = this.interpretation_policy_id**)  
  *Description:* Reverse lookup to all QuantumStates referencing this policy.

### Aggregations
- **wavefunction_count**  
  *Description:* Counts how many QuantumState records currently use this interpretation policy.  
  *Formula:* `COUNT(applied_wavefunctions)`
- **interpretation_consistency_check**  
  *Description:* Checks high-level alignment of fields (e.g., 'Copenhagen' must use 'single_outcome').  
  *Formula:* `EnsurePolicyAlignment(interpretation_name, collapse_behavior, observer_specificity, allow_partial_branching)`
- **rqm_policy_coherence**  
  *Description:* Verifies that RQM-related fields do not conflict with each other. E.g., hierarchical model might forbid certain merges.  
  *Formula:* `CheckRQMPolicyCoherence(allow_partial_branching, observer_specificity, observer_hierarchy_model)`
- **policy_alignment_inference**  
  *Description:* Summarizes whether the chosen 'interpretation_name', 'collapse_behavior', and 'observer_specificity' are consistent with each other.  
  *Formula:* `IF(interpretation_consistency_check == 'ok' AND rqm_policy_coherence == 'ok', 'Interpretation policy aligned', 'Mismatch or error in policy config')`

### Lambdas
- **assign_rqm_ruleset**
  (Parameters: ruleset_id)  
  *Formula:* `ApplyRQMRuleset(this.interpretation_policy_id, ruleset_id, allow_partial_branching)`

### Constraints
- **copenhagen_collapse_behavior_constraint**  
  *Formula:* `IF(interpretation_name='Copenhagen', collapse_behavior='single_outcome', true)`  
  *Error Message:* If interpretation_name is 'Copenhagen', collapse_behavior must be 'single_outcome'.
- **many_worlds_collapse_behavior_constraint**  
  *Formula:* `IF(interpretation_name='ManyWorlds', collapse_behavior='branch', true)`  
  *Error Message:* If interpretation_name is 'ManyWorlds', collapse_behavior must be 'branch'.
- **rqm_collapse_behavior_constraint**  
  *Formula:* `IF(interpretation_name='RQM', collapse_behavior='observer_relative', true)`  
  *Error Message:* If interpretation_name is 'RQM', collapse_behavior must be 'observer_relative'.
- **rqm_observer_specificity_constraint**  
  *Formula:* `IF(interpretation_name='RQM', observer_specificity=true, true)`  
  *Error Message:* If interpretation_name is 'RQM', observer_specificity must be true.

---

## Entity: MeasurementEvent

**Description**: Logs a measurement or observation that might cause wavefunction collapse, branching, or observer-relative updates under different interpretations.

### Fields
- **meas_id**  
  *Type:* scalar, *Datatype:* string  
  
- **wavefunction_id**  
  *Type:* lookup, *Datatype:*   
  
- **measurement_type**  
  *Type:* scalar, *Datatype:* string  
  
- **observable_id**  
  *Type:* lookup, *Datatype:*   
  
- **observable_operator**  
  *Type:* scalar, *Datatype:* json  
  
- **possible_outcomes**  
  *Type:* scalar, *Datatype:* json  
  
- **time_stamp**  
  *Type:* scalar, *Datatype:* datetime  
  
- **spacetime_coords**  
  *Type:* scalar, *Datatype:* json  
  
- **observer_id**  
  *Type:* lookup, *Datatype:*   
  
- **selected_outcome**  
  *Type:* scalar, *Datatype:* string  
  
- **branch_ids_generated**  
  *Type:* scalar, *Datatype:* json  
  
- **observed_observer_id**  
  *Type:* lookup, *Datatype:*   
  
- **relational_records**  
  *Type:* scalar, *Datatype:* json  
  


### Aggregations
- **outcome_probabilities**  
  *Description:* Computes Born-rule outcome probabilities by projecting the wavefunction’s amplitude data onto the measurement operator basis.  
  *Formula:* `ComputeOutcomeDistribution(wavefunction_id.amplitude_data, observable_operator)`
- **temporal_consistency_check**  
  *Description:* Ensures this measurement event aligns with the wavefunction’s timeline or previously logged measurement events.  
  *Formula:* `CheckMeasurementConsistency(wavefunction_id, meas_id)`
- **history_consistency**  
  *Description:* Checks if the measurement’s recorded outcome or branching is consistent with the wavefunction’s known measurement history.  
  *Formula:* `ComputeHistoryConsistency(this.meas_id, wavefunction_id)`
- **causality_check**  
  *Description:* Verifies that the measurement’s timestamp does not conflict with causality constraints (e.g., out-of-order events).  
  *Formula:* `CheckTemporalOrdering(time_stamp, wavefunction_id)`
- **classical_fact_agreement**  
  *Description:* If multiple observers recorded the same event, checks how consistently they match on the outcome.  
  *Formula:* `ComputeClassicalFactAgreement(meas_id)`
- **observer_relative_outcomes**  
  *Description:* For RQM or partial branching, computes outcome distributions specifically from the perspective of observer_id.  
  *Formula:* `ComputeObserverRelativeOutcomes(wavefunction_id, observer_id, possible_outcomes)`
- **relational_outcome_update**  
  *Description:* For an observer measuring another observer in RQM, updates the relational outcome data if partial or observer-relative.  
  *Formula:* `ComputeRelationalMeasurementOutcome(wavefunction_id, observer_id, observed_observer_id)`
- **interpretation_inference**  
  *Description:* Heuristic aggregator that guesses the used interpretation based on outcome selection vs. branching.  
  *Formula:* `IF(selected_outcome != '', 'Copenhagen', IF(branch_ids_generated != null AND LENGTH(branch_ids_generated) > 0, 'ManyWorlds', 'PossibleRQM'))`
- **policy_vs_outcome_consistency**  
  *Description:* Verifies the measurement result or branching matches the wavefunction’s assigned interpretation policy.  
  *Formula:* `CheckPolicyOutcomeConsistency(wavefunction_id.interpretation_policy_id, selected_outcome, branch_ids_generated)`
- **no_signalling_constraint_check**  
  *Description:* Ensures local measurement outcomes do not allow faster-than-light signalling if there are space-like separated events.  
  *Formula:* `CheckNoSignallingConstraintsAcrossSubsystems(this.meas_id, wavefunction_id, possible_outcomes, spacetime_coords)`
- **observed_outcome_probability**  
  *Description:* Retrieves the Born-rule probability for the measurement's collapsed outcome, if single-outcome was selected.  
  *Formula:* `IF(selected_outcome != '', outcome_probabilities[selected_outcome], null)`
- **determine_macro_object_quantum_tracing**  
  *Description:* Examines whether a large, presumably classical object is still in superposition post-measurement or has collapsed.  
  *Formula:* `CheckIfMacroscopicSystemUnderMeasurementRetainsQuantumSuperposition(meas_id, wavefunction_id)`
- **extended_kochen_specker_survey**  
  *Description:* Checks multiple measurement bases for Kochen–Specker–type contextual contradictions in the same measurement dataset.  
  *Formula:* `AggregateContextualityViolationsAcrossMeasurementSets(this.meas_id, wavefunction_id)`

### Lambdas
- **execute_measurement**
    
  *Formula:* `InterpretationBasedMeasurement(wavefunction_id, observer_id, this.possible_outcomes, this.outcome_probabilities)`
- **execute_relational_measurement**
    
  *Formula:* `RelationalMeasurementProtocol(this.meas_id, this.observer_id, this.observed_observer_id, wavefunction_id)`

### Constraints
- **copenhagen_no_branching**  
  *Formula:* `IF(wavefunction_id.interpretation_policy_id.interpretation_name='Copenhagen', LENGTH(branch_ids_generated)=0, true)`  
  *Error Message:* Copenhagen measurements must not generate new branches.
- **manyworlds_single_outcome_forbidden**  
  *Formula:* `IF(wavefunction_id.interpretation_policy_id.interpretation_name='ManyWorlds', (selected_outcome IS NULL OR selected_outcome=''), true)`  
  *Error Message:* Many-Worlds measurements should not store a single collapsed outcome.

---

## Entity: ObserverFrame

**Description**: Represents an observer’s vantage in RQM or multi-observer scenarios. Each observer can maintain partial wavefunction data, self-history, and perspectives on other observers.

### Fields
- **observer_id**  
  *Type:* scalar, *Datatype:* string  
  
- **observer_name**  
  *Type:* scalar, *Datatype:* string  
  
- **observed_state_records**  
  *Type:* scalar, *Datatype:* json  
  
- **reference_frame_transform**  
  *Type:* scalar, *Datatype:* json  
  
- **contextual_state_data**  
  *Type:* scalar, *Datatype:* json  
  
- **view_of_other_observers**  
  *Type:* scalar, *Datatype:* json  
  
- **self_observed_history**  
  *Type:* scalar, *Datatype:* json  
  
- **epistemic_context**  
  *Type:* scalar, *Datatype:* json  
  


### Aggregations
- **quantum_darwinism_index**  
  *Description:* Measures how many distinct observer frames share consistent or redundant outcome records with this observer, indicating emergent classicality.  
  *Formula:* `ComputeDarwinismIndex(this.observer_id)`
- **shared_state_agreement**  
  *Description:* Scores how well this observer’s recorded outcomes align with other observers who measured the same events.  
  *Formula:* `ComputeObserverConvergence(this.observer_id)`
- **intersubjective_consistency_check**  
  *Description:* Determines whether this observer’s recorded data conflicts with external logs from other observers.  
  *Formula:* `CompareWithOtherObservers(this.observer_id)`
- **observer_consensus**  
  *Description:* Aggregates partial states or measurement outcomes from multiple sources to measure consensus on events or wavefunction states.  
  *Formula:* `ComputeObserverConsensus(this.observer_id)`
- **observer_relative_state**  
  *Description:* Reconstructs the local quantum state from this observer’s vantage, combining contextual_state_data with relevant measurements.  
  *Formula:* `ComputeObserverRelativeState(this.observer_id, contextual_state_data)`
- **multi_observer_consensus**  
  *Description:* Generalizes observer_consensus to multiple observers, summarizing how many frames converge with this observer's outcomes/states.  
  *Formula:* `ComputeMultiObserverConsensus(this.observer_id)`
- **self_consistency**  
  *Description:* Verifies that the observer’s self-observed timeline does not contradict the partial wavefunction they assign to themselves.  
  *Formula:* `CheckSelfConsistency(self_observed_history, contextual_state_data)`
- **observer_consistency_inference**  
  *Description:* Summarizes if the observer’s vantage is consistent both internally (self-consistency) and externally (intersubjective consistency).  
  *Formula:* `IF(intersubjective_consistency_check == 'ok' AND self_consistency == 'ok', 'Fully consistent vantage', 'Mismatch or paradox in observer frame')`
- **classicality_inference**  
  *Description:* Simple threshold-based measure for emergent classicality if the Darwinism index is high.  
  *Formula:* `IF(quantum_darwinism_index > 5, 'Classical-like pointer states emergent', 'Quantum coherence remains significant')`
- **darwinism_timeline**  
  *Description:* Tracks how pointer-state redundancy evolves over time from this observer’s perspective.  
  *Formula:* `ComputeDarwinismOverTime(this.observer_id)`
- **multi_observer_merge**  
  *Description:* Attempts partial or full 'merge' of multiple observer frames in RQM contexts, reconciling different vantage-dependent states if possible.  
  *Formula:* `PerformRQMObserverMerge(this.observer_id)`
- **self_vs_external_consistency**  
  *Description:* Checks how this observer’s self-history compares to how other observers record this observer’s events—detecting potential RQM paradoxes or mismatches.  
  *Formula:* `ComputeSelfExternalConsistency(this.observer_id, self_observed_history, view_of_other_observers)`
- **darwinist_redundancy_curve**  
  *Description:* Computes environment-fragment redundancy R(δ) for Darwinism analysis from this observer’s vantage.  
  *Formula:* `ComputeRedundancyFunction(this.observer_id)`
- **decoherence_history**  
  *Description:* Generates a timeline or log of decoherence events affecting measurements made by (or on) this observer.  
  *Formula:* `TrackDecoherenceEvents(this.observer_id)`
- **distinct_others_count**  
  *Description:* Counts the number of distinct observer IDs that this observer is actively tracking.  
  *Formula:* `COUNT_DISTINCT(KEYS(view_of_other_observers))`
- **superobserver_view_index**  
  *Description:* Scores how comprehensively this observer can reconstruct the states of other observers (Wigner-like vantage).  
  *Formula:* `ComputeSuperobserverIndex(this.observer_id, view_of_other_observers)`
- **observer_observer_frame_overlap**  
  *Description:* Measures how much this observer's vantage or transforms coincide with other observers' known frames.  
  *Formula:* `ComputeFrameOverlap(this.observer_id, view_of_other_observers)`
- **superobserver_emergence_index**  
  *Description:* Rates how completely this observer can reconstruct other observers' wavefunction states—i.e. a 'Wigner vantage.'  
  *Formula:* `AssessSuperobserverCoverage(this.observer_id, view_of_other_observers)`
- **rqm_relative_timeline_consistency**  
  *Description:* Verifies that the sequence of events in this observer’s local timeline does not contradict external observer logs.  
  *Formula:* `CheckTimelineOrderConsistency(this.observer_id, self_observed_history, ObserverRelationship.*)`
- **observer_pointer_basis_stability_timeline**  
  *Description:* Tracks how stable the local pointer basis is from this observer’s vantage as new measurements or environment data arrive.  
  *Formula:* `EvaluatePointerBasisStabilityOverTime(this.observer_id, contextual_state_data)`

### Lambdas
- **update_observed_context**
  (Parameters: measurement_id)  
  *Formula:* `BayesianObserverUpdate(this.observer_id, measurement_id, contextual_state_data)`
- **update_relational_view**
  (Parameters: target_observer_id, measurement_data)  
  *Formula:* `RQMRelationalUpdate(this.observer_id, target_observer_id, measurement_data, view_of_other_observers)`
- **synchronize_self_view**
  (Parameters: new_self_data)  
  *Formula:* `UpdateSelfObservedHistory(this.observer_id, new_self_data, self_observed_history)`


---

## Entity: BranchRecord

**Description**: Many-Worlds or partial RQM branching metadata—each branch is a distinct wavefunction slice after measurement.

### Fields
- **branch_id**  
  *Type:* scalar, *Datatype:* string  
  
- **wavefunction_id**  
  *Type:* lookup, *Datatype:*   
  
- **origin_meas_id**  
  *Type:* lookup, *Datatype:*   
  
- **branch_amplitude_data**  
  *Type:* scalar, *Datatype:* json  
  
- **prob_weight**  
  *Type:* calculated, *Datatype:*   
  
- **parent_branch_id**  
  *Type:* lookup, *Datatype:*   
  
- **branch_depth**  
  *Type:* calculated, *Datatype:*   
  
- **coherence_factor**  
  *Type:* calculated, *Datatype:*   
  
- **relative_phase**  
  *Type:* scalar, *Datatype:* float  
  
- **branch_history**  
  *Type:* scalar, *Datatype:* json  
  
- **observer_scope**  
  *Type:* scalar, *Datatype:* json  
  
- **observer_relational_cut**  
  *Type:* scalar, *Datatype:* json  
  


### Aggregations
- **recombination_potential**  
  *Description:* Numerical measure of how likely this branch can recombine with other branches, factoring in coherence overlap.  
  *Formula:* `ComputeRecombinationPotential(coherence_factor, branch_amplitude_data)`
- **recombination_feasibility**  
  *Description:* Examines whether re-interference is feasible given the current coherence factor and relative phase.  
  *Formula:* `CheckRecombinationFeasibility(coherence_factor, relative_phase, wavefunction_id)`
- **rqm_merge_potential**  
  *Description:* Evaluates if branches can be merged from an RQM standpoint, e.g., when the same observer updates knowledge in partial branching.  
  *Formula:* `ComputeRQMBranchMergePotential(observer_scope, parent_branch_id)`
- **observer_scope_overlap**  
  *Description:* Determines which observers are co-branching here vs. which remain in superposition from each other’s viewpoint.  
  *Formula:* `CheckBranchObserverOverlap(this.branch_id, observer_scope, observer_relational_cut)`
- **branch_interference_inference**  
  *Description:* Classifies whether this branch can still interfere with others or if it is effectively decohered.  
  *Formula:* `IF(coherence_factor > 1e-3, 'Potential for re-interference', 'Effectively orthogonal')`
- **branch_merge_probability**  
  *Description:* Numerical measure of how likely partial branches can unify from an observer’s vantage.  
  *Formula:* `ComputeBranchMergeProbability(this.branch_id, observer_scope, coherence_factor)`
- **branch_reunion_check**  
  *Description:* Analyzes whether sibling branches can genuinely recombine based on coherence_factor, relative_phase, and decoherence state.  
  *Formula:* `EvaluateBranchReunionFeasibility(this.branch_id, sibling_branches)`
- **child_branches_count**  
  *Description:* Counts how many immediate child branches were spawned by this branch.  
  *Formula:* `COUNT(BranchRecord WHERE parent_branch_id = this.branch_id)`
- **relational_merge_index**  
  *Description:* Rates how likely partial RQM branches can unify from an observer’s perspective, considering overlap in observer_scope.  
  *Formula:* `ComputeRelationalMergeIndex(this.branch_id, observer_scope, coherence_factor)`
- **branch_probability_flow_over_time**  
  *Description:* Shows how amplitude/weight flows from one measurement event to the next across branching records.  
  *Formula:* `ComputeProbabilityFlowFromParentBranchesToChildren(this.branch_id)`
- **branch_reunification_pathway**  
  *Description:* Analyzes whether this branch can unify with siblings, given coherence_factor, relative_phase, and observer scopes.  
  *Formula:* `IdentifyPotentialBranchMerges(this.branch_id, sibling_branches)`
- **partial_branch_probability_vs_observer_scope**  
  *Description:* Computes the fraction of events or amplitude where only some observers see a collapsed branch but others do not.  
  *Formula:* `SummarizePartialBranchDistribution(this.branch_id, observer_scope)`
- **branch_interpretation_switching_or_coexistence**  
  *Description:* Flags if the branch's measurement event indicates a different interpretation mode than the wavefunction’s assigned policy.  
  *Formula:* `CheckBranchLevelInterpretationConflicts(origin_meas_id, wavefunction_id.interpretation_policy_id)`

### Lambdas
- **merge_partial_branches**
  (Parameters: other_branch_id)  
  *Formula:* `RQMPartialBranchMerge(this.branch_id, other_branch_id, observer_relational_cut)`
- **merge_branches_for_observer**
  (Parameters: target_branch_id, observer_id)  
  *Formula:* `RQMPartialBranchMergeLogic(this.state_id, target_branch_id, observer_id)`


---

## Entity: Observable

**Description**: Holds operator definitions (matrix, eigenvalues/eigenvectors) for measurable quantities (spin, position, etc.). Must be Hermitian.

### Fields
- **operator_id**  
  *Type:* string, *Datatype:*   
  
- **matrix_representation**  
  *Type:* array, *Datatype:*   
  
- **eigenvalues**  
  *Type:* array, *Datatype:*   
  
- **eigenvectors**  
  *Type:* array, *Datatype:*   
  


### Aggregations
- **checkHermiticity**  
  *Description:* Ensures the operator is Hermitian, which is required for a valid observable.  
  *Formula:* `VerifyHermitian(matrix_representation)`



---

## Entity: DensityMatrixRecord

**Description**: Stores a density matrix representation for quantum states, possibly for open systems or mixtures. May be partial or full state.

### Fields
- **record_id**  
  *Type:* string, *Datatype:*   
  
- **matrix_data**  
  *Type:* array, *Datatype:*   
  
- **subsystem_ids**  
  *Type:* array, *Datatype:*   
  
- **purity**  
  *Type:* number, *Datatype:*   
  


### Aggregations
- **computePurity**  
  *Description:* Calculates the purity Tr(ρ²) from the matrix_data.  
  *Formula:* `Purity(matrix_data)`
- **traceValue**  
  *Description:* Computes the trace of the density matrix, which should be 1 for proper normalization.  
  *Formula:* `ComputeMatrixTrace(matrix_data)`
- **tomographic_reconstruction**  
  *Description:* Performs quantum state tomography by aggregating measurement outcomes across various bases.  
  *Formula:* `ReconstructDensityMatrixFromMeasurements(this.record_id, MeasurementEvent.*)`
- **quantum_discord**  
  *Description:* Computes the quantum discord for this density matrix, highlighting nonclassical correlations beyond entanglement.  
  *Formula:* `ComputeQuantumDiscord(matrix_data)`
- **multipartite_negativity**  
  *Description:* Estimates the degree of entanglement across multiple partitions by generalizing the negativity measure.  
  *Formula:* `ComputeMultipartiteNegativity(matrix_data)`
- **mutual_information**  
  *Description:* Calculates the total mutual information among the subsystems described in this density matrix.  
  *Formula:* `ComputeTotalMutualInformation(matrix_data)`
- **classical_correlation**  
  *Description:* Separates the classical portion of correlations, used with quantum discord to distinguish classical vs. quantum correlations.  
  *Formula:* `ComputeClassicalCorrelation(matrix_data)`
- **density_matrix_extended_kochen_specker_survey**  
  *Description:* Applies Kochen–Specker checks by generating projectors from the density matrix's observable bases.  
  *Formula:* `ComputeContextualityFromDensityMatrix(matrix_data, associated_measurements)`
- **partial_trace_vs_branch_consistency_check**  
  *Description:* Ensures the partial-trace viewpoint matches the sum of branch probabilities for the same subsystems (Many-Worlds vs. density operator).  
  *Formula:* `CompareTracedOutDensityMatrixWithBranchProbabilities(record_id, BranchRecord.*)`

### Lambdas
- **applyKrausOperators**
    
  *Formula:* ``

### Constraints
- **trace_must_be_one**  
  *Formula:* `ABS(ComputeMatrixTrace(matrix_data) - 1) <= 0.0001`  
  *Error Message:* Density matrix must have trace ~ 1.

---

## Entity: Subsystem

**Description**: Represents a subsystem in a larger Hilbert space, identified by an ID, dimension, or relevant data.

### Fields
- **subsystem_id**  
  *Type:* string, *Datatype:*   
  
- **description**  
  *Type:* string, *Datatype:*   
  
- **dimensions**  
  *Type:* number, *Datatype:*   
  





---

## Entity: DecoherenceChannel

**Description**: Captures a decoherence or noise model for open quantum systems, described by Kraus operators for each subsystem.

### Fields
- **channel_id**  
  *Type:* string, *Datatype:*   
  
- **kraus_operators**  
  *Type:* array, *Datatype:*   
  
- **applied_subsystems**  
  *Type:* array, *Datatype:*   
  


### Aggregations
- **simulateDecoherence**  
  *Description:* Applies the stored Kraus set to a density matrix, simulating open-system evolution.  
  *Formula:* `ApplyKrausSet(density_matrix, kraus_operators)`
- **validateKrausOperators**  
  *Description:* Ensures the sum of K^†K = I across all Kraus operators, confirming validity of the channel.  
  *Formula:* `CheckKrausCompleteness(kraus_operators)`
- **channel_capacity**  
  *Description:* Computes the quantum channel capacity, i.e. the max rate (in qubits per channel use) for reliably transmitting quantum information.  
  *Formula:* `ComputeQuantumChannelCapacity(kraus_operators)`
- **holevo_bound**  
  *Description:* Estimates the classical capacity (Holevo limit) given a typical ensemble of input states.  
  *Formula:* `EstimateHolevoBound(kraus_operators, typical_input_ensemble)`



---

## Entity: QuantumEvolution

**Description**: Specifies a time-evolution process (e.g. unitary or Trotter steps) for a target wavefunction, referencing a Hamiltonian.

### Fields
- **evolution_id**  
  *Type:* string, *Datatype:*   
  
- **hamiltonian_ref**  
  *Type:* string, *Datatype:*   
  
- **time_step**  
  *Type:* number, *Datatype:*   
  
- **evolution_method**  
  *Type:* string, *Datatype:*   
  
- **target_state_id**  
  *Type:* lookup, *Datatype:*   
  

### Lookups
- **hamiltonian_record_id**  
  *Target Entity:* HamiltonianRecord, *Type:* lookup  
    
    
  *Description:* Which Hamiltonian definition we are using for this evolution (classical or quantum).

### Aggregations
- **applyTimeEvolution**  
  *Description:* Applies the time evolution operator to the target wavefunction. Implementation depends on the evolution_method.  
  *Formula:* `U(t) = exp(-i * H * t); wavefunction' = U(t)*wavefunction`
- **hamiltonian_validity**  
  *Description:* Checks that the referenced Hamiltonian is Hermitian, required for a valid unitary evolution.  
  *Formula:* `VerifyHermitian(hamiltonian_ref)`
- **quantum_speed_limit**  
  *Description:* Evaluates known quantum speed limits (e.g. Mandelstam–Tamm) to see how quickly the wavefunction can evolve away from its initial state.  
  *Formula:* `ComputeQuantumSpeedLimit(target_state_id, hamiltonian_ref)`
- **otoc_scrambling_metric**  
  *Description:* Computes an Out-of-Time-Ordered Correlator (OTOC) to measure information scrambling or chaotic dynamics under the specified Hamiltonian.  
  *Formula:* `ComputeOTOCScrambling(hamiltonian_ref, target_state_id)`
- **pointer_basis_stability_timeline**  
  *Description:* Monitors whether identified pointer states remain stable or begin interfering again as the system evolves in time.  
  *Formula:* `TrackPointerStabilityOverEvolution(target_state_id, hamiltonian_ref, time_step)`
- **unitarity_deviation**  
  *Description:* Estimates how non-unitary the resulting time evolution operator might be (e.g., from Trotterization error).  
  *Formula:* `ComputeUnitarityDeviation(hamiltonian_ref, time_step, evolution_method)`
- **quantum_speed_classical_emergence_ratio**  
  *Description:* Evaluates the ratio between the quantum speed limit timescale and the classical emergence timescale from decoherence.  
  *Formula:* `ComputeSpeedClassicalEmergenceRatio(quantum_speed_limit, QuantumState.classical_limit_indicator)`
- **classical_limit_check**  
  *Description:* Toy aggregator to see if quantum evolution effectively appears classical under certain dynamic conditions.  
  *Formula:* `AssessIfKineticTerm >> PotentialTerm or decoherence times => classical limit?`



---

## Entity: QuantumEvent

**Description**: Logs a broader quantum event (not strictly a measurement), e.g. a unitary gate, entangling interaction, or a specialized operation.

### Fields
- **event_id**  
  *Type:* string, *Datatype:*   
  
- **type**  
  *Type:* string, *Datatype:*   
  
- **operator_ref**  
  *Type:* string, *Datatype:*   
  
- **applied_to**  
  *Type:* array, *Datatype:*   
  
- **timestamp**  
  *Type:* string, *Datatype:*   
  
- **metadata**  
  *Type:* object, *Datatype:*   
  


### Aggregations
- **verifyEventApplicability**  
  *Description:* Ensures that measurement events reference a valid measurement operator, or that a unitary event references a valid gate, etc.  
  *Formula:* `CheckEventConsistency(type, operator_ref, applied_to)`



---

## Entity: ObserverRelationship

**Description**: Describes the relationship between two observers, capturing shared measurement events, cross-checking, or potential paradoxes (Wigner’s friend).

### Fields
- **relationship_id**  
  *Type:* string, *Datatype:*   
  
- **observer_A**  
  *Type:* string, *Datatype:*   
  
- **observer_B**  
  *Type:* string, *Datatype:*   
  
- **shared_events**  
  *Type:* array, *Datatype:*   
  
- **consistency_state**  
  *Type:* string, *Datatype:*   
  
- **relational_view_consistency**  
  *Type:* scalar, *Datatype:* json  
  


### Aggregations
- **observer_agreement_score**  
  *Description:* Calculates a numeric or qualitative measure of how consistently the two observers interpret shared measurement events.  
  *Formula:* `ComputeObserverAgreement(observer_A, observer_B, shared_events)`
- **rqm_intersubjective_discrepancy**  
  *Description:* Quantifies mismatch between how A sees B’s wavefunction and how B sees their own wavefunction in RQM contexts.  
  *Formula:* `ComputeRQMDiscrepancy(observer_A, observer_B, relational_view_consistency)`
- **wigners_friend_paradox_indicator**  
  *Description:* Flags a mismatch if observer A sees a collapsed outcome while observer B sees a superposition for the same event.  
  *Formula:* `DetectWignersFriendParadox(observer_A, observer_B, shared_events)`
- **nested_wigners_friend_indicator**  
  *Description:* Detects multi-level scenarios where B sees A in superposition after A measured the system.  
  *Formula:* `CheckNestedWignerScenario(observer_A, observer_B, shared_events)`
- **detect_cyclic_measurement_loop**  
  *Description:* Checks if observer A measures observer B while B also measures A, forming a cycle (relevant in RQM or Wigner’s friend).  
  *Formula:* `IdentifyMeasurementCyclesBetweenObservers(observer_A, observer_B, shared_events)`
- **extended_nested_wigner_analysis**  
  *Description:* Performs a deeper search for multi-level nested Wigner’s friend arrangements, analyzing partial collapses or superpositions at each vantage.  
  *Formula:* `ComputeMultiLevelWignerFriendScenario(observer_A, observer_B, shared_events)`
- **multi_level_paradox_analysis**  
  *Description:* Examines whether observer A or B is also being observed by other frames, forming multi-tier Wigner’s friend loops.  
  *Formula:* `AnalyzeMultiLevelWignerScenarios(observer_A, observer_B, shared_events)`
- **frame_discrepancy**  
  *Description:* Compares reference_frame_transform data from the two observers to identify any relative shift/boost or basis difference.  
  *Formula:* `ComputeFrameDifference(observer_A, observer_B)`
- **relational_wigner_analysis**  
  *Description:* General check for whether observer A sees B in superposition while B sees themselves as collapsed, indicating a Wigner’s friend paradox at the relational level.  
  *Formula:* `ComputeRelationalWignerFriendAnalysis(observer_A, observer_B, shared_events)`
- **reference_frame_transform_consistency**  
  *Description:* Examines the coordinate transformations each observer applies to confirm they do not produce contradictory measurement accounts.  
  *Formula:* `CheckReferenceFrameAlignment(observer_A, observer_B, ObserverFrame.*)`
- **shared_context_agreement**  
  *Description:* Measures overlap in Bayesian priors or knowledge states between the two observers.  
  *Formula:* `ComputeSharedContextualOverlap(observer_A.epistemic_context, observer_B.epistemic_context)`
- **asymmetric_view_check**  
  *Description:* Flags if A sees B in superposition while B sees themselves collapsed, or vice versa.  
  *Formula:* `CheckAsymmetricObservation(observer_A, observer_B, relational_view_consistency)`
- **multi_level_wigner_nesting_indicator**  
  *Description:* Detects and quantifies multi-level Wigner’s friend nesting by analyzing observer relationship records for cycles and nested measurement dependencies.  
  *Formula:* `AnalyzeNestedWignerFriendScenarios(shared_events, nested_wigners_friend_indicator)`
- **multi_level_observation_loop_score**  
  *Description:* Produces a numeric or qualitative score indicating the depth of nested or cyclical measurement loops between these observers.  
  *Formula:* `DetectNestedObservationLoops(observer_A, observer_B, shared_events)`

### Lambdas
- **resolve_rqm_inconsistency**
    
  *Formula:* `AttemptRQMInconsistencyResolution(observer_A, observer_B, shared_events, relational_view_consistency)`


---

## Entity: ConsistencyCheck

**Description**: General entity for logging or storing consistency-check results across quantum or classical data, possibly referencing warnings or errors.

### Fields
- **check_id**  
  *Type:* string, *Datatype:*   
  
- **description**  
  *Type:* string, *Datatype:*   
  
- **severity**  
  *Type:* string, *Datatype:*   
  
- **results**  
  *Type:* array, *Datatype:*   
  





---

## Entity: QuantumCircuit

**Description**: Represents a sequence of quantum gates operating on a target wavefunction or subsystem(s), with optional aggregator to run gates and measure.

### Fields
- **circuit_id**  
  *Type:* string, *Datatype:*   
  
- **gates**  
  *Type:* array, *Datatype:*   
  
- **target_wavefunction**  
  *Type:* string, *Datatype:*   
  


### Aggregations
- **generateCircuitMatrix**  
  *Description:* Composes all gates in this circuit into a single operator matrix.  
  *Formula:* `ComposeAllGatesIntoMatrix(gates)`
- **validateCircuit**  
  *Description:* Validates gate definitions and ensures they match the dimension of the target wavefunction or subsystem.  
  *Formula:* `CheckGateSequence(gates, target_wavefunction)`
- **executeCircuitAndMeasure**  
  *Description:* Convenience aggregator that applies all gates in sequence and then performs measurement events as specified.  
  *Formula:* `ApplyCircuitThenMeasure(this.circuit_id, target_wavefunction, measurement_config)`
- **gate_count**  
  *Description:* Returns the total number of gates in this circuit.  
  *Formula:* `LENGTH(gates)`
- **circuit_depth**  
  *Description:* Calculates how many gate layers exist, i.e. the circuit depth.  
  *Formula:* `ComputeCircuitDepth(gates)`
- **controlled_gate_count**  
  *Description:* Counts how many gates in the circuit specify a 'control' field (e.g., CNOT, Toffoli).  
  *Formula:* `COUNT(gates WHERE gates.control IS NOT NULL)`

### Lambdas
- **executeCircuit**
    
  *Formula:* ``


---

## Entity: IntersubjectiveRecord

**Description**: Stores how a group of observers come to (or fail to reach) mutual agreement in RQM contexts, referencing multi-observer final states.

### Fields
- **record_id**  
  *Type:* scalar, *Datatype:* string  
  
- **participants**  
  *Type:* scalar, *Datatype:* json  
  
- **comparison_strategy**  
  *Type:* scalar, *Datatype:* string  
  
- **final_state_agreement**  
  *Type:* scalar, *Datatype:* json  
  


### Aggregations
- **participant_discrepancies**  
  *Description:* Checks for outcome/state discrepancies among all participants.  
  *Formula:* `ComputeMultiObserverDiscrepancies(participants)`
- **multi_observer_inference**  
  *Description:* Evaluates whether multiple observers end up with the same final outcome or if they disagree.  
  *Formula:* `IF(participant_discrepancies == 0, 'All participants in agreement', 'Discrepancies found among participants')`
- **multi_observer_classical_darwinism**  
  *Description:* Checks if participants collectively share enough overlapping measurement info to treat the outcome as a classical pointer.  
  *Formula:* `IF( SUM(ObserverFrame.quantum_darwinism_index FOR each participant) > some_threshold, 'Classical pointer states emergent', 'Significant quantum coherence remains' )`
- **multi_level_paradox_analysis**  
  *Description:* Checks for multi-level nested or cyclical observer-measurements across all participants, detecting possible RQM paradoxes.  
  *Formula:* `AnalyzeNestedWignerFriendsAmongParticipants(this.record_id, participants)`
- **categorize_multi_observer_agreement**  
  *Description:* Distinguishes complete agreement (classical consensus), partial disagreement resolvable by communication, or irreconcilable RQM paradox among participants.  
  *Formula:* `ClassifyObserverConsensus(final_state_agreement, participant_discrepancies)`
- **classical_ledger_construction**  
  *Description:* Derives an 'effective classical record' from multiple observers' final outcomes if they converge strongly.  
  *Formula:* `BuildIntersubjectiveClassicalRecord(this.record_id, participants)`
- **fully_classical_ledger_flag**  
  *Description:* Indicates if participants converge on a classical-like pointer outcome with no discrepancies.  
  *Formula:* `IF(participant_discrepancies == 0 AND multi_observer_classical_darwinism == 'Classical pointer states emergent', 'Yes', 'No')`
- **robust_classical_fact_index**  
  *Description:* Scores how stable the final agreed-upon outcome is under small changes. Higher index => robustly shared classical fact.  
  *Formula:* `ComputeRobustClassicalFactIndex(participants, final_state_agreement, participant_discrepancies)`

### Lambdas
- **execute_comparison_protocol**
    
  *Formula:* `RunRQMIntersubjectiveComparison(this.record_id, participants)`


---

## Entity: ScenarioWavefunctionLink

**Description**: Bridging entity linking a GlobalScenarioRecord with QuantumStates included in that scenario.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **scenario_id**  
  *Type:* lookup, *Datatype:*   
  
- **state_id**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: ParameterSweepRecord

**Description**: Logs a parameter sweep over a QuantumEvolution for scanning different Hamiltonian or system parameters and storing results.

### Fields
- **sweep_id**  
  *Type:* scalar, *Datatype:* string  
  
- **parameters**  
  *Type:* scalar, *Datatype:* json  
  
- **target_evolution_id**  
  *Type:* lookup, *Datatype:*   
  


### Aggregations
- **run_sweep_and_store_results**  
  *Description:* Executes the time evolution for each parameter set, storing aggregator or wavefunction results as needed.  
  *Formula:* `ExecuteParameterSweep(target_evolution_id, parameters)`



---

## Entity: MeasurementResult

**Description**: Stores the raw or aggregated outcomes of a particular measurement event, e.g. repeated shots yielding a bitstring distribution.

### Fields
- **result_id**  
  *Type:* scalar, *Datatype:* string  
  
- **measurement_id**  
  *Type:* lookup, *Datatype:*   
  
- **raw_bitstring**  
  *Type:* scalar, *Datatype:* string  
  
- **count**  
  *Type:* scalar, *Datatype:* int  
  





---

## Entity: PhysicalConstantsRecord

**Description**: Stores fundamental constants (Planck, speed of light, G, Boltzmann, etc.) with numeric value, units, and optional uncertainty.

### Fields
- **record_id**  
  *Type:* scalar, *Datatype:* string  
  
- **symbol**  
  *Type:* scalar, *Datatype:* string  
  
- **value**  
  *Type:* scalar, *Datatype:* float  
  
- **units**  
  *Type:* scalar, *Datatype:* string  
  
- **uncertainty**  
  *Type:* scalar, *Datatype:* float  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  





---

## Entity: ReferenceFrameRecord

**Description**: Stores or indexes classical coordinate systems, transformations, or Minkowski references for usage by wavefunctions or particles.

### Fields
- **reference_frame_id**  
  *Type:* scalar, *Datatype:* string  
  
- **frame_name**  
  *Type:* scalar, *Datatype:* string  
  
- **dimensions**  
  *Type:* scalar, *Datatype:* int  
  
- **coordinate_model**  
  *Type:* scalar, *Datatype:* string  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  





---

## Entity: PotentialRecord

**Description**: For classical or quantum usage, storing a potential function (harmonic oscillator, inverse-square, etc.) with symbolic or param-based expression.

### Fields
- **potential_id**  
  *Type:* scalar, *Datatype:* string  
  
- **potential_name**  
  *Type:* scalar, *Datatype:* string  
  
- **functional_form**  
  *Type:* scalar, *Datatype:* json  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  


### Aggregations
- **value_at_position**  
  *Description:* Computes the potential's numeric value at given coordinate(s).  
  *Formula:* `Evaluate(functional_form, coords)`



---

## Entity: HamiltonianRecord

**Description**: Combines kinetic + potential terms in classical or quantum contexts. Might reference an associated PotentialRecord for the V(x) portion.

### Fields
- **hamiltonian_id**  
  *Type:* scalar, *Datatype:* string  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **domain_type**  
  *Type:* scalar, *Datatype:* string  
  
- **kinetic_term**  
  *Type:* scalar, *Datatype:* json  
  
- **potential_id**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: ParticleRecord

**Description**: Represents a (possibly classical) particle: mass, charge, spin, classical position/velocity, or references to quantum states.

### Fields
- **particle_id**  
  *Type:* scalar, *Datatype:* string  
  
- **label**  
  *Type:* scalar, *Datatype:* string  
  
- **mass**  
  *Type:* scalar, *Datatype:* float  
  
- **charge**  
  *Type:* scalar, *Datatype:* float  
  
- **spin**  
  *Type:* scalar, *Datatype:* float  
  
- **classical_position**  
  *Type:* scalar, *Datatype:* json  
  
- **classical_velocity**  
  *Type:* scalar, *Datatype:* json  
  
- **reference_frame_id**  
  *Type:* lookup, *Datatype:*   
  
- **attached_quantum_state_id**  
  *Type:* lookup, *Datatype:*   
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  


### Aggregations
- **velocity_magnitude**  
  *Description:* Computes the magnitude of the particle’s velocity vector, if it has one.  
  *Formula:* `SQRT( (classical_velocity.x^2) + (classical_velocity.y^2) + (classical_velocity.z^2) )`

### Lambdas
- **update_position**
  (Parameters: delta_t)  
  *Formula:* `classical_position + classical_velocity * delta_t`


---

## Entity: ParticleWavefunctionMapping

**Description**: Bridging table attaching multiple Particles to a single QuantumState. Useful for multi-particle wavefunctions in a shared Hilbert space.

### Fields
- ****  
  *Type:* scalar, *Datatype:* string  
  
- ****  
  *Type:* lookup, *Datatype:*   
  
- ****  
  *Type:* lookup, *Datatype:*   
  
- ****  
  *Type:* scalar, *Datatype:* string  
  





---

## Entity: ForceRecord

**Description**: Classical force concept, e.g. gravitational or electromagnetic, typically bridging classical realms. Could be used in N-body computations.

### Fields
- **force_id**  
  *Type:* scalar, *Datatype:* string  
  
- **force_type**  
  *Type:* scalar, *Datatype:* string  
  
- **particle_id**  
  *Type:* lookup, *Datatype:*   
  
- **force_vector**  
  *Type:* scalar, *Datatype:* json  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  



### Lambdas
- **compute_newtonian_force**
  (Parameters: other_particle_ids)  
  *Formula:* `e.g. G*m1*m2 / r^2 direction, storing in force_vector`


---

## Entity: GaugeFieldRecord

**Description**: Stores e.g. (E,B) or (Aμ) for a classical or quantum gauge field. May be U(1) or non-Abelian, used for field dynamics or transformations.

### Fields
- **gauge_field_id**  
  *Type:* scalar, *Datatype:* string  
  
- **gauge_type**  
  *Type:* scalar, *Datatype:* string  
  
- **field_components**  
  *Type:* scalar, *Datatype:* json  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  


### Aggregations
- **field_strength_tensor**  
  *Description:* Builds the field strength tensor Fμν from the gauge field components.  
  *Formula:* `ConstructFmuNu(field_components)`

### Lambdas
- **perform_gauge_transformation**
  (Parameters: gauge_function)  
  *Formula:* `Aμ -> Aμ + ∂μ(gauge_function)`


---

## Entity: ClassicalSystemRecord

**Description**: Groups multiple classical or partially classical particles for aggregated properties like total mass, momentum, etc.

### Fields
- **system_id**  
  *Type:* scalar, *Datatype:* string  
  
- **system_name**  
  *Type:* scalar, *Datatype:* string  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **members**  
  *Target Entity:* ParticleRecord, *Type:* one_to_many  
    
  (Join condition: **ParticleRecord.classical_system_id = this.system_id**)  
  *Description:* Particles in this system, if they store classical_system_id = system_id.

### Aggregations
- **sum_of_particle_energies**  
  *Description:* Placeholder aggregator for summing particle energies if they have kinetic or potential definitions.  
  *Formula:* `SUM( if we define kinetic + potential )`
- **total_system_mass**  
  *Description:* Computes the total mass of all particles in this classical system.  
  *Formula:* `SUM(members.mass)`
- **total_system_momentum**  
  *Description:* Computes the net momentum of the system by summing each member’s mass * velocity.  
  *Formula:* `VECTOR_SUM(members.mass * members.velocity)`



---

## Entity: SpacetimeMetricRecord

**Description**: Stores a 3+1 or 4D metric. Potentially references Einstein equation aggregator referencing stress-energy, etc.

### Fields
- **metric_record_id**  
  *Type:* scalar, *Datatype:* string  
  
- **metric_tensor**  
  *Type:* scalar, *Datatype:* json  
  
- **reference_frame_id**  
  *Type:* lookup, *Datatype:*   
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  


### Aggregations
- **ricci_scalar**  
  *Description:* Computes the Ricci scalar (R) for the metric.  
  *Formula:* `ComputeRicciScalar(metric_tensor)`
- **ricci_tensor**  
  *Description:* Computes the Ricci tensor (Rμν) from the metric.  
  *Formula:* `ComputeRicciTensor(metric_tensor)`
- **einstein_tensor**  
  *Description:* Builds the Einstein tensor Gμν = Rμν - 0.5*gμν*R.  
  *Formula:* `ComputeEinsteinTensor(ricci_tensor, ricci_scalar)`



---

## Entity: BlackHoleSystemRecord

**Description**: Entity for horizon radius, Hawking temperature, referencing mass, etc. Particularly for analyzing black-hole thermodynamics in a scenario.

### Fields
- **bh_system_id**  
  *Type:* scalar, *Datatype:* string  
  
- **bh_label**  
  *Type:* scalar, *Datatype:* string  
  
- **approx_mass**  
  *Type:* scalar, *Datatype:* float  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **scenario_id**  
  *Target Entity:* GlobalScenarioRecord, *Type:* lookup  
    
    
  *Description:* Which global scenario this black hole system is part of, enabling cross-referencing scenario-level aggregators.

### Aggregations
- **schwarzschild_radius**  
  *Description:* Computes the Schwarzschild radius for a non-rotating black hole, referencing G and c from PhysicalConstants if desired.  
  *Formula:* `(2 * G * approx_mass)/(c^2)`
- **branch_depth_blackhole_thermo_inference**  
  *Description:* Correlates the scenario's maximum wavefunction branch depth with black-hole horizon properties.  
  *Formula:* `AnalyzeBranchDepthAndBHProperties(scenario_id.max_branch_depth_across_scenario, this.schwarzschild_radius, hawking_temperature)`
- **branch_cut_analysis**  
  *Description:* Checks if the black-hole horizon functions as a decoherence boundary, correlating wavefunction branching data with BH mass/horizon size.  
  *Formula:* `AnalyzeBHAsHeisenbergCut(this.bh_system_id, scenario_id)`

### Lambdas
- **hawking_temperature**
    
  *Formula:* `UseApproximationsForHawkingTemp(approx_mass)`


---

## Entity: DarkMatterInferenceRecord

**Description**: 2.0 style entity summarizing missing mass, potential DM cross-sections, confidence, etc., referencing a scenario and region.

### Fields
- **record_id**  
  *Type:* scalar, *Datatype:* string  
  
- **scenario_id**  
  *Type:* lookup, *Datatype:*   
  
- **region_reference**  
  *Type:* lookup, *Datatype:*   
  
- **observed_mass**  
  *Type:* scalar, *Datatype:* float  
  
- **total_system_mass**  
  *Type:* scalar, *Datatype:* float  
  
- **missing_mass**  
  *Type:* lambda, *Datatype:*   
  
- **residual_mass_fraction**  
  *Type:* lambda, *Datatype:*   
  
- **confidence_level**  
  *Type:* scalar, *Datatype:* float  
  
- **timestamp**  
  *Type:* scalar, *Datatype:* datetime  
  


### Aggregations
- **dm_entanglement_correlation**  
  *Description:* Analyzes wavefunction entanglement across the scenario and compares it with the fraction of missing dark mass.  
  *Formula:* `CorrelateEntanglementWithMissingMass(this.record_id, scenario_id)`



---

## Entity: HaloSubstructureRecord

**Description**: Captures local density fluctuations and subhalo mass distributions within DM halos, referencing a scenario if needed.

### Fields
- **subhalo_id**  
  *Type:* scalar, *Datatype:* string  
  
- **subhalo_mass_distribution**  
  *Type:* scalar, *Datatype:* json  
  
- **concentration_parameter**  
  *Type:* scalar, *Datatype:* float  
  
- **local_density_variation**  
  *Type:* scalar, *Datatype:* float  
  
- **scenario_id**  
  *Type:* lookup, *Datatype:*   
  
- **linked_region**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: BaryonicFeedbackRecord

**Description**: Captures effects of baryonic processes (star formation, AGN feedback) on mass distribution, referencing a region or system.

### Fields
- **feedback_id**  
  *Type:* scalar, *Datatype:* string  
  
- **feedback_intensity**  
  *Type:* scalar, *Datatype:* float  
  
- **energy_injection_rate**  
  *Type:* scalar, *Datatype:* float  
  
- **mass_loss_fraction**  
  *Type:* scalar, *Datatype:* float  
  
- **linked_region**  
  *Type:* lookup, *Datatype:*   
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  





---

## Entity: CosmicEvolutionRecord

**Description**: Tracks evolution of cosmic parameters over redshift/time, allowing correlation with scenario data such as wavefunctions or observers.

### Fields
- **evolution_id**  
  *Type:* scalar, *Datatype:* string  
  
- **redshift**  
  *Type:* scalar, *Datatype:* float  
  
- **cosmic_time**  
  *Type:* scalar, *Datatype:* float  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  
- **scenario_id**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: EnvironmentalInfluenceRecord

**Description**: Captures local environmental effects such as tidal interactions or merger history in cosmic contexts, referencing a classical region or system.

### Fields
- **environment_id**  
  *Type:* scalar, *Datatype:* string  
  
- **local_density**  
  *Type:* scalar, *Datatype:* float  
  
- **tidal_effects**  
  *Type:* scalar, *Datatype:* float  
  
- **merger_history**  
  *Type:* scalar, *Datatype:* json  
  
- **linked_region**  
  *Type:* lookup, *Datatype:*   
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  


### Aggregations
- **influence_modifier**  
  *Description:* Produces a numeric or qualitative factor adjusting dark matter or baryonic inferences based on environmental conditions.  
  *Formula:* `ComputeInfluenceModifier(local_density, tidal_effects, merger_history)`



---

## Entity: DarkMatterInference

**Description**: Entity capturing second-order inferences regarding dark matter from aggregated system data, possibly referencing subhalo structures, cosmic evolution, etc.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **region_reference**  
  *Type:* lookup, *Datatype:*   
  
- **total_system_mass**  
  *Type:* aggregation, *Datatype:*   
  
- **observed_mass**  
  *Type:* aggregation, *Datatype:*   
  
- **missing_mass**  
  *Type:* lambda, *Datatype:*   
  
- **residual_mass_fraction**  
  *Type:* lambda, *Datatype:*   
  
- **DM_particle_mass_estimate**  
  *Type:* lambda, *Datatype:*   
  
- **interaction_cross_section**  
  *Type:* lambda, *Datatype:*   
  
- **confidence_level**  
  *Type:* aggregation, *Datatype:*   
  
- **associated_references**  
  *Type:* lookup, *Datatype:*   
  
- **timestamp**  
  *Type:* scalar, *Datatype:* datetime  
  





---

## Entity: ObservationalDataset

**Description**: Entity representing raw observational data from surveys, capturing parameters such as photometry, spectroscopy, and derived uncertainties.

### Fields
- **dataset_id**  
  *Type:* scalar, *Datatype:* string  
  
- **source_name**  
  *Type:* scalar, *Datatype:* string  
  
- **data_parameters**  
  *Type:* scalar, *Datatype:* json  
  
- **measurement_uncertainty**  
  *Type:* scalar, *Datatype:* float  
  
- **data_quality_flag**  
  *Type:* scalar, *Datatype:* string  
  
- **collection_date**  
  *Type:* scalar, *Datatype:* datetime  
  
- **associated_references**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: TheoreticalExperiment

**Description**: Entity for logging simulation runs and theoretical experiments, capturing input parameters and resulting inferences.

### Fields
- **experiment_id**  
  *Type:* scalar, *Datatype:* string  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **parameter_set**  
  *Type:* scalar, *Datatype:* json  
  
- **simulation_results**  
  *Type:* scalar, *Datatype:* json  
  
- **timestamp**  
  *Type:* scalar, *Datatype:* datetime  
  
- **associated_references**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: HaloSubstructure

**Description**: Entity capturing local density fluctuations and subhalo mass distributions within dark matter halos (alternative name to HaloSubstructureRecord).

### Fields
- **subhalo_id**  
  *Type:* scalar, *Datatype:* string  
  
- **subhalo_mass_distribution**  
  *Type:* scalar, *Datatype:* json  
  
- **concentration_parameter**  
  *Type:* scalar, *Datatype:* float  
  
- **local_density_variation**  
  *Type:* scalar, *Datatype:* float  
  
- **subhalo_mass_function**  
  *Type:* lambda, *Datatype:*   
  
- **linked_to**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: BaryonicFeedback

**Description**: Entity capturing the effects of baryonic processes (e.g. star formation, AGN feedback) on mass distribution (alternative name to BaryonicFeedbackRecord).

### Fields
- **feedback_id**  
  *Type:* scalar, *Datatype:* string  
  
- **feedback_intensity**  
  *Type:* scalar, *Datatype:* float  
  
- **energy_injection_rate**  
  *Type:* scalar, *Datatype:* float  
  
- **mass_loss_fraction**  
  *Type:* scalar, *Datatype:* float  
  
- **feedback_adjustment_factor**  
  *Type:* lambda, *Datatype:*   
  
- **linked_region**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: CosmicEvolution

**Description**: Entity representing the evolution of dark matter properties over cosmic time (alternative name to CosmicEvolutionRecord).

### Fields
- **evolution_id**  
  *Type:* scalar, *Datatype:* string  
  
- **redshift**  
  *Type:* scalar, *Datatype:* float  
  
- **cosmic_time**  
  *Type:* scalar, *Datatype:* float  
  
- **evolution_modifier**  
  *Type:* lambda, *Datatype:*   
  
- **associated_datasets**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: EnvironmentalInfluence

**Description**: Entity capturing local environmental effects such as density, tidal interactions, or merger history, referencing a region or system (alternative name).

### Fields
- **environment_id**  
  *Type:* scalar, *Datatype:* string  
  
- **local_density**  
  *Type:* scalar, *Datatype:* float  
  
- **tidal_effects**  
  *Type:* scalar, *Datatype:* float  
  
- **merger_history**  
  *Type:* scalar, *Datatype:* json  
  
- **influence_modifier**  
  *Type:* lambda, *Datatype:*   
  
- **linked_region**  
  *Type:* lookup, *Datatype:*   
  





---

## Entity: CosmologyCurvatureRecord

**Description**: Captures curvature parameters (Ω values) and derived geometry classification for the universe. These do not overlap with existing v2 fields.

### Fields
- **curvature_id**  
  *Type:* scalar, *Datatype:* string  
  
- **omega_mass**  
  *Type:* scalar, *Datatype:* float  
  
- **omega_relativistic**  
  *Type:* scalar, *Datatype:* float  
  
- **omega_lambda**  
  *Type:* scalar, *Datatype:* float  
  
- **omega_total**  
  *Type:* scalar, *Datatype:* float  
  
- **omega_k**  
  *Type:* scalar, *Datatype:* float  
  
- **curvature_classification**  
  *Type:* scalar, *Datatype:* enum  
  


### Aggregations
- **check_flatness**  
  *Description:* Simple aggregator that flags if universe is nearly flat or curved based on threshold.  
  *Formula:* `IF(ABS(omega_total - 1) <= 0.01, 'NearlyFlat', 'Curved')`

### Lambdas
- **update_curvature_classification**
    
  *Formula:* `IF(ABS(omega_total - 1) < 1e-3, 'flat', IF(omega_total > 1, 'positive','negative'))`


---

## Entity: GlobalTopologyRecord

**Description**: Represents global shape/topology hypotheses: finite vs infinite, multiply/simply connected, etc.

### Fields
- **topology_id**  
  *Type:* scalar, *Datatype:* string  
  
- **finite_or_infinite**  
  *Type:* scalar, *Datatype:* enum  
  
- **edge_or_boundary_flag**  
  *Type:* scalar, *Datatype:* boolean  
  
- **manifold_family**  
  *Type:* scalar, *Datatype:* enum  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  


### Aggregations
- **implied_volume**  
  *Description:* Simple aggregator that flags if volume is definable or not, based on finite/infinite enum.  
  *Formula:* `IF(finite_or_infinite='finite', 'computable or closed', 'no well-defined finite volume')`

### Lambdas
- **describe_edge_scenario**
    
  *Formula:* `IF(edge_or_boundary_flag=true, 'Universe has boundary—difficult to interpret physically', 'No boundary (closed manifold or infinite)')`


---

## Entity: CosmologyMeasurementRecord

**Description**: Logs observational data sets (e.g. WMAP, Planck, BOOMERanG) referencing their curvature or topology findings, or constraints on them.

### Fields
- **measurement_id**  
  *Type:* scalar, *Datatype:* string  
  
- **mission_name**  
  *Type:* scalar, *Datatype:* string  
  
- **omega_values_reported**  
  *Type:* scalar, *Datatype:* json  
  
- **angular_scale_or_method**  
  *Type:* scalar, *Datatype:* string  
  
- **quoted_error_margin**  
  *Type:* scalar, *Datatype:* float  
  
- **date_of_release**  
  *Type:* scalar, *Datatype:* datetime  
  

### Lookups
- **inferred_curvature_link**  
  *Target Entity:* CosmologyCurvatureRecord, *Type:* lookup  
    
    
  *Description:* Optionally links this measurement’s derived curvature to a stored CosmologyCurvatureRecord row.
- **inferred_topology_link**  
  *Target Entity:* GlobalTopologyRecord, *Type:* lookup  
    
    
  *Description:* If the measurement concluded or placed constraints on a certain topology, link it here.

### Aggregations
- **coarse_curvature_label**  
  *Description:*   
  *Formula:* `IF(ABS(omega_values_reported.Omega_total - 1) < quoted_error_margin, 'FlatWithinError', 'PossiblyCurved')`



---


