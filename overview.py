from graphviz import Digraph

# Initialize diagram
dot = Digraph(comment='GVHD Microbiome Pipeline')
dot.attr(rankdir='LR', style='filled', fontsize='12', fillcolor='white', fontname='Helvetica')

# Style
node_attrs = {'shape': 'box', 'style': 'rounded,filled', 'fillcolor': '#e6f0ff', 'fontname': 'Helvetica'}
dot.attr('node', **node_attrs)

# Nodes
dot.node('GITHUB', 'Initialize GitHub Repository')
dot.node('TF', 'Set Up Terraform Environment')
dot.node('NF', 'Run Nextflow Pipeline')
dot.node('DATA', 'Public 16S rRNA Data')
dot.node('DADA2', 'Nextflow DADA2 Analysis')
dot.node('EXPORT', 'Export Feature Table')
dot.node('ML', 'Train GVHD Prediction Model')
dot.node('COST', 'Download Results + Destroy Infra')

# Edges
dot.edge('GITHUB', 'TF')
dot.edge('TF', 'NF')
dot.edge('DATA', 'NF', label='public input', style='dashed')
dot.edge('NF', 'DADA2')
dot.edge('DADA2', 'EXPORT')
dot.edge('EXPORT', 'ML')
dot.edge('ML', 'COST', style='dashed')

# Render to file
dot.render('gvhd_pipeline_workflow', format='png', cleanup=True)

