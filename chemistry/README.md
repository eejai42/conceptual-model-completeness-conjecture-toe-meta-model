# All-In-One CMCC Chemistry Model

A schema extending the PhysicsTOE with atoms, molecules, bonds, reactions, etc.

## Depends On:
- CMCC_Complete_ToEMM_Math
- CMCC_Complete_ToEMM_Physics

## Metadata

**Title**: CMCC Complete Chemistry ToE Meta-Model  
**Subtitle**: A Declarative Structural Approach to Chemical Entities and Reactions  
**Date**: March 2025

### Authors
- **EJ Alexandra** <start@anabstractlevel.com>  
  Affiliations: SSoT.me, EffortlessAPI.com

### Abstract
This Chemistry extension broadens the CMCC (Conceptual Model Completeness Conjecture) approach to cover atomic, molecular, and reaction-level concepts. Building on the existing ACID-based schema that unifies math and physics, this domain model encodes all chemical structures—like atoms, bonds, molecules, solutions, and reactions—via five fundamental primitives (S, D, L, A, F). The resulting framework allows cross-domain reasoning (such as quantum-level wavefunctions or reaction kinetics) in a unified, syntax-free data structure.

### Key Points
- Introduces detailed entities for atoms, bonds, molecules, and reactions within the broader CMCC environment.
- Showcases how aggregator rollups and lambda formulas handle chemical logic (e.g., stoichiometry, bond polarity, reaction energetics).
- Demonstrates a purely declarative approach, enabling Turing-completeness without writing domain-specific code.
- Integrates seamlessly with the CMCC Physics model for quantum wavefunctions and multiway branching, bridging quantum to classical chemistry.

### Implications
- Enables cross-domain queries (e.g., quantum wavefunctions plus reaction stoichiometry) using a single cohesive schema.
- Reduces translation overhead between domain-specific tools, offering a universal repository for chemical knowledge.
- Lays groundwork for expansions into biology or materials science by extending the same structural paradigm.

### Narrative
#### CMCC Chemistry Extension
Chemistry often requires bridging multiple scales: quantum mechanical interactions, molecular geometry, reaction kinetics, and thermodynamics. In a standard approach, each scale might be handled by separate tools and data formats, leading to fragmentation and repeated redefinition of core concepts.
By contrast, the CMCC Chemistry Model encodes these layers in a single, self-describing set of tables, references, and formulas—every concept is data-driven. 'Atoms' link to fundamental 'Particle' definitions, 'Molecules' aggregate atoms (and optionally wavefunctions), while 'Reactions' track stoichiometry, thermodynamic estimates, and kinetic data. The system handles partial or complete references to quantum states for advanced calculations, but remains fully consistent with the overarching ACID-based design that anchors the entire CMCC framework.
Whether you're investigating ring strain, measuring reaction feasibility, or bridging into the biology domain, the same five fundamental primitives apply—Schema, Data, Lookups, Aggregations, and Lambda fields—ensuring minimal friction in cross-domain expansions and maximum clarity in capturing complex chemical phenomena.


---

# Schema Overview

## Entity: Atom

**Description**: Represents a single element or ion, referencing the underlying physics Particle optionally.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **element_symbol**  
  *Type:* scalar, *Datatype:* string  
  
- **atomic_number**  
  *Type:* scalar, *Datatype:* int  
  
- **mass_override**  
  *Type:* scalar, *Datatype:* float  
  > Note: If present, use this mass instead of Particle.mass, e.g. for isotopes
- **charge_state**  
  *Type:* scalar, *Datatype:* float  
  > Note: Net charge, e.g. +1 for Na+
- **underlying_particle_id**  
  *Type:* lookup, *Datatype:*   
  > Note: Optional link to the physics-level Particle if we want to unify mass, spin, etc.


### Aggregations
- **effective_mass**  
  *Description:*   
  *Formula:* `IF mass_override != null THEN mass_override ELSE (LOOKUP(underlying_particle_id).mass)`
- **ion_electrons**  
  *Description:*   
  *Formula:* `atomic_number - charge_state`
- **valence_electron_count**  
  *Description:* Approximate valence electron count by atomic number and charge.  
  *Formula:* `ComputeValenceElectrons(atomic_number, charge_state)`
- **electronegativity_estimate**  
  *Description:* Estimated electronegativity (Pauling-like scale).  
  *Formula:* `EstimateElectronegativity(atomic_number)`
- **radius_estimate**  
  *Description:* Rough covalent radius or van der Waals radius in pm.  
  *Formula:* `ApproximateAtomicRadius(atomic_number)`
- **ionization_energy_estimate**  
  *Description:* First-ionization energy approximation.  
  *Formula:* `LookupIonizationEnergy(atomic_number)`
- **electron_affinity_estimate**  
  *Description:* Approximate electron affinity for the atom.  
  *Formula:* `LookupElectronAffinity(atomic_number)`
- **predicted_isotope_distribution**  
  *Description:* Returns approximate isotope ratios for this element.  
  *Formula:* `ComputeIsotopeDistribution(atomic_number, mass_override)`
- **orbital_configuration_string**  
  *Description:* Generates a string describing electron configuration, e.g. '1s2 2s2 ...'.  
  *Formula:* `ApproximateElectronConfiguration(atomic_number, charge_state)`
- **predicted_atomic_density**  
  *Description:* A naive aggregator for density (g/cm³) in the bulk elemental form.  
  *Formula:* `EstimateAtomicDensity(atomic_number)`
- **nuclear_binding_energy_estimate**  
  *Description:* Rough nuclear binding energy from mass defect.  
  *Formula:* `ComputeNuclearBindingEnergy(atomic_number, mass_override)`


### Constraints
- **integer_atom_number**  
  *Formula:* `atomic_number > 0`  
  *Error Message:* Atomic number must be positive integer
- **valid_charge_state**  
  *Formula:* `charge_state >= -atomic_number`  
  *Error Message:* Cannot have more electrons than Z+some large number, toy rule

---

## Entity: Bond

**Description**: Represents a chemical bond between two atoms (intra-molecular or otherwise).

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **bond_type**  
  *Type:* scalar, *Datatype:* string  
  > Note: e.g. single, double, triple, ionic, etc.
- **atom_id_1**  
  *Type:* lookup, *Datatype:*   
  
- **atom_id_2**  
  *Type:* lookup, *Datatype:*   
  
- **bond_order**  
  *Type:* scalar, *Datatype:* float  
  


### Aggregations
- **bond_polarity_index**  
  *Description:* Rough measure of bond polarity from electronegativity difference.  
  *Formula:* `ABS(Atom(atom_id_1).electronegativity_estimate - Atom(atom_id_2).electronegativity_estimate)`
- **bond_length_estimate**  
  *Description:* Estimates bond length in Å or pm.  
  *Formula:* `ApproximateBondLength( atom_id_1.radius_estimate, atom_id_2.radius_estimate, bond_order )`
- **bond_dissociation_energy_estimate**  
  *Description:* A rough BDE estimate, e.g. single vs double bond, polar vs nonpolar.  
  *Formula:* `ComputeBondDissociationEnergy(bond_type, bond_order, bond_polarity_index)`
- **is_resonance_bond**  
  *Description:* Flags if this bond might be part of a resonance system.  
  *Formula:* `CheckForResonance(atom_id_1, atom_id_2)`
- **bond_angle_with_third_atom**  
  *Description:* Predicts angle (in degrees) formed with a third reference atom (toy geometry approach).  
  *Formula:* `ComputeBondAngle(atom_id_1, atom_id_2, third_atom_id)`
- **bond_vibrational_frequency**  
  *Description:* Approx IR vibrational frequency (cm^-1) using reduced mass and bond order.  
  *Formula:* `EstimateBondVibrationFrequency(atom_id_1.effective_mass, atom_id_2.effective_mass, bond_order)`
- **bond_rotational_barrier**  
  *Description:* Estimates torsional barrier for single bonds or partial for double.  
  *Formula:* `EstimateRotationalBarrier(bond_type, bond_order, atom_id_1, atom_id_2)`
- **bond_reactivity_score**  
  *Description:* Scores how likely the bond is to break or rearrange under common reactions.  
  *Formula:* `ComputeBondReactivity(bond_order, bond_polarity_index, local_environment)`
- **estimated_bond_angle_strain**  
  *Description:* Flags strain if part of a ring or unusual geometry, referencing ring size or known angle deviance.  
  *Formula:* `CheckBondAngleStrain(atom_id_1, atom_id_2)`


### Constraints
- **bond_atoms_different**  
  *Formula:* `atom_id_1 != atom_id_2`  
  *Error Message:* No self-bonds
- **bond_order_valid**  
  *Formula:* `bond_order > 0 AND bond_order <= 3`  
  *Error Message:* Toy constraint: bond_order must be between 0 and 3

---

## Entity: Molecule

**Description**: Collection of atoms connected by bonds, plus optional reference to quantum wavefunction.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **notes**  
  *Type:* scalar, *Datatype:* string  
  
- **wavefunction_id**  
  *Type:* lookup, *Datatype:*   
  > Note: If we have a quantum wavefunction at the molecular level

### Lookups
- **atoms**  
  *Target Entity:* Atom, *Type:* many_to_many  
  (Join entity: **MoleculeAtomMapping**)  
  (Join condition: **MoleculeAtomMapping.molecule_id = this.id AND MoleculeAtomMapping.atom_id = Atom.id**)  
  *Description:* Atoms in the molecule
- **bonds**  
  *Target Entity:* Bond, *Type:* one_to_many  
    
  (Join condition: **Bond.atom_id_1 IN atoms OR Bond.atom_id_2 IN atoms**)  
  *Description:* Bonds referencing this molecule (optionally)

### Aggregations
- **molecular_mass**  
  *Description:*   
  *Formula:* `SUM( atoms.effective_mass )`
- **total_net_charge**  
  *Description:*   
  *Formula:* `SUM( atoms.charge_state )`
- **formula_string**  
  *Description:*   
  *Formula:* `ComputeStoichiometricFormula(atoms)`
- **total_valence_electrons**  
  *Description:* Sum of valence electrons from all constituent atoms.  
  *Formula:* `SUM( atoms.valence_electron_count )`
- **is_organic**  
  *Description:* Simple check for presence of carbon to label molecule as organic.  
  *Formula:* `IF( COUNT( atoms where element_symbol='C' ) > 0, true, false )`
- **predicted_solubility_in_water**  
  *Description:* Rough guess of water solubility from polar groups and net charge.  
  *Formula:* `EstimateSolubility(atoms, total_net_charge)`
- **formal_charge_distribution**  
  *Description:* Array or mapping of formal charges for each atom.  
  *Formula:* `ComputeFormalCharges(atoms, bonds)`
- **heavy_atom_count**  
  *Description:* Number of atoms heavier than hydrogen.  
  *Formula:* `COUNT( atoms where atomic_number > 1 )`
- **estimated_boiling_point**  
  *Description:* Naive or ML-based boiling point predictor.  
  *Formula:* `PredictBoilingPoint(molecular_mass, predicted_solubility_in_water)`
- **predicted_HOMO_energy**  
  *Description:* Estimated HOMO energy from partial quantum or empirical approach.  
  *Formula:* `ComputeHOMOEnergy(wavefunction_id, total_valence_electrons)`
- **predicted_LUMO_energy**  
  *Description:* Estimated LUMO energy from partial quantum or empirical approach.  
  *Formula:* `ComputeLUMOEnergy(wavefunction_id, total_valence_electrons)`
- **HOMO_LUMO_gap**  
  *Description:* Difference between the predicted LUMO and HOMO energies.  
  *Formula:* `predicted_LUMO_energy - predicted_HOMO_energy`
- **approximate_pKa**  
  *Description:* Naive aggregator for acid dissociation constant based on functional groups.  
  *Formula:* `EstimatePkaFromFunctionalGroups(atoms, bonds)`
- **predicted_UV_Vis_absorbance**  
  *Description:* Rough guess of UV-Vis absorbance max in nm.  
  *Formula:* `ApproximateUVVisPeak(HOMO_LUMO_gap, heavy_atom_count)`
- **ro5_violation_count**  
  *Description:* Counts how many Lipinski Rule of 5 criteria are violated.  
  *Formula:* `CountRuleOfFiveViolations(molecular_mass, total_valence_electrons, predicted_solubility_in_water)`

### Lambdas
- **optimize_geometry**
    
  *Formula:* `PerformMolecularGeometryOptimization(bonds, wavefunction_id)`
- **compute_properties**
  (Parameters: temperature)  
  *Formula:* `RunQuantumChemistryCalc(wavefunction_id, temperature)`
- **possible_tautomers**
    
  *Formula:* `GenerateTautomers(this.id, atoms, bonds)`

### Constraints
- **bond_connectivity_check**  
  *Formula:* `CheckIfAllAtomsConnected(bonds)`  
  *Error Message:* All atoms in a molecule must be connected via bonds

---

## Entity: MoleculeAtomMapping

**Description**: Bridging table for many-to-many: which atoms belong to which molecule and in what count (for coarse stoichiometric models).

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **molecule_id**  
  *Type:* lookup, *Datatype:*   
  
- **atom_id**  
  *Type:* lookup, *Datatype:*   
  
- **count_in_molecule**  
  *Type:* scalar, *Datatype:* int  
  > Note: If >1, e.g. for repeated subunits


### Aggregations
- **fraction_in_molecule**  
  *Description:* Fraction of total atom count for this species in the molecule.  
  *Formula:* `count_in_molecule / SUM(MoleculeAtomMapping.count_in_molecule WHERE molecule_id = this.molecule_id)`
- **mass_fraction_in_molecule**  
  *Description:* Fraction of total molecular mass contributed by this atom type.  
  *Formula:* `(Atom(effective_mass) * count_in_molecule) / Molecule(molecule_id).molecular_mass`


### Constraints
- **nonnegative_count**  
  *Formula:* `count_in_molecule >= 1`  
  *Error Message:* Must have at least one

---

## Entity: Reaction

**Description**: A chemical reaction with references to reactants, products, and optional details.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **label**  
  *Type:* scalar, *Datatype:* string  
  
- **activation_energy**  
  *Type:* scalar, *Datatype:* float  
  > Note: In Joules or eV, etc.
- **notes**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **reactants**  
  *Target Entity:* Molecule, *Type:* many_to_many  
  (Join entity: **ReactionParticipant**)  
  (Join condition: **ReactionParticipant.reaction_id = this.id AND ReactionParticipant.role='reactant'**)  
  *Description:* Reactant molecules
- **products**  
  *Target Entity:* Molecule, *Type:* many_to_many  
  (Join entity: **ReactionParticipant**)  
  (Join condition: **ReactionParticipant.reaction_id = this.id AND ReactionParticipant.role='product'**)  
  *Description:* Product molecules

### Aggregations
- **alias_R**  
  *Description:*   
  *Formula:* `LOOKUP(CMCC_Complete_ToEMM_Physics.PhysicalConstants where symbol='R').value`
- **delta_mass**  
  *Description:*   
  *Formula:* `SUM(products.molecular_mass) - SUM(reactants.molecular_mass)`
- **arrhenius_rate**  
  *Description:*   
  *Formula:* `pre_exponential_factor * EXP( -activation_energy / (alias_R * temperature) )`
- **reaction_exothermicity_estimate**  
  *Description:* Crude enthalpy difference to gauge exo vs endo.  
  *Formula:* `SUM(products.molecular_mass) * SomeEnthalpyTable - SUM(reactants.molecular_mass)* AnotherEnthalpyTable`
- **reaction_order_estimate**  
  *Description:* Counts sum of stoichiometric exponents as naive overall order.  
  *Formula:* `SUM( reactants.ReactionParticipant.stoichiometric_coefficient )`
- **reaction_rate_constant_estimate**  
  *Description:* A direct aggregator for rate constant using Arrhenius-like logic.  
  *Formula:* `ArrheniusEstimate( activation_energy, alias_R, some_temperature )`
- **equilibrium_constant_estimate**  
  *Description:* Rough K_eq from enthalpy/entropy or guess.  
  *Formula:* `ComputeEquilibriumConstant( reaction_exothermicity_estimate, some_temperature )`
- **reaction_feasibility_score**  
  *Description:* Generates an integer or float rating: 0=not feasible, 1=partially feasible, etc.  
  *Formula:* `AssessReactionFeasibility(delta_mass, reaction_exothermicity_estimate, alias_R)`
- **approximate_gibbs_free_energy**  
  *Description:* Rough ∆G estimate from enthalpy difference and guessed entropy term.  
  *Formula:* `ComputeGibbsEnergyFromEnthalpyAndEntropy(reaction_exothermicity_estimate, some_temperature)`
- **predicted_equilibrium_conversion**  
  *Description:* Guesses reaction's extent at equilibrium using a toy model.  
  *Formula:* `ComputeEqConversion(equilibrium_constant_estimate, reaction_feasibility_score)`
- **reaction_mechanism_classification**  
  *Description:* Labels reaction as SN2, radical, elimination, etc., in a simplified manner.  
  *Formula:* `ClassifyReactionMechanism(reactants, products, activation_energy)`
- **catalysis_susceptibility**  
  *Description:* Rates how easily a catalyst can lower the barrier, from 0=low to 1=high.  
  *Formula:* `AssessCatalysisFeasibility( reaction_mechanism_classification, activation_energy )`

### Lambdas
- **perform_reaction_step**
  (Parameters: time_step, reactant_concentrations)  
  *Formula:* `UpdateConcentrationsUsingKinetics( this, time_step, reactant_concentrations )`

### Constraints
- **mass_conservation**  
  *Formula:* `ABS( delta_mass ) < tiny_epsilon`  
  *Error Message:* Mass must be conserved (toy constraint ignoring binding energy).
- **charge_conservation**  
  *Formula:* `SUM(products.total_net_charge) = SUM(reactants.total_net_charge) ± tiny_epsilon`  
  *Error Message:* Charge must be conserved

---

## Entity: ReactionParticipant

**Description**: Bridging entity for Reaction, specifying which Molecule is a reactant or product.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **reaction_id**  
  *Type:* lookup, *Datatype:*   
  
- **molecule_id**  
  *Type:* lookup, *Datatype:*   
  
- **role**  
  *Type:* scalar, *Datatype:* string  
  > Note: 'reactant' or 'product' etc.
- **stoichiometric_coefficient**  
  *Type:* scalar, *Datatype:* float  
  


### Aggregations
- **quantity_needed**  
  *Description:* Compute how many moles or grams are required given stoichiometry.  
  *Formula:* `stoichiometric_coefficient * SomeBaseScaleFactor`
- **limiting_reagent_check**  
  *Description:* Flags if this reactant is limiting based on available amounts.  
  *Formula:* `CheckIfLimitingReagent(this.reaction_id, this.molecule_id)`
- **stoichiometric_excess**  
  *Description:* Checks how much of this participant is over the stoichiometric need, referencing what's 'on-hand'.  
  *Formula:* `ComputeStoichiometricExcess( this.molecule_id, this.reaction_id )`
- **partial_pressure_contribution**  
  *Description:* Estimates partial pressure if gas-phase and partial pressures are tracked.  
  *Formula:* `EstimatePartialPressure( this.molecule_id, reaction_id, total_pressure )`
- **per_atom_contribution**  
  *Description:* Fraction of total reaction atoms contributed by this participant.  
  *Formula:* `ComputePerAtomReactionShare(this.molecule_id, stoichiometric_coefficient)`


### Constraints
- **valid_role**  
  *Formula:* `role IN ('reactant','product','catalyst')`  
  *Error Message:* Role must be recognized

---

## Entity: Solution

**Description**: A new entity for solutions or mixtures containing one or more solutes and a solvent.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **solvent_molecule_id**  
  *Type:* lookup, *Datatype:*   
  
- **temperature**  
  *Type:* scalar, *Datatype:* float  
  
- **volume_liters**  
  *Type:* scalar, *Datatype:* float  
  

### Lookups
- **solute_molecules**  
  *Target Entity:* Molecule, *Type:* many_to_many  
  (Join entity: **SolutionSoluteMapping**)  
  (Join condition: **SolutionSoluteMapping.solution_id = this.id AND SolutionSoluteMapping.solute_molecule_id = Molecule.id**)  
  *Description:* 

### Aggregations
- **total_solute_concentration**  
  *Description:* Sum of all solute concentrations in the solution.  
  *Formula:* `SUM( SolutionSoluteMapping.concentration_of_solute WHERE solution_id = this.id )`
- **solution_ionic_strength**  
  *Description:* Half the sum of c_i * z_i^2 for each ionic species i in the solution.  
  *Formula:* `ComputeIonicStrength(solute_molecules, volume_liters)`
- **freezing_point_depression_estimate**  
  *Description:* Predicts ∆Tf from a simplistic colligative property formula.  
  *Formula:* `ComputeColligativeFPDepression( total_solute_concentration, solvent_molecule_id )`



---

## Entity: SolutionSoluteMapping

**Description**: Bridging entity to link solutions with solute molecules, storing concentration or amount data.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **solution_id**  
  *Type:* lookup, *Datatype:*   
  
- **solute_molecule_id**  
  *Type:* lookup, *Datatype:*   
  
- **concentration_of_solute**  
  *Type:* scalar, *Datatype:* float  
  





---


