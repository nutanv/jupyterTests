# Quick Start Guide

## Enterprise Risk Management Matrix

### 1. Installation (5 minutes)

```bash
# Clone the repository
git clone <repo-url>
cd jupyterTests

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Validate Installation (1 minute)

```bash
# Run test suite
python test_erm.py
```

Expected output: `✓ ALL TESTS PASSED`

### 3. Launch Interactive Notebook (2 minutes)

```bash
# Start Jupyter
jupyter notebook

# Open: Enterprise_Risk_Management_Matrix.ipynb
# Run all cells: Cell → Run All
```

### 4. Quick Validation Checklist

After running the notebook, verify you can see:

- [ ] Risk decomposition hierarchy (Enterprise → IT → InfoSec → Categories)
- [ ] 9 formal risk statements with inherent/residual ratings
- [ ] Risk-Control matrix with 29+ rows
- [ ] Control-Compliance matrix with regulatory mappings
- [ ] Platform-specific implementations
- [ ] Evidence artifacts for audit
- [ ] Gap analysis identifying areas needing attention
- [ ] Interactive risk heatmap visualization
- [ ] Control analytics dashboard
- [ ] Regulatory coverage chart
- [ ] Interactive graph visualization
- [ ] Filtering dashboard with dropdowns

### 5. Common Use Cases

#### For Auditors
```python
# Filter to PCI DSS requirements
df_pci = df_compliance[df_compliance['Regulation'].str.contains('PCI DSS')]
display(df_pci)

# Get evidence for PCI controls
pci_controls = df_pci['Control ID'].unique()
evidence = df_complete[df_complete['Control ID'].isin(pci_controls)]
display(evidence[['Control ID', 'Platform', 'Evidence']])
```

#### For Architects
```python
# Filter to AWS implementations
df_aws = df_impl[df_impl['Platform'] == 'AWS']
display(df_aws[['Control ID', 'Implementation Details', 'Tooling']])
```

#### For Risk Managers
```python
# View high/critical risks
high_risks = [r for r in model.risks if r.inherent_rating in ['Critical', 'High']]
for risk in high_risks:
    print(f"{risk.risk_id}: {risk.risk_event}")
```

#### For Executives
```python
# View visualizations
visualizer = ERMVisualizer(model)
visualizer.create_risk_heatmap().show()
visualizer.create_control_dashboard().show()
```

### 6. Export Artifacts

```python
# Generate Excel workbook
matrix_gen.export_to_excel('ERM_Matrix_Complete.xlsx')

# Generate JSON for external tools
matrix_gen.export_graph_to_json('erm_graph.json')

# Generate filter metadata
matrix_gen.export_filter_metadata('filter_metadata.json')
```

### 7. Customization

To add your organization's data:

1. **Edit `erm_data_model.py`**
2. **Update risk statements** in `define_risk_statements()`
3. **Add controls** in `define_controls()`
4. **Add implementations** in `define_platform_implementations()`
5. **Add evidence** in `define_evidence_artifacts()`
6. **Add mappings** in `define_regulatory_mappings()`
7. **Re-run** `python test_erm.py` to validate
8. **Re-run notebook** to generate updated matrices

### 8. Troubleshooting

**Problem:** Import errors
**Solution:** Ensure all dependencies installed: `pip install -r requirements.txt`

**Problem:** Notebook won't open
**Solution:** Launch Jupyter: `jupyter notebook`, then navigate to file

**Problem:** Visualizations don't show
**Solution:** Ensure plotly and ipywidgets installed: `pip install plotly ipywidgets`

**Problem:** Excel export fails
**Solution:** Ensure openpyxl installed: `pip install openpyxl`

**Problem:** Graph layout looks messy
**Solution:** Try different layout: `layout='spring'` or `layout='circular'`

### 9. Next Steps

1. **Review Gap Analysis** - Address identified gaps
2. **Validate Data** - Cross-reference with internal sources
3. **Expand Coverage** - Add more controls and implementations
4. **Collect Evidence** - Define evidence for all implementations
5. **Complete Mappings** - Map all controls to all applicable regulations
6. **Schedule Maintenance** - Set up quarterly/annual reviews

### 10. Support

For issues or questions:
1. Review README.md for detailed documentation
2. Check test_erm.py output for specific failures
3. Review erm_data_model.py for data structure
4. Consult your Risk Committee or CISO

---

**REMINDER:** This system uses template data. All risks, controls, and mappings MUST be validated against your organization's authoritative internal sources before production use.
