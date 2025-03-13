# Cybersecurity ToE Meta-Model

A unified meta-model capturing cybersecurity aspects including threat models, vulnerabilities, IT asset mappings, incident logs, security audits, and patches, using a declarative, Snapshot-Consistent approach.


## Metadata

**Title**: CMCC Complete Cybersecurity ToE Meta-Model  
**Subtitle**: A Declarative Framework for Cybersecurity Data and Rule Management  
**Date**: March 2025
**Domain Identifier**: CMCC_ToEMM_Cybersecurity

### Authors
- **EJ Alexandra** <start@anabstractlevel.com>  
  Affiliations: SSoT.me, EffortlessAPI.com

### Abstract
This meta-model enables a syntax‐free declarative representation of cybersecurity systems. It captures threat models, vulnerabilities, IT asset mappings, incident logs, security audits, and patches. Key computed fields include risk prioritization scoring and anomaly detection indicators.

![Cybersecurity ToE Meta-Model entity diagram](cybersecurity.png)

### Key Points
- Represents cybersecurity data using five primitives: Schema, Data, Lookups, Aggregations, and Calculated Fields.
- Integrates threat models, vulnerabilities, and IT asset mapping with incident and audit data.
- Provides computed risk scores and anomaly indicators to support dynamic security assessments.

### Implications
- Facilitates rapid, consistent security analysis across heterogeneous IT environments.
- Reduces complexity and semantic drift via Snapshot-Consistent, syntax‐free models.
- Enables automated risk prioritization and real-time anomaly detection.

### Narrative

---

# Schema Overview

## Entity: ThreatModel

**Description**: Represents a conceptual model of potential threats against IT assets.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **asset_scope**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **vulnerabilities**  
  *Target Entity:* Vulnerability, *Type:* one_to_many  
    
  (Join condition: **Vulnerability.threat_model_id = this.id**)  
  *Description:* List of vulnerabilities associated with this threat model.

### Aggregations
- **vulnerability_count**  
  *Description:* Counts the number of associated vulnerabilities.  
  *Formula:* `COUNT(vulnerabilities)`



---

## Entity: Vulnerability

**Description**: Represents a vulnerability or weakness in an IT asset.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **threat_model_id**  
  *Type:* lookup, *Datatype:*   
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **severity**  
  *Type:* scalar, *Datatype:* string  
  
- **CVE_id**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **patches**  
  *Target Entity:* Patch, *Type:* one_to_many  
    
  (Join condition: **Patch.vulnerability_id = this.id**)  
  *Description:* Patches addressing this vulnerability.

### Aggregations
- **vulnerability_score**  
  *Description:* Calculated risk score based on severity.  
  *Formula:* `ComputeVulnScore(severity)`



---

## Entity: ITAsset

**Description**: Represents an IT asset such as servers, endpoints, or network devices.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **name**  
  *Type:* scalar, *Datatype:* string  
  
- **asset_type**  
  *Type:* scalar, *Datatype:* string  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  

### Lookups
- **vulnerabilities**  
  *Target Entity:* Vulnerability, *Type:* one_to_many  
    
  (Join condition: **Vulnerability.it_asset_id = this.id**)  
  *Description:* Vulnerabilities affecting the asset.
- **incidents**  
  *Target Entity:* Incident, *Type:* one_to_many  
    
  (Join condition: **Incident.it_asset_id = this.id**)  
  *Description:* Security incidents associated with the asset.

### Aggregations
- **risk_score**  
  *Description:* Calculated overall risk score for the asset.  
  *Formula:* `ComputeAssetRisk(vulnerabilities, incidents)`



---

## Entity: Incident

**Description**: Represents a recorded security incident or intrusion detection event.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **it_asset_id**  
  *Type:* lookup, *Datatype:*   
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **incident_date**  
  *Type:* scalar, *Datatype:* datetime  
  
- **type**  
  *Type:* scalar, *Datatype:* string  
  
- **severity**  
  *Type:* scalar, *Datatype:* string  
  


### Aggregations
- **anomaly_indicator**  
  *Description:* Indicator of anomalous behavior based on incident characteristics.  
  *Formula:* `ComputeAnomalyIndicator(severity, incident_date)`



---

## Entity: SecurityAudit

**Description**: Represents a security audit or assessment of IT systems.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **audit_date**  
  *Type:* scalar, *Datatype:* datetime  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  
- **results**  
  *Type:* scalar, *Datatype:* json  
  


### Aggregations
- **audit_score**  
  *Description:* Score based on audit findings.  
  *Formula:* `ComputeAuditScore(results)`



---

## Entity: Patch

**Description**: Represents a patch or remediation applied to address a vulnerability.

### Fields
- **id**  
  *Type:* scalar, *Datatype:* string  
  
- **vulnerability_id**  
  *Type:* lookup, *Datatype:*   
  
- **patch_date**  
  *Type:* scalar, *Datatype:* datetime  
  
- **description**  
  *Type:* scalar, *Datatype:* string  
  





---


