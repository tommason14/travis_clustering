#!/usr/bin/env python3

"""
Random select n clusters with the sample evenly distributed between the
groups assigned by the KMeans algorithm, taking 20% of each KMeans cluster
"""
import pandas as pd
import ete3

df = pd.read_csv('data/kmeans_assignments.csv')
selection = (
    df.groupby('kmeans_cluster')
    .apply(lambda group: group.sample(frac=0.2))
    .reset_index(drop=True)
)

########################################
#  print tree showing KMeans clusters  #
########################################

treedata = []

selection['xyz'] = selection['xyz'].apply(lambda x: f"cluster-{x}.xyz")

for kmeans_cluster, group in selection.groupby('kmeans_cluster'):
    xyzs = group['xyz'].tolist()
    string = f"({','.join(xyzs)}){kmeans_cluster}"
    treedata.append(string)

treedata = '(' + ','.join(treedata) + ');'

tree = ete3.Tree(treedata, format=1)

def layout(node):
    if node.is_leaf():
        N = ete3.AttrFace("name", ftype='Ubuntu', text_prefix=' ')
        ete3.faces.add_face_to_node(N, node, 0, position='aligned')

ts = ete3.TreeStyle()
# ts.mode = 'c'
# ts.arc_start = -180
# ts.arc_span = 180
ts.layout_fn = layout
ts.show_leaf_name = False # use our changes
ts.branch_vertical_margin = 10 # px
tree.render('plots/chosen-structures.png', dpi=300, w=1500, tree_style=ts)
