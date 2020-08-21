#!/usr/bin/env python3

"""
Random select n clusters with the sample evenly distributed between the
groups assigned by the KMeans algorithm, taking 20% of each KMeans cluster
"""
import pandas as pd
df = pd.read_csv('csv_files/kmeans_assignments.csv')
print(df.groupby('kmeans_cluster')
    .apply(lambda group: group.sample(frac=0.2))
    .reset_index(drop=True)
)
