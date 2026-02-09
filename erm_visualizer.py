"""
Interactive Visualization Module
=================================
This module provides interactive graph visualization and filtering capabilities
for the Enterprise Risk Management Matrix.
"""

import networkx as nx
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ipywidgets as widgets
from IPython.display import display, HTML
import pandas as pd
from typing import List, Dict, Optional
from erm_data_model import ERMDataModel
from matrix_generator import MatrixGenerator


class ERMVisualizer:
    """Interactive visualization for ERM graph"""
    
    def __init__(self, model: ERMDataModel):
        self.model = model
        self.matrix_gen = MatrixGenerator(model)
        self.nx_graph = self._build_networkx_graph()
        
    def _build_networkx_graph(self) -> nx.DiGraph:
        """Convert ERM graph to NetworkX for layout and analysis"""
        
        G = nx.DiGraph()
        
        # Add nodes
        for node in self.model.graph.nodes:
            G.add_node(node.node_id, 
                      node_type=node.node_type,
                      **node.attributes)
        
        # Add edges
        for edge in self.model.graph.edges:
            G.add_edge(edge.source_node_id, 
                      edge.target_node_id,
                      relationship=edge.relationship_type,
                      **edge.attributes)
        
        return G
    
    def create_interactive_graph(self, 
                                filter_node_types: Optional[List[str]] = None,
                                filter_platforms: Optional[List[str]] = None,
                                filter_regulations: Optional[List[str]] = None,
                                layout: str = 'hierarchical') -> go.Figure:
        """
        Create interactive Plotly graph visualization
        
        Args:
            filter_node_types: List of node types to include
            filter_platforms: List of platforms to include
            filter_regulations: List of regulations to include
            layout: Layout algorithm ('hierarchical', 'spring', 'circular')
        """
        
        # Filter graph
        filtered_nodes = self.model.graph.nodes
        if filter_node_types:
            filtered_nodes = [n for n in filtered_nodes if n.node_type in filter_node_types]
        
        # Create subgraph
        node_ids = [n.node_id for n in filtered_nodes]
        subgraph = self.nx_graph.subgraph(node_ids)
        
        # Calculate layout
        if layout == 'hierarchical':
            # Use graphviz_layout if available, otherwise use spring
            try:
                pos = nx.nx_agraph.graphviz_layout(subgraph, prog='dot')
            except:
                pos = nx.spring_layout(subgraph, k=2, iterations=50)
        elif layout == 'circular':
            pos = nx.circular_layout(subgraph)
        else:  # spring
            pos = nx.spring_layout(subgraph, k=2, iterations=50)
        
        # Create edge traces
        edge_traces = []
        for edge in subgraph.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            edge_trace = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=1, color='#888'),
                hoverinfo='none',
                showlegend=False
            )
            edge_traces.append(edge_trace)
        
        # Create node traces by type
        node_types = set(n.node_type for n in filtered_nodes)
        node_color_map = {
            'Enterprise Risk': '#FF6B6B',
            'IT Risk': '#FFA07A',
            'Information Security Risk': '#FFD700',
            'Security Risk Category': '#98D8C8',
            'Risk Statement': '#F7DC6F',
            'Control Objective': '#85C1E2',
            'Control': '#6C5CE7',
            'Technical Control Implementation': '#00B894',
            'Evidence Artifact': '#FDCB6E',
            'Regulation / Standard': '#E17055',
            'Role / Accountability': '#74B9FF',
            'Platform': '#A29BFE',
            'Operating Environment': '#FD79A8',
            'Regulatory Mapping': '#FFEAA7'
        }
        
        node_traces = []
        for node_type in node_types:
            type_nodes = [n for n in filtered_nodes if n.node_type == node_type]
            node_ids_of_type = [n.node_id for n in type_nodes]
            
            node_x = []
            node_y = []
            node_text = []
            node_hover = []
            
            for node in type_nodes:
                if node.node_id in pos:
                    x, y = pos[node.node_id]
                    node_x.append(x)
                    node_y.append(y)
                    
                    # Create label
                    label = node.attributes.get('name', node.node_id)
                    node_text.append(label[:30])
                    
                    # Create hover text
                    hover_text = f"<b>{node_type}</b><br>"
                    hover_text += f"ID: {node.node_id}<br>"
                    for key, value in node.attributes.items():
                        if isinstance(value, str) and len(value) < 100:
                            hover_text += f"{key}: {value}<br>"
                    node_hover.append(hover_text)
            
            node_trace = go.Scatter(
                x=node_x,
                y=node_y,
                mode='markers+text',
                name=node_type,
                text=node_text,
                textposition='top center',
                hovertext=node_hover,
                hoverinfo='text',
                marker=dict(
                    size=15,
                    color=node_color_map.get(node_type, '#95A5A6'),
                    line=dict(width=2, color='white')
                )
            )
            node_traces.append(node_trace)
        
        # Create figure
        fig = go.Figure(data=edge_traces + node_traces)
        
        fig.update_layout(
            title='Enterprise Risk Management Graph',
            titlefont_size=16,
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20, l=5, r=5, t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=800,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.01
            )
        )
        
        return fig
    
    def create_risk_heatmap(self) -> go.Figure:
        """Create risk heatmap showing inherent vs residual risk"""
        
        risk_data = []
        for risk in self.model.risks:
            risk_data.append({
                'Risk ID': risk.risk_id,
                'Risk Event': risk.risk_event[:50],
                'Inherent': self._risk_to_numeric(risk.inherent_rating),
                'Residual': self._risk_to_numeric(risk.residual_rating)
            })
        
        df = pd.DataFrame(risk_data)
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Inherent Risk', 'Residual Risk'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        fig.add_trace(
            go.Bar(
                x=df['Risk ID'],
                y=df['Inherent'],
                name='Inherent Risk',
                marker_color='red',
                text=df['Risk Event'],
                hovertemplate='<b>%{x}</b><br>%{text}<br>Rating: %{y}<extra></extra>'
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=df['Risk ID'],
                y=df['Residual'],
                name='Residual Risk',
                marker_color='green',
                text=df['Risk Event'],
                hovertemplate='<b>%{x}</b><br>%{text}<br>Rating: %{y}<extra></extra>'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text='Risk Reduction Analysis',
            showlegend=False,
            height=500
        )
        
        fig.update_yaxes(title_text='Risk Rating', row=1, col=1)
        fig.update_yaxes(title_text='Risk Rating', row=1, col=2)
        
        return fig
    
    def _risk_to_numeric(self, rating: str) -> int:
        """Convert risk rating to numeric value"""
        mapping = {
            'Critical': 5,
            'High': 4,
            'Medium': 3,
            'Low': 2,
            'Very Low': 1
        }
        return mapping.get(rating, 0)
    
    def create_control_dashboard(self) -> go.Figure:
        """Create dashboard showing control statistics"""
        
        # Control type distribution
        control_types = {}
        for control in self.model.controls:
            control_types[control.control_type] = control_types.get(control.control_type, 0) + 1
        
        # Automation level distribution
        automation_levels = {}
        for control in self.model.controls:
            automation_levels[control.automation_level] = automation_levels.get(control.automation_level, 0) + 1
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Control Types', 'Automation Levels', 
                          'Control Categories', 'Controls by Owner'),
            specs=[[{'type': 'pie'}, {'type': 'pie'}],
                   [{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # Control types pie
        fig.add_trace(
            go.Pie(labels=list(control_types.keys()), 
                   values=list(control_types.values()),
                   name='Control Types'),
            row=1, col=1
        )
        
        # Automation levels pie
        fig.add_trace(
            go.Pie(labels=list(automation_levels.keys()), 
                   values=list(automation_levels.values()),
                   name='Automation'),
            row=1, col=2
        )
        
        # Control categories bar
        categories = {}
        for control in self.model.controls:
            categories[control.control_category] = categories.get(control.control_category, 0) + 1
        
        fig.add_trace(
            go.Bar(x=list(categories.keys()), 
                   y=list(categories.values()),
                   name='Categories'),
            row=2, col=1
        )
        
        # Controls by owner bar
        owners = {}
        for control in self.model.controls:
            owner = control.control_owner_role.split('(')[0].strip()
            owners[owner] = owners.get(owner, 0) + 1
        
        fig.add_trace(
            go.Bar(x=list(owners.keys()), 
                   y=list(owners.values()),
                   name='Owners'),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text='Control Analytics Dashboard',
            showlegend=False,
            height=800
        )
        
        return fig
    
    def create_regulatory_coverage_chart(self) -> go.Figure:
        """Create chart showing regulatory coverage"""
        
        reg_coverage = {}
        for mapping in self.model.regulatory_mappings:
            reg_coverage[mapping.regulation] = reg_coverage.get(mapping.regulation, 0) + 1
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(reg_coverage.keys()),
                y=list(reg_coverage.values()),
                text=list(reg_coverage.values()),
                textposition='auto',
                marker_color='#6C5CE7'
            )
        ])
        
        fig.update_layout(
            title='Regulatory Framework Coverage (Control Mappings)',
            xaxis_title='Regulation / Standard',
            yaxis_title='Number of Control Mappings',
            height=500
        )
        
        return fig
    
    def create_interactive_dashboard(self):
        """Create complete interactive dashboard with filters"""
        
        # Create filter widgets
        platform_filter = widgets.SelectMultiple(
            options=['All'] + list(set(i.platform for i in self.model.implementations)),
            value=['All'],
            description='Platforms:',
            disabled=False
        )
        
        regulation_filter = widgets.SelectMultiple(
            options=['All'] + list(set(m.regulation for m in self.model.regulatory_mappings)),
            value=['All'],
            description='Regulations:',
            disabled=False
        )
        
        risk_category_filter = widgets.SelectMultiple(
            options=['All'] + [
                "Identity & Access Governance Risk",
                "Undetected Use of Credentials Risk",
                "Cloud Control Plane Risk",
                "Data Security & Privacy Risk",
                "Workload & Non-Human Identity Risk",
                "Endpoint & Device Security Risk",
                "Network & Connectivity Risk",
                "Detection, Response & Recovery Risk",
                "Third-Party & SaaS Integration Risk"
            ],
            value=['All'],
            description='Risk Category:',
            disabled=False
        )
        
        # Create output widget
        output = widgets.Output()
        
        def update_dashboard(platform_change=None, regulation_change=None, risk_change=None):
            with output:
                output.clear_output(wait=True)
                
                # Filter data based on selections
                platforms = list(platform_filter.value) if 'All' not in platform_filter.value else None
                regulations = list(regulation_filter.value) if 'All' not in regulation_filter.value else None
                
                # Generate filtered matrix
                df = self.matrix_gen.generate_complete_matrix()
                
                if platforms and platforms != ['All']:
                    df = df[df['Platform'].isin(platforms)]
                
                if regulations and regulations != ['All']:
                    # Filter rows where Regulations column contains any of the selected regulations
                    mask = df['Regulations'].apply(
                        lambda x: any(reg in str(x) for reg in regulations) if pd.notna(x) else False
                    )
                    df = df[mask]
                
                # Display summary
                display(HTML(f"<h3>Filtered Results: {len(df)} control implementations</h3>"))
                
                # Display table
                display(df.head(20))
                
                # Summary statistics
                unique_risks = df['Risk ID'].nunique()
                unique_controls = df['Control ID'].nunique()
                display(HTML(f"""
                <div style='background-color: #f0f0f0; padding: 15px; margin: 10px 0; border-radius: 5px;'>
                    <h4>Summary</h4>
                    <p><b>Risks Covered:</b> {unique_risks}</p>
                    <p><b>Controls Applied:</b> {unique_controls}</p>
                    <p><b>Total Implementations:</b> {len(df)}</p>
                </div>
                """))
        
        # Link filters to update function
        platform_filter.observe(update_dashboard, names='value')
        regulation_filter.observe(update_dashboard, names='value')
        risk_category_filter.observe(update_dashboard, names='value')
        
        # Display dashboard
        display(HTML("<h2>Enterprise Risk Management Interactive Dashboard</h2>"))
        display(widgets.HBox([platform_filter, regulation_filter, risk_category_filter]))
        display(output)
        
        # Initial update
        update_dashboard()
