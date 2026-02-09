"""
Enterprise Risk Management Graph Ontology
==========================================
This module defines the node types and relationships for the ERM graph.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum


class NodeType(Enum):
    """Defines all node types in the ERM graph"""
    ENTERPRISE_RISK = "Enterprise Risk"
    IT_RISK = "IT Risk"
    INFORMATION_SECURITY_RISK = "Information Security Risk"
    SECURITY_RISK_CATEGORY = "Security Risk Category"
    RISK_STATEMENT = "Risk Statement"
    CONTROL_OBJECTIVE = "Control Objective"
    CONTROL = "Control"
    TECHNICAL_CONTROL_IMPLEMENTATION = "Technical Control Implementation"
    EVIDENCE_ARTIFACT = "Evidence Artifact"
    REGULATION_STANDARD = "Regulation / Standard"
    ROLE_ACCOUNTABILITY = "Role / Accountability"
    PLATFORM = "Platform"
    OPERATING_ENVIRONMENT = "Operating Environment"


class RelationshipType(Enum):
    """Defines all relationship types in the ERM graph"""
    DECOMPOSES_INTO = "decomposes_into"
    MITIGATED_BY = "mitigated_by"
    IMPLEMENTED_VIA = "implemented_via"
    PRODUCES_EVIDENCE = "produces_evidence"
    MAPS_TO_REGULATION = "maps_to_regulation"
    OWNED_BY = "owned_by"
    APPLICABLE_TO_PLATFORM = "applicable_to_platform"
    APPLICABLE_TO_ENVIRONMENT = "applicable_to_environment"


class ControlType(Enum):
    """Control type classification"""
    PREVENTIVE = "Preventive"
    DETECTIVE = "Detective"
    RESPONSIVE = "Responsive"
    CORRECTIVE = "Corrective"


class ControlCategory(Enum):
    """Control category classification"""
    ADMINISTRATIVE = "Administrative"
    TECHNICAL = "Technical"
    PHYSICAL = "Physical"


class AutomationLevel(Enum):
    """Control automation level"""
    MANUAL = "Manual"
    SEMI_AUTOMATED = "Semi-Automated"
    FULLY_AUTOMATED = "Fully Automated"


class RiskRating(Enum):
    """Risk rating levels"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    VERY_LOW = "Very Low"


@dataclass
class RiskStatement:
    """Formal risk statement following Cause → Risk Event → Business Impact"""
    risk_id: str
    cause: str
    risk_event: str
    business_impact: str
    inherent_likelihood: str
    inherent_impact: str
    inherent_rating: str
    residual_likelihood: str
    residual_impact: str
    residual_rating: str


@dataclass
class Control:
    """Control definition"""
    control_id: str
    control_name: str
    control_objective: str
    control_type: str  # Preventive/Detective/Responsive
    control_category: str  # Administrative/Technical/Physical
    automation_level: str
    frequency: str
    failure_mode: str
    risks_mitigated: List[str]
    control_owner_role: str
    description: str = ""


@dataclass
class TechnicalImplementation:
    """Technical control implementation for a specific platform/environment"""
    implementation_id: str
    control_id: str
    platform: str
    operating_environment: str
    implementation_details: str
    tooling: List[str]
    configuration_baseline: str


@dataclass
class EvidenceArtifact:
    """Evidence artifact for audit"""
    evidence_id: str
    implementation_id: str
    evidence_type: str
    evidence_source_system: str
    evidence_location: str
    retention_period: str
    audit_test_procedure: str
    test_frequency: str
    control_effectiveness_criteria: str


@dataclass
class RegulatoryMapping:
    """Regulatory/compliance framework mapping"""
    control_id: str
    regulation: str
    requirement_id: str
    requirement_description: str
    applicability: str
    applicability_rationale: str


@dataclass
class GraphNode:
    """Generic graph node"""
    node_id: str
    node_type: str
    attributes: Dict[str, any] = field(default_factory=dict)


@dataclass
class GraphEdge:
    """Generic graph edge"""
    edge_id: str
    source_node_id: str
    target_node_id: str
    relationship_type: str
    attributes: Dict[str, any] = field(default_factory=dict)


@dataclass
class ERMGraph:
    """Complete ERM graph structure"""
    nodes: List[GraphNode] = field(default_factory=list)
    edges: List[GraphEdge] = field(default_factory=list)
    
    def add_node(self, node: GraphNode):
        """Add a node to the graph"""
        self.nodes.append(node)
    
    def add_edge(self, edge: GraphEdge):
        """Add an edge to the graph"""
        self.edges.append(edge)
    
    def get_nodes_by_type(self, node_type: str) -> List[GraphNode]:
        """Get all nodes of a specific type"""
        return [node for node in self.nodes if node.node_type == node_type]
    
    def get_edges_by_type(self, relationship_type: str) -> List[GraphEdge]:
        """Get all edges of a specific relationship type"""
        return [edge for edge in self.edges if edge.relationship_type == relationship_type]
