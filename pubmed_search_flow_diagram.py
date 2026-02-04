# pubmed_search_flow_diagram.py
# ------------------------------------------
# Visual diagram of the hybridized PubMed evidence search process
# Requires: pip install graphviz
# ------------------------------------------

from graphviz import Digraph

def create_pubmed_flow_diagram(output_path="pubmed_search_flow"):
    dot = Digraph(comment="Hybrid PubMed Search Flow", format="png")

    # Global style
    dot.attr(rankdir='LR', size='8,5')
    dot.attr('node', shape='rect', style='rounded,filled', fillcolor='lightgoldenrod1', color='black')

    # Nodes
    dot.node('A', '🧍 User Input\n(Symptoms, Age, Vitals, Notes)')
    dot.node('B', '📋 Validate Input\nCheck for PHI or name leakage')
    dot.node('C', '⚙️ Phase 1: Individual Searches\nQuery each symptom + age range')
    dot.node('D', '📚 Collect Results\nAggregate article titles & abstracts')
    dot.node('E', '🧠 Extract Keywords\nIdentify common clinical terms')
    dot.node('F', '🎯 Phase 2: Refined Query\nCombine symptoms + keywords')
    dot.node('G', '🔎 Fetch Final Articles\nPubMed ESummary results')
    dot.node('H', '🧩 Merge & Deduplicate\nRemove duplicate studies')
    dot.node('I', '📝 Generate Summary JSON\n(Patient ID, Query, Top 10 Articles, Snippet)')
    dot.node('J', '📄 Display Evidence Snippet\nTop 5 findings shown to user')

    # Edges (flow connections)
    dot.edge('A', 'B', label='Validate input fields')
    dot.edge('B', 'C', label='If valid → continue')
    dot.edge('C', 'D', label='Store article metadata')
    dot.edge('D', 'E', label='Extract top keywords')
    dot.edge('E', 'F', label='Build refined hybrid query')
    dot.edge('F', 'G', label='Run final PubMed search')
    dot.edge('G', 'H', label='Combine and deduplicate')
    dot.edge('H', 'I', label='Create structured summary')
    dot.edge('I', 'J', label='Display to clinician')

    # Save and render
    output_file = dot.render(filename=output_path, cleanup=True)
    print(f"✅ Diagram generated successfully: {output_file}")

if __name__ == "__main__":
    create_pubmed_flow_diagram()
