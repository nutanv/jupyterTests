# Enterprise Risk Management Matrix

## Interactive, Graph-Native, Auditor-Certifiable ERM System

This repository contains a comprehensive Enterprise Risk Management (ERM) system that is:
- **Graph-native** with formal ontology and relationships
- **Auditor-certifiable** with evidence trails and test procedures
- **Architect-usable** with platform/environment abstractions
- **Executive-readable** with interactive visualizations

## ⚠️ Critical Warning

**This system uses internal organizational data.** All risks, controls, implementations, and mappings provided are templates and MUST be validated against your organization's actual:

- Enterprise risk registers
- IT risk assessments
- Security architecture documents
- Policies and standards
- Cloud landing zone designs
- Tooling inventories
- Configuration baselines
- Audit workpapers
- Prior certifications
- Incident reports
- Regulatory interpretations

**DO NOT use this system in production without validating all data against authoritative internal sources.**

## Features

### 1. Graph Ontology
Defines and uses the following node types:
- Enterprise Risk
- IT Risk
- Information Security Risk
- Security Risk Category
- Risk Statement
- Control Objective
- Control
- Technical Control Implementation
- Evidence Artifact
- Regulation / Standard
- Role / Accountability
- Platform
- Operating Environment

### 2. Risk Decomposition
- Starts at Enterprise Risk Management (COSO ERM / ISO 31000)
- Decomposes into IT Risk Management
- Further decomposes into Information Security Risk
- Categorizes into 9 Security Risk Categories:
  1. Identity & Access Governance Risk
  2. Undetected Use of Credentials Risk
  3. Cloud Control Plane Risk
  4. Data Security & Privacy Risk
  5. Workload & Non-Human Identity Risk
  6. Endpoint & Device Security Risk
  7. Network & Connectivity Risk
  8. Detection, Response & Recovery Risk
  9. Third-Party & SaaS Integration Risk

### 3. Control Framework
Each control includes:
- Control ID, Name, and Objective
- Control Type (Preventive / Detective / Responsive)
- Control Category (Administrative / Technical / Physical)
- Automation Level
- Frequency
- Failure Mode
- Risk(s) mitigated
- Control Owner role

### 4. Platform Abstraction
Controls are defined platform-agnostically, then mapped to specific implementations for:

**Platforms:**
- Azure
- AWS
- GCP
- Oracle Cloud Infrastructure (OCI)
- On-Premises

**Operating Environments:**
- Windows
- Linux
- macOS
- Mobile (iOS / Android)

### 5. Evidence & Auditability
For each technical control implementation:
- Evidence Type
- Evidence Source System
- Evidence Location
- Retention Period
- Audit Test Procedure
- Test Frequency
- Control Effectiveness criteria

### 6. Regulatory Mapping
Controls mapped to:
- ISO 27001 (Annex A)
- PCI DSS v4.0
- SOC 2 Trust Services Criteria
- HIPAA Security Rule
- SOX IT General Controls
- GDPR Articles
- DORA ICT Risk & Resilience requirements

### 7. Interactive Capabilities
- Graph visualization with filtering
- Risk heatmaps (inherent vs. residual)
- Control analytics dashboards
- Regulatory coverage charts
- Platform/Environment selection with dynamic filtering
- Regulation-based filtering for audit purposes

## Installation

### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab

### Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd jupyterTests
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Launch Jupyter:
```bash
jupyter notebook
```

5. Open `Enterprise_Risk_Management_Matrix.ipynb`

## Usage

### For Executives
Run the notebook and view:
- Risk heatmaps showing risk reduction
- Control analytics dashboards
- Regulatory coverage charts
- High-level gap analysis

### For Risk Managers
Use the interactive dashboard to:
- Filter risks by category
- View controls by risk rating
- Track risk treatment progress
- Identify control gaps

### For Security Architects
Filter by platform (Azure, AWS, GCP, OCI, On-Prem) to:
- See exact technical implementations
- Review configuration baselines
- Identify tooling requirements
- Plan security architecture changes

### For Auditors
Filter by regulation (ISO 27001, PCI DSS, SOC 2, etc.) to:
- See all mapped controls
- Access evidence locations
- Review test procedures
- Assess control effectiveness

### For Compliance Teams
Generate reports showing:
- Regulatory coverage by framework
- Control-to-requirement mappings
- Evidence collection requirements
- Gap analysis by regulation

## File Structure

```
.
├── Enterprise_Risk_Management_Matrix.ipynb  # Main interactive notebook
├── erm_ontology.py                          # Graph ontology definitions
├── erm_data_model.py                        # Complete data model
├── matrix_generator.py                      # Matrix generation and export
├── erm_visualizer.py                        # Interactive visualizations
├── requirements.txt                         # Python dependencies
├── README.md                                # This file
└── .gitignore                               # Git ignore rules
```

## Output Artifacts

The system generates:

1. **ERM_Matrix_Complete.xlsx** - Multi-sheet Excel workbook containing:
   - Complete integrated matrix
   - Risk-Control mappings
   - Control-Compliance mappings
   - Technical implementations
   - Evidence artifacts
   - Gap analysis

2. **erm_graph.json** - Graph structure in JSON format for:
   - External visualization tools
   - Graph database imports
   - Integration with other systems

3. **filter_metadata.json** - Metadata for interactive filtering:
   - Platform options
   - Operating environment options
   - Regulation options
   - Risk rating values
   - Control types and categories

## Validation

The notebook includes built-in validation checks:
- ✓ Risk hierarchy completeness
- ✓ Formal risk statement structure
- ✓ Risk-to-control coverage
- ✓ Platform implementation coverage
- ✓ Evidence artifact existence
- ✓ Regulatory mapping completeness
- ✓ Graph connectivity

## Customization

### Adding New Risks
1. Edit `erm_data_model.py`
2. Add risk statement in `define_risk_statements()`
3. Follow the format: Cause → Risk Event → Business Impact
4. Specify inherent and residual ratings

### Adding New Controls
1. Edit `erm_data_model.py`
2. Add control in `define_controls()`
3. Specify all required metadata
4. Link to risks mitigated

### Adding Platform Implementations
1. Edit `erm_data_model.py`
2. Add implementation in `define_platform_implementations()`
3. Specify platform, environment, and tooling
4. Reference actual configuration baselines

### Adding Evidence Artifacts
1. Edit `erm_data_model.py`
2. Add evidence in `define_evidence_artifacts()`
3. Specify evidence location and test procedures
4. Define effectiveness criteria

### Adding Regulatory Mappings
1. Edit `erm_data_model.py`
2. Add mapping in `define_regulatory_mappings()`
3. Specify requirement ID and description
4. Provide applicability rationale

## Gap Analysis

The system automatically identifies:
- Controls without implementations
- Implementations without evidence
- Controls without regulatory mappings
- Risks without controls
- Weak controls (manual, low automation)

Address these gaps to achieve full certification readiness.

## Maintenance Schedule

Recommended maintenance activities:

**Quarterly:**
- Risk reassessment
- Control effectiveness spot checks
- Evidence collection verification

**Semi-Annual:**
- Comprehensive control testing
- Platform implementation updates
- Regulatory mapping review

**Annual:**
- Complete risk reassessment
- Full control effectiveness testing
- External audit preparation
- Framework updates (ISO, PCI, etc.)

**Continuous:**
- Evidence artifact collection
- Configuration baseline monitoring
- Incident-driven risk updates
- New platform/service onboarding

## Support and Contributions

This is an internal organizational tool. All modifications should be:
- Approved by Risk Committee
- Reviewed by CISO
- Validated by Audit & Compliance
- Documented in change log

## License

See LICENSE file for details.

## Disclaimer

This ERM system provides a framework and template. Organizations are responsible for:
- Validating all data against internal sources
- Ensuring compliance with applicable regulations
- Maintaining evidence and documentation
- Conducting regular risk assessments
- Testing control effectiveness
- Updating the system as changes occur

**NO GUARANTEES:** This system does not guarantee regulatory compliance or audit success. Professional judgment and validation are required.
