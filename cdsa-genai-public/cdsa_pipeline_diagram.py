# cds_pipeline_diagram.py

from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment='CDS Pipeline Workflow', format='png')

# ----------------- Nodes ----------------- #
dot.node('A', 'User / Front-End\n(Patient Input)')
dot.node('B', 'test_user_input.py\n- Input Validation\n- BMI Calculation')
dot.node('C', 'pubmed_evidence_summary_final.py\n- Symptom-focused PubMed Query\n- Fetch Top Articles\n- Relevance Scoring')
dot.node('D', 'CDS Model / OCI\n- Reads patient vitals, labs, BMI, symptoms\n- Cross-references with PubMed evidence\n- Clinical Assessment / Recommendations')
dot.node('E', 'Front-End / EHR\n- Display JSON & Evidence Snippets')

# ----------------- Edges ----------------- #
dot.edge('A', 'B', label='Enter clinical data')
dot.edge('B', 'C', label='ClinicalInput object')
dot.edge('C', 'D', label='Evidence + Patient JSON')
dot.edge('D', 'E', label='Recommendations / Assessment')

# Optional: show multiple patients
dot.node('F', 'Additional Patients\n(Multi-session support)')
dot.edge('F', 'B', label='Loop for next patient', style='dashed')

# ----------------- Render diagram ----------------- #
output_file = 'cds_pipeline_workflow'
dot.render(output_file, view=True)

print(f"CDS workflow diagram generated: {output_file}.png")
