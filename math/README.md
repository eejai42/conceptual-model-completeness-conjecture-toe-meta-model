# CMCC Complete Mathematics TOE Meta Model

A unified meta-model capturing foundational mathematics (sets, elements, functions, algebraic structures, category theory, propositions, equations, etc.) in a single ACID-compliant, declarative structure. All domain logic—like group axioms, function composition, theorem proofs—are expressed using lookups, aggregations, lambdas, and constraints.

## Depends On:

## Metadata

**Title**: CMCC Complete Mathematics ToE Meta-Model  
**Subtitle**: A Unified Declarative Framework for Abstract Structures, Axioms, and Proofs  
**Date**: March 2025

### Authors
- **EJ Alexandra** <start@anabstractlevel.com>  
  Affiliations: SSoT.me, EffortlessAPI.com

### Abstract
The Mathematics extension of the CMCC (Conceptual Model Completeness Conjecture) systematically represents abstract mathematical concepts—sets, elements, functions, propositions, equations, algebraic structures—under a single ACID-based schema. Using five foundational primitives (S, D, L, A, F), it captures axioms, proofs, and domain relationships (e.g., group axioms, ring axioms, function surjectivity) in a purely declarative format, enabling cross-domain synergy with physics, chemistry, and beyond.

### Key Points
- Models foundational mathematics (sets, elements, structures, proofs) declaratively, through aggregator formulas and constraints.
- Eliminates the need for domain-specific programming languages or proof scripts by storing the 'what' (the rules) as first-class data.
- Demonstrates Turing-completeness via lambda-calculus–style aggregator functions and references to universal computational models.
- Seamlessly integrates with other CMCC domains (e.g., physics, chemistry) to unify advanced mathematics with real-world applications.

### Implications
- Provides a universal environment for exploring proofs, theorems, and algebraic structures alongside other domains’ data.
- Supports flexible expansions—add new aggregator-based axioms or constraints without needing specialized theorem-proving code.
- Facilitates knowledge-sharing: once an axiom or proof is declared, other domains can reference it for consistent cross-domain logic.

### Narrative
#### CMCC Mathematics Extension
Mathematics is famously broad, encompassing everything from the basics of set theory and arithmetic to higher structures like rings, fields, categories, and beyond. Traditional approaches involve specialized notations, proof assistants, or programming languages, often siloed from one another.
In contrast, the CMCC Mathematics Model encodes these concepts within a single, self-describing schema. Each 'Set,' 'Element,' or 'Proposition' is a record in an ACID-compliant datastore, with domain logic (axioms, aggregator checks for commutativity or associativity, etc.) expressed as formulas. Proofs become derivation steps, re-usable by other theorems or even other domain models (like the CMCC Physics or Chemistry models).
By remaining purely declarative, this approach decouples syntax from semantics. Whether capturing something simple like the geometry of triangles or something advanced like category theory, the math extension inherits the same fundamental building blocks (S, D, L, A, F) that drive the entire CMCC framework. This ensures the utmost consistency, reusability, and cross-domain synergy in your knowledge representation.


---

# Schema Overview

## Entity: Set

**Description**: A fundamental collection of mathematical objects. Includes properties like countability, cardinality, discrete/continuous classification, plus aggregator fields to compute subsets or check emptiness.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **countable**  
  *Type:* scalar, *Datatype:* boolean  
  
- **cardinality**  
  *Type:* scalar, *Datatype:* string  
  
- **discrete_or_continuous**  
  *Type:* scalar, *Datatype:* string  
  
- **parent_set_id**  
  *Type:* lookup, *Datatype:*   
  
- **construction_rule**  
  *Type:* scalar, *Datatype:* json  
  

### Lookups
- **elements**  
  *Target Entity:* Element, *Type:* one_to_many  
    
  (Join condition: **Element.containing_set_id = this.id**)  
  *Description:* All Element records that belong to this set.

### Aggregations
- **is_empty**  
  *Description:* True if this set has zero elements.  
  *Formula:* `COUNT(elements) = 0`
- **is_finite**  
  *Description:* Naive aggregator: if set is labeled countable but not infinite, treat as finite.  
  *Formula:* `countable AND cardinality != 'aleph_0'`
- **cardinality_estimate**  
  *Description:* Gives a naive numeric count if finite, else refers to cardinality field for infinite sets.  
  *Formula:* `IF is_finite THEN COUNT(elements) ELSE '∞ (or as specified by cardinality)'`
- **min_element**  
  *Description:* Finds the minimum element if a strict ordering is known. Null if not found or no order defined.  
  *Formula:* `IF (some ordering is declared) THEN pick e in elements s.t. ∀x in elements, e <= x, else null`
- **has_min_element**  
  *Description:* Checks if there is a well-defined minimum element among 'elements'.  
  *Formula:* `IF (min_element != null) THEN true ELSE false`
- **has_max_element**  
  *Description:* Checks if there is a well-defined maximum element among 'elements'.  
  *Formula:* `IF (some ordering is declared AND an element e s.t. ∀x in elements: x ≤ e) THEN true ELSE false`
- **sum_of_elements**  
  *Description:* If numeric, returns the sum of all elements. Null if non-numeric or infinite.  
  *Formula:* `IF (all e in elements are numeric) THEN SUM(elements.value) ELSE null`
- **is_subset_of_integers**  
  *Description:* True if every element of this set is also in the 'integers' set. Null if 'integers' not found.  
  *Formula:* `IF LOOKUP('integers') != null THEN FOR ALL e in this.elements => e IN LOOKUP('integers').elements ELSE null`
- **singleton_check**  
  *Description:* Checks if the set has exactly one element.  
  *Formula:* `COUNT(elements) = 1`
- **average_of_elements**  
  *Description:* If numeric elements exist, returns the average. Null otherwise.  
  *Formula:* `IF (all e in elements are numeric) THEN AVERAGE(elements.value) ELSE null`
- **supremum**  
  *Description:* For an ordered set, attempts to find the least upper bound among elements, or null if not well-defined.  
  *Formula:* `FindSupremum(elements)`
- **power_set_size**  
  *Description:* Number of all subsets, i.e. 2^n if the set is finite with n elements.  
  *Formula:* `IF (is_finite) THEN POWER(2, COUNT(elements)) ELSE null`
- **infimum**  
  *Description:* Least element or lower bound if numeric. Returns null if not well-defined or set is empty.  
  *Formula:* `ComputeInfimum(elements)`
- **largest_element**  
  *Description:* Returns the maximum element if an order is declared and a maximum exists, otherwise null.  
  *Formula:* `IF (some ordering is declared) THEN MaxElement(elements) ELSE null`
- **finite_subset_count**  
  *Description:* Same as power_set_size for a finite set. If infinite, returns null.  
  *Formula:* `IF (is_finite) THEN POWER(2, COUNT(elements)) ELSE null`
- **count_of_even_elements**  
  *Description:* Counts how many elements are even integers, if numeric.  
  *Formula:* `IF all e in elements are integers THEN COUNT(e where e.value % 2 = 0) ELSE null`
- **contains_only_positive_numbers**  
  *Description:* Checks if every numeric element in the set is > 0.  
  *Formula:* `IF all e in elements are numeric THEN (FOR ALL e in elements => e.value > 0) ELSE null`
- **lowest_common_multiple**  
  *Description:* Computes LCM of all positive integers in the set, if applicable.  
  *Formula:* `IF all e in elements are positive integers THEN LCM(elements.value) ELSE null`
- **contains_only_primes**  
  *Description:* True if every element in this set is a prime integer. Null if non-integer or empty.  
  *Formula:* `IF (all e in elements are integers) THEN (FOR ALL e in elements => isPrime(e.value)) ELSE null`
- **max_gap_between_consecutive_elements**  
  *Description:* For a sorted set of integers, computes the largest difference between consecutive elements. Null if non-integer or empty.  
  *Formula:* `IF (all e in elements are integers) THEN (MAX( consecutiveDifferences(sorted(elements.value)) )) ELSE null`
- **sum_of_squares**  
  *Description:* Sums the squares of each numeric element, or null if any element is non-numeric.  
  *Formula:* `IF (all e in elements are numeric) THEN SUM( e.value^2 for e in elements ) ELSE null`
- **gcd_of_elements**  
  *Description:* Computes the GCD of all integer elements, or null if non-integer or empty.  
  *Formula:* `IF (all e in elements are integers AND COUNT(elements) > 0) THEN GCD(elements.value) ELSE null`
- **standard_deviation**  
  *Description:* Sample standard deviation of numeric elements. Null if not numeric or too few elements.  
  *Formula:* `IF (all e in elements are numeric AND COUNT(elements) > 1) THEN ComputeStdDev(elements.value) ELSE null`
- **closure_under_addition**  
  *Description:* Checks if for all x,y in the set, x + y is still in the set. Implementation conceptual; references a known addition operator if relevant.  
  *Formula:* `CheckClosureOverAddition(this.id)`
- **accumulation_point_count**  
  *Description:* If subset of reals, attempts to count how many distinct accumulation points. Null otherwise.  
  *Formula:* `IF (discrete_or_continuous='continuous' OR all e in elements are real) THEN CountAccumulationPoints(elements) ELSE null`
- **lowest_negative_element**  
  *Description:* Finds the minimum among negative elements if the set is numeric and has negative values.  
  *Formula:* `IF (all e in elements are numeric) THEN MIN(e in elements WHERE e.value < 0) ELSE null`
- **contains_rational_numbers**  
  *Description:* Checks if every numeric element is a rational number (p/q). Returns null if set is non-numeric or empty.  
  *Formula:* `IF (all e in elements are numeric) THEN (FOR ALL e in elements => isRational(e.value)) ELSE null`
- **contains_square_numbers_only**  
  *Description:* True if every integer element is a perfect square, false if any element is a non-square, null if non-integer or empty.  
  *Formula:* `IF (all e in elements are integers AND COUNT(elements) > 0) THEN (FOR ALL e in elements => isPerfectSquare(e.value)) ELSE null`
- **has_primitive_root**  
  *Description:* For sets referencing modular arithmetic, checks if a generator (primitive root) exists. Conceptual, returns boolean/null.  
  *Formula:* `CheckPrimitiveRootExists(this.id)`

### Lambdas
- **subset**
  (Parameters: predicate)  
  *Formula:* `CreateSet( elements.filter(e => evaluate(predicate,e)) )`
- **power_set**
    
  *Formula:* `GenerateAllSubsets(this)`
- **intersection**
  (Parameters: other_set_id)  
  *Formula:* `CreateSet( elements.filter(e => e IN LOOKUP(other_set_id).elements ) )`
- **cartesian_product**
  (Parameters: other_set_id)  
  *Formula:* `GenerateCartesianProduct(this.elements, LOOKUP(other_set_id).elements)`
- **union**
  (Parameters: other_set_id)  
  *Formula:* `CreateSet( DISTINCT( elements ∪ LOOKUP(other_set_id).elements ) )`
- **difference**
  (Parameters: other_set_id)  
  *Formula:* `CreateSet( elements.filter(e => e NOT IN LOOKUP(other_set_id).elements) )`
- **random_element**
    
  *Formula:* `PickRandom(elements)`
- **random_subset**
    
  *Formula:* `GenerateRandomSubset(this.elements)`

### Constraints
- **valid_cardinality**  
  *Formula:* `cardinality IN ['finite','aleph_0','aleph_1','c','etc']`  
  *Error Message:* Unrecognized cardinality specification

---

## Entity: Element

**Description**: An atomic or composite member of a Set. Can reference structured or raw data in 'value'.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **containing_set_id**  
  *Type:* lookup, *Datatype:*   
  
- **value_type**  
  *Type:* scalar, *Datatype:* string  
  
- **value**  
  *Type:* scalar, *Datatype:* json  
  


### Aggregations
- **index_in_set**  
  *Description:* An optional aggregator to position the element within the set’s ordering (if any). If no ordering, returns null.  
  *Formula:* `RankWithin(containing_set_id.elements, this.id)`
- **is_positive**  
  *Description:* Checks if this element’s numeric value is > 0, if containing_set_id is integers/reals.  
  *Formula:* `IF (containing_set_id in ["integers","reals"]) THEN (value > 0) ELSE null`
- **absolute_value**  
  *Description:* If numeric, returns |value|. Otherwise null.  
  *Formula:* `IF (value_type in ["int","float"]) THEN ABS(value) ELSE null`
- **is_zero_element**  
  *Description:* Checks if this element is 0, for numeric types.  
  *Formula:* `IF value_type in ['int','float'] THEN (value == 0) ELSE null`
- **negation**  
  *Description:* Returns the additive inverse if numeric, else null.  
  *Formula:* `IF value_type in ['int','float'] THEN (-value) ELSE null`
- **prime_factorization**  
  *Description:* Returns prime factors of an integer, or null otherwise.  
  *Formula:* `IF value_type='int' THEN FactorInteger(value) ELSE null`
- **is_prime**  
  *Description:* Checks if this element’s value is prime (only valid for int).  
  *Formula:* `IF (value_type='int') THEN CheckPrimality(value) ELSE null`
- **digit_sum**  
  *Description:* Sum of the decimal digits if this element is an integer.  
  *Formula:* `IF (value_type='int') THEN SumOfDigits(value) ELSE null`
- **count_of_distinct_prime_factors**  
  *Description:* Number of distinct prime factors if value_type='int'. Null otherwise.  
  *Formula:* `IF (value_type='int') THEN LENGTH(UNIQUE(PrimeFactorization(value))) ELSE null`
- **complex_conjugate**  
  *Description:* If the element is a complex number, return its conjugate. Null if real-only or not complex.  
  *Formula:* `IF (value_type='complex') THEN Conjugate(value) ELSE null`



---

## Entity: ArithmeticOperator

**Description**: Represents a standard arithmetic operator (+, -, *, /, ^) with optional domain/codomain. Could also store matrix or group ops.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **symbol**  
  *Type:* scalar, *Datatype:* string  
  
- **domain_set_id**  
  *Type:* lookup, *Datatype:*   
  
- **codomain_set_id**  
  *Type:* lookup, *Datatype:*   
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  


### Aggregations
- **is_commutative**  
  *Description:* Indicates if the operator is commutative over its domain set. E.g. '+' on ℤ => true, '-' => false.  
  *Formula:* `CheckPairwiseCommutativity(symbol, domain_set_id)`
- **is_associative**  
  *Description:* Checks if (a op b) op c = a op (b op c) for all a,b,c in domain_set_id, ignoring domain/codomain if not numeric.  
  *Formula:* `CheckPairwiseAssociativity(symbol, domain_set_id)`
- **neutral_element**  
  *Description:* Finds e in domain_set_id such that e op x = x op e = x for all x, or returns null if none.  
  *Formula:* `SearchForIdentityElement(symbol, domain_set_id)`
- **neutral_element_exists**  
  *Description:* Simpler variant checking if any identity element is found in the domain.  
  *Formula:* `IF neutral_element != null THEN true ELSE false`
- **is_bounded**  
  *Description:* Checks if the operator yields outputs within a certain range for all inputs in domain_set_id. Implementation is conceptual.  
  *Formula:* `CheckBoundedness(symbol, domain_set_id)`
- **is_idempotent**  
  *Description:* Verifies x op x = x for all x in the domain.  
  *Formula:* `CheckIdempotency(symbol, domain_set_id)`
- **absorbing_element**  
  *Description:* Finds an element a such that a op x = a for all x in domain_set_id. Returns the element or null if none.  
  *Formula:* `FindAbsorbingElement(symbol, domain_set_id)`
- **is_left_invertible**  
  *Description:* True if for every x in domain, ∃y s.t. y op x = identity. Implementation conceptual.  
  *Formula:* `CheckLeftInvertibility(symbol, domain_set_id)`
- **closed_under_operator**  
  *Description:* Verifies that x op y remains in the domain for all x,y.  
  *Formula:* `FOR ALL x,y in domain_set_id => (x op y) in domain_set_id`
- **range_in_domain**  
  *Description:* Constructs the set of {x op y | x,y in domain} and checks subset. Implementation conceptual.  
  *Formula:* `CreateSetOfOperationResults(symbol, domain_set_id)`
- **exponentiation_table**  
  *Description:* If the domain is finite and operator is multiplication, enumerates x^y for x,y in domain. Null otherwise.  
  *Formula:* `IF (symbol='*' AND domain_set_id.is_finite) THEN BuildExponentTable(domain_set_id) ELSE null`
- **is_associated_operator**  
  *Description:* Checks if this operator is recognized as the official operation in a referencing AlgebraicStructure record.  
  *Formula:* `ScanAlgebraicStructuresForOperator(this.id)`
- **closure_under_operator_with_identity**  
  *Description:* Verifies closure plus presence of identity in domain_set_id for this operator. Returns bool or null.  
  *Formula:* `IF (CheckClosure(domain_set_id, symbol) AND FindIdentityElement(domain_set_id, symbol) != null) THEN true ELSE false`

### Lambdas
- **restrict_operator_domain**
  (Parameters: subset_set_id)  
  *Formula:* `CreateRestrictedOperator(this.id, subset_set_id)`


---

## Entity: Proposition

**Description**: 



### Aggregations
- **all_dependencies_proven**  
  *Description:* Looks at 'depends_on' array. Returns true if each referenced Proposition is_proven == true.  
  *Formula:* `For each p in depends_on => p.is_proven => must be true. If all true => this aggregator= true.`



---

## Entity: Function

**Description**: A mapping from a domain Set to a codomain Set. Fields to store rule definitions, aggregator checks for injectivity, surjectivity, etc.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **domain_set_id**  
  *Type:* lookup, *Datatype:*   
  
- **codomain_set_id**  
  *Type:* lookup, *Datatype:*   
  
- **rule**  
  *Type:* scalar, *Datatype:* json  
  


### Aggregations
- **is_injective**  
  *Description:* Aggregator that determines if f(x1)=f(x2) => x1=x2 by scanning the rule or partial table.  
  *Formula:* `CheckInjectivity(rule)`
- **is_surjective**  
  *Description:* Determines if the function’s range covers the entire codomain.  
  *Formula:* `CheckSurjectivity(rule,codomain_set_id)`
- **is_bijective**  
  *Description:* True if aggregator sees both injectivity and surjectivity.  
  *Formula:* `is_injective AND is_surjective`
- **periodicity_check**  
  *Description:* Indicates if there’s a smallest positive period p. E.g. for sin(x), p=2π. If none, returns null.  
  *Formula:* `DetectIfExistsPeriod(rule, domain_set_id)`
- **is_total**  
  *Description:* Checks if the function is defined for every element in its domain set. If any missing mapping => false.  
  *Formula:* `Scan domain_set_id.elements => all have a mapped output in rule => true, else false`
- **fixed_points**  
  *Description:* All elements x in the domain for which f(x) = x.  
  *Formula:* `FOR ALL x in domain_set_id.elements => if (ApplyRule(rule, x) = x) then collect x`
- **image_set**  
  *Description:* The set of all distinct outputs in the codomain that f maps to.  
  *Formula:* `CreateSet( domain_set_id.elements.map(x => ApplyRule(rule,x)) )`
- **surjectivity_ratio**  
  *Description:* Ratio of how many elements in the codomain are actually hit by f, over total codomain size if finite.  
  *Formula:* `IF (codomain_set_id.is_finite) THEN (COUNT(DISTINCT image_set) / COUNT(codomain_set_id.elements)) ELSE null`
- **non_trivial_preimages_count**  
  *Description:* Count how many distinct output values have more than one input mapping to them.  
  *Formula:* `ComputeNumberOfOutputValuesWithMultiples(domain_set_id, rule)`
- **coimage_set**  
  *Description:* Groups domain elements by their mapped output to create the coimage structure.  
  *Formula:* `ConstructCoimage(domain_set_id, rule)`
- **rank**  
  *Description:* If finite domain/codomain, rank is the size of the image. Else null.  
  *Formula:* `IF (domain_set_id.is_finite AND codomain_set_id.is_finite) THEN COUNT(DISTINCT domain_set_id.elements.map(e => ApplyRule(rule,e))) ELSE null`
- **max_fiber_size**  
  *Description:* Returns the largest cardinality among all preimages for a single codomain value.  
  *Formula:* `ComputeMaxPreimageSize(domain_set_id, rule)`
- **injectivity_violations_list**  
  *Description:* All pairs (x1,x2) with x1 != x2 but f(x1) = f(x2).  
  *Formula:* `GatherInjectivityViolations(rule, domain_set_id)`
- **antiderivative_check**  
  *Description:* If domain is real, tries symbolic integration and returns indefinite integral if possible.  
  *Formula:* `IF domain_set_id = 'reals' THEN AttemptSymbolicAntiderivative(rule) ELSE null`
- **codomain_coverage_percentage**  
  *Description:* If codomain is finite, computes (|image_set| / |codomain|)*100.  
  *Formula:* `IF codomain_set_id.is_finite THEN (COUNT(DISTINCT image_set) / COUNT(codomain_set_id.elements)) * 100 ELSE null`
- **limit_at_infinity**  
  *Description:* Attempts to evaluate lim(x→∞) of f(x) if domain is unbounded real. Returns numeric or symbolic result.  
  *Formula:* `IF (domain_set_id = 'reals') THEN EvaluateLimitAtInfinity(rule) ELSE null`
- **derivative_expression**  
  *Description:* Symbolic derivative if domain is real and f is differentiable. Returns expression or null.  
  *Formula:* `IF (domain_set_id = 'reals') THEN DifferentiateExpression(rule) ELSE null`
- **is_monotonic**  
  *Description:* Checks if f is strictly increasing, strictly decreasing, or neither, over real domain.  
  *Formula:* `IF (domain_set_id = 'reals') THEN CheckMonotonicity(rule) ELSE null`
- **function_table**  
  *Description:* If domain is finite, returns a table mapping each input to its output.  
  *Formula:* `IF (domain_set_id.is_finite) THEN ConstructFunctionTable(domain_set_id.elements, rule) ELSE null`
- **bounded_function_check**  
  *Description:* For real-valued f: domain->ℝ, checks if |f(x)| ≤ M < ∞ for all x. Null if not numeric or domain infinite.  
  *Formula:* `IF (domain_set_id='reals') THEN CheckFunctionBoundedness(rule) ELSE null`
- **superadditive_check**  
  *Description:* If numeric, checks f(x+y) ≥ f(x) + f(y). Implementation conceptual. Returns bool or null.  
  *Formula:* `IF (domain_set_id='reals') THEN CheckSuperadditivity(rule) ELSE null`

### Lambdas
- **compose**
  (Parameters: other_function_id)  
  *Formula:* `ComposeRules(this.rule, LOOKUP(other_function_id).rule)`
- **inverse**
    
  *Formula:* `IF is_bijective THEN InvertRule(rule) ELSE null`
- **restrict_domain**
  (Parameters: subset_set_id)  
  *Formula:* `CreateNewFunction( domain=subset_set_id, codomain=codomain_set_id, rule=rule restricted to that subset )`
- **fiber_over_value**
  (Parameters: target_value)  
  *Formula:* `domain_set_id.elements.filter(x => ApplyRule(rule,x) = target_value)`
- **compose_self**
    
  *Formula:* `IF (domain_set_id = codomain_set_id) THEN ComposeRules(rule, rule) ELSE null`
- **partial_eval**
  (Parameters: subset_domain_id)  
  *Formula:* `CreateNewFunction( domain=subset_domain_id, codomain=codomain_set_id, rule=rule restricted )`


---

## Entity: AlgebraicStructure

**Description**: An algebraic or mathematical structure built on a base set, plus operations and relations. E.g. group, ring, field. Aggregators check axioms.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **base_set_id**  
  *Type:* lookup, *Datatype:*   
  
- **algebraic_structure_type**  
  *Type:* scalar, *Datatype:* string  
  
- **algebraic_operations**  
  *Type:* scalar, *Datatype:* json  
  
- **relations**  
  *Type:* scalar, *Datatype:* json  
  


### Aggregations
- **is_group**  
  *Description:* Confirms associativity, identity, inverses under the 'addition' operation if structure_type is 'group'.  
  *Formula:* `CheckGroupAxioms(algebraic_operations, base_set_id)`
- **is_ring**  
  *Description:* Confirms ring axioms if structure_type is 'ring' (two operations, distributivity, etc.).  
  *Formula:* `CheckRingAxioms(algebraic_operations, base_set_id)`
- **is_field**  
  *Description:* Checks commutative ring with unity + multiplicative inverses for all non-zero elements, etc.  
  *Formula:* `CheckFieldAxioms(algebraic_operations, base_set_id)`
- **is_integral_domain**  
  *Description:* True if ring has no zero divisors, ignoring edge cases unless structure_type is 'ring'.  
  *Formula:* `CheckIfNoZeroDivisors(base_set_id, algebraic_operations.multiplication)`
- **has_identity_for_all_ops**  
  *Description:* Checks if there is a single element that serves as identity for each operation in 'algebraic_operations'.  
  *Formula:* `CheckCommonIdentityElement(base_set_id, algebraic_operations)`
- **all_inverses_exist**  
  *Description:* If the structure is supposed to be a group or field, ensures every non-zero element has an inverse w.r.t. each operation.  
  *Formula:* `For each op in algebraic_operations => checkInverses(base_set_id, op)`
- **is_commutative_ring**  
  *Description:* If structure_type is 'ring', checks if addition and multiplication are commutative for all elements.  
  *Formula:* `IF (algebraic_structure_type='ring') THEN CheckRingCommutativity(base_set_id, algebraic_operations) ELSE null`
- **potential_contradictions**  
  *Description:* Searches for other propositions that might contradict this one if both are proven.  
  *Formula:* `FindContradictoryPropositions(this.id)`
- **similar_propositions**  
  *Description:* Returns a list of propositions with statements that match a certain similarity threshold to this statement.  
  *Formula:* `ComputePropositionSimilarity(this.statement)`
- **operation_count**  
  *Description:* Counts how many distinct operations are defined in algebraic_operations JSON.  
  *Formula:* `COUNT_KEYS(algebraic_operations)`
- **commutative_operations_list**  
  *Description:* Returns a list of operations that are verified to be commutative on base_set_id.  
  *Formula:* `For each op in algebraic_operations => if CheckCommutativity(op, base_set_id) => add op`
- **center_of_structure**  
  *Description:* All elements z that commute with every x in base_set for each operation in algebraic_operations.  
  *Formula:* `FindCenter(base_set_id, algebraic_operations)`
- **characteristic**  
  *Description:* For rings/fields, smallest n>0 s.t. n*1=0, or 0 if none. Implementation conceptual.  
  *Formula:* `ComputeCharacteristic(base_set_id, algebraic_operations)`
- **commutative_operations_count**  
  *Description:* Counts how many operations in algebraic_operations are commutative over base_set_id.  
  *Formula:* `For each op in algebraic_operations => if CheckCommutativity(op, base_set_id) then increment count`
- **zero_divisor_detection**  
  *Description:* Collects all (a,b) != (0,0) with a*b=0 in ring structures.  
  *Formula:* `IF algebraic_structure_type in ['ring','field'] THEN FindZeroDivisors(base_set_id, algebraic_operations) ELSE null`
- **idempotent_elements_list**  
  *Description:* All elements e for which e op e = e (in the relevant operation).  
  *Formula:* `IF 'multiplication' in algebraic_operations THEN For all e => e * e = e ELSE null`
- **operation_table**  
  *Description:* Constructs a Cayley/operation table if the domain set is finite and not too large.  
  *Formula:* `IF (domain_set_id.is_finite) THEN BuildOperationTable(this.id, domain_set_id) ELSE null`
- **invertible_element_count**  
  *Description:* If the operator behaves group-like, counts how many elements have inverses. Implementation conceptual.  
  *Formula:* `CountInvertibleElements(this.id, domain_set_id)`
- **commutator_subgroup**  
  *Description:* If the structure is a group, returns the subgroup generated by all commutators [a,b]. Null otherwise.  
  *Formula:* `IF algebraic_structure_type='group' THEN GenerateCommutatorSubgroup(base_set_id, algebraic_operations) ELSE null`
- **maximal_ideals_list**  
  *Description:* If the structure is a ring, attempts to list its maximal ideals. Implementation conceptual.  
  *Formula:* `IF algebraic_structure_type='ring' THEN FindMaximalIdeals(base_set_id, algebraic_operations) ELSE null`
- **dimension_if_vector_space**  
  *Description:* If this structure is a vector space, tries to compute dimension over its field. Null otherwise.  
  *Formula:* `IF algebraic_structure_type='vector_space' THEN ComputeVectorSpaceDimension(base_set_id) ELSE null`
- **homomorphism_count**  
  *Description:* Counts how many Functions in the data are labeled or detected as homomorphisms from this structure to any other.  
  *Formula:* `SearchFunctionsForHomomorphisms(this.id)`
- **group_center_cardinality**  
  *Description:* If structure_type='group', returns the size of the center Z(G). Null if not a group.  
  *Formula:* `IF (algebraic_structure_type='group') THEN COUNT(FindCenter(base_set_id, algebraic_operations)) ELSE null`

### Lambdas
- **has_unit_element**
    
  *Formula:* `Scan base_set_id for e => ∀x, e*x = x*e = x. If found, return e else null`
- **invoke_axiom**
  (Parameters: axiom_proposition_id)  
  *Formula:* `AddPropositionDependency(this.id, axiom_proposition_id)`
- **validate_structure_type**
    
  *Formula:* `CompareDeclaredStructureTypeWithAxioms(this.id)`


---

## Entity: Proposition

**Description**: A formal statement (lemma, theorem, corollary). We can store its statement, proof steps, dependencies, aggregator to check if proven, etc.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **statement**  
  *Type:* scalar, *Datatype:* string  
  
- **result_type**  
  *Type:* scalar, *Datatype:* string  
  
- **proof_type**  
  *Type:* scalar, *Datatype:* string  
  
- **derivation_steps**  
  *Type:* scalar, *Datatype:* json  
  
- **depends_on**  
  *Type:* scalar, *Datatype:* json  
  


### Aggregations
- **is_proven**  
  *Description:* Yes/no aggregator verifying the proof steps are recognized as valid. Implementation is conceptual.  
  *Formula:* `ValidateProof(derivation_steps)`
- **is_trivial_proof**  
  *Description:* Naive aggregator: if proof is extremely short, we label it 'trivial'.  
  *Formula:* `IF LENGTH(derivation_steps) <= 2 THEN true ELSE false`
- **complexity_estimate**  
  *Description:* A naive measure of proof complexity, e.g. # of steps or references in derivation_steps.  
  *Formula:* `LENGTH(derivation_steps)`
- **reference_count**  
  *Description:* How many distinct external references or theorems appear in 'depends_on'.  
  *Formula:* `IF depends_on != null THEN LENGTH(depends_on) ELSE 0`
- **dependency_depth**  
  *Description:* Longest chain of nested depends_on references leading to axioms or base statements.  
  *Formula:* `ComputeDependencyDepth(this.id)`
- **is_axiom**  
  *Description:* Returns true if result_type or proof_type indicates an axiom, or forcibly accepted with no dependencies.  
  *Formula:* `CheckIfAxiom(this.result_type, this.proof_type, this.depends_on)`
- **references_in_proof**  
  *Description:* Parses derivation_steps to locate any cited references or external theorems.  
  *Formula:* `ExtractReferences(derivation_steps)`
- **use_of_contradiction**  
  *Description:* Checks if proof uses a contradiction approach (assume ¬p => derive false).  
  *Formula:* `DetectProofByContradiction(derivation_steps)`
- **statement_similarity_score**  
  *Description:* Compares proposition statement to known library, returns similarity measure [0..1].  
  *Formula:* `ComputeStatementSimilarity(this.statement)`
- **is_equivalence_statement**  
  *Description:* True if statement has the form p <-> q or is logically a biconditional.  
  *Formula:* `CheckBiconditional(statement)`
- **requires_choice_axiom**  
  *Description:* Heuristic aggregator to see if the proof steps rely on the Axiom of Choice.  
  *Formula:* `DetectAxiomOfChoiceUsage(derivation_steps)`
- **equivalent_statements_list**  
  *Description:* Search for other Proposition statements that appear logically equivalent (p ⇔ q). Returns an array or null.  
  *Formula:* `ComputeEquivalentPropositions(this.id)`
- **used_logical_axioms_list**  
  *Description:* Parses derivation_steps to detect references to standard logical axioms or proof rules.  
  *Formula:* `ScanProofForLogicalAxioms(derivation_steps)`
- **corollary_generation_suggestions**  
  *Description:* Heuristic aggregator: suggests corollaries or immediate consequences that might be proven from this proposition.  
  *Formula:* `ComputePotentialCorollaries(this.id)`

### Lambdas
- **remove_dependency**
  (Parameters: prop_id)  
  *Formula:* `UpdateDependsOn(this.id, prop_id, 'remove')`
- **mark_proof_as_complete**
    
  *Formula:* `ValidateAndFinalizeProof(this.id)`
- **apply**
  (Parameters: context)  
  *Formula:* `ApplyProposition(this, context)`
- **apply_to_equation**
  (Parameters: equation_id)  
  *Formula:* `AttemptUnification(this.statement, LOOKUP(equation_id).equation_text)`


---

## Entity: Equation

**Description**: A symbolic expression representing an equality or functional relationship (polynomial, differential eqn, wave eqn, etc.). Useful in advanced math or cross-domain usage.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **equation_text**  
  *Type:* scalar, *Datatype:* string  
  
- **latex_repr**  
  *Type:* scalar, *Datatype:* string  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **related_sets**  
  *Type:* scalar, *Datatype:* json  
  
- **is_polynomial**  
  *Type:* rollup, *Datatype:*   
  


### Aggregations
- **is_linear_equation**  
  *Description:* Examines if the equation is linear in its variables. E.g. 'ax + b=0'.  
  *Formula:* `CheckIfLinear(equation_text)`
- **is_polynomial**  
  *Description:* Examines equation_text to see if it’s a polynomial equation in standard variables, e.g. a1*x^n + ... = 0.  
  *Formula:* `CheckIfPolynomial(equation_text)`
- **degree**  
  *Description:* If the equation is a polynomial, returns the highest exponent found. Otherwise null.  
  *Formula:* `IF (is_polynomial) THEN DeterminePolynomialDegree(equation_text) ELSE null`
- **discriminant**  
  *Description:* If polynomial is quadratic, returns b^2 - 4ac or the appropriate generalization. Else null.  
  *Formula:* `IF (degree=2) THEN ComputeQuadraticDiscriminant(equation_text) ELSE null`
- **num_variables**  
  *Description:* Counts distinct variable symbols used in equation_text, e.g. {x, y, z}.  
  *Formula:* `ParseVariables(equation_text).length`
- **is_homogeneous_polynomial**  
  *Description:* True if polynomial and every term has the same total degree. Else false or null.  
  *Formula:* `CheckHomogeneity(equation_text)`
- **root_count**  
  *Description:* If domain is finite, count how many assignments satisfy the equation. Otherwise null or partial.  
  *Formula:* `CountFiniteSolutions(equation_text, related_sets)`
- **is_solvable_by_radicals**  
  *Description:* Checks if polynomial degree ≤4 for symbolic solutions. True/false/unknown.  
  *Formula:* `DetermineSolvabilityByRadicals(equation_text)`
- **symmetry_detection**  
  *Description:* Identifies which variables can be permuted without changing the equation’s form.  
  *Formula:* `AnalyzeEquationSymmetry(equation_text)`
- **dimension_of_solution_space**  
  *Description:* For linear equations, estimates dimension of solution set. Implementation is conceptual.  
  *Formula:* `ComputeSolutionSpaceDimension(equation_text, related_sets)`
- **definite_integral**  
  *Description:* For single-var real eqn, attempts ∫ f(x) dx from a to b if specified somewhere.  
  *Formula:* `IF (is_polynomial AND domain=ℝ) THEN EvaluateDefIntegral(equation_text, bounds) ELSE null`
- **leading_coefficient**  
  *Description:* If polynomial, returns the coefficient of highest-degree term.  
  *Formula:* `IF is_polynomial THEN GetLeadingCoefficient(equation_text) ELSE null`
- **evaluate_for_naturals**  
  *Description:* If related_sets includes ℕ, evaluates eqn for n=0..some range, collecting results or solutions.  
  *Formula:* `IF 'naturals' in related_sets THEN EvaluateEqnOverRange(equation_text, n=0..10) ELSE null`
- **integer_solutions_count**  
  *Description:* Counts how many integer solutions exist if feasible. Implementation conceptual.  
  *Formula:* `IF (related_sets includes 'integers') THEN CountIntegerSolutions(equation_text) ELSE null`
- **solutions_mod_n**  
  *Description:* Enumerates or counts solutions modulo a given n if the equation is integer-based. Implementation conceptual.  
  *Formula:* `IF (related_sets includes 'integers') THEN SolveModN(equation_text, n) ELSE null`
- **numerical_solution_count**  
  *Description:* Estimates how many numeric solutions exist (finite/infinite) or returns null if unknown.  
  *Formula:* `AttemptNumericSolve(equation_text, related_sets)`
- **dominant_term**  
  *Description:* Identifies which term in the equation (polynomial or rational form) dominates as |x|→∞. Null if not polynomial-like.  
  *Formula:* `FindDominantTerm(equation_text)`
- **evaluate_at_infinity**  
  *Description:* Evaluates or approximates the limit of LHS (and possibly RHS) as x→∞/-∞. Returns symbolic or numeric result.  
  *Formula:* `CheckLimitAtInfinity(equation_text)`
- **coefficient_vector**  
  *Description:* For polynomial equations, extracts the list of coefficients in standard form, e.g. x^3+4x-7 => [1,0,4,-7]. Null otherwise.  
  *Formula:* `IF (is_polynomial) THEN ParsePolynomialCoefficients(equation_text) ELSE null`

### Lambdas
- **solve_equation**
  (Parameters: var_list)  
  *Formula:* `ApplySymbolicSolver(equation_text, var_list)`
- **simplify_equation**
    
  *Formula:* `SymbolicallySimplify(equation_text)`
- **partial_derivative**
  (Parameters: var_name)  
  *Formula:* `ComputePartialDerivative(equation_text, var_name)`


---

## Entity: Category

**Description**: Captures objects and morphisms in category theory. May store them as references to sets, functions, or other structures. Aggregators check composition closure, identity morphisms, etc.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **objects**  
  *Type:* scalar, *Datatype:* json  
  
- **morphisms**  
  *Type:* scalar, *Datatype:* json  
  


### Aggregations
- **is_small**  
  *Description:* Naive aggregator to see if the category is 'small' (if the class of objects is a set).  
  *Formula:* `CheckIfObjectCollectionIsSetSized(objects)`
- **num_morphisms**  
  *Description:* A count aggregator for how many morphisms (arrows) are declared in this Category.  
  *Formula:* `COUNT(morphisms) // or sum of their definitions if morphisms is array-like`
- **has_zero_object**  
  *Description:* Detects if there’s an object that is both initial and terminal. For each object, check if it’s unique that all morphisms come from/to it in exactly one way. Returns true if found.  
  *Formula:* `Search objects => find candidate that’s both initial_object & terminal_object => if found => true else false`
- **has_zero_object**  
  *Description:* Detects if there’s an object that is both initial and terminal. For each object, check if it’s unique that all morphisms come from/to it in exactly one way. Returns true if found.  
  *Formula:* `Search objects => find candidate that’s both initial_object & terminal_object => if found => true else false`
- **object_count**  
  *Description:* Number of declared objects in the category.  
  *Formula:* `COUNT(objects)`
- **morphism_count**  
  *Description:* Number of declared morphisms in the category (summing if 'morphisms' is an object map).  
  *Formula:* `IF (morphisms is array) THEN COUNT(morphisms) ELSE SUM(LENGTH(morphisms))`
- **has_initial_object**  
  *Description:* Checks if there's an object I s.t. there's exactly one morphism from I to any object in the category.  
  *Formula:* `For each candidate I in objects => check uniqueness of morphisms(I -> X) for all X`
- **has_binary_products**  
  *Description:* Checks if a product object exists for every pair of objects, with suitable projection morphisms.  
  *Formula:* `CheckBinaryProducts(objects, morphisms)`
- **has_equalizers**  
  *Description:* Checks if for all parallel morphisms f,g an equalizer object and morphism exist.  
  *Formula:* `CheckEqualizers(objects, morphisms)`
- **distinct_object_pairs_count**  
  *Description:* Counts ordered pairs (A,B) of distinct objects in the category. Implementation is straightforward.  
  *Formula:* `ComputeDistinctObjectPairs(objects)`
- **functor_count**  
  *Description:* How many known Functor definitions originate from this category to others.  
  *Formula:* `CountFunctorsFromThisCategory(this.id)`
- **object_isomorphism_pairs_count**  
  *Description:* Counts pairs of objects (A,B) that are isomorphic. Implementation conceptual.  
  *Formula:* `CountIsomorphicObjectPairs(objects, morphisms)`
- **terminal_object_count**  
  *Description:* Counts how many objects T have exactly one morphism from every other object.  
  *Formula:* `CountTerminalObjects(objects, morphisms)`
- **exponential_objects_check**  
  *Description:* Checks if the category has exponentials B^A for all A,B, with evaluation morphism.  
  *Formula:* `ScanForExponentialObjects(this.id)`
- **number_of_endofunctors**  
  *Description:* Counts all functors from this category to itself in the stored data.  
  *Formula:* `CountEndofunctors(this.id)`
- **auto_equivalences_count**  
  *Description:* Counts how many equivalences of categories from this cat to itself.  
  *Formula:* `IdentifyAutoEquivalences(this.id)`
- **has_pullbacks**  
  *Description:* Checks if every diagram has a pullback object and morphisms. Implementation conceptual.  
  *Formula:* `AnalyzePullbacks(objects, morphisms)`
- **has_pushouts**  
  *Description:* Checks if every cospan has a pushout object and morphisms. Implementation conceptual.  
  *Formula:* `AnalyzePushouts(objects, morphisms)`
- **is_cartesian_closed**  
  *Description:* Verifies if the category has exponentials B^A with the usual universal property. Implementation conceptual.  
  *Formula:* `CheckCartesianClosedProperty(this.id)`
- **automorphism_count**  
  *Description:* Counts isomorphisms object->itself across all objects, summing for a total number of 'auto' morphisms in this category.  
  *Formula:* `ComputeCategoryAutomorphisms(this.id)`
- **inverse_morphism_count**  
  *Description:* Counts how many morphisms are invertible. Implementation conceptual, scanning morphisms for isomorphisms.  
  *Formula:* `CountInvertibleMorphisms(morphisms)`
- **endofunction_count**  
  *Description:* If objects are sets, counts how many endofunctions exist for each object f: A->A, summing across the category. Null if infinite.  
  *Formula:* `Sum(For each Obj in objects => |Obj|^|Obj|) // conceptual`
- **functor_composition_closure_check**  
  *Description:* Verifies that if functor F: Cat->Cat2 and G: Cat2->Cat3 exist, the composition G∘F is recognized as a functor as well.  
  *Formula:* `CheckFunctorComposition(this.id)`

### Lambdas
- **functor**
  (Parameters: target_category_id)  
  *Formula:* `ConstructFunctor(this, LOOKUP(target_category_id))`
- **has_terminal_object**
    
  *Formula:* `Scan objects => find candidate T => check for unique arrow from each object => T`

### Constraints
- **composition_closed**  
  *Formula:* `CheckCompositionClosure(morphisms)`  
  *Error Message:* Category must be closed under morphism composition.

---


