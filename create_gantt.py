from graphviz import Digraph

g = Digraph('gvhd_timeline', format='png')
g.attr(rankdir='LR', fontname='Helvetica')
g.attr('node', shape='box', style='rounded,filled', fontname='Helvetica', fontsize='10', fillcolor='#e6f0ff')

# Setup Phase
with g.subgraph(name='cluster_setup') as c:
    c.attr(label='Setup Phase (0–0.25 hr)', style='dashed')
    c.node('infra', 'Terraform: Provision EC2, S3')

# Data Processing Phase
with g.subgraph(name='cluster_processing') as c:
    c.attr(label='Data Processing (0.25–10.25 hr)', style='solid')
    c.node('qiime', 'QIIME2 (800 samples, 20 parallel EC2)')
    c.node('feature', 'Export Feature Tables')

# Modeling + Cleanup Phase
with g.subgraph(name='cluster_analysis') as c:
    c.attr(label='Modeling & Cleanup (10.25–12 hr)', style='dotted')
    c.node('ml', 'Model Training & Evaluation')
    c.node('cleanup', 'Download + Teardown')

# Edges
g.edge('infra', 'qiime')
g.edge('qiime', 'feature')
g.edge('feature', 'ml')
g.edge('ml', 'cleanup')

# Render diagram
g.render(filename='gvhd_timeline', cleanup=True)

