from graphviz import Digraph

dot = Digraph(comment='GVHD Microbiome Pipeline')
dot.attr(rankdir='LR', style='filled', fontsize='12', fillcolor='white', fontname='Helvetica')

node_attrs = {
    'shape': 'box',
    'style': 'rounded,filled',
    'fillcolor': '#e6f0ff',
    'fontname': 'Helvetica'
}
dot.attr('node', **node_attrs)

# Main pipeline nodes (horizontal flow)
dot.node('GITHUB', 'Initialize GitHub Repository')
dot.node('TF', 'Set Up Terraform Environment')
dot.node('NF', 'Run Nextflow Pipeline')
dot.node('DATA', 'Public 16S rRNA Data')
dot.node('DADA2', 'Nextflow DADA2 Analysis')

# Vertical sub-pipeline
dot.node('EXPORT', 'Export Feature Table', pos='1,1!')
dot.node('ML', 'Train GVHD Prediction Model')
dot.node('COST', 'Download Results + Destroy Infra')

# Edges for horizontal main flow
dot.edge('GITHUB', 'TF')
dot.edge('TF', 'NF')
dot.edge('DATA', 'NF', label='public input', style='dashed')
dot.edge('NF', 'DADA2')

# Downward flow from DADA2
dot.edge('DADA2', 'EXPORT')
dot.edge('EXPORT', 'ML')
dot.edge('ML', 'COST', style='dashed')

# Layout hint: Keep EXPORT/ML/COST below DADA2
dot.body.append('{ rank = same; DADA2 }')  # Keeps DADA2 in top row
dot.body.append('{ rank = sink; EXPORT ML COST }')  # Forces these to descend

# Output file
dot.render('gvhd_pipeline_workflow_vertical_tail', format='png', cleanup=True)

