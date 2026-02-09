"""
Enterprise Risk Management Data Model
======================================
This module defines the complete data model including risks, controls, 
platforms, and regulatory mappings.

NOTE: This uses internal organizational data. All risks, controls, 
and mappings should be validated against internal risk registers, 
security architecture documents, and compliance documentation.
"""

from typing import List, Dict
from erm_ontology import (
    RiskStatement, Control, TechnicalImplementation, 
    EvidenceArtifact, RegulatoryMapping, ERMGraph, GraphNode, GraphEdge
)


# PLATFORMS
PLATFORMS = {
    "AZURE": "Azure",
    "AWS": "AWS",
    "GCP": "GCP",
    "OCI": "Oracle Cloud Infrastructure (OCI)",
    "ON_PREM": "On-Premises"
}

# OPERATING ENVIRONMENTS
OPERATING_ENVIRONMENTS = {
    "WINDOWS": "Windows",
    "LINUX": "Linux",
    "MACOS": "macOS",
    "MOBILE_IOS": "Mobile (iOS)",
    "MOBILE_ANDROID": "Mobile (Android)"
}

# ORGANIZATIONAL ROLES
ROLES = {
    "BOARD_RISK_COMMITTEE": "Board / Risk Committee",
    "CISO": "Chief Information Security Officer (CISO)",
    "CIO": "Chief Information Officer (CIO)",
    "RISK_MANAGER": "Risk Manager",
    "SOC": "Security Operations Center (SOC)",
    "CLOUD_PLATFORM_TEAM": "Cloud Platform Team",
    "AUDIT_COMPLIANCE": "Audit & Compliance Team",
    "IT_OPERATIONS": "IT Operations",
    "IAM_TEAM": "Identity & Access Management Team",
    "DATA_GOVERNANCE": "Data Governance Team"
}

# REGULATIONS
REGULATIONS = {
    "ISO_27001": "ISO 27001:2022",
    "PCI_DSS": "PCI DSS v4.0",
    "SOC_2": "SOC 2 Trust Services Criteria",
    "HIPAA": "HIPAA Security Rule",
    "SOX": "SOX IT General Controls",
    "GDPR": "GDPR",
    "DORA": "DORA ICT Risk & Resilience"
}

# SECURITY RISK CATEGORIES (from problem statement)
SECURITY_RISK_CATEGORIES = [
    "Identity & Access Governance Risk",
    "Undetected Use of Credentials Risk",
    "Cloud Control Plane Risk",
    "Data Security & Privacy Risk",
    "Workload & Non-Human Identity Risk",
    "Endpoint & Device Security Risk",
    "Network & Connectivity Risk",
    "Detection, Response & Recovery Risk",
    "Third-Party & SaaS Integration Risk"
]


class ERMDataModel:
    """
    Enterprise Risk Management Data Model
    
    This class constructs the complete ERM graph with all nodes and relationships.
    """
    
    def __init__(self):
        self.graph = ERMGraph()
        self.risks: List[RiskStatement] = []
        self.controls: List[Control] = []
        self.implementations: List[TechnicalImplementation] = []
        self.evidence_artifacts: List[EvidenceArtifact] = []
        self.regulatory_mappings: List[RegulatoryMapping] = []
        
    def build_risk_taxonomy(self):
        """Build the risk decomposition hierarchy"""
        
        # Level 1: Enterprise Risk
        enterprise_risk = GraphNode(
            node_id="RISK-L1-001",
            node_type="Enterprise Risk",
            attributes={
                "name": "Enterprise Risk Management",
                "framework": "COSO ERM / ISO 31000",
                "description": "Top-level enterprise risk management framework"
            }
        )
        self.graph.add_node(enterprise_risk)
        
        # Level 2: IT Risk
        it_risk = GraphNode(
            node_id="RISK-L2-001",
            node_type="IT Risk",
            attributes={
                "name": "IT Risk Management",
                "description": "Information Technology risk domain"
            }
        )
        self.graph.add_node(it_risk)
        
        # Relationship: Enterprise Risk decomposes into IT Risk
        self.graph.add_edge(GraphEdge(
            edge_id="REL-001",
            source_node_id="RISK-L1-001",
            target_node_id="RISK-L2-001",
            relationship_type="decomposes_into"
        ))
        
        # Level 3: Information Security Risk
        infosec_risk = GraphNode(
            node_id="RISK-L3-001",
            node_type="Information Security Risk",
            attributes={
                "name": "Information Security Risk",
                "description": "Information security and cyber risk domain"
            }
        )
        self.graph.add_node(infosec_risk)
        
        # Relationship: IT Risk decomposes into Information Security Risk
        self.graph.add_edge(GraphEdge(
            edge_id="REL-002",
            source_node_id="RISK-L2-001",
            target_node_id="RISK-L3-001",
            relationship_type="decomposes_into"
        ))
        
        # Level 4: Security Risk Categories
        edge_id_counter = 3
        for idx, category in enumerate(SECURITY_RISK_CATEGORIES, 1):
            category_node = GraphNode(
                node_id=f"RISK-L4-{idx:03d}",
                node_type="Security Risk Category",
                attributes={
                    "name": category,
                    "description": f"{category} category"
                }
            )
            self.graph.add_node(category_node)
            
            # Relationship: Information Security Risk decomposes into category
            self.graph.add_edge(GraphEdge(
                edge_id=f"REL-{edge_id_counter:03d}",
                source_node_id="RISK-L3-001",
                target_node_id=f"RISK-L4-{idx:03d}",
                relationship_type="decomposes_into"
            ))
            edge_id_counter += 1
    
    def define_risk_statements(self):
        """Define formal risk statements for each security risk category"""
        
        risk_statements = [
            RiskStatement(
                risk_id="RISK-IAG-001",
                cause="Inadequate identity governance and access provisioning processes",
                risk_event="Unauthorized users gain access to sensitive systems or data",
                business_impact="Data breach, regulatory fines, reputational damage",
                inherent_likelihood="High",
                inherent_impact="High",
                inherent_rating="Critical",
                residual_likelihood="Low",
                residual_impact="Medium",
                residual_rating="Low"
            ),
            RiskStatement(
                risk_id="RISK-CRED-001",
                cause="Lack of comprehensive credential monitoring and anomaly detection",
                risk_event="Compromised credentials used without detection",
                business_impact="Unauthorized access, data exfiltration, system compromise",
                inherent_likelihood="High",
                inherent_impact="High",
                inherent_rating="Critical",
                residual_likelihood="Low",
                residual_impact="High",
                residual_rating="Medium"
            ),
            RiskStatement(
                risk_id="RISK-CCP-001",
                cause="Insufficient security controls on cloud management interfaces",
                risk_event="Unauthorized modification of cloud infrastructure configuration",
                business_impact="Service disruption, data loss, security control bypass",
                inherent_likelihood="Medium",
                inherent_impact="High",
                inherent_rating="High",
                residual_likelihood="Low",
                residual_impact="High",
                residual_rating="Medium"
            ),
            RiskStatement(
                risk_id="RISK-DSP-001",
                cause="Inadequate data classification and encryption implementation",
                risk_event="Sensitive data exposed or accessed without authorization",
                business_impact="Privacy violations, regulatory fines, customer trust erosion",
                inherent_likelihood="Medium",
                inherent_impact="High",
                inherent_rating="High",
                residual_likelihood="Low",
                residual_impact="Medium",
                residual_rating="Low"
            ),
            RiskStatement(
                risk_id="RISK-WNH-001",
                cause="Weak management of service accounts and API keys",
                risk_event="Service accounts compromised or misused",
                business_impact="Automated attack propagation, privileged access abuse",
                inherent_likelihood="Medium",
                inherent_impact="High",
                inherent_rating="High",
                residual_likelihood="Low",
                residual_impact="Medium",
                residual_rating="Low"
            ),
            RiskStatement(
                risk_id="RISK-EDS-001",
                cause="Insufficient endpoint security controls and patch management",
                risk_event="Endpoints compromised with malware or exploited vulnerabilities",
                business_impact="Data breach, ransomware, lateral movement in network",
                inherent_likelihood="High",
                inherent_impact="High",
                inherent_rating="Critical",
                residual_likelihood="Medium",
                residual_impact="Medium",
                residual_rating="Medium"
            ),
            RiskStatement(
                risk_id="RISK-NET-001",
                cause="Inadequate network segmentation and access controls",
                risk_event="Unauthorized lateral movement across network segments",
                business_impact="Widespread compromise, difficulty containing incidents",
                inherent_likelihood="Medium",
                inherent_impact="High",
                inherent_rating="High",
                residual_likelihood="Low",
                residual_impact="Medium",
                residual_rating="Low"
            ),
            RiskStatement(
                risk_id="RISK-DRR-001",
                cause="Insufficient security monitoring and incident response capabilities",
                risk_event="Security incidents not detected or responded to in timely manner",
                business_impact="Extended breach duration, increased damage and recovery costs",
                inherent_likelihood="Medium",
                inherent_impact="High",
                inherent_rating="High",
                residual_likelihood="Low",
                residual_impact="Medium",
                residual_rating="Low"
            ),
            RiskStatement(
                risk_id="RISK-TPI-001",
                cause="Inadequate third-party security assessment and monitoring",
                risk_event="Third-party vendor introduces security vulnerability or breach",
                business_impact="Supply chain compromise, data exposure, service disruption",
                inherent_likelihood="Medium",
                inherent_impact="High",
                inherent_rating="High",
                residual_likelihood="Low",
                residual_impact="Medium",
                residual_rating="Low"
            )
        ]
        
        self.risks = risk_statements
        
        # Add risk statements as nodes
        for risk in risk_statements:
            risk_node = GraphNode(
                node_id=risk.risk_id,
                node_type="Risk Statement",
                attributes={
                    "cause": risk.cause,
                    "risk_event": risk.risk_event,
                    "business_impact": risk.business_impact,
                    "inherent_likelihood": risk.inherent_likelihood,
                    "inherent_impact": risk.inherent_impact,
                    "inherent_rating": risk.inherent_rating,
                    "residual_likelihood": risk.residual_likelihood,
                    "residual_impact": risk.residual_impact,
                    "residual_rating": risk.residual_rating
                }
            )
            self.graph.add_node(risk_node)
            
            # Link risk statement to appropriate security risk category
            category_mapping = {
                "RISK-IAG-001": "RISK-L4-001",  # Identity & Access Governance
                "RISK-CRED-001": "RISK-L4-002",  # Undetected Use of Credentials
                "RISK-CCP-001": "RISK-L4-003",   # Cloud Control Plane
                "RISK-DSP-001": "RISK-L4-004",   # Data Security & Privacy
                "RISK-WNH-001": "RISK-L4-005",   # Workload & Non-Human Identity
                "RISK-EDS-001": "RISK-L4-006",   # Endpoint & Device Security
                "RISK-NET-001": "RISK-L4-007",   # Network & Connectivity
                "RISK-DRR-001": "RISK-L4-008",   # Detection, Response & Recovery
                "RISK-TPI-001": "RISK-L4-009"    # Third-Party & SaaS Integration
            }
            
            category_id = category_mapping.get(risk.risk_id)
            if category_id:
                self.graph.add_edge(GraphEdge(
                    edge_id=f"REL-RISK-{risk.risk_id}",
                    source_node_id=category_id,
                    target_node_id=risk.risk_id,
                    relationship_type="decomposes_into"
                ))
    
    def define_controls(self):
        """Define controls and control objectives"""
        
        controls = [
            # Identity & Access Governance Controls
            Control(
                control_id="CTRL-IAM-001",
                control_name="Centralized Identity Management",
                control_objective="Ensure all user identities are managed through centralized identity provider",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Continuous",
                failure_mode="Manual fallback to local authentication",
                risks_mitigated=["RISK-IAG-001"],
                control_owner_role=ROLES["IAM_TEAM"],
                description="All user authentication goes through central IdP with SSO"
            ),
            Control(
                control_id="CTRL-IAM-002",
                control_name="Multi-Factor Authentication (MFA)",
                control_objective="Require MFA for all privileged and remote access",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Per authentication event",
                failure_mode="Access denied if MFA unavailable",
                risks_mitigated=["RISK-IAG-001", "RISK-CRED-001"],
                control_owner_role=ROLES["IAM_TEAM"],
                description="MFA required for all administrative and remote access"
            ),
            Control(
                control_id="CTRL-IAM-003",
                control_name="Privileged Access Management",
                control_objective="Control and monitor privileged account access",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Continuous",
                failure_mode="Access denied if PAM system unavailable",
                risks_mitigated=["RISK-IAG-001", "RISK-CCP-001"],
                control_owner_role=ROLES["IAM_TEAM"],
                description="PAM solution manages privileged accounts with just-in-time access"
            ),
            Control(
                control_id="CTRL-IAM-004",
                control_name="Access Review and Recertification",
                control_objective="Periodically review and recertify user access rights",
                control_type="Detective",
                control_category="Administrative",
                automation_level="Semi-Automated",
                frequency="Quarterly",
                failure_mode="Manual review escalation",
                risks_mitigated=["RISK-IAG-001"],
                control_owner_role=ROLES["IAM_TEAM"],
                description="Quarterly access reviews by data owners"
            ),
            
            # Credential Monitoring Controls
            Control(
                control_id="CTRL-CRED-001",
                control_name="Credential Monitoring and Anomaly Detection",
                control_objective="Detect anomalous credential usage patterns",
                control_type="Detective",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Real-time",
                failure_mode="Alert generation continues via backup channel",
                risks_mitigated=["RISK-CRED-001"],
                control_owner_role=ROLES["SOC"],
                description="UEBA system monitors credential usage for anomalies"
            ),
            Control(
                control_id="CTRL-CRED-002",
                control_name="Password Policy Enforcement",
                control_objective="Enforce strong password requirements",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Per password change",
                failure_mode="Password change rejected",
                risks_mitigated=["RISK-CRED-001", "RISK-IAG-001"],
                control_owner_role=ROLES["IAM_TEAM"],
                description="Minimum 14 characters, complexity, no reuse of last 24 passwords"
            ),
            
            # Cloud Control Plane Controls
            Control(
                control_id="CTRL-CCP-001",
                control_name="Cloud Console Access Control",
                control_objective="Restrict access to cloud management consoles",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Continuous",
                failure_mode="Access denied",
                risks_mitigated=["RISK-CCP-001"],
                control_owner_role=ROLES["CLOUD_PLATFORM_TEAM"],
                description="MFA + IP restriction + just-in-time elevation for console access"
            ),
            Control(
                control_id="CTRL-CCP-002",
                control_name="Infrastructure-as-Code (IaC) Controls",
                control_objective="All infrastructure changes via approved IaC",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Per deployment",
                failure_mode="Deployment blocked",
                risks_mitigated=["RISK-CCP-001"],
                control_owner_role=ROLES["CLOUD_PLATFORM_TEAM"],
                description="All changes through version-controlled IaC with peer review"
            ),
            Control(
                control_id="CTRL-CCP-003",
                control_name="Cloud Configuration Monitoring",
                control_objective="Continuously monitor cloud configurations for drift",
                control_type="Detective",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Continuous",
                failure_mode="Alert via secondary channel",
                risks_mitigated=["RISK-CCP-001"],
                control_owner_role=ROLES["CLOUD_PLATFORM_TEAM"],
                description="CSPM monitors configurations against baseline"
            ),
            
            # Data Security & Privacy Controls
            Control(
                control_id="CTRL-DSP-001",
                control_name="Data Classification",
                control_objective="Classify all data according to sensitivity",
                control_type="Preventive",
                control_category="Administrative",
                automation_level="Semi-Automated",
                frequency="Per data creation",
                failure_mode="Default to highest classification",
                risks_mitigated=["RISK-DSP-001"],
                control_owner_role=ROLES["DATA_GOVERNANCE"],
                description="Data owners classify data using approved taxonomy"
            ),
            Control(
                control_id="CTRL-DSP-002",
                control_name="Encryption at Rest",
                control_objective="Encrypt sensitive data at rest",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Continuous",
                failure_mode="Write operations fail if encryption unavailable",
                risks_mitigated=["RISK-DSP-001"],
                control_owner_role=ROLES["CLOUD_PLATFORM_TEAM"],
                description="AES-256 encryption for all sensitive data at rest"
            ),
            Control(
                control_id="CTRL-DSP-003",
                control_name="Encryption in Transit",
                control_objective="Encrypt data in transit",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Per transmission",
                failure_mode="Connection refused if TLS unavailable",
                risks_mitigated=["RISK-DSP-001"],
                control_owner_role=ROLES["CLOUD_PLATFORM_TEAM"],
                description="TLS 1.2+ for all data transmission"
            ),
            Control(
                control_id="CTRL-DSP-004",
                control_name="Data Loss Prevention (DLP)",
                control_objective="Prevent unauthorized data exfiltration",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Real-time",
                failure_mode="Block suspicious transfers",
                risks_mitigated=["RISK-DSP-001"],
                control_owner_role=ROLES["SOC"],
                description="DLP monitors and blocks unauthorized data transfers"
            ),
            
            # Service Account Controls
            Control(
                control_id="CTRL-WNH-001",
                control_name="Service Account Management",
                control_objective="Manage service accounts with least privilege",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Semi-Automated",
                frequency="Per provisioning",
                failure_mode="Manual approval required",
                risks_mitigated=["RISK-WNH-001"],
                control_owner_role=ROLES["IAM_TEAM"],
                description="Service accounts follow least privilege with regular rotation"
            ),
            Control(
                control_id="CTRL-WNH-002",
                control_name="API Key Rotation",
                control_objective="Rotate API keys and secrets regularly",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Quarterly",
                failure_mode="Alert on rotation failure",
                risks_mitigated=["RISK-WNH-001"],
                control_owner_role=ROLES["IAM_TEAM"],
                description="Automated rotation of API keys every 90 days"
            ),
            
            # Endpoint Security Controls
            Control(
                control_id="CTRL-EDS-001",
                control_name="Endpoint Detection and Response (EDR)",
                control_objective="Deploy EDR on all endpoints",
                control_type="Detective",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Real-time",
                failure_mode="Alert on agent failure",
                risks_mitigated=["RISK-EDS-001"],
                control_owner_role=ROLES["SOC"],
                description="EDR deployed on all workstations and servers"
            ),
            Control(
                control_id="CTRL-EDS-002",
                control_name="Patch Management",
                control_objective="Apply security patches in timely manner",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Monthly (critical within 30 days)",
                failure_mode="Manual remediation",
                risks_mitigated=["RISK-EDS-001"],
                control_owner_role=ROLES["IT_OPERATIONS"],
                description="Automated patching with critical patches within 30 days"
            ),
            Control(
                control_id="CTRL-EDS-003",
                control_name="Device Encryption",
                control_objective="Encrypt all endpoint devices",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Continuous",
                failure_mode="Device non-compliant flag",
                risks_mitigated=["RISK-EDS-001", "RISK-DSP-001"],
                control_owner_role=ROLES["IT_OPERATIONS"],
                description="Full disk encryption on all endpoints"
            ),
            
            # Network Security Controls
            Control(
                control_id="CTRL-NET-001",
                control_name="Network Segmentation",
                control_objective="Segment network into security zones",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Continuous",
                failure_mode="Default deny",
                risks_mitigated=["RISK-NET-001"],
                control_owner_role=ROLES["CLOUD_PLATFORM_TEAM"],
                description="Micro-segmentation with zero-trust architecture"
            ),
            Control(
                control_id="CTRL-NET-002",
                control_name="Network Firewall Rules",
                control_objective="Control network traffic via firewall rules",
                control_type="Preventive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Continuous",
                failure_mode="Default deny",
                risks_mitigated=["RISK-NET-001"],
                control_owner_role=ROLES["CLOUD_PLATFORM_TEAM"],
                description="Firewall rules follow least privilege"
            ),
            
            # Detection & Response Controls
            Control(
                control_id="CTRL-DRR-001",
                control_name="Security Information and Event Management (SIEM)",
                control_objective="Centralize security event monitoring",
                control_type="Detective",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Real-time",
                failure_mode="Alert via backup channel",
                risks_mitigated=["RISK-DRR-001"],
                control_owner_role=ROLES["SOC"],
                description="SIEM aggregates logs from all sources"
            ),
            Control(
                control_id="CTRL-DRR-002",
                control_name="Incident Response Plan",
                control_objective="Maintain documented incident response procedures",
                control_type="Responsive",
                control_category="Administrative",
                automation_level="Manual",
                frequency="Per incident",
                failure_mode="Escalation to CISO",
                risks_mitigated=["RISK-DRR-001"],
                control_owner_role=ROLES["CISO"],
                description="Documented IRP with defined roles and escalation paths"
            ),
            Control(
                control_id="CTRL-DRR-003",
                control_name="Backup and Recovery",
                control_objective="Maintain backups for critical systems",
                control_type="Responsive",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Daily",
                failure_mode="Alert on backup failure",
                risks_mitigated=["RISK-DRR-001"],
                control_owner_role=ROLES["IT_OPERATIONS"],
                description="Daily backups with quarterly recovery testing"
            ),
            
            # Third-Party Controls
            Control(
                control_id="CTRL-TPI-001",
                control_name="Vendor Security Assessment",
                control_objective="Assess vendor security before onboarding",
                control_type="Preventive",
                control_category="Administrative",
                automation_level="Manual",
                frequency="Per vendor onboarding",
                failure_mode="Vendor not approved",
                risks_mitigated=["RISK-TPI-001"],
                control_owner_role=ROLES["AUDIT_COMPLIANCE"],
                description="Security questionnaire and evidence review for all vendors"
            ),
            Control(
                control_id="CTRL-TPI-002",
                control_name="Third-Party Access Monitoring",
                control_objective="Monitor third-party access to systems",
                control_type="Detective",
                control_category="Technical",
                automation_level="Fully Automated",
                frequency="Real-time",
                failure_mode="Alert on anomaly",
                risks_mitigated=["RISK-TPI-001"],
                control_owner_role=ROLES["SOC"],
                description="Monitor all third-party connections and activities"
            ),
        ]
        
        self.controls = controls
        
        # Add controls as nodes and create relationships
        control_obj_counter = 1
        for control in controls:
            # Add Control Objective node (if not exists)
            ctrl_obj_id = f"CTRLOBJ-{control_obj_counter:03d}"
            ctrl_obj_node = GraphNode(
                node_id=ctrl_obj_id,
                node_type="Control Objective",
                attributes={
                    "objective": control.control_objective
                }
            )
            self.graph.add_node(ctrl_obj_node)
            
            # Add Control node
            control_node = GraphNode(
                node_id=control.control_id,
                node_type="Control",
                attributes={
                    "name": control.control_name,
                    "objective": control.control_objective,
                    "type": control.control_type,
                    "category": control.control_category,
                    "automation_level": control.automation_level,
                    "frequency": control.frequency,
                    "failure_mode": control.failure_mode,
                    "owner": control.control_owner_role,
                    "description": control.description
                }
            )
            self.graph.add_node(control_node)
            
            # Link risks to control objectives (risk mitigated_by control_objective)
            for risk_id in control.risks_mitigated:
                self.graph.add_edge(GraphEdge(
                    edge_id=f"REL-{risk_id}-{ctrl_obj_id}",
                    source_node_id=risk_id,
                    target_node_id=ctrl_obj_id,
                    relationship_type="mitigated_by"
                ))
            
            # Link control objective to control (decomposition)
            self.graph.add_edge(GraphEdge(
                edge_id=f"REL-{ctrl_obj_id}-{control.control_id}",
                source_node_id=ctrl_obj_id,
                target_node_id=control.control_id,
                relationship_type="decomposes_into"
            ))
            
            # Link control to owner role
            role_id = f"ROLE-{control.control_owner_role.replace(' ', '-').replace('/', '-')}"
            # Add role node if not exists
            if not any(node.node_id == role_id for node in self.graph.nodes):
                role_node = GraphNode(
                    node_id=role_id,
                    node_type="Role / Accountability",
                    attributes={"name": control.control_owner_role}
                )
                self.graph.add_node(role_node)
            
            self.graph.add_edge(GraphEdge(
                edge_id=f"REL-{control.control_id}-{role_id}",
                source_node_id=control.control_id,
                target_node_id=role_id,
                relationship_type="owned_by"
            ))
            
            control_obj_counter += 1
    
    def define_platform_implementations(self):
        """
        Define platform-specific technical implementations
        
        NOTE: These implementations reference internal tooling and should be 
        validated against actual deployed solutions.
        """
        
        implementations = []
        
        # Example implementations for CTRL-IAM-001 (Centralized Identity Management)
        implementations.extend([
            TechnicalImplementation(
                implementation_id="IMPL-IAM-001-AZURE",
                control_id="CTRL-IAM-001",
                platform=PLATFORMS["AZURE"],
                operating_environment="All",
                implementation_details="Azure Entra ID (formerly Azure AD) as primary IdP with Conditional Access policies",
                tooling=["Azure Entra ID", "Conditional Access"],
                configuration_baseline="Azure Entra ID baseline v2.1"
            ),
            TechnicalImplementation(
                implementation_id="IMPL-IAM-001-AWS",
                control_id="CTRL-IAM-001",
                platform=PLATFORMS["AWS"],
                operating_environment="All",
                implementation_details="AWS IAM Identity Center (SSO) federated with Azure Entra ID",
                tooling=["AWS IAM Identity Center", "SAML Federation"],
                configuration_baseline="AWS SSO baseline v1.3"
            ),
            TechnicalImplementation(
                implementation_id="IMPL-IAM-001-GCP",
                control_id="CTRL-IAM-001",
                platform=PLATFORMS["GCP"],
                operating_environment="All",
                implementation_details="Google Cloud Identity federated with Azure Entra ID",
                tooling=["Google Cloud Identity", "SAML Federation"],
                configuration_baseline="GCP Identity baseline v1.2"
            ),
            TechnicalImplementation(
                implementation_id="IMPL-IAM-001-OCI",
                control_id="CTRL-IAM-001",
                platform=PLATFORMS["OCI"],
                operating_environment="All",
                implementation_details="Oracle Cloud Infrastructure IAM federated with Azure Entra ID",
                tooling=["OCI IAM", "SAML Federation"],
                configuration_baseline="OCI IAM baseline v1.0"
            ),
            TechnicalImplementation(
                implementation_id="IMPL-IAM-001-ONPREM-WIN",
                control_id="CTRL-IAM-001",
                platform=PLATFORMS["ON_PREM"],
                operating_environment=OPERATING_ENVIRONMENTS["WINDOWS"],
                implementation_details="Active Directory integrated with Azure Entra ID via Azure AD Connect",
                tooling=["Active Directory", "Azure AD Connect"],
                configuration_baseline="AD baseline v3.2"
            ),
            TechnicalImplementation(
                implementation_id="IMPL-IAM-001-ONPREM-LINUX",
                control_id="CTRL-IAM-001",
                platform=PLATFORMS["ON_PREM"],
                operating_environment=OPERATING_ENVIRONMENTS["LINUX"],
                implementation_details="SSSD integrated with Active Directory for Linux authentication",
                tooling=["SSSD", "Active Directory"],
                configuration_baseline="Linux authentication baseline v2.1"
            ),
        ])
        
        # MFA implementations
        implementations.extend([
            TechnicalImplementation(
                implementation_id="IMPL-IAM-002-AZURE",
                control_id="CTRL-IAM-002",
                platform=PLATFORMS["AZURE"],
                operating_environment="All",
                implementation_details="Azure Entra ID MFA with Conditional Access enforcement",
                tooling=["Azure Entra ID MFA", "Conditional Access"],
                configuration_baseline="MFA policy baseline v2.0"
            ),
            TechnicalImplementation(
                implementation_id="IMPL-IAM-002-AWS",
                control_id="CTRL-IAM-002",
                platform=PLATFORMS["AWS"],
                operating_environment="All",
                implementation_details="AWS MFA enforced via SCPs and IAM policies",
                tooling=["AWS IAM MFA", "Service Control Policies"],
                configuration_baseline="AWS MFA baseline v1.5"
            ),
        ])
        
        # EDR implementations
        implementations.extend([
            TechnicalImplementation(
                implementation_id="IMPL-EDS-001-WIN",
                control_id="CTRL-EDS-001",
                platform="All",
                operating_environment=OPERATING_ENVIRONMENTS["WINDOWS"],
                implementation_details="Microsoft Defender for Endpoint deployed on Windows devices",
                tooling=["Microsoft Defender for Endpoint"],
                configuration_baseline="Defender baseline v4.0"
            ),
            TechnicalImplementation(
                implementation_id="IMPL-EDS-001-LINUX",
                control_id="CTRL-EDS-001",
                platform="All",
                operating_environment=OPERATING_ENVIRONMENTS["LINUX"],
                implementation_details="Microsoft Defender for Endpoint Linux agent deployed",
                tooling=["Microsoft Defender for Endpoint (Linux)"],
                configuration_baseline="Defender Linux baseline v2.0"
            ),
            TechnicalImplementation(
                implementation_id="IMPL-EDS-001-MACOS",
                control_id="CTRL-EDS-001",
                platform="All",
                operating_environment=OPERATING_ENVIRONMENTS["MACOS"],
                implementation_details="Microsoft Defender for Endpoint macOS agent deployed",
                tooling=["Microsoft Defender for Endpoint (macOS)"],
                configuration_baseline="Defender macOS baseline v2.0"
            ),
        ])
        
        # Encryption implementations
        implementations.extend([
            TechnicalImplementation(
                implementation_id="IMPL-DSP-002-AZURE",
                control_id="CTRL-DSP-002",
                platform=PLATFORMS["AZURE"],
                operating_environment="All",
                implementation_details="Azure Storage Service Encryption with customer-managed keys in Key Vault",
                tooling=["Azure Storage Service Encryption", "Azure Key Vault"],
                configuration_baseline="Azure encryption baseline v2.2"
            ),
            TechnicalImplementation(
                implementation_id="IMPL-DSP-002-AWS",
                control_id="CTRL-DSP-002",
                platform=PLATFORMS["AWS"],
                operating_environment="All",
                implementation_details="AWS KMS encryption for all storage services",
                tooling=["AWS KMS", "S3 Encryption", "EBS Encryption"],
                configuration_baseline="AWS encryption baseline v2.0"
            ),
        ])
        
        # NOTE: Additional implementations would be defined for all controls
        # This is a representative sample
        
        self.implementations = implementations
        
        # Add implementation nodes and relationships
        for impl in implementations:
            impl_node = GraphNode(
                node_id=impl.implementation_id,
                node_type="Technical Control Implementation",
                attributes={
                    "platform": impl.platform,
                    "environment": impl.operating_environment,
                    "details": impl.implementation_details,
                    "tooling": ", ".join(impl.tooling),
                    "baseline": impl.configuration_baseline
                }
            )
            self.graph.add_node(impl_node)
            
            # Link control to implementation
            self.graph.add_edge(GraphEdge(
                edge_id=f"REL-{impl.control_id}-{impl.implementation_id}",
                source_node_id=impl.control_id,
                target_node_id=impl.implementation_id,
                relationship_type="implemented_via"
            ))
            
            # Link to platform if not "All"
            if impl.platform != "All":
                platform_id = f"PLATFORM-{impl.platform.replace(' ', '-').replace('(', '').replace(')', '')}"
                if not any(node.node_id == platform_id for node in self.graph.nodes):
                    platform_node = GraphNode(
                        node_id=platform_id,
                        node_type="Platform",
                        attributes={"name": impl.platform}
                    )
                    self.graph.add_node(platform_node)
                
                self.graph.add_edge(GraphEdge(
                    edge_id=f"REL-{impl.implementation_id}-{platform_id}",
                    source_node_id=impl.implementation_id,
                    target_node_id=platform_id,
                    relationship_type="applicable_to_platform"
                ))
            
            # Link to operating environment if not "All"
            if impl.operating_environment != "All":
                env_id = f"ENV-{impl.operating_environment.replace(' ', '-').replace('(', '').replace(')', '')}"
                if not any(node.node_id == env_id for node in self.graph.nodes):
                    env_node = GraphNode(
                        node_id=env_id,
                        node_type="Operating Environment",
                        attributes={"name": impl.operating_environment}
                    )
                    self.graph.add_node(env_node)
                
                self.graph.add_edge(GraphEdge(
                    edge_id=f"REL-{impl.implementation_id}-{env_id}",
                    source_node_id=impl.implementation_id,
                    target_node_id=env_id,
                    relationship_type="applicable_to_environment"
                ))
    
    def define_evidence_artifacts(self):
        """Define evidence artifacts for audit"""
        
        evidence_artifacts = [
            EvidenceArtifact(
                evidence_id="EVID-001",
                implementation_id="IMPL-IAM-001-AZURE",
                evidence_type="Configuration Export",
                evidence_source_system="Azure Entra ID",
                evidence_location="Audit evidence repository /azure-entra-id/",
                retention_period="7 years",
                audit_test_procedure="Export and review Conditional Access policies",
                test_frequency="Annually",
                control_effectiveness_criteria="All users authenticate via Azure Entra ID with Conditional Access enforced"
            ),
            EvidenceArtifact(
                evidence_id="EVID-002",
                implementation_id="IMPL-IAM-002-AZURE",
                evidence_type="Policy Report",
                evidence_source_system="Azure Entra ID",
                evidence_location="Audit evidence repository /azure-entra-id/mfa/",
                retention_period="7 years",
                audit_test_procedure="Export MFA enrollment report and Conditional Access policy",
                test_frequency="Annually",
                control_effectiveness_criteria="100% of privileged users and remote access users enrolled in MFA"
            ),
            EvidenceArtifact(
                evidence_id="EVID-003",
                implementation_id="IMPL-EDS-001-WIN",
                evidence_type="Agent Deployment Report",
                evidence_source_system="Microsoft Defender for Endpoint",
                evidence_location="Audit evidence repository /defender/",
                retention_period="7 years",
                audit_test_procedure="Export device inventory showing Defender agent status",
                test_frequency="Quarterly",
                control_effectiveness_criteria="95%+ of Windows devices have active Defender agent"
            ),
        ]
        
        self.evidence_artifacts = evidence_artifacts
        
        # Add evidence nodes and relationships
        for evidence in evidence_artifacts:
            evidence_node = GraphNode(
                node_id=evidence.evidence_id,
                node_type="Evidence Artifact",
                attributes={
                    "type": evidence.evidence_type,
                    "source": evidence.evidence_source_system,
                    "location": evidence.evidence_location,
                    "retention": evidence.retention_period,
                    "test_procedure": evidence.audit_test_procedure,
                    "test_frequency": evidence.test_frequency,
                    "effectiveness_criteria": evidence.control_effectiveness_criteria
                }
            )
            self.graph.add_node(evidence_node)
            
            # Link implementation to evidence
            self.graph.add_edge(GraphEdge(
                edge_id=f"REL-{evidence.implementation_id}-{evidence.evidence_id}",
                source_node_id=evidence.implementation_id,
                target_node_id=evidence.evidence_id,
                relationship_type="produces_evidence"
            ))
    
    def define_regulatory_mappings(self):
        """Map controls to regulatory requirements"""
        
        mappings = [
            # IAM Controls
            RegulatoryMapping(
                control_id="CTRL-IAM-001",
                regulation=REGULATIONS["ISO_27001"],
                requirement_id="A.9.2.1",
                requirement_description="User registration and de-registration",
                applicability="Applicable",
                applicability_rationale="Centralized identity management directly satisfies user registration requirements"
            ),
            RegulatoryMapping(
                control_id="CTRL-IAM-001",
                regulation=REGULATIONS["PCI_DSS"],
                requirement_id="8.2",
                requirement_description="User identification and authentication",
                applicability="Applicable",
                applicability_rationale="Central IdP provides unique user identification"
            ),
            RegulatoryMapping(
                control_id="CTRL-IAM-001",
                regulation=REGULATIONS["SOC_2"],
                requirement_id="CC6.1",
                requirement_description="Logical and physical access controls",
                applicability="Applicable",
                applicability_rationale="Centralized access control system"
            ),
            RegulatoryMapping(
                control_id="CTRL-IAM-002",
                regulation=REGULATIONS["ISO_27001"],
                requirement_id="A.9.4.2",
                requirement_description="Secure log-on procedures",
                applicability="Applicable",
                applicability_rationale="MFA provides secure authentication"
            ),
            RegulatoryMapping(
                control_id="CTRL-IAM-002",
                regulation=REGULATIONS["PCI_DSS"],
                requirement_id="8.4",
                requirement_description="Multi-factor authentication",
                applicability="Applicable",
                applicability_rationale="MFA required for all privileged access"
            ),
            RegulatoryMapping(
                control_id="CTRL-IAM-002",
                regulation=REGULATIONS["SOC_2"],
                requirement_id="CC6.1",
                requirement_description="Logical and physical access controls",
                applicability="Applicable",
                applicability_rationale="MFA strengthens access controls"
            ),
            RegulatoryMapping(
                control_id="CTRL-IAM-002",
                regulation=REGULATIONS["HIPAA"],
                requirement_id="164.312(a)(2)(i)",
                requirement_description="Unique user identification",
                applicability="Applicable",
                applicability_rationale="MFA ensures unique user identification"
            ),
            RegulatoryMapping(
                control_id="CTRL-DSP-002",
                regulation=REGULATIONS["ISO_27001"],
                requirement_id="A.8.24",
                requirement_description="Use of cryptography",
                applicability="Applicable",
                applicability_rationale="Encryption at rest using approved algorithms"
            ),
            RegulatoryMapping(
                control_id="CTRL-DSP-002",
                regulation=REGULATIONS["PCI_DSS"],
                requirement_id="3.5",
                requirement_description="Protect stored account data",
                applicability="Applicable",
                applicability_rationale="Strong cryptography for cardholder data at rest"
            ),
            RegulatoryMapping(
                control_id="CTRL-DSP-002",
                regulation=REGULATIONS["GDPR"],
                requirement_id="Article 32",
                requirement_description="Security of processing",
                applicability="Applicable",
                applicability_rationale="Encryption ensures confidentiality of personal data"
            ),
            RegulatoryMapping(
                control_id="CTRL-DSP-002",
                regulation=REGULATIONS["HIPAA"],
                requirement_id="164.312(a)(2)(iv)",
                requirement_description="Encryption and decryption",
                applicability="Applicable",
                applicability_rationale="Encryption of ePHI at rest"
            ),
            RegulatoryMapping(
                control_id="CTRL-DRR-001",
                regulation=REGULATIONS["ISO_27001"],
                requirement_id="A.8.15",
                requirement_description="Logging",
                applicability="Applicable",
                applicability_rationale="SIEM provides centralized logging and monitoring"
            ),
            RegulatoryMapping(
                control_id="CTRL-DRR-001",
                regulation=REGULATIONS["PCI_DSS"],
                requirement_id="10.4",
                requirement_description="Audit logs",
                applicability="Applicable",
                applicability_rationale="SIEM aggregates and retains audit logs"
            ),
            RegulatoryMapping(
                control_id="CTRL-DRR-001",
                regulation=REGULATIONS["SOC_2"],
                requirement_id="CC7.2",
                requirement_description="System monitoring",
                applicability="Applicable",
                applicability_rationale="SIEM monitors system activities and anomalies"
            ),
            RegulatoryMapping(
                control_id="CTRL-DRR-001",
                regulation=REGULATIONS["DORA"],
                requirement_id="Article 17",
                requirement_description="ICT-related incident detection",
                applicability="Applicable",
                applicability_rationale="SIEM provides ICT incident detection capabilities"
            ),
            RegulatoryMapping(
                control_id="CTRL-DRR-002",
                regulation=REGULATIONS["ISO_27001"],
                requirement_id="A.5.24",
                requirement_description="Information security incident management planning and preparation",
                applicability="Applicable",
                applicability_rationale="Documented incident response plan"
            ),
            RegulatoryMapping(
                control_id="CTRL-DRR-002",
                regulation=REGULATIONS["SOC_2"],
                requirement_id="CC7.3",
                requirement_description="Incident response",
                applicability="Applicable",
                applicability_rationale="Incident response procedures documented and tested"
            ),
            RegulatoryMapping(
                control_id="CTRL-DRR-002",
                regulation=REGULATIONS["DORA"],
                requirement_id="Article 11",
                requirement_description="ICT-related incident management process",
                applicability="Applicable",
                applicability_rationale="Incident response plan covers ICT incidents"
            ),
            RegulatoryMapping(
                control_id="CTRL-DRR-003",
                regulation=REGULATIONS["ISO_27001"],
                requirement_id="A.8.13",
                requirement_description="Information backup",
                applicability="Applicable",
                applicability_rationale="Regular backups with tested recovery procedures"
            ),
            RegulatoryMapping(
                control_id="CTRL-DRR-003",
                regulation=REGULATIONS["SOC_2"],
                requirement_id="CC9.1",
                requirement_description="Business continuity",
                applicability="Applicable",
                applicability_rationale="Backups support business continuity"
            ),
            RegulatoryMapping(
                control_id="CTRL-TPI-001",
                regulation=REGULATIONS["ISO_27001"],
                requirement_id="A.5.19",
                requirement_description="Information security in supplier relationships",
                applicability="Applicable",
                applicability_rationale="Vendor security assessment before onboarding"
            ),
            RegulatoryMapping(
                control_id="CTRL-TPI-001",
                regulation=REGULATIONS["PCI_DSS"],
                requirement_id="12.8",
                requirement_description="Service provider management",
                applicability="Applicable",
                applicability_rationale="Security assessment for service providers"
            ),
            RegulatoryMapping(
                control_id="CTRL-TPI-001",
                regulation=REGULATIONS["SOC_2"],
                requirement_id="CC9.2",
                requirement_description="Vendor management",
                applicability="Applicable",
                applicability_rationale="Vendor security due diligence"
            ),
        ]
        
        self.regulatory_mappings = mappings
        
        # Add regulation nodes and create relationships
        for mapping in mappings:
            # Add regulation node if not exists
            reg_id = f"REG-{mapping.regulation.replace(' ', '-').replace(':', '-').replace('.', '-')}"
            if not any(node.node_id == reg_id for node in self.graph.nodes):
                reg_node = GraphNode(
                    node_id=reg_id,
                    node_type="Regulation / Standard",
                    attributes={"name": mapping.regulation}
                )
                self.graph.add_node(reg_node)
            
            # Create unique mapping node for each control-regulation-requirement combination
            mapping_id = f"MAPPING-{mapping.control_id}-{reg_id}-{mapping.requirement_id.replace('.', '-')}"
            mapping_node = GraphNode(
                node_id=mapping_id,
                node_type="Regulatory Mapping",
                attributes={
                    "regulation": mapping.regulation,
                    "requirement_id": mapping.requirement_id,
                    "requirement_description": mapping.requirement_description,
                    "applicability": mapping.applicability,
                    "rationale": mapping.applicability_rationale
                }
            )
            self.graph.add_node(mapping_node)
            
            # Link control to mapping
            self.graph.add_edge(GraphEdge(
                edge_id=f"REL-{mapping.control_id}-{mapping_id}",
                source_node_id=mapping.control_id,
                target_node_id=mapping_id,
                relationship_type="maps_to_regulation"
            ))
            
            # Link mapping to regulation
            self.graph.add_edge(GraphEdge(
                edge_id=f"REL-{mapping_id}-{reg_id}",
                source_node_id=mapping_id,
                target_node_id=reg_id,
                relationship_type="maps_to_regulation"
            ))
    
    def build_complete_model(self):
        """Build the complete ERM data model"""
        print("Building risk taxonomy...")
        self.build_risk_taxonomy()
        
        print("Defining risk statements...")
        self.define_risk_statements()
        
        print("Defining controls...")
        self.define_controls()
        
        print("Defining platform implementations...")
        self.define_platform_implementations()
        
        print("Defining evidence artifacts...")
        self.define_evidence_artifacts()
        
        print("Defining regulatory mappings...")
        self.define_regulatory_mappings()
        
        print(f"Model complete: {len(self.graph.nodes)} nodes, {len(self.graph.edges)} edges")
        
        return self.graph
