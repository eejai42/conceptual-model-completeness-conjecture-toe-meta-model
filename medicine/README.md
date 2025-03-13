# Medicine & Healthcare ToE Meta-Model
## A Declarative Framework for Modeling Medical Data and Healthcare Processes

A unified meta-model capturing the foundational aspects of medicine and healthcare, including patient records, clinical trial data, treatment plans, and healthcare analytics.

**Date**: March 2025
**Domain Identifier**: CMCC_ToEMM_Medicine

### Authors
- **EJ Alexandra** <start@anabstractlevel.com>  
  Affiliations: SSoT.me, EffortlessAPI.com

### Abstract
This meta-model provides a syntax‐free, declarative representation for medicine and healthcare systems. It encodes patient records, conditions, symptoms, treatment plans, clinical trial data, lab results, and vital signs using the five fundamental primitives: Schema, Data, Lookups, Aggregations, and Lambda Calculated Fields.

![Medicine & Healthcare ToE Meta-Model Entity Diagram](medicine.png)


### Key Points
- Enables a syntax‐free representation of medical and healthcare data.
- Unifies patient records, clinical analytics, and treatment workflows within an Snapshot-Consistent environment.
- Facilitates risk assessment and predictive modeling via declarative calculated fields.
- Bridges clinical, laboratory, and treatment data for comprehensive healthcare management.

### Implications
- Reduces redundancy and semantic drift in healthcare systems.
- Supports rapid, no-code customization and integration across platforms.
- Improves decision support through transparent and unified analytics.

### Narrative

---

# Schema Overview

## Entity: Patient

**Description**: Represents a patient in the healthcare system.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **date_of_birth**  
  *Type:* scalar, *Datatype:* date  
  
- **gender**  
  *Type:* scalar, *Datatype:* string  
  
- **contact_information**  
  *Type:* scalar, *Datatype:* json  
  
- **medical_history**  
  *Type:* scalar, *Datatype:* json  
  

### Lookups
- **conditions**  
  *Target Entity:* Condition, *Type:* one_to_many  
    
  (Join condition: **Condition.patient_id = this.id**)  
  *Description:* Medical conditions diagnosed for the patient.
- **treatment_plans**  
  *Target Entity:* TreatmentPlan, *Type:* one_to_many  
    
  (Join condition: **TreatmentPlan.patient_id = this.id**)  
  *Description:* Treatment plans prescribed for the patient.
- **lab_results**  
  *Target Entity:* LabResult, *Type:* one_to_many  
    
  (Join condition: **LabResult.patient_id = this.id**)  
  *Description:* Lab test results for the patient.
- **vital_signs**  
  *Target Entity:* VitalSign, *Type:* one_to_many  
    
  (Join condition: **VitalSign.patient_id = this.id**)  
  *Description:* Vital sign measurements.

### Aggregations
- **age**  
  *Description:* Calculates the patient's current age.  
  *Formula:* `ComputeAge(date_of_birth)`
- **number_of_conditions**  
  *Description:* Counts the number of diagnosed conditions.  
  *Formula:* `COUNT(conditions)`

### Lambdas
- **risk_assessment**
    
  *Formula:* `ComputeRisk(conditions, lab_results, vital_signs)`

### Constraints
- **valid_date_of_birth**  
  *Formula:* `date_of_birth < CURRENT_DATE`  
  *Error Message:* Date of birth must be in the past.

---

## Entity: Condition

**Description**: Represents a diagnosed medical condition for a patient.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **patient_id**  
  *Type:* lookup, *Datatype:*   
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **diagnosis_date**  
  *Type:* scalar, *Datatype:* date  
  
- **severity**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **symptoms**  
  *Target Entity:* Symptom, *Type:* one_to_many  
    
  (Join condition: **Symptom.condition_id = this.id**)  
  *Description:* Symptoms associated with the condition.
- **treatment_plans**  
  *Target Entity:* TreatmentPlan, *Type:* one_to_many  
    
  (Join condition: **TreatmentPlan.condition_id = this.id**)  
  *Description:* Treatment plans addressing the condition.

### Aggregations
- **duration_since_diagnosis**  
  *Description:* Time elapsed since diagnosis.  
  *Formula:* `ComputeDuration(diagnosis_date, CURRENT_DATE)`



---

## Entity: Symptom

**Description**: Represents a symptom experienced by a patient, linked to a condition.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **condition_id**  
  *Type:* lookup, *Datatype:*   
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **onset_date**  
  *Type:* scalar, *Datatype:* date  
  





---

## Entity: TreatmentPlan

**Description**: Represents a treatment plan prescribed for a specific condition.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **patient_id**  
  *Type:* lookup, *Datatype:*   
  
- **condition_id**  
  *Type:* lookup, *Datatype:*   
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **start_date**  
  *Type:* scalar, *Datatype:* date  
  
- **end_date**  
  *Type:* scalar, *Datatype:* date  
  
- **medications**  
  *Type:* scalar, *Datatype:* json  
  
- **procedures**  
  *Type:* scalar, *Datatype:* json  
  


### Aggregations
- **treatment_duration**  
  *Description:* Calculates the duration of the treatment plan.  
  *Formula:* `ComputeDuration(start_date, end_date)`

### Lambdas
- **update_plan**
  (Parameters: new_details)  
  *Formula:* `Merge(this, new_details)`


---

## Entity: ClinicalTrial

**Description**: Represents a clinical trial study for testing medical interventions.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **trial_name**  
  *Type:* scalar, *Datatype:* string  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **start_date**  
  *Type:* scalar, *Datatype:* date  
  
- **end_date**  
  *Type:* scalar, *Datatype:* date  
  
- **phase**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **enrolled_patients**  
  *Target Entity:* Patient, *Type:* many_to_many  
    
  (Join condition: **Enrollment.trial_id = this.id**)  
  *Description:* Patients enrolled in this trial.

### Aggregations
- **number_of_patients**  
  *Description:* Counts the number of enrolled patients.  
  *Formula:* `COUNT(enrolled_patients)`



---

## Entity: LabResult

**Description**: Represents a laboratory test result for a patient.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **patient_id**  
  *Type:* lookup, *Datatype:*   
  
- **test_name**  
  *Type:* scalar, *Datatype:* string  
  
- **result_value**  
  *Type:* scalar, *Datatype:* float  
  
- **unit**  
  *Type:* scalar, *Datatype:* string  
  
- **test_date**  
  *Type:* scalar, *Datatype:* date  
  


### Aggregations
- **average_result**  
  *Description:* Average value of the test result.  
  *Formula:* `AVERAGE(result_value)`



---

## Entity: VitalSign

**Description**: Represents a vital sign measurement for a patient.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **patient_id**  
  *Type:* lookup, *Datatype:*   
  
- **type**  
  *Type:* scalar, *Datatype:* string  
  
- **value**  
  *Type:* scalar, *Datatype:* float  
  
- **unit**  
  *Type:* scalar, *Datatype:* string  
  
- **measurement_date**  
  *Type:* scalar, *Datatype:* date  
  


### Aggregations
- **average_vital**  
  *Description:* Average measurement value for the vital sign.  
  *Formula:* `AVERAGE(value)`



---