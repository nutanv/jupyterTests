#!/usr/bin/env python
"""
Test and Validation Script for Enterprise Risk Management Matrix
=================================================================
Run this script to validate the ERM system implementation.
"""

import sys
from erm_data_model import ERMDataModel
from matrix_generator import MatrixGenerator


def test_data_model():
    """Test data model construction"""
    print("=" * 80)
    print("TEST 1: Data Model Construction")
    print("=" * 80)
    
    try:
        model = ERMDataModel()
        graph = model.build_complete_model()
        
        print(f"✓ Model built successfully")
        print(f"  Nodes: {len(graph.nodes)}")
        print(f"  Edges: {len(graph.edges)}")
        print(f"  Risks: {len(model.risks)}")
        print(f"  Controls: {len(model.controls)}")
        print(f"  Implementations: {len(model.implementations)}")
        print(f"  Evidence: {len(model.evidence_artifacts)}")
        print(f"  Regulatory Mappings: {len(model.regulatory_mappings)}")
        
        return True, model
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False, None


def test_matrices(model):
    """Test matrix generation"""
    print("\n" + "=" * 80)
    print("TEST 2: Matrix Generation")
    print("=" * 80)
    
    try:
        matrix_gen = MatrixGenerator(model)
        
        # Generate all matrices
        df_complete = matrix_gen.generate_complete_matrix()
        print(f"✓ Complete matrix: {len(df_complete)} rows")
        
        df_risk_control = matrix_gen.generate_risk_control_matrix()
        print(f"✓ Risk-Control matrix: {len(df_risk_control)} rows")
        
        df_compliance = matrix_gen.generate_control_compliance_matrix()
        print(f"✓ Control-Compliance matrix: {len(df_compliance)} rows")
        
        df_impl = matrix_gen.generate_implementation_matrix()
        print(f"✓ Implementation matrix: {len(df_impl)} rows")
        
        df_evidence = matrix_gen.generate_evidence_matrix()
        print(f"✓ Evidence matrix: {len(df_evidence)} rows")
        
        return True, matrix_gen
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False, None


def test_gap_analysis(matrix_gen):
    """Test gap analysis"""
    print("\n" + "=" * 80)
    print("TEST 3: Gap Analysis")
    print("=" * 80)
    
    try:
        gaps = matrix_gen.identify_gaps()
        print("✓ Gap analysis completed")
        
        total_gaps = sum(len(gap_list) for gap_list in gaps.values())
        print(f"\nTotal gaps identified: {total_gaps}")
        
        for gap_type, gap_list in gaps.items():
            print(f"  {gap_type}: {len(gap_list)} items")
            if gap_list and len(gap_list) <= 3:
                for gap in gap_list[:3]:
                    print(f"    - {gap}")
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_exports(matrix_gen):
    """Test export functionality"""
    print("\n" + "=" * 80)
    print("TEST 4: Export Functionality")
    print("=" * 80)
    
    try:
        import os
        
        # Export files
        matrix_gen.export_to_excel('test_output.xlsx')
        matrix_gen.export_graph_to_json('test_graph.json')
        matrix_gen.export_filter_metadata('test_metadata.json')
        
        # Verify files exist
        files = ['test_output.xlsx', 'test_graph.json', 'test_metadata.json']
        for filename in files:
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"✓ {filename}: {size:,} bytes")
                os.remove(filename)  # Clean up
            else:
                print(f"✗ {filename}: NOT FOUND")
                return False
        
        return True
    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_validation_requirements(model):
    """Test against validation requirements"""
    print("\n" + "=" * 80)
    print("TEST 5: Validation Requirements")
    print("=" * 80)
    
    results = []
    
    # Check 1: Risk hierarchy exists
    enterprise_risks = [n for n in model.graph.nodes if n.node_type == 'Enterprise Risk']
    check1 = len(enterprise_risks) > 0
    results.append(('Risk hierarchy exists', check1))
    print(f"{'✓' if check1 else '✗'} Risk hierarchy: {len(enterprise_risks)} enterprise risk node(s)")
    
    # Check 2: All risks have formal statements
    check2 = all(
        hasattr(r, 'cause') and hasattr(r, 'risk_event') and hasattr(r, 'business_impact')
        for r in model.risks
    )
    results.append(('Formal risk statements', check2))
    print(f"{'✓' if check2 else '✗'} All {len(model.risks)} risks have formal statements")
    
    # Check 3: All risks have controls
    risks_with_controls = len(set(
        risk_id for control in model.controls for risk_id in control.risks_mitigated
    ))
    check3 = risks_with_controls == len(model.risks)
    results.append(('Risk coverage', check3))
    print(f"{'✓' if check3 else '✗'} Risk coverage: {risks_with_controls}/{len(model.risks)} risks have controls")
    
    # Check 4: Platform implementations exist
    platforms_covered = len(set(i.platform for i in model.implementations))
    check4 = platforms_covered >= 3
    results.append(('Platform coverage', check4))
    print(f"{'✓' if check4 else '✗'} Platform coverage: {platforms_covered} platforms")
    
    # Check 5: Evidence artifacts exist
    check5 = len(model.evidence_artifacts) > 0
    results.append(('Evidence artifacts', check5))
    print(f"{'✓' if check5 else '✗'} Evidence artifacts: {len(model.evidence_artifacts)} items")
    
    # Check 6: Regulatory mappings exist
    regulations_covered = len(set(m.regulation for m in model.regulatory_mappings))
    check6 = regulations_covered >= 5
    results.append(('Regulatory coverage', check6))
    print(f"{'✓' if check6 else '✗'} Regulatory coverage: {regulations_covered} regulations mapped")
    
    # Check 7: Graph is connected
    check7 = len(model.graph.edges) > 0
    results.append(('Graph connectivity', check7))
    print(f"{'✓' if check7 else '✗'} Graph connectivity: {len(model.graph.edges)} relationships")
    
    all_passed = all(result[1] for result in results)
    return all_passed


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("ENTERPRISE RISK MANAGEMENT MATRIX - TEST SUITE")
    print("=" * 80 + "\n")
    
    all_tests_passed = True
    
    # Test 1: Data Model
    success, model = test_data_model()
    all_tests_passed = all_tests_passed and success
    
    if not model:
        print("\n✗ Cannot continue testing without valid model")
        sys.exit(1)
    
    # Test 2: Matrix Generation
    success, matrix_gen = test_matrices(model)
    all_tests_passed = all_tests_passed and success
    
    if not matrix_gen:
        print("\n✗ Cannot continue testing without matrix generator")
        sys.exit(1)
    
    # Test 3: Gap Analysis
    success = test_gap_analysis(matrix_gen)
    all_tests_passed = all_tests_passed and success
    
    # Test 4: Exports
    success = test_exports(matrix_gen)
    all_tests_passed = all_tests_passed and success
    
    # Test 5: Validation Requirements
    success = test_validation_requirements(model)
    all_tests_passed = all_tests_passed and success
    
    # Final summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    if all_tests_passed:
        print("✓ ALL TESTS PASSED")
        print("\nThe ERM system is ready for use.")
        print("\nNext steps:")
        print("  1. Review and validate all data against internal sources")
        print("  2. Expand control catalog and implementations")
        print("  3. Add evidence artifacts for all implementations")
        print("  4. Complete regulatory mappings")
        print("  5. Launch Jupyter notebook for interactive use")
        sys.exit(0)
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease review the failures above and fix before using.")
        sys.exit(1)


if __name__ == "__main__":
    main()
