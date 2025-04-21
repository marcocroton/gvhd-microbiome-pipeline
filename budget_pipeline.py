from graphviz import Digraph

g = Digraph('ec2_decision', format='png')
g.attr(rankdir='TB', fontname='Helvetica', fontsize='11')
g.attr('node', shape='box', style='rounded,filled', fontname='Helvetica', fontsize='10')

# Start point
g.node('Start', 'How do we provision compute & storage\nfor 800-sample microbiome analysis?', fillcolor='#f0f8ff')

# Compute branch
g.node('Compute', 'Step 1: Choose Compute Option', fillcolor='#e6f0ff')
g.edge('Start', 'Compute')

g.node('OnDemand', 'On-Demand EC2?\nToo expensive at scale (~$0.13/hr)', fillcolor='#ffe0cc')
g.node('Spot', '✔ Spot EC2\n~$0.028/hr (78% savings)', fillcolor='#ccffcc')
g.edge('Compute', 'OnDemand')
g.edge('Compute', 'Spot')

# Instance choice
g.node('InstanceChoice', 'Choose instance size\n✔ r5.large (2 vCPU, 16 GB RAM)\n• Just enough RAM for QIIME2\n• Handles 2–4 samples in parallel', fillcolor='#cce5ff')
g.edge('Spot', 'InstanceChoice')

# Storage branch
g.node('Storage', 'Step 2: Choose Storage', fillcolor='#e6f0ff')
g.edge('InstanceChoice', 'Storage')

g.node('EBS', 'EBS Volume?\nPersistent, but more expensive\n~$0.08/GB/month', fillcolor='#ffe0cc')
g.node('S3', '✔ S3 Bucket\n~$0.023/GB/month\n• Lifecycle rule to auto-delete\n• Shareable across jobs', fillcolor='#ccffcc')
g.edge('Storage', 'EBS')
g.edge('Storage', 'S3')

# Budget goal
g.node('Budget', '🎯 Result: Total infra cost < $25\n• EC2: ~400 compute-hours via Spot = ~$11\n• S3: ~200 GB for 1 week = ~$1.15\n• IAM + Terraform = Free', shape='note', fillcolor='#f9f9f9')

g.edge('S3', 'Budget', style='dashed', color='gray')

g.render(filename='budget_pipeline_minimal', cleanup=True)
