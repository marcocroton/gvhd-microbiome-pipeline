from graphviz import Digraph

dot = Digraph(comment='Enhanced GVHD Microbiome Pipeline')
dot.attr(rankdir='LR', style='filled', fontsize='12', fontname='Helvetica')

# === Node Styles ===
dot.attr('node', shape='box', style='rounded,filled', fontname='Helvetica')

# GitHub and pipeline steps (light blue)
dot.node('GITHUB', 'Initialize GitHub Repo', fillcolor='#e6f0ff')
dot.node('NF', 'Run Nextflow Pipeline', fillcolor='#e6f0ff')
dot.node('DADA2', 'Nextflow DADA2 Analysis', fillcolor='#e6f0ff')
dot.node('EXPORT', 'Export Feature Table', fillcolor='#e6f0ff')
dot.node('ML', 'Train GVHD Prediction Model', fillcolor='#e6f0ff')

# AWS Resources (orange)
dot.node('TF', 'Provision Infrastructure (Terraform)', fillcolor='#ffe0cc')
dot.node('COST', 'Download Results + Destroy Infra', fillcolor='#ffe0cc')

# External Input (gray/neutral)
dot.node('DATA', 'Public 16S rRNA Data', fillcolor='#dddddd')

# === Edges ===
dot.edge('GITHUB', 'TF')
dot.edge('TF', 'NF')
dot.edge('NF', 'DADA2')

# Dashed input from external data
dot.edge('DATA', 'NF', label='public input', style='dashed', color='gray')

# Vertical tail
dot.edge('DADA2', 'EXPORT')
dot.edge('EXPORT', 'ML')
dot.edge('ML', 'COST', style='dashed', color='gray')

# Layout hint to stack last 5 nodes vertically
#dot.body.append('{ rank = same; DADA2 }')
dot.body.append('{ rank = sink; NF DADA2 EXPORT ML COST }')

# Render
dot.render('gvhd_pipeline_workflow_enhanced', format='svg', cleanup=True)

