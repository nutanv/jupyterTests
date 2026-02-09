"""
Risk-Control-Compliance Matrix Generation
==========================================
This module generates tabular matrices and exports for the ERM system.
"""

import pandas as pd
from typing import List, Dict
import json
from erm_data_model import ERMDataModel


class MatrixGenerator:
    """Generate various matrix views of the ERM data"""
    
    def __init__(self, model: ERMDataModel):
        self.model = model
        
    def generate_risk_control_matrix(self) -> pd.DataFrame:
        """Generate the core Risk-Control mapping matrix"""
        
        rows = []
        for risk in self.model.risks:
            # Find controls that mitigate this risk
            mitigating_controls = [
                ctrl for ctrl in self.model.controls 
                if risk.risk_id in ctrl.risks_mitigated
            ]
            
            for control in mitigating_controls:
                rows.append({
                    'Risk ID': risk.risk_id,
                    'Risk Cause': risk.cause,
                    'Risk Event': risk.risk_event,
                    'Business Impact': risk.business_impact,
                    'Inherent Rating': risk.inherent_rating,
                    'Residual Rating': risk.residual_rating,
                    'Control ID': control.control_id,
                    'Control Name': control.control_name,
                    'Control Type': control.control_type,
                    'Control Category': control.control_category,
                    'Automation Level': control.automation_level,
                    'Control Owner': control.control_owner_role,
                    'Frequency': control.frequency
                })
        
        return pd.DataFrame(rows)
    
    def generate_control_compliance_matrix(self) -> pd.DataFrame:
        """Generate Control-Compliance mapping matrix"""
        
        rows = []
        for mapping in self.model.regulatory_mappings:
            # Find the control
            control = next((c for c in self.model.controls if c.control_id == mapping.control_id), None)
            if not control:
                continue
            
            rows.append({
                'Control ID': mapping.control_id,
                'Control Name': control.control_name,
                'Control Type': control.control_type,
                'Regulation': mapping.regulation,
                'Requirement ID': mapping.requirement_id,
                'Requirement Description': mapping.requirement_description,
                'Applicability': mapping.applicability,
                'Applicability Rationale': mapping.applicability_rationale
            })
        
        return pd.DataFrame(rows)
    
    def generate_implementation_matrix(self) -> pd.DataFrame:
        """Generate Control Implementation matrix by platform/environment"""
        
        rows = []
        for impl in self.model.implementations:
            # Find the control
            control = next((c for c in self.model.controls if c.control_id == impl.control_id), None)
            if not control:
                continue
            
            rows.append({
                'Control ID': impl.control_id,
                'Control Name': control.control_name,
                'Platform': impl.platform,
                'Operating Environment': impl.operating_environment,
                'Implementation Details': impl.implementation_details,
                'Tooling': ', '.join(impl.tooling),
                'Configuration Baseline': impl.configuration_baseline
            })
        
        return pd.DataFrame(rows)
    
    def generate_evidence_matrix(self) -> pd.DataFrame:
        """Generate Evidence Artifact matrix"""
        
        rows = []
        for evidence in self.model.evidence_artifacts:
            # Find implementation
            impl = next((i for i in self.model.implementations if i.implementation_id == evidence.implementation_id), None)
            if not impl:
                continue
            
            rows.append({
                'Evidence ID': evidence.evidence_id,
                'Control ID': impl.control_id,
                'Implementation ID': evidence.implementation_id,
                'Platform': impl.platform,
                'Environment': impl.operating_environment,
                'Evidence Type': evidence.evidence_type,
                'Source System': evidence.evidence_source_system,
                'Evidence Location': evidence.evidence_location,
                'Retention Period': evidence.retention_period,
                'Test Procedure': evidence.audit_test_procedure,
                'Test Frequency': evidence.test_frequency,
                'Effectiveness Criteria': evidence.control_effectiveness_criteria
            })
        
        return pd.DataFrame(rows)
    
    def generate_complete_matrix(self) -> pd.DataFrame:
        """Generate the complete integrated matrix"""
        
        rows = []
        for risk in self.model.risks:
            # Find controls
            mitigating_controls = [c for c in self.model.controls if risk.risk_id in c.risks_mitigated]
            
            for control in mitigating_controls:
                # Find implementations
                implementations = [i for i in self.model.implementations if i.control_id == control.control_id]
                
                # Find regulatory mappings
                mappings = [m for m in self.model.regulatory_mappings if m.control_id == control.control_id]
                regulations = ', '.join(set(m.regulation for m in mappings)) if mappings else 'N/A'
                
                if implementations:
                    for impl in implementations:
                        # Find evidence
                        evidence_list = [e for e in self.model.evidence_artifacts if e.implementation_id == impl.implementation_id]
                        evidence_ids = ', '.join(e.evidence_id for e in evidence_list) if evidence_list else 'GAP: No evidence defined'
                        
                        rows.append({
                            'Risk ID': risk.risk_id,
                            'Risk Statement': f"{risk.cause} → {risk.risk_event} → {risk.business_impact}",
                            'Inherent Rating': risk.inherent_rating,
                            'Residual Rating': risk.residual_rating,
                            'Control ID': control.control_id,
                            'Control Name': control.control_name,
                            'Control Type': control.control_type,
                            'Automation': control.automation_level,
                            'Owner': control.control_owner_role,
                            'Platform': impl.platform,
                            'Environment': impl.operating_environment,
                            'Implementation': impl.implementation_details[:100] + '...' if len(impl.implementation_details) > 100 else impl.implementation_details,
                            'Tooling': ', '.join(impl.tooling),
                            'Evidence': evidence_ids,
                            'Regulations': regulations
                        })
                else:
                    # Control exists but no implementation
                    rows.append({
                        'Risk ID': risk.risk_id,
                        'Risk Statement': f"{risk.cause} → {risk.risk_event} → {risk.business_impact}",
                        'Inherent Rating': risk.inherent_rating,
                        'Residual Rating': risk.residual_rating,
                        'Control ID': control.control_id,
                        'Control Name': control.control_name,
                        'Control Type': control.control_type,
                        'Automation': control.automation_level,
                        'Owner': control.control_owner_role,
                        'Platform': 'GAP: No implementation',
                        'Environment': 'N/A',
                        'Implementation': 'GAP: Implementation not defined',
                        'Tooling': 'N/A',
                        'Evidence': 'GAP: No evidence',
                        'Regulations': regulations
                    })
        
        return pd.DataFrame(rows)
    
    def identify_gaps(self) -> Dict[str, List[str]]:
        """Identify gaps in the ERM model"""
        
        gaps = {
            'controls_without_implementations': [],
            'implementations_without_evidence': [],
            'controls_without_regulatory_mapping': [],
            'risks_without_controls': [],
            'weak_controls': []
        }
        
        # Controls without implementations
        control_ids_with_impl = set(i.control_id for i in self.model.implementations)
        for control in self.model.controls:
            if control.control_id not in control_ids_with_impl:
                gaps['controls_without_implementations'].append(
                    f"{control.control_id}: {control.control_name}"
                )
        
        # Implementations without evidence
        impl_ids_with_evidence = set(e.implementation_id for e in self.model.evidence_artifacts)
        for impl in self.model.implementations:
            if impl.implementation_id not in impl_ids_with_evidence:
                gaps['implementations_without_evidence'].append(
                    f"{impl.implementation_id}: {impl.control_id} on {impl.platform}/{impl.operating_environment}"
                )
        
        # Controls without regulatory mapping
        control_ids_with_mapping = set(m.control_id for m in self.model.regulatory_mappings)
        for control in self.model.controls:
            if control.control_id not in control_ids_with_mapping:
                gaps['controls_without_regulatory_mapping'].append(
                    f"{control.control_id}: {control.control_name}"
                )
        
        # Risks without controls
        risk_ids_with_controls = set()
        for control in self.model.controls:
            risk_ids_with_controls.update(control.risks_mitigated)
        for risk in self.model.risks:
            if risk.risk_id not in risk_ids_with_controls:
                gaps['risks_without_controls'].append(
                    f"{risk.risk_id}: {risk.risk_event}"
                )
        
        # Weak controls (manual, low automation)
        for control in self.model.controls:
            if control.automation_level == "Manual" and control.control_type == "Preventive":
                gaps['weak_controls'].append(
                    f"{control.control_id}: {control.control_name} - Manual preventive control"
                )
        
        return gaps
    
    def export_to_excel(self, filename: str):
        """Export all matrices to Excel with multiple sheets"""
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Complete matrix
            df_complete = self.generate_complete_matrix()
            df_complete.to_excel(writer, sheet_name='Complete Matrix', index=False)
            
            # Risk-Control matrix
            df_risk_control = self.generate_risk_control_matrix()
            df_risk_control.to_excel(writer, sheet_name='Risk-Control', index=False)
            
            # Control-Compliance matrix
            df_compliance = self.generate_control_compliance_matrix()
            df_compliance.to_excel(writer, sheet_name='Control-Compliance', index=False)
            
            # Implementation matrix
            df_impl = self.generate_implementation_matrix()
            df_impl.to_excel(writer, sheet_name='Implementations', index=False)
            
            # Evidence matrix
            df_evidence = self.generate_evidence_matrix()
            df_evidence.to_excel(writer, sheet_name='Evidence', index=False)
            
            # Gaps
            gaps = self.identify_gaps()
            gap_rows = []
            for gap_type, gap_list in gaps.items():
                for gap in gap_list:
                    gap_rows.append({'Gap Type': gap_type, 'Description': gap})
            df_gaps = pd.DataFrame(gap_rows)
            df_gaps.to_excel(writer, sheet_name='Gaps & Weaknesses', index=False)
        
        print(f"Exported matrices to {filename}")
    
    def export_graph_to_json(self, filename: str):
        """Export graph structure to JSON for visualization"""
        
        graph_data = {
            'nodes': [
                {
                    'id': node.node_id,
                    'type': node.node_type,
                    'attributes': node.attributes
                }
                for node in self.model.graph.nodes
            ],
            'edges': [
                {
                    'id': edge.edge_id,
                    'source': edge.source_node_id,
                    'target': edge.target_node_id,
                    'relationship': edge.relationship_type,
                    'attributes': edge.attributes
                }
                for edge in self.model.graph.edges
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(graph_data, f, indent=2)
        
        print(f"Exported graph to {filename}")
    
    def export_filter_metadata(self, filename: str):
        """Export metadata for interactive filtering"""
        
        metadata = {
            'platforms': list(set(i.platform for i in self.model.implementations)),
            'operating_environments': list(set(i.operating_environment for i in self.model.implementations)),
            'regulations': list(set(m.regulation for m in self.model.regulatory_mappings)),
            'risk_ratings': ['Critical', 'High', 'Medium', 'Low', 'Very Low'],
            'control_types': ['Preventive', 'Detective', 'Responsive', 'Corrective'],
            'control_categories': ['Administrative', 'Technical', 'Physical'],
            'automation_levels': ['Manual', 'Semi-Automated', 'Fully Automated'],
            'roles': list(set(c.control_owner_role for c in self.model.controls)),
            'security_risk_categories': [
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
        }
        
        with open(filename, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Exported filter metadata to {filename}")
